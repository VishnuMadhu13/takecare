from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse
import io
from django.http import FileResponse
from .models import admin
from doctor.models import dregister
from patient.models import pregister
from pharmacy.models import phregister
from patient.models import payment
from patient.models import d_payment
from patient.models import l_payment
from patient.models import homenurserequest
from .models import *

from .forms import times
from labs.models import labreg

def first(request):
    return render(request, 'index.html')

def homes(request):
    return render(request, 'index.html')
    
    
def homelogin(request):
    return render(request,'homenurselogin.html')
        
def homeeee(request):
    return render(request, 'index.html')
    
def loog5(request):
    return render(request,'login5.html')
    
def homenurse(request):
    return render(request, 'homenurse.html')


def patientt(request):
    return render(request, 'phome.html')
def dreg(request):
    return render(request, 'dreg.html')

def log4(request):
    return render(request,'login4.html')

def preg(request):
    return render(request, 'preg.html')
def phreg(request):
    return render(request, 'phreg.html')
def login4(request):
    return render(request, 'login4.html')
def log2(request):
    return render(request, 'log1.html')

def labsreg(request):
    return render(request, 'labreg.html')


def lg(request):
    return render(request, 'lg.html')
def adhome(request):
    return render(request, 'login.html')
def login1(request):
    return render(request, 'login1.html')
def dhome(request):
    return render(request, 'dhome.html')
def labhome(request):
    return render(request, 'labhome.html')

def labshome(request):
    return render(request, 'labshome.html')

def homeee(request):
    return render(request, 'welcome5.html')


def viewwhomereq(request):
    users=homenurserequest.objects.all()
    return render(request, 'viewrequestss.html',{'result':users})

"""def viewwhomereq(request):
    #sid=request.session['sid']

    fetch_patients = homenurses.objects.all()
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
    user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'p_name':user_dat[int(i.p_name)],'id':i.id,'amount':i.amount,'description':i.description})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)   
    return render(request,'viewrequestss.html', {'data': fetch_patients,'result':dat})"""

def phome(request):
    return render(request, 'phome.html')
def phhome(request):
    return render(request, 'phhome.html')

def logint(request):

    if request.method == 'POST':
        try:
            userdetails =admin.objects.get(email=request.POST['email'],password=request.POST['password'])
            print(userdetails.password)
            if userdetails.password == request.POST['password']:
                request.session['aid'] = userdetails.id

                return render(request, 'welcome.html')
        except admin.DoesNotExist as e:
            return render(request, 'user name or password invalid')
    return render(request, 'welcome.html')
    
def adddhomelogin(request):

    if request.method == 'POST':
        try:
            userdetails =homenurses.objects.get(email=request.POST['email'],password=request.POST['password'])
            print(userdetails.password)
            if userdetails.password == request.POST['password']:
                request.session['hid'] = userdetails.id

                return render(request, 'welcome5.html')
        except admin.DoesNotExist as e:
            return render(request, 'user name or password invalid')
    return render(request, 'login4.html')


"""def adddhomelogin(request):

    if request.method == 'POST':
        try:
            userdetails =homenurses.objects.get(email=request.POST['email'],password=request.POST['password'])
            print(userdetails.password)
            if userdetails.password == request.POST['password']:
                request.session['hid'] = userdetails.id

                return render(request, 'welcome5.html')
        except admin.DoesNotExist as e:
            return render(request, 'user name or password invalid')
    return render(request, 'login4.html')"""

def doctors(request):
    user = dregister.objects.filter(status='pending')

    return render(request, 'viewdoctors.html', {'res': user})



def approve(request,id):
    if request.method == 'GET':
        user = dregister.objects.get(id=id)
        user.status='approved'
        user.save()

    return redirect('doctors')


def viewpa(request):
    user = pregister.objects.filter(status='pending')

    return render(request, 'viewp.html', {'res': user})

def approvep(request,id):
    if request.method == 'GET':
        user = pregister.objects.get(id=id)
        user.status='approved'
        user.save()
        return redirect('viewpa')

def viewpha(request):
    user = phregister.objects.filter(status='pending')

    return render(request, 'viewpha.html', {'res': user})

def approvepha(request,id):
    if request.method == 'GET':
        user = phregister.objects.get(id=id)
        user.status='approved'
        user.save()
        return redirect('viewpha')
        
def requestapprove(request,id):
    user = homenurserequest.objects.get(id=id)
    a=user.pid
    b=user.homenurse_id
    c=user.amount
    d=user.description
    
    
    userr=homenurserequest(pid=a,homenurse_id=b,amount=c,description=d,status="approved",id=id)
    userr.save()
    return redirect('viewhomeuserrequest')

#def logoutt(request):
#       return render(request,'index.html')

#def logout5(request):
#   return render(request, 'index.html')

def logouttt(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
       del request.session[key]
   return redirect('first')

def logout10(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
       del request.session[key]
    return render(request, 'index.html')





def time(request):
    user = dregister.objects.filter(status='approved')

    return render(request, 'time.html', {'res': user})


"""def vp(request):
    #sid=request.session['sid']

    fetch_patients = payment.objects.all()
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[int(i.pid)],'id':i.id,'medicine':i.medicine,'date':i.date,'rate':i.rate,'cardno':i.cardno,'cardname':i.cardname})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)
    user2 = dregister.objects.all()

    user3 = l_payment.objects.all()   
    return render(request,'vp.html', {'data': fetch_patients,'res1':dat,'res2':user2,'res3':user3})"""




def viewhomeuserrequest(request):
    #sid=request.session['sid']

    fetch_patients = homenurserequest.objects.all()
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[int(i.pid)],'id':i.id,'amount':i.amount,'description':i.description})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)

    user = homenurserequest.objects.filter(status='pending')

    return render(request, 'homenurserequest.html', {'dat': fetch_patients,'res':dat})


def timeshe(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = times( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'time.html')
    else:
        # GET, generate unbound (blank) form
        form = time()
        return render(request,'time.html', {'form': form})




def viewlab(request):
    user = labreg.objects.filter(status='pending')

    return render(request, 'viewlab.html', {'res': user})


def approvelab(request,id):
    if request.method == 'GET':
        user = labreg.objects.get(id=id)
        user.status='approved'
        user.save()
        return redirect('viewlab')

def vp(request):
    #sid=request.session['sid']

    fetch_patients = payment.objects.all()
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[int(i.pid)],'id':i.id,'medicine':i.medicine,'date':i.date,'rate':i.rate,'cardno':i.cardno,'cardname':i.cardname})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)
    user2 = d_payment.objects.all()
    user_data1 = pregister.objects.all()
    user_dat1=dict()
    for i in user_data1:
        user_dat1[i.id]=i.p_name
    print(user_dat1)
    dat1=list()
    c=0
    for i in user2:
        dat1.append({'pid':user_dat[int(i.pid)],'id':i.id,'medicine':i.medicine,'date':i.date,'rate':i.rate,'cardno':i.cardno,'cardname':i.cardname})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)
    user3 = l_payment.objects.all()  
    user_data2 = pregister.objects.all()
    user_dat2=dict()
    for i in user_data2:
        user_dat2[i.id]=i.p_name
    print(user_dat2)
    dat2=list()
    c=0
    for i in user3:
        dat2.append({'pid':user_dat[int(i.pid)],'id':i.id,'medicine':i.medicine,'date':i.date,'rate':i.rate,'cardno':i.cardno,'cardname':i.cardname})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)    
    return render(request,'vp.html', {'data': fetch_patients,'res1':dat,'res2':dat1,'res3':dat2})






def export_page(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    
    
    
    

def addhomenurse(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        experience=request.POST.get('experience')
        specialization=request.POST.get('specialization')
        amount=request.POST.get('amount')
        password=request.POST.get('password')
        status=request.POST.get('status')

        if homenurses.objects.filter(email=email,password=password):
            return render(request,'homenurse.html',{'status':'Email or Password already Exists'})
           
        else:
            donor=homenurses(name=name,email=email,status=status,phone=phone,address=address,experience=experience,specialisation=specialization,amount=amount,password=password)
            donor.save()
        return render(request,'homenurse.html',{'status':'Successfully Inserted'})
