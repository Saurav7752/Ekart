from django.urls import path
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),     
    path('about',views.about),
    path('edit/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('greet',views.greet),
    path('addproduct',views.addproduct),
    path('index',views.index),
    path('details/<id>',views.details),
    path('login',views.userlogin),
    path('register',views.register),
    path('payment',views.payment),
    path('order',views.place_order),
    path('contact',views.contact),
    path('addcart/<rid>',views.addcart),
    path('catfilter/<cv>',views.catfilter),
    path('pricerange',views.pricerange),
    path('sort/<sv>',views.sort),
    path('logout',views.user_logout),
    path('cart',views.viewcart),
    path('remove/<rid>',views.removecart),
    path('cartqty/<sig>/<pid>',views.cartqty),
    path('sendmail',views.sendmail)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)