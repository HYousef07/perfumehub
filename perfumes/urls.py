from django.urls import path
from . import views

app_name = 'perfumes'

urlpatterns = [
    path('', views.prod_list, name='all_products'),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('product/<int:pk>/', views.PerfumeDetailView.as_view(), name='product_detail'),
]