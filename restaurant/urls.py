"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restaurant import views
from django.conf.urls.static import static
from .import settings
from .views import OrderPanel
from .views import Cart
from .views import Checkout
from .views import Myorders
from order.middlewares.auth import auth_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    path('restro/',views.index,name='restro'),
    path('register',views.register,name='register'),

    path('login',views.login,name='login'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('confirm_pwd<token>',views.confirm_pwd,name='confirm_pwd'),
    path('logout',views.logout,name='logout'),
    
    path('booktable',views.booktable,name='booktable'),
    path('table_booked',views.table_booked,name='table_booked'),
   
    path('order',views.order,name='order'), 
    path('orderpanel',OrderPanel.as_view(),name='orderpanel'), 
    path('cart',Cart.as_view(),name='cart'),
    path('checkout',Checkout.as_view(),name='checkout'),
    path('myorders',auth_middleware(Myorders.as_view()),name='myorders'),
   
    path('contact',views.contact,name='contact'),  



   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

