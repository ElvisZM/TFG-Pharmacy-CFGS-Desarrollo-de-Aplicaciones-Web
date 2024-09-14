from django.urls import path
from .import views

urlpatterns = [
    path('openai/api', views.get_answer_bot_openai),
    path('end/chat', views.terminar_chat)
    
]