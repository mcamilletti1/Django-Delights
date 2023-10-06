from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} requires {self.quantity_required} of {self.ingredient.name}"
    
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchased {self.menu_item.name} at {self.purchase_time}"