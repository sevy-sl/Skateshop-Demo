import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.template import loader
from .models import SkateboardBrand, DeckBrand, TruckBrand, CompleteSkateboard, Deck, Truck, FavoriteSkateboard, FavoriteDeck, FavoriteTruck
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


brands = {
	'skateboards': SkateboardBrand,
	'decks': DeckBrand,
	'trucks': TruckBrand,
}

items = {
	'skateboards': CompleteSkateboard,
	'decks': Deck,
	'trucks': Truck,
}

favorite_models = {
	'skateboards': FavoriteSkateboard,
	'decks': FavoriteDeck,
	'trucks': FavoriteTruck,
}

@login_required(login_url='/profile/login/')
def favorite_toggle(request):
    if request.method != 'POST':
        return redirect('/')
    
    brand_type = request.POST.get('brand_type')
    brand_slug = request.POST.get('brand_slug')
    item_slug = request.POST.get('item_slug')

    item_model = items[brand_type]
    
    item = get_object_or_404(
		item_model,
		slug=item_slug,
		parent_brand__slug=brand_slug
	)

    FavoriteModel = favorite_models[brand_type]

    favorite, created = FavoriteModel.objects.get_or_create(
		user=request.user,
		original_item=item
	)

    if not created:
        favorite.delete()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    skateboards = list(SkateboardBrand.objects.all())
    decks = list(DeckBrand.objects.all())
    trucks = list(TruckBrand.objects.all())
    context = {
        'random_skate': random.sample(skateboards, min(len(skateboards), 5)),
        'random_deck': random.sample(decks, min(len(decks), 5)),
        'random_truck': random.sample(trucks, min(len(trucks), 5)),
    }
    return render(request, 'store/index.html', context)

def brands_view(request, brand_type):
    brand_model = brands.get(brand_type)

    if not brand_model:
        raise Http404()
      
    context = {
        'brand_type': brand_type,
        'brands': brand_model.objects.all()
    }
    return render(request, 'store/brands.html', context)

def items_view(request, brand_type, brand_slug):
    brand = get_object_or_404(brands[brand_type], slug=brand_slug) 
    brand_items = items[brand_type].objects.filter(parent_brand=brand)
    paginator = Paginator(brand_items, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'brand_slug': brand.slug,
	    'brand_name': brand.name,
        'brand_type': brand_type,
        'items': page_obj,
    }
    return render(request, 'store/items.html', context)

def detail_view(request, brand_type, brand_slug, item_slug):
    brand = get_object_or_404(brands[brand_type], slug=brand_slug) 
    item = get_object_or_404(items[brand_type], parent_brand__slug=brand_slug, slug=item_slug)
    fields = [
        f.name
        for f in item._meta.fields
        if f.name not in ['slug','id', 'pdate', 'parent_brand', 'name', 'favorites', 'price']
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
    }
    return render(request, 'store/detail.html', context)

def search_view(request):
    query = request.GET.get('q', '')
    skateboards = CompleteSkateboard.objects.filter(name__icontains=query)
    decks = Deck.objects.filter(name__icontains=query)
    trucks = Truck.objects.filter(name__icontains=query)
    objects = list(skateboards) + list(decks) + list(trucks)
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'query': query,
        'items': page_obj,
    }
    return render(request, 'store/search.html', context)