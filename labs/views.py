from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import labreg
from .models import testreport
from .forms import testsreport

from patient.models import payment
from patient.models import requests
from .forms import labbills
from .forms import testcategory
from .forms import regg

from .forms import labtestadd
from .models import labreg
from .models import labbill
from .models import labtestcat
from .models import labtest
from patient.models import pregister
from patient.models import l_payment

def labshome(request):
    return render(request, 'labshome.html')

def labsreg(request):
    return render(request, 'labreg.html')

def logouts(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
       del request.session[key]
   return redirect('first')


def labregi(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = regg( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
        return render(request, 'labreg.html')
    else:
        # GET, generate unbound (blank) form
        form = labreg()
        return render(request,'labreg.html', {'form': form})

def lg(request):
    return render(request, 'lg.html')


"""def log1(request):

    if request.method == 'POST':
        try:
            userdetails =dregister.objects.get(email=request.POST['email'],password=request.POST['password'],status='approved')
            if userdetails.password == request.POST['password']:
                request.session['did'] = userdetails.id

                return render(request, 'welcome1.html')
        except dregister.DoesNotExist as e:
            return render(request,'login1.html',{'status':'You Are Not A valid User'})
    return render(request, 'welcome1.html')"""

def lg1(request):

    if request.method == 'POST':
        try:
            userdetails =labreg.objects.get(email=request.POST['email'],password=request.POST['password'],status='approved')
            print(userdetails.password)
            if userdetails.password == request.POST['password']:
                request.session['lid'] = userdetails.id

                return render(request, 'welcome4.html')
        except labreg.DoesNotExist as e:
                return render(request,'lg.html',{'status':'You Are Not A valid User'})
    return render(request, 'welcome4.html')

def vpay(request):
    lid=request.session['lid']
    fetch_patients = l_payment.objects.filter(labname=lid)
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[int(i.pid)],'id':i.id,'medicine':i.medicine,'date':i.date,'rate':i.rate,'cardno':i.cardno})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)
    return render(request,'vpt.html', {'data': fetch_patients,'res':dat})

    #user = payment.objects.all()
    #return render(request,'vpt.html',{'res':user})



def vbillss(request):
    user=requests.objects.all()
    return render(request, 'vrequests.html',{'res':user})

def labcategory(request):
    return render(request, 'category.html')


def bills(request,id):
    user = requests.objects.get(id=id)
    if request.session.has_key('lid'):
        temp=request.session['lid']
        users = labreg.objects.get(id=request.session['lid'])

    return render(request,'bills.html',{'result':user,'res':temp})

def billings(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = labbills( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'bills.html')
    else:
        # GET, generate unbound (blank) form
        form = labbill()
        return render(request,'bills.html', {'form': form})

def labcategorys(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = testcategory( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
        return redirect('viewtestcategory')
    else:
        # GET, generate unbound (blank) form
        form = labtestcat()
        return render(request,'category.html', {'form': form})


def addtest(request):
    user = labtestcat.objects.all()

    return render(request, 'addtest.html',{'result':user})

def addtests(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = labtestadd( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
        return redirect('vpay')
    else:
        # GET, generate unbound (blank) form
        form = labtest()
        return render(request,'addtest.html', {'form': form})


def viewtest(request):
    user = labtest.objects.all()

    return render(request, 'viewtest.html',{'result':user})


def testreport(request,id):
    user = payment.objects.get(id=id)
    if request.session.has_key('lid'):
        temp=request.session['lid']
        users = labreg.objects.get(id=request.session['lid'])

    return render(request,'testreport.html',{'result':user,'res':users})


def testreports(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = testsreport( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
        return redirect('vpay')
    else:
        # GET, generate unbound (blank) form
        form = testreport()
        return render(request,'testreport.html', {'form': form})
        
        
        

def viewtestcategory(request):
    user = labtestcat.objects.all()

    return render(request, 'viewcategory.html',{'res':user})
    
    
def deletecat(request,id):
    user = labtestcat.objects.get(id=id)
    user.delete()
    return redirect('viewtestcategory')
    
    