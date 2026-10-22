
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.phome, name='phome'),
    path('preg', views.preg, name='preg'),
    path('pregisters', views.pregisters, name='pregisters'),
    path('log2', views.log2, name='log2'),
    path('loginn1', views.loginn1, name='loginn1'),
    path('pprofile', views.pprofile, name='pprofile'),
    path('viewtime', views.viewtime, name='viewtime'),
    path('book/<int:id>', views.book, name='book'),
    path('labsuserpay/<int:id>', views.labsuserpay, name='labsuserpay'),
    path('labsuserpay/labuserpayment', views.labuserpayment, name='labuserpayment'),
    path('book/booking', views.booking, name='booking'),
    path('logout1', views.logout1, name='logout1'),
    path('viewp', views.viewp, name='viewp'),
    path('viewbill', views.viewbill, name='viewbill'),
    path('pay/<int:id>', views.pay, name='pay'),
    
    path('pharmacypay/<int:id>', views.pharmacypay, name='pharmacypay'),
    path('pharmacypay/paymentpharmacy', views.paymentpharmacy, name='paymentpharmacy'),

    path('clickhere/<int:id>', views.clickhere, name='clickhere'),
    path('homerequest/<int:id>', views.homerequest, name='homerequest'),
    path('homerequest/addhomenurserequest', views.addhomenurserequest, name='addhomenurserequest'),
    path('pay/paymenttt', views.paymenttt, name='paymenttt'),
    path('next', views.next, name='next'),
    path('homes', views.homes, name='homes'),
    path('viewr', views.viewr, name='viewr'),
    path('dash', views.dash, name='dash'),

    path('viewbill', views.viewbill, name='viewbill'),
    path('viewhomenurse', views.viewhomenurse, name='viewhomenurse'),
    path('download/<int:id>', views.download, name='download'),
    path('updatepprofile/<int:id>', views.updatepprofile, name='updatepprofile'),

    path('updatepprofile/updatepatient/<int:id>', views.updatepatient, name='updatepatient'),

    path('viewpbill', views.viewpbill, name='viewpbill'),
    path('vieww', views.vieww, name='vieww'),
    path('viewlabbill', views.viewlabbill, name='viewlabbill'),
    path('viewdbill', views.viewdbill, name='viewdbill'),
    path('call', views.call, name='call'),
    path('report', views.report, name='report'),
    path('reports', views.reports, name='reports'),
    path('viewp/<int:id>/', views.request, name='viewp'),
    path('request/<int:id>', views.request, name='request'),
    path('request/requestss', views.requestss, name='requestss'),
    

    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)