from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_new_poll, name='upload'),
    path('thankyou/', views.update_thankyou, name='update_thanks')
]