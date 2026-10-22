from django.shortcuts import render
from django.shortcuts import redirect

from takecare.models import time
from .models import medical_report
from doctor.models import vediocall

from pharmacy.models import phregister
from .models import payment
from labs.models import labreg
from labs.models import testreport
from takecare.models import homenurses

from .models import *
from .forms import ins
from .forms import med
from .forms import req1
from .forms import pays

from .models import requests
from pharmacy.models import bill
from labs.models import labbill

from .forms import booked
from doctor.models import prescription
from doctor.models import dregister

def phome(request):
    return render(request, 'phome.html')
def dash(request):
    return render(request, 'index.html')



def preg(request):
    return render(request, 'preg.html')

def pregisters(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ins( request.POST)
        print(form)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()

        #redirect to a new URL:
            return render(request, 'preg.html')
    else:
        # GET, generate unbound (blank) form
        form = pregister()
        return render(request,'preg.html', {'form': form})

def log2(request):
        return render(request, 'log1.html')





def loginn1(request):

    if request.method == 'POST':
        try:
            userdetails =pregister.objects.get(email=request.POST['email'],password=request.POST['password'],status='approved')
            if userdetails.password == request.POST['password']:
                request.session['pid'] = userdetails.id
                request.session['pname'] = userdetails.p_name
                return render(request, 'welcome2.html')
        except pregister.DoesNotExist as e:
            return render(request,'log1.html',{'status':'You Are Not A valid User'})
    return render(request, 'welcome2.html')



def pprofile(request):
    temp=request.session['pid']
    user = pregister.objects.get(id=request.session['pid'])
        #pprofile=pregister.objects.all(user=user)
        # us=[]
        # us['id']=user.id
        # email= user.email
    return render(request, 'pprofile.html', {'result': user})


      
def updatepprofile(request,id):
    user = pregister.objects.get(id=id)


    return render(request,'updatepprofile.html',{'result':user})


def updatepatient(request,id):
    if request.method == 'POST':
        p=request.POST['p_name']
        i=request.POST['address']
        rt=request.POST['email']
        d=request.POST['pincode']
        dt=request.POST['age']
        s=request.POST['status']
        st=request.POST['password']

        
        data = pregister(p_name=p,address=i,email=rt,pincode=d,age=dt,status=s,password=st,id=id)

        data.save()

        return redirect(pprofile)

'''def viewtime(request):
    user = time.objects.filter()
    return render(request, 'viewtime.html',{'res':user})'''

def viewtime(request):
    user = time.objects.filter(status='available')
    return render(request, 'viewtime.html', {'res': user})


def viewhomenurse(request):
    user = homenurses.objects.filter(status='available')

    return render(request, 'viewhomenurse.html', {'res': user})



def book(request,id):
    user = time.objects.get(id=id)
    u=user.name
    userss = dregister.objects.get(name=u)

    if request.session.has_key('pid'):
        temp = request.session['pid']
        print("hello",temp)
        if request.method == 'GET':
            user = time.objects.get(id=id)
            user.status = 'booked'
            user.save()

        patient = pregister.objects.get(id = request.session['pid'])

    return render(request,'book.html',{'result':user,'res':patient,'row':userss})

def booking(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = booked( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'book.html')
    else:
        # GET, generate unbound (blank) form
        form = pregister()
        return render(request,'book.html', {'form': form})


#def vbook(request):
    #if request.session.has_key('pid'):
        #temp=request.session['pid']
        #print("hello", temp)
        #user = booking.objects.filter(pid=temp)
        #print("hello",user)
    #user = book.objects.all()

    #return render(request,'viewbook.html',{'res': user})


def next(request):
    return render(request, 'phome.html')



def logout1(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
       del request.session[key]
   return redirect('first')


def homes(request):
    return render(request, 'welcome2.html')




def viewp(request):
    a=request.session['pid']
    user = prescription.objects.filter(pname=a)
    return render(request,'viewpre.html', {'res': user})



def reports(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = med( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'medical.html')
    else:
        # GET, generate unbound (blank) form
        form = medical_report()
        return render(request,'medical.html', {'form': form})

def report(request):
    if request.session.has_key('pid'):
        temp=request.session['pid']
        user = pregister.objects.get(id=request.session['pid'])
        # us=[]
        # us['id']=user.id
        # email= user.email

        return render(request, 'medical.html', {'result': user})

def vcall(request):
    user = vediocall.objects.all()
    return render(request,'view_vediocall.html', {'res': user})




def request(request,id):
    user = prescription.objects.get(id=id)
    users = phregister.objects.all()
    userss = labreg.objects.all()




    return render(request,'request.html',{'result':user,'row':users,'rs':userss})

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


def viewbill(request):
    pid=request.session['pid']

    fetch_patients = bill.objects.filter(pid=pid)
    '''print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[str(i.pid)],'id':i.id,'date':i.date,'medicine':i.medicine,'rate':i.rate,})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)'''
    return render(request,'viewbill.html',{'res': fetch_patients})


def pay(request,id):
    user = prescription.objects.get(id=id)
    if request.session.has_key('pid'):
        temp = request.session['pid']
        print("hello", temp)

        users = pregister.objects.get(id=request.session['pid'])

    return render(request, 'pay.html', {'res': user,'result':temp})




def labsuserpay(request,id):
    user = labbill.objects.get(id=id)


    return render(request, 'paylabs.html', {'res': user})
def pharmacypay(request,id):
    user = bill.objects.get(id=id)
    if request.session.has_key('pid'):
        temp = request.session['pid']
        print("hello", temp)

        users = pregister.objects.get(id=request.session['pid'])

    return render(request, 'paypharmacy.html', {'res': user,'result':temp})
def addhomenurserequest(request):
    if request.method=="POST":
        amount=request.POST.get('amount')
        homenurse_id=request.POST.get('homenurse_id')
        description=request.POST.get('description')
        cardname=request.POST.get('cardname')
        cardtype=request.POST.get('cardtype')
        cardno=request.POST.get('cardno')
        pid=request.session['pid']
        donor=homenurserequest(amount=amount,homenurse_id=homenurse_id,description=description,cardname=cardname,cardtype=cardtype,cardno=cardno,status='pending',pid=pid)
        donor.save()
        return redirect(viewhomenurse)






def paymentpharmacy(request):
    if request.method=='POST':
        pid=request.POST.get('pid')
        medicine=request.POST.get('medicine')
        date=request.POST.get('date')
        rate=request.POST.get('rate')
        cardno=request.POST.get('cardno')
        cardname=request.POST.get('cardname')
        cardmonth=request.POST.get('cardmonth')
        cardyear=request.POST.get('cardyear')
        phname=request.POST.get('phname')
        cv=request.POST.get('cv')

        log=payment(pid=pid,pname=phname,medicine=medicine,date=date,rate=rate,cardno=cardno,cardname=cardname,cardmonth=cardmonth,cardyear=cardyear,cv=cv)
        log.save()
    return render(request,'paypharmacy.html')

def labuserpayment(request):
    if request.method=='POST':
        pid=request.POST.get('pid')
        medicine=request.POST.get('medicine')
        date=request.POST.get('date')
        rate=request.POST.get('rate')
        cardno=request.POST.get('cardno')
        cardname=request.POST.get('cardname')
        cardmonth=request.POST.get('cardmonth')
        cardyear=request.POST.get('cardyear')
        labname=request.POST.get('labname')
        cv=request.POST.get('cv')

        log=l_payment(pid=pid,labname=labname,medicine=medicine,date=date,rate=rate,cardno=cardno,cardname=cardname,cardmonth=cardmonth,cardyear=cardyear,cv=cv)
        log.save()
    return render(request,'paylabs.html')

def homerequest(request,id):
    user = homenurses.objects.get(id=id)
    '''a=user.name
    b=user.email
    c=user.address
    d=user.phone
    e=user.password
    f=user.specialisation
    h=user.experience
    i=user.amount
    ress=homenurses(name=a,email=b,address=c,phone=d,password=e,specialisation=f,experience=h,amount=i,status='allo',id=id)'''
    
    return render(request, 'requesthome.html', {'res': user})



def paymenttt(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = pays( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'pay.html')
    else:
        # GET, generate unbound (blank) form
        form = d_payment()
        return render(request,'pay.html', {'form': form})



def requestss(request):
    if request.method == 'POST':
        a=request.POST.get("dname")
        print(a)
        b=request.POST.get("diseases")
        print(a)
        c=request.POST.get("medicine")
        print(a)
        d=request.POST.get("date")
        print(a)
        e=request.POST.get("pharmacy")
        print(a)
        f=request.POST.get("lab")
        print(a)
        g = request.POST.get("pid")
        print(a)
        # POST, generate bound form with data from the request
        # check if it's valid:
        userr=requests(dname=a,diseases=b,medicine=c,date=d,pharmacy=e,lab=f,pid=g,status='pending')
        userr.save()
        return render(request,'request.html')
    else:
        # GET, generate unbound (blank) form
        form = requests()
        return render(request,'request.html', {'form': form})


def vieww(request):
    return render(request, 'viewwbill.html')


def viewlabbill(request):
    pid=request.session['pid']
    fetch_patients = labbill.objects.filter(pid=pid)

    return render(request,'viewlabbill.html', {'res': fetch_patients})
    

def viewdbill(request):
    a=request.session['pid']
    user = prescription.objects.filter(pname=a)
    return render(request,'viewdbill.html', {'res': user})

def call(request):
    if request.session.has_key('pid'):
        temp = request.session['pid']
        user = vediocall.objects.filter(pid=temp)
    return render(request, 'call.html', {'res': user})


def viewpbill(request,id):
    user = bill.objects.get(id=id)
    if request.session.has_key('pid'):
        temp = request.session['pid']
        print("hello", temp)

        users = pregister.objects.get(id=request.session['pid'])

    return render(request, 'viewpbill.html', {'res': user,'result':users})

def download(request,id):
    user = prescription.objects.get(id=id)

    return render(request, 'print.html',{'result':user})
def clickhere(request,id):
    user = testreport.objects.get(id=id)

    return render(request, 'viewreport.html',{'result':user})

def viewr(request):
    if request.session.has_key('pid'):
        temp = request.session['pid']
        print("hello", temp)
        users=testreport.objects.filter(p_id=request.session['pid'])
    return render(request, 'viewr.html',{'result':users})

