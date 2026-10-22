from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import dregister
from .models import prescription
from .forms import insert1
from .forms import vedios
from .models import vediocall

from .forms import insert
from patient.models import booking
from patient.models import d_payment
from patient.models import pregister

def dhome(request):
    return render(request, 'dhome.html')

def dreg(request):
    return render(request, 'dreg.html')
def dregisters(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = insert( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'dreg.html')
    else:
        # GET, generate unbound (blank) form
        form = dregister()
        return render(request,'dreg.html', {'form': form})


def bkd(request):
    dname=request.session['dname'] 
    fetch_patients = booking.objects.filter(did=dname)
    print(fetch_patients)
    user_data = pregister.objects.all()
    user_dat=dict()
    for i in user_data:
        user_dat[i.id]=i.p_name
    print(user_dat)
    dat=list()
    c=0
    for i in fetch_patients:
        dat.append({'pid':user_dat[int(i.pid)],'id':i.id,'did':i.did,'rate':i.rate,'date':i.date})
        #names.append(user_dat[int(i.studentname)])
        c+=1
    print(dat)
    user = dregister.objects.all()
    return render(request, 'vbooks.html', {'data': fetch_patients,'res':dat})


def login1(request):
    return render(request, 'login1.html')

def logout(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
       del request.session[key]
   return redirect('first')

def log1(request):

    if request.method == 'POST':
        try:
            userdetails =dregister.objects.get(email=request.POST['email'],password=request.POST['password'],status='approved')
            if userdetails.password == request.POST['password']:
                request.session['did'] = userdetails.id
                request.session['dname'] = userdetails.name

                return render(request, 'welcome1.html')
        except dregister.DoesNotExist as e:
            return render(request,'login1.html',{'status':'You Are Not A valid User'})
            
    return render(request, 'welcome1.html')


def profile(request):
        temp=request.session['did']
        user = dregister.objects.get(id=request.session['did'])
        print(user.name)
        # us=[]n
        email = user.email
        return render(request, 'dprofile.html', {'result': user})
        # us['id']=user.id
        #
def pres(request,id):
    user = booking.objects.get(id=id)
    return render(request,'pres.html',{'result':user})


def prescript(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = insert1( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'pres.html')
    else:
        # GET, generate unbound (blank) form
        form = prescription()
        return render(request,'pres.html', {'form': form})


def viewss(request):
    user = prescription.objects.all()


    return render(request,'views.html',{'result':user})


def vedio(request,id):
    user = booking.objects.get(id=id)


    return render(request,'vedio.html',{'result':user})

def vediocalls(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = vedios( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
        return render(request,'vedio.html')
    else:
        # GET, generate unbound (blank) form
        form = vediocall()
        return render(request,'vedio.html', {'form': form})

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
    user2 = dregister.objects.all()

    user3 = l_payment.objects.all()   
    return render(request,'vp.html', {'data': fetch_patients,'res1':dat,'res2':user2,'res3':user3})

def viewdoctorpayment(request):  
    dname=request.session['dname']
    fetch_patients = d_payment.objects.filter(dname=dname)
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
    return render(request,'view_doctor_payment.html', {'data': fetch_patients,'result':dat})



def updateprofile(request,id):
    user = dregister.objects.get(id=id)
    return render(request,'updateprofile.html',{'result':user})



def updatedr(request,id):
    if request.method == 'POST':
        p=request.POST['name']
        i=request.POST['specialisation']
        rt=request.POST['email']
        d=request.POST['phno']
        dt=request.POST['fees']
        s=request.POST['status']
        st=request.POST['password']

        
        data = dregister(name=p,specialisation=i,email=rt,phno=d,fees=dt,status=s,password=st,id=id)

        data.save()

        return redirect(profile)

