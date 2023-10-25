from django.urls import path
from . import views
from .views import InventoryView, PurchaseView, MenuView, FinancialsView, IngredientDeleteView, home
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='base'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('purchases/', PurchaseView.as_view(), name='purchases'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('financials/', FinancialsView.as_view(), name='financials'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('add_recipe_requirement/', views.add_recipe_requirement, name='add_recipe_requirement'),
    path('purchase_menu_item/', views.purchase_menu_item, name='record_purchase'),
    path('login/', LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]