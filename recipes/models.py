from django.db import models

# Create your models here.

class Recipe(models.Model):
    Name = models.CharField(max_length=400)
    Image = models.TextField(max_length=400)
    Source = models.TextField(max_length=400)
    Ingredients = models.TextField(max_length=400)

    def __str__(self):
        return self.Name

