from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
class Perfume(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size_ml = models.PositiveIntegerField()
    launch_year = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='perfume_images/')
    
    def __str__(self):
        return self.name

