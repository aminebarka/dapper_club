from django.urls import path
from . import views

urlpatterns = [
    path('place-order', views.place_order, name='place_order'),
    path('cancel-order/<int:order_number>', views.cancel_order, name='cancel_order'),

    
    

]