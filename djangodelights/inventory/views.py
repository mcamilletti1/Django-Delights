from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
# Create your views here.

class InventoryView(TemplateView):
    template_name = 'inventory.html'

    def get_context_data(self, **kwargs)
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context

class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'ingredient_confirm_delete.html'
    success_url = reverse_lazy('inventory')   
    
class PurchaseView(TemplateView):
    template_name = 'purchase.html'

    def get_contest_data(self, **kwargs)
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        return context
    
class MenuView(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        return context
    
class FinancialsView(TemplateView):
    template_name = 'financials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_revenue = Purchase.objects.aggregate(total=Sum('menu_item__price'))['total']
        total_cost = sum([req.ingredient.unit_price * req.quantity for purchase in Purchase.objects.all() for req in RecipeRequirement.objects.filter(menu_item=purchase.menu_item)])
        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = total_revenue - total_cost
        return context