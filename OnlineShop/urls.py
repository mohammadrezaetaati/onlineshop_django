

from django.contrib import admin
from django.urls import path,include
from Shopping.views import ProductShow # a better name maybe?

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Shopping.urls')),
    path('', include('Payment.urls')),
    path('', ProductShow.as_view(),name='productshow'),
    path('', include('User.urls')),
    path('accounts/', include('allauth.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)