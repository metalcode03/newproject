from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('checkout', views.checkout_page, name='checkout'),
    path('order-summary', views.OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    # path('product', views.product_page, name='product'),
]
