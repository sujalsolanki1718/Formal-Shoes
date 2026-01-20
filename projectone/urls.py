"""
URL configuration for projectone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # client urls
    # path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('shop/',views.shop,name="shop"),
    path('cart/', views.cart,name="cart"),
    path('remove/<int:id>/',views.remove,name="remove"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path("clogout/", views.clogout, name="clogout"),
    path("oneproduct/<int:id>/",views.oneproduct,name="oneproduct"),

    path('checkout/',views.checkout,name="checkout"),


    # Admin urls

      path("admin/",views.alogin,name="alogin"),
      path("products/", views.products, name="products"),
      path("logout/", views.logout, name="logout"),
      path("viewproduct/",views.viewproduct,name="viewproduct"),
      path("vieworders/",views.vieworders,name="vieworders"),
      path("viewusers/",views.viewusers,name="viewusers"),
      path("report/",views.report,name="report"),
      path("viewaddress/<str:name>/",views.viewaddress,name="viewaddress"),
      path("delete/<int:id>/",views.delete,name="delete"),
      path("update/<int:id>/",views.update,name="update"),


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


