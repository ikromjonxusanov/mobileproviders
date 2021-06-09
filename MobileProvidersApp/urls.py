from django.urls import path
from .views import *

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', home, name="home"),
    path('providers/', providers, name="providers"),
    path('providers/<int:pk>', provider, name="provider"),
    path('providers/number/create/<int:pk>/', numberCreate, name="numberCreateMore"),
    path('numbers/', numbers, name="numbers"),
    path('numbers/buy/<int:pk>/', numberBuy, name="numberBuy"),
    path('clients/', clients, name="clients"),
    path('providers/settings/', providerSettings, name="providerSettings"),
    path('registration/provider/', registerPro, name="regProvider"),
    path('registration/dealer/', registerDealler, name="regDealer"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
