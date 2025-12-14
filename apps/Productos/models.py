from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(blank=False, null=False)
    
    def __str__(self):
        return f"{self.nombre}"