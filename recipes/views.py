from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.template.defaultfilters import stringfilter

from .models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic import TemplateView
import csv, io
import random

from django import template

register = template.Library()
@register.filter
def shuffle(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux


# Class View
class RecipeView(ListView):
    model = Recipe
    paginate_by = 8
    context_object_name = 'all_recipes'
    template_name = 'main.html'

    def get_queryset(self):
       return Recipe.objects.order_by('?')








# Create your views here.
def main_view(request):
    all_recipes = Recipe.objects.all()
    context = {'all_recipes': all_recipes}
    return render(request, 'main.html', context)

@permission_required('admin.can_add_entry')
def recipe_upload(request):
    template = 'uploads.html'
    data = Recipe.objects.all()

    prompt = {
        'order': 'Order of CSV should be Name, Image, Source, Ingredients',
        'profiles': data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string) # Skip csv header

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        _, created = Recipe.objects.update_or_create(
            Name=column[0],
            Image=column[1],
            Source=column[2],
            Ingredients=column[3],
        )
    all_recipes = Recipe.objects.order_by('?').first()

    context = {'all_recipes': all_recipes}

    return render(request, template, context)



def temp_view(request):
    context={}
    return render(request, 'temp.html', context)

