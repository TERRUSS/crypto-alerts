from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('deleteAccount/', views.deleteAccount)
]