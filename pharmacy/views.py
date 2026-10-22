from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse
from patient.models import requests
from patient.models import payment
from django.contrib import messages #import messages

from .models import phregister
from .forms import select
from .models import bill
from .forms import stocks
from .models import stock
from patient.models import pregister

from .forms import ins

def phhome(request):
    return render(request, 'phhome.html')

def phreg(request):
    return render(request, 'phreg.html')

def phregisters(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = select( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'phreg.html')
    else:
        # GET, generate unbound (blank) form
        form = phregister()
        return render(request,'phreg.html', {'form': form})


def login4(request):
    return render(request, 'login4.html')




def log4(request):

    if request.method == 'POST':
        try:
            userdetails =phregister.objects.get(email=request.POST['email'],password=request.POST['password'],status='approved')
            if userdetails.password == request.POST['password']:
                request.session['phid'] = userdetails.id

                return render(request, 'welcome3.html')
        except phregister.DoesNotExist as e:
                return render(request,'login4.html',{'status':'You Are Not A valid User'})
    return render(request, 'welcome3.html')

def vie(request):
    if request.session.has_key('phid'):
        temp = request.session['phid']
        user=requests.objects.filter(pharmacy=temp,status='pending')


    return render(request, 'viewrequest.html',{'res':user})

def logout5(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
       del request.session[key]
   return redirect('first')


def billed(request,id):
    user = requests.objects.get(id=id)
    if request.session.has_key('phid'):
        temp=request.session['phid']
        users = phregister.objects.get(id=request.session['phid'])

    return render(request,'bill.html',{'result':user,'res':temp})


def billingg(request):
    if request.method=='POST':
        pid=request.POST.get('pid')
        pharmacyname=request.POST.get('pharmacyname')
        medicine=request.POST.get('medicine')
        date=request.POST.get('date')
        rate=request.POST.get('rate')
        status=request.POST.get('status')
        
        log=bill(pid=pid,pharmacyname=pharmacyname,medicine=medicine,date=date,rate=rate,status=status)
        log.save()
    return render(request,'bill.html')






def viewpay(request):
    name=request.session['phid']
    fetch_patients = payment.objects.filter(pname=name)
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
    return render(request,'viewpayment.html', {'data': fetch_patients,'res':dat})
    #user = payment.objects.all()
    


def viewstock(request):
    user = stock.objects.all()

    return render(request,'viewstock.html',{'res':user})


def viewwrequest(request):
    user = requests.objects.all()

    return render(request,'viewwrequest.html',{'res':user})


def addstock(request):
    return render(request, 'addstock.html')


def addstocks(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = stocks( request.POST)
        # check if it's valid:
        if form.is_valid():

            #Insert into DB
            form.save()

            messages.success(request,"Stock Add  Successfull")

        #redirect to a new URL:
            return render(request, 'addstock.html')
    else:
        # GET, generate unbound (blank) form
        form = stock()
        return render(request,'addstock.html', {'form': form})
        
        
def updatestock(request,id):
    user = stock.objects.get(id=id)


    return render(request,'updatestock.html',{'result':user})


def editstock(request,id):
    if request.method == 'POST':
        p=request.POST['medicine']
        i=request.POST['rate']
        rt=request.POST['export_date']
        d=request.POST['expiry_date']
        dt=request.POST['availability']

        
        data = stock(medicine=p,rate=i,export_date=rt,expiry_date=d,availability=dt,id=id)

        data.save()

        return redirect(viewstock)

      
def deletestock(request,id):
    user = stock.objects.get(id=id)
    user.delete()

    return redirect(viewstock)
