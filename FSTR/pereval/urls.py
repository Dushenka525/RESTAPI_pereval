from django.urls import path
from . import views

urlpatterns = [
    path('submitData/', views.submit_data, name='submit_data'),
    path('images/', views.ImageUploadView.as_view(), name='image-upload'),

]