from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.labhome, name='labhome'),
    path('labreg', views.labreg, name='labreg'),
    path('labregi', views.labregi, name='labregi'),
    path('logg5', views.logg5, name='logg5'),
    path('viewbills', views.viewbills, name='viewbills'),
    path('billss/<int:id>', views.billss, name='billss'),
    path('billss/billings', views.billings, name='billings'),
    path('viewspayment', views.viewspayment, name='viewspayment'),

    path('loog5', views.loog5, name='loog5'),

    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)