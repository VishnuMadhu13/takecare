from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.dhome, name='dhome'),
    path('dreg', views.dreg, name='dreg'),
    path('dregisters', views.dregisters, name='dregisters'),
    path('login1', views.login1, name='login1'),
    path('log1', views.log1, name='log1'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('bkd', views.bkd, name='bkd'),
    path('pres/<int:id>', views.pres, name='pres'),
    path('pres/prescript', views.prescript, name='prescript'),
    path('viewss', views.viewss, name='viewss'),
    path('vedio/<int:id>', views.vedio, name='vedio'),
    path('vedio/vediocalls', views.vediocalls, name='vediocalls'),
    
    path('viewdoctorpayment', views.viewdoctorpayment, name='viewdoctorpayment'),
    path('updateprofile/<int:id>', views.updateprofile, name='updateprofile'),
    path('updateprofile/updatedr/<int:id>', views.updatedr, name='updatedr'),

    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)