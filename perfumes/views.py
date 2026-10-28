from django.shortcuts import render, get_object_or_404
from .models import Perfume, Category
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.db.models import Q

def prod_list(request):
    perfumes = Perfume.objects.all()
    categories = Category.objects.all()

    search_query = request.GET.get('q', '').strip()

    if search_query:
        perfumes = perfumes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(perfumes, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'perfumes/category.html', {
        'perfumes': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
    })


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    perfumes = Perfume.objects.filter(category=category)
    categories = Category.objects.all()

    search_query = request.GET.get('q', '').strip()

    if search_query:
        perfumes = perfumes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(perfumes, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'perfumes/category.html', {
        'perfumes': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'category': category,
        'search_query': search_query,
    })


class PerfumeDetailView(DetailView):
    model = Perfume
    template_name = 'perfumes/product.html'
    context_object_name = 'perfume'