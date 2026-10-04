from django.shortcuts import render, get_object_or_404
from .models import Perfume, Category
from django.views.generic import DetailView

def prod_list(request):
    perfumes = Perfume.objects.all()
    categories = Category.objects.all()

    return render(request, 'perfumes/category.html', {
        'perfumes': perfumes,
        'categories': categories
    })


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    perfumes = Perfume.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'perfumes/category.html', {
        'perfumes': perfumes,
        'categories': categories,
        'category': category
    })

class PerfumeDetailView(DetailView):
    model = Perfume
    template_name = 'perfumes/product.html'
    context_object_name = 'perfume'