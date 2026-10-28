from django.shortcuts import render, get_object_or_404
from .models import Perfume, Category, Brand
from django.views.generic import DetailView
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator
from django.db.models import Q

def render_catalogue(request, perfumes, category=None):
    query = request.GET.get('q', '').strip()
    brands = [int(b) for b in request.GET.getlist('brand') if b.isdigit()]
    categories_selected = [int(c) for c in request.GET.getlist('category') if c.isdigit()]

    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '500')

    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if brands:
        perfumes = perfumes.filter(brand_id__in=brands)

    if categories_selected:
        perfumes = perfumes.filter(
            category__id__in=categories_selected
        )

    
    try:
        minimum = Decimal(min_price or '0')
        maximum = Decimal(max_price or '500')

        if (
            not minimum.is_finite()
            or not maximum.is_finite()
            or minimum < 0
            or maximum < 0
            or minimum > maximum
        ):
            raise InvalidOperation

        perfumes = perfumes.filter(
            price__gte=minimum,
            price__lte=maximum
        )

    except (InvalidOperation, ValueError):
        min_price = '0'
        max_price = '500'
        perfumes = perfumes.filter(
            price__gte=Decimal('0'),
            price__lte=Decimal('500')
        )

    paginator = Paginator(perfumes.distinct(), 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'perfumes/category.html', {
        'perfumes': page_obj,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'category': category,
        'search_query': query,
        'selected_brands': brands,
        'selected_categories': categories_selected,
        'min_price': min_price,
        'max_price': max_price,
    })



def prod_list(request):
    return render_catalogue(request, Perfume.objects.all())


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    return render_catalogue(
        request,
        Perfume.objects.filter(category=category),
        category
    )



class PerfumeDetailView(DetailView):
    model = Perfume
    template_name = 'perfumes/product.html'
    context_object_name = 'perfume'