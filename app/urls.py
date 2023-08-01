from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home_page'),
    path('more_products/<int:pk>/',views.details,name='product_details'),
    path('electronics/<int:pk>/',views.electronics,name='electronics'),
    path('product/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('Signup/',views.Signup,name='Signup'),
    path('success_page/',views.success,name='successpage'),
    path('login_page/',views.login,name='login'),
    path('delete_product/<int:pk>',views.deletecat,name='delete_product'),
    path('update/<int:pk>',views.update,name='update_product'),
    path('checkout/',views.checkout,name='checkout')

    
]
