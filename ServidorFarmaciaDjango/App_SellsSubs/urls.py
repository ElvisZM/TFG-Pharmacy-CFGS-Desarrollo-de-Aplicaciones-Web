from django.urls import path
from .import views

urlpatterns = [
    path('save/payment', views.save_payment),
    path('create/review', views.create_review),
    path('product/review/<int:product_id>', views.product_reviews)
    
    
]