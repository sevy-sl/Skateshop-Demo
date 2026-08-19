import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.template import loader
from .models import Brand, CompleteSkateboard, Deck, Truck, FavoriteItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef


ITEM_TYPES = {
    'skateboards': {
        'model': CompleteSkateboard,
        'name': 'skateboard',
    },
    'decks': {
        'model': Deck,
        'name': 'deck',
    },
    'trucks': {
        'model': Truck,
        'name': 'truck',
    },
}


def get_item_type(brand_type):
    item_type = ITEM_TYPES.get(brand_type)

    if not item_type:
        raise Http404('Invalid item type.')

    return item_type

@login_required(login_url='/profile/login/')
def favorite_toggle(request):
    if request.method != 'POST':
        return redirect('/')

    brand_type = request.POST.get('brand_type')
    brand_slug = request.POST.get('brand_slug')
    item_slug = request.POST.get('item_slug')

    item_type = get_item_type(brand_type)
    item_model = item_type['model']

    item = get_object_or_404(
        item_model,
        parent_brand__slug=brand_slug,
        slug=item_slug,
    )

    favorite, created = FavoriteItem.objects.get_or_create(
        user=request.user,
        original_item=item,
    )

    if not created:
        favorite.delete()

    return redirect(
        request.META.get('HTTP_REFERER', '/')
    )

def index(request):
    skateboard_brands = Brand.objects.filter(
        items__in=CompleteSkateboard.objects.all()
    ).distinct()

    deck_brands = Brand.objects.filter(
        items__in=Deck.objects.all()
    ).distinct()

    truck_brands = Brand.objects.filter(
        items__in=Truck.objects.all()
    ).distinct()

    context = {
        'random_skate': random.sample(list(skateboard_brands), min(skateboard_brands.count(), 5)),
        'random_deck': random.sample(list(deck_brands), min(deck_brands.count(), 5)),
        'random_truck': random.sample(list(truck_brands), min(truck_brands.count(), 5)),
    }
    return render(request, 'store/index.html', context)

def brands_view(request, brand_type):
    item_type = get_item_type(brand_type)
    item_model = item_type['model']

    brands = Brand.objects.filter(
        items__in=item_model.objects.all()
    ).distinct()

    context = {
        'brand_type': brand_type,
        'brands': brands,
    }
    return render(request, 'store/brands.html', context)

def items_view(request, brand_type, brand_slug):
    item_type = get_item_type(brand_type)
    item_model = item_type['model']

    brand = get_object_or_404(Brand, slug=brand_slug)

    brand_items = item_model.objects.filter(
        parent_brand=brand,
    ).order_by('-pdate')

    paginator = Paginator(brand_items, 15)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    context = {
        'brand_slug': brand.slug,
        'brand_name': brand.name,
        'brand_type': brand_type,
        'item_type': item_type['name'],
        'items': page_obj,
    }
    return render(request, 'store/items.html', context)

def detail_view(request, brand_type, brand_slug, item_slug):
    item_type = get_item_type(brand_type)
    item_model = item_type['model']

    brand = get_object_or_404(Brand, slug=brand_slug)

    item = get_object_or_404(item_model, parent_brand=brand, slug=item_slug)
    favorite_item = FavoriteItem.objects.filter(user=request.user, original_item=item)

    fields = [
        f.name
        for f in item._meta.fields
        if f.name not in ['slug','id', 'pdate', 'parent_brand', 'name', 'favorites', 'price', 'item_ptr']
    ]

    context = {
        'item': item,
        'brand_slug': brand.slug,
        'brand_name': brand.name,
        'item_slug': item.slug,
        'item_name': item.name,
        'brand_type': brand_type,
        'item_type': brand_type[:-1],
        'features': fields,
        'favorite_item': favorite_item
    }
    return render(request, 'store/detail.html', context)

def search_view(request):
    query = request.GET.get('q', '').strip()

    skateboard_items = CompleteSkateboard.objects.filter(name__icontains=query)
    deck_items = Deck.objects.filter(name__icontains=query)
    truck_items = Truck.objects.filter(name__icontains=query)

    objects = list(skateboard_items)
    objects += list(deck_items)
    objects += list(truck_items)

    paginator = Paginator(objects, 10)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    context = {
        'query': query,
        'items': page_obj,
    }

    return render(request, 'store/search.html',context)