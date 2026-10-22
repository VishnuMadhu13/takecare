from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import labreg
from .forms import regg
from .forms import labbills
from .models import labreg
from .models  import labbill
from patient.models  import payment


from patient.models import requests

def labhome(request):
    return render(request, 'labhome.html')

def labreg(request):
    return render(request, 'labreg.html')


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

def logg5(request):
    return render(request, 'login5.html')


def loog5(request):

    if request.method == 'POST':
        try:
            userdetails =labreg.objects.get(email=request.POST['email'])
            if userdetails.password == request.POST['password']:
                request.session['lid'] = userdetails.id

                return render(request,'welcome4.html')
        except labreg.DoesNotExist:
                return render(request, 'user name or password invalid')
    return render(request, 'welcome4.html')



def logout5(request):
    return render(request, 'index.html')

def viewbills(request):
    user=payment.objects.all()
    return render(request, 'viewrequests.html',{'res':user})



def billss(request,id):
    user = requests.objects.get(id=id)


    return render(request,'labbills.html',{'result':user})

def billings(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = labbills( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'bill.html')
    else:
        # GET, generate unbound (blank) form
        form = labbill()
        return render(request,'bill.html', {'form': form})




def viewspayment(request):
    user = payment.objects.all()


    return render(request,'viewss.html',{'result':user})