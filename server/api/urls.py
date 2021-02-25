from django.urls import include, path
from . import views

urlpatterns = [
  path('ping', views.ping),
  path('ping2', views.ping_for_logged),

  path('getnotifs', views.get_notifications),
  path('addnotif', views.add_notification),
  path('updatenotif/<int:notif_id>', views.update_notification),
  path('deletenotif/<int:notif_id>', views.delete_notification)
]