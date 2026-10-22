
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.phhome, name='phhome'),
    path('phreg', views.phreg, name='phreg'),
    path('logout5', views.logout5, name='logout5'),
    path('billed/<int:id>', views.billed, name='billed'),
    path('billed/billingg', views.billingg, name='billingg'),
    path('viewpay', views.viewpay, name='viewpay'),
    path('viewwrequest', views.viewwrequest, name='viewwrequest'),
    path('addstock', views.addstock, name='addstock'),
    path('addstocks', views.addstocks, name='addstocks'),
    path('viewstock', views.viewstock, name='viewstock'),
    
    path('updatestock/<int:id>', views.updatestock, name='updatestock'),
    path('updatestock/editstock/<int:id>', views.editstock, name='editstock'),
    path('deletestock/<int:id>', views.deletestock, name='deletestock'),

    path('phregisters', views.phregisters, name='phregisters'),
    path('login4', views.login4, name='login4'),
    path('log4', views.log4, name='log4'),
    path('vie', views.vie, name='vie'),

    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)