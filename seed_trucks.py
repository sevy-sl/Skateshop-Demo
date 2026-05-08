import os
import sys
import django
import random
from decimal import Decimal
from django.core.files import File
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from store.models import (
	Truck,
	TruckBrand,
	AttachmentTruck,
)

ASSETS_DIR = os.path.join(BASE_DIR, 'seed_assets')

brand_images = [
	os.path.join(ASSETS_DIR, f'{i}.jpg')
	for i in range(1, 11)
]

item_images = [
	os.path.join(ASSETS_DIR, 'default_truck.png'),
	os.path.join(ASSETS_DIR, 'default_truck2.png'),
]

brands_data = {
	'Independent': ['Stage 11 Standard', 'Hollow Mid', 'Forged Hollow'],
	'Thunder': ['Team Polished', 'Lights II', 'Hollow Lights'],
	'Venture': ['V-Light Low', 'All Polished', 'High Raw'],
	'Ace': ['AF1 Classic', 'AF1 Hollow', 'AF1 Low'],
	'Tensor': ['Alloy Standard', 'Mag Light', 'Aluminum Raw'],
	'Krux': ['K5 Standard', 'DLK Hollow', 'K5 Polished'],
	'Royal': ['Standard Raw', 'Ultra Light', 'Low Series'],
	'Destructo': ['D1 Mid', 'D2 Lite', 'Raw Series'],
	'Mini Logo': ['Standard Raw', 'Blackout', 'Polished Series'],
	'Film Trucks': ['Logo Raw', 'Team Edition', 'Classic Polished'],
}

heights = ['Low', 'Mid', 'High']
materials = ['Aluminum', 'Steel', 'Titanium', 'Magnesium']
colors = ['Black', 'Silver', 'White', 'Raw', 'Gold']

variants = [
	(7.75, 8.0),
	(8.0, 8.25),
	(8.25, 8.5),
]

for i, (brand_name, models) in enumerate(brands_data.items()):

	brand, created = TruckBrand.objects.get_or_create(name=brand_name)

	if created and i < len(brand_images):
		with open(brand_images[i], 'rb') as f:
			brand.image.save(os.path.basename(brand_images[i]), File(f), save=True)

	print(f'Creating trucks for {brand.name}...')

	for model in models:

		w, axle = random.choice(variants)

		truck, created = Truck.objects.get_or_create(
			parent_brand=brand,
			name=f'{model} Trucks',
			defaults={
				'width': w,
				'axle_width': axle,
				'height': random.choice(heights),
				'material': random.choice(materials),
				'weight': random.uniform(280.0, 420.0),
				'price': Decimal(random.randint(40, 120)),
				'color': random.choice(colors),
				'pdate': timezone.now(),
			}
		)

		if created:
			for img in item_images:
				with open(img, 'rb') as f:
					AttachmentTruck.objects.create(
						truck=truck,
						image=File(f, name=os.path.basename(img))
					)