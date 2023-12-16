from django.urls import path 
from .finance.chatgpt import views 
  
  
urlpatterns = [ 
    
    path('', views.query_view, name='query'), 
  
]