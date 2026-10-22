#!/usr/bin/env python3
"""Build one self-contained security-report.html from the pipeline's scan outputs.

Everything ends up in ONE file: SonarQube results (queried from its API), Bandit, pip-audit,
Trivy, and the ZAP report (alerts table + the full original ZAP HTML embedded).

Inputs (all optional, looked up in the current directory):
  bandit-report.json  pip-audit.json  trivy-report.json (or trivy-report.txt)  zap-report.json  zap-report.html
SonarQube: --sonar-host http://sonarqube:9000 --sonar-project takecare, token in env SONAR_TOKEN.
Stdlib only.
"""
import argparse
import base64
import datetime
import html
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter

e = html.escape
SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4, "UNKNOWN": 5}
ANSI = re.compile(r"\x1b\[[0-9;]*m")
TAGS = re.compile(r"<[^>]+>")


def load(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


SONAR_CLS = {"BLOCKER": "critical", "CRITICAL": "high", "MAJOR": "medium", "MINOR": "low", "INFO": "info"}


def badge(sev, cls=None):
    sev = (sev or "UNKNOWN").upper()
    return f'<span class="b {cls or sev.lower()}">{e(sev)}</span>'


def table(headers, rows):
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def card(title, big, sub, cls=""):
    return f'<div class="card {cls}"><div class="ct">{e(title)}</div><div class="cb">{big}</div><div class="cs">{sub}</div></div>'


def counts_line(counter, order):
    return " &middot; ".join(f"{counter.get(k, 0)} {k.title()}" for k in order)


# ---------- Bandit ----------
def bandit(data):
    if not data:
        return None, "<p class='muted'>No bandit-report.json found.</p>"
    res = sorted(data.get("results", []), key=lambda r: SEV_ORDER.get(r.get("issue_severity", "").upper(), 9))
    c = Counter(r.get("issue_severity", "").upper() for r in res)
    rows = [[badge(r.get("issue_severity")), e(r.get("issue_confidence", "")),
             f"{e(r.get('test_id', ''))}<br><small>{e(r.get('test_name', ''))}</small>",
             e(r.get("issue_text", "")),
             f"{e(r.get('filename', '').lstrip('./'))}:{r.get('line_number', '')}"] for r in res]
    body = table(["Severity", "Confidence", "Test", "Issue", "Location"], rows) if rows else "<p>No issues found.</p>"
    return card("SAST - Bandit", len(res), counts_line(c, ["HIGH", "MEDIUM", "LOW"]),
                "bad" if c.get("HIGH") else ""), body


# ---------- pip-audit ----------
def pip_audit(data):
    if not data:
        return None, "<p class='muted'>No pip-audit.json found.</p>"
    seen, rows, pkgs, fixable = set(), [], set(), 0
    for dep in data.get("dependencies", []):
        for v in dep.get("vulns", []):
            key = (dep["name"], v["id"])
            if key in seen:
                continue
            seen.add(key)
            pkgs.add(dep["name"])
            fixes = v.get("fix_versions") or []
            fixable += bool(fixes)
            aliases = ", ".join(v.get("aliases", [])[:3])
            rows.append([e(dep["name"]), e(dep.get("version", "")),
                         f"{e(v['id'])}<br><small>{e(aliases)}</small>",
                         e(", ".join(fixes)) or "<span class='muted'>none</span>"])
    rows.sort(key=lambda r: r[0])
    body = table(["Package", "Installed", "Vulnerability", "Fixed in"], rows) if rows else "<p>No known vulnerabilities.</p>"
    return card("Dependency scan - pip-audit", len(rows),
                f"{len(pkgs)} packages affected &middot; {fixable} have a fix",
                "bad" if rows else ""), body


# ---------- Trivy ----------
def trivy(data, txt_path):
    if not data:
        try:
            with open(txt_path, encoding="utf-8", errors="replace") as f:
                raw = ANSI.sub("", f.read())
            return None, ("<p class='muted'>Only the plain-text report is available "
                          "(re-run the pipeline with the updated Trivy stage for a table).</p>"
                          f"<details><summary>Show raw trivy-report.txt</summary><pre>{e(raw)}</pre></details>")
        except OSError:
            return None, "<p class='muted'>No Trivy report found.</p>"
    c, parts = Counter(), []
    seen = set()
    for res in data.get("Results", []):
        vulns = res.get("Vulnerabilities") or []
        rows = []
        for v in sorted(vulns, key=lambda v: (SEV_ORDER.get(v.get("Severity", ""), 9), v.get("PkgName", ""))):
            key = (res.get("Target"), v.get("VulnerabilityID"), v.get("PkgName"))
            if key in seen:
                continue
            seen.add(key)
            c[v.get("Severity", "UNKNOWN")] += 1
            vid = e(v.get("VulnerabilityID", ""))
            url = v.get("PrimaryURL")
            vid = f'<a href="{e(url)}" target="_blank" rel="noopener">{vid}</a>' if url else vid
            rows.append([badge(v.get("Severity")), e(v.get("PkgName", "")), e(v.get("InstalledVersion", "")),
                         e(v.get("FixedVersion", "")) or "<span class='muted'>no fix yet</span>",
                         vid, e(v.get("Title", ""))])
        if rows:
            parts.append(f"<h3>{e(res.get('Target', ''))} <small>({e(res.get('Class', ''))})</small></h3>"
                         + table(["Severity", "Package", "Installed", "Fixed", "ID", "Title"], rows))
    total = sum(c.values())
    body = "".join(parts) or "<p>No HIGH/CRITICAL vulnerabilities.</p>"
    return card("Image scan - Trivy", total, counts_line(c, ["CRITICAL", "HIGH"]),
                "bad" if c.get("CRITICAL") else ""), body


# ---------- ZAP ----------
def zap(data):
    if not data:
        return None, "<p class='muted'>No zap-report.json found.</p>"
    names = {"3": "HIGH", "2": "MEDIUM", "1": "LOW", "0": "INFO"}
    alerts = [a for s in data.get("site", []) for a in s.get("alerts", [])]
    alerts.sort(key=lambda a: -int(a.get("riskcode", 0)))
    c = Counter(names.get(str(a.get("riskcode")), "INFO") for a in alerts)
    rows = [[badge(names.get(str(a.get("riskcode")), "INFO")), e(a.get("name", "")),
             e(str(a.get("count", len(a.get("instances", []))))),
             e(TAGS.sub("", a.get("solution", ""))[:300])] for a in alerts]
    body = table(["Risk", "Alert", "Instances", "Solution"], rows) if rows else "<p>No alerts.</p>"
    return card("DAST - OWASP ZAP", len(alerts), counts_line(c, ["HIGH", "MEDIUM", "LOW", "INFO"]),
                "bad" if c.get("HIGH") else ""), body


def zap_embed(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
    except OSError:
        return ""
    return ('<details><summary>Full original ZAP report (embedded)</summary>'
            f'<iframe sandbox="" srcdoc="{e(raw, quote=True)}" '
            'style="width:100%;height:900px;border:1px solid var(--line);border-radius:8px;background:#fff"></iframe></details>')


# ---------- SonarQube (queried from its API) ----------
def sonar_get(host, path, params, token):
    url = host.rstrip("/") + path + "?" + urllib.parse.urlencode(params)
    auth = base64.b64encode(f"{token}:".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + auth})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def rating(v):
    try:
        return "ABCDE"[int(float(v)) - 1]
    except (ValueError, IndexError, TypeError):
        return v or "-"


def sonar(host, project, token, public_url):
    if not (host and token):
        return None, "<p class='muted'>SonarQube not queried (needs --sonar-host and SONAR_TOKEN).</p>"
    try:
        gate = sonar_get(host, "/api/qualitygates/project_status", {"projectKey": project}, token)["projectStatus"]
        metrics = "bugs,vulnerabilities,code_smells,security_hotspots,coverage,duplicated_lines_density,ncloc,reliability_rating,security_rating,sqale_rating"
        ms = {m["metric"]: m.get("value", "") for m in sonar_get(
            host, "/api/measures/component", {"component": project, "metricKeys": metrics}, token)["component"]["measures"]}
        issues = sonar_get(host, "/api/issues/search", {"componentKeys": project, "resolved": "false", "ps": 500,
                                                         "s": "SEVERITY", "asc": "false"}, token).get("issues", [])
    except Exception as ex:  # network/auth problems must not break the pipeline
        return None, f"<p class='muted'>Could not query SonarQube: {e(str(ex))}</p>"
    try:
        hotspots = sonar_get(host, "/api/hotspots/search", {"projectKey": project, "ps": 500}, token).get("hotspots", [])
    except Exception:
        hotspots = []

    status = gate.get("status", "NONE")
    ok = status == "OK"
    link = f'<p><a href="{e(public_url)}" target="_blank" rel="noopener">Open the SonarQube dashboard</a></p>' if public_url else ""
    cond_rows = [[e(c.get("metricKey", "")), badge(c.get("status", ""), "low" if c.get("status") == "OK" else "high"),
                  e(str(c.get("actualValue", ""))), e(str(c.get("errorThreshold", "")))]
                 for c in gate.get("conditions", [])]
    body = f"<p>Quality gate: {badge('PASSED' if ok else status, 'low' if ok else 'high')}</p>"
    body += table(["Gate condition", "Status", "Actual", "Threshold"], cond_rows) if cond_rows else ""
    body += "<h3>Measures</h3>" + table(
        ["Bugs", "Vulnerabilities", "Code smells", "Hotspots", "Coverage %", "Duplication %", "Lines of code", "Reliability", "Security", "Maintainability"],
        [[e(ms.get("bugs", "-")), e(ms.get("vulnerabilities", "-")), e(ms.get("code_smells", "-")),
          e(ms.get("security_hotspots", "-")), e(ms.get("coverage", "-")), e(ms.get("duplicated_lines_density", "-")),
          e(ms.get("ncloc", "-")), rating(ms.get("reliability_rating")), rating(ms.get("security_rating")),
          rating(ms.get("sqale_rating"))]])
    rows = [[badge(i.get("severity"), SONAR_CLS.get(i.get("severity", ""), "info")), e(i.get("type", "").replace("_", " ").title()),
             e(i.get("rule", "")), e(i.get("message", "")),
             f"{e(i.get('component', '').split(':', 1)[-1])}:{i.get('line', '')}"] for i in issues]
    body += "<h3>Open issues</h3>" + (table(["Severity", "Type", "Rule", "Message", "Location"], rows) if rows else "<p>No open issues.</p>")
    if hotspots:
        body += "<h3>Security hotspots to review</h3>" + table(
            ["Risk", "Category", "Message", "Location"],
            [[badge(h.get("vulnerabilityProbability", ""), (h.get("vulnerabilityProbability") or "info").lower()),
              e(h.get("securityCategory", "")), e(h.get("message", "")),
              f"{e(h.get('component', '').split(':', 1)[-1])}:{h.get('line', '')}"] for h in hotspots])
    sub = f"{ms.get('bugs', '0')} bugs &middot; {ms.get('vulnerabilities', '0')} vulns &middot; {ms.get('code_smells', '0')} smells &middot; {len(hotspots)} hotspots"
    return card("SAST - SonarQube", "PASSED" if ok else status, sub, "" if ok else "bad"), link + body


CSS = """
:root{--bg:#f6f7f9;--fg:#1c2128;--card:#fff;--line:#dfe3e8;--muted:#6b7280;--accent:#2563eb}
@media(prefers-color-scheme:dark){:root{--bg:#0f1318;--fg:#e6e9ee;--card:#171c23;--line:#2a313b;--muted:#9aa4b2;--accent:#6ea8fe}}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
main{max-width:1200px;margin:0 auto;padding:24px 16px 64px}h1{margin:0 0 4px}h2{margin:36px 0 12px;padding-top:8px;border-top:1px solid var(--line)}
h3{margin:20px 0 8px;font-size:15px}small,.muted{color:var(--muted)}a{color:var(--accent)}
.meta{color:var(--muted);margin-bottom:20px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}.card.bad{border-left:4px solid #dc2626}
.ct{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}.cb{font-size:34px;font-weight:700;line-height:1.2}.cs{font-size:13px;color:var(--muted)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{background:rgba(127,127,127,.08);position:sticky;top:0}
tr:last-child td{border-bottom:0}.b{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11px;font-weight:700;color:#fff}
.critical{background:#7f1d1d}.high{background:#dc2626}.medium{background:#d97706}.low{background:#2563eb}.info,.unknown{background:#6b7280}
pre{white-space:pre-wrap;font-size:12px;background:var(--card);border:1px solid var(--line);padding:12px;border-radius:8px;overflow-x:auto}
"""


def safe(fn, *args):
    try:
        return fn(*args)
    except Exception as ex:  # one bad input must never break the report
        return None, f"<p class='muted'>Could not render this section: {e(str(ex))}</p>"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--build", default="")
    p.add_argument("--image", default="")
    p.add_argument("--sonar-url", default="", help="browser URL of the SonarQube dashboard (link only)")
    p.add_argument("--sonar-host", default="", help="SonarQube API base URL reachable from this container")
    p.add_argument("--sonar-project", default="takecare")
    p.add_argument("--out", default="security-report.html")
    a = p.parse_args()

    sections = [
        ("SAST - SonarQube", "sonar", safe(sonar, a.sonar_host, a.sonar_project, os.environ.get("SONAR_TOKEN", ""), a.sonar_url)),
        ("SAST - Bandit", "bandit", safe(bandit, load("bandit-report.json"))),
        ("Dependency scan - pip-audit", "pipaudit", safe(pip_audit, load("pip-audit.json"))),
        ("Container image scan - Trivy", "trivy", safe(trivy, load("trivy-report.json"), "trivy-report.txt")),
        ("DAST - OWASP ZAP", "zap", safe(zap, load("zap-report.json"))),
    ]
    cards = [c for _, _, (c, _) in sections if c]
    meta = " &middot; ".join(x for x in [
        f"Build #{e(a.build)}" if a.build else "", f"Image {e(a.image)}" if a.image else "",
        "Generated " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")] if x)
    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>Security report</title><style>{CSS}</style></head><body><main>",
           f"<h1>Security scan report</h1><div class='meta'>{meta}</div>",
           f"<div class='cards'>{''.join(cards)}</div>"]
    for title, sid, (_, body) in sections:
        if sid == "zap":
            body += zap_embed("zap-report.html")
        out.append(f"<h2 id='{sid}'>{e(title)}</h2>{body}")
    out.append("</main></body></html>")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()