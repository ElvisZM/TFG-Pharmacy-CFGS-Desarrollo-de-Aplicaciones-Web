"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include 
from App_AuthUsers import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('service/auth/users/', include('App_AuthUsers.urls')),
    # path('service/cart/promos/', include('App_CartPromos.urls')),
    path('service/product/provider/', include('App_ProductProvider.urls')),
    # path('service/sells/subs/', include('App_SellsSubs.urls')),
    path('oauth2/', include('oauth2_provider.urls',namespace='oauth2_provider')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler400 = 'App_Farmacia.views.mi_error_400'
# handler403 = 'App_Farmacia.views.mi_error_403'
# handler404 = 'App_Farmacia.views.mi_error_404'
# handler500 = 'App_Farmacia.views.mi_error_500'

