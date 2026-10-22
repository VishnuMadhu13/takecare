
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.labshome, name='labshome'),
    path('labsreg', views.labsreg, name='labsreg'),
    path('labregi', views.labregi, name='labregi'),
    path('lg', views.lg, name='lg'),
    path('lg1', views.lg1, name='lg1'),
    path('vpay', views.vpay, name='vpay'),
    path('vbillss', views.vbillss, name='vbillss'),
    path('bills/<int:id>', views.bills, name='bills'),
    path('bills/billings', views.billings, name='billings'),
    path('logouts', views.logouts, name='logouts'),
    path('labcategory', views.labcategory, name='labcategory'),
    path('labcategorys', views.labcategorys, name='labcategorys'),
    path('addtest', views.addtest, name='addtest'),
    path('addtests', views.addtests, name='addtests'),
    path('viewtest', views.viewtest, name='viewtest'),
    path('testreport/<int:id>', views.testreport, name='testreport'),
    path('testreport/testreports', views.testreports, name='testreports'),
    path('deletecat/<int:id>', views.deletecat, name='deletecat'),

    path('viewtestcategory', views.viewtestcategory, name='viewtestcategory'),

    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)