from django.urls import path
from .views import InventoryView, PurchaseView, MenuView, FinancialsView, IngredientDeleteView

urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('purchases.', PurchaseView.as_view(), name='purchases'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('financials/', FinancialsView.as_view(), name='financials'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
]