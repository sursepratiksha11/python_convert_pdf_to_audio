from django.urls import path
from . import views

urlpatterns =[
 	path('login', views.login),
    path('home/', views.home),
    path('signup/', views.SignUp1),
    path('text/', views.TextToLang),
    path('', views.HomePage),
    path('download/', views.download, name='download')
    # path('process_upload', views.process_upload, name='process_upload'),
]