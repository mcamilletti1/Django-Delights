from django.shortcuts import render, redirect
from .forms import IngredientForm, PurchaseForm, MenuItemForm, RecipeRequirementForm
from .models import Ingredient, RecipeRequirement
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def home(request):
    return render(request, 'inventory/base.html')

@login_required
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory/inventory.html')
    else: 
        form = IngredientForm()
    return render(request, 'add_ingredient.html', {'form': form})

@login_required
def purchase_menu_item(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            menu_item = form.cleaned_data.get('menu_item')
            requirements = RecipeRequirement.objects.filter(meneu_item=menu_item)
            for req in requirements:
                ingredient = req.ingredient
                if ingredient.quantity < req.quantity:
                    return render(request, 'error.html', {'message': 'Not enought ingredients'})
                ingredient.quantity -= req.quantity
                ingredient.save()
            form.save()
            return redirect('inventory/menu.html')
        else:
            form = PurchaseForm()
        return render(request, 'purchase_menu_item.html', {'form': form})
 
@login_required   
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory/menu.html') 
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})

@login_required
def add_recipe_requirement(request):
    if request.method == 'POST':
        form = RecipeRequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory/inventory.html')
    else:
        form = RecipeRequirementForm()
    return render(request, 'add_recipe_requirement.html', {'form': form})

class InventoryView(TemplateView):
    template_name = 'inventory/inventory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('inventory')   
    
class PurchaseView(TemplateView):
    template_name = 'inventory/purchase.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        return context
    
class MenuView(TemplateView):
    template_name = 'inventory/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        return context
    
class FinancialsView(TemplateView):
    template_name = 'inventory/financials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_revenue = Purchase.objects.aggregate(total=Sum('menu_item__price'))['total']
        total_cost = sum(req.ingredient.unit_price * req.quantity for purchase in Purchase.objects.all() for req in RecipeRequirement.objects.filter(menu_item=purchase.menu_item))
        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = total_revenue - total_cost
        return context
