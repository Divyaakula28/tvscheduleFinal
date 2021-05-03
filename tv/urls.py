from tv import views
from django.urls import path, include

urlpatterns = [
    path('loc/',views.loc,name='loc'), 
    path('drop/',views.drop,name='drop'), 
    path('home/',views.home,name='home'),
    path('home1/',views.home1,name='home1'), 
    path('nav/',views.nav,name='nav'), 
    path('dis/',views.dis,name='dis'), 
    path('test/',views.test,name='test'),
    path('all/',views.all,name='all'),
    path('present/',views.present,name='present'),     
]
