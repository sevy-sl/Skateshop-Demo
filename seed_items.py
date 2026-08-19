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
	Brand,
	CompleteSkateboard,
	Deck,
	Truck,
	Attachment,
)


ASSETS_DIR = os.path.join(BASE_DIR, 'seed_assets')

brand_images = [
	os.path.join(ASSETS_DIR, f'{i}.jpg')
	for i in range(1, 11)
]

skateboard_images = [
	os.path.join(ASSETS_DIR, 'default_skate.png'),
	os.path.join(ASSETS_DIR, 'default_skate2.png'),
]

deck_images = [
	os.path.join(ASSETS_DIR, 'default_deck.png'),
	os.path.join(ASSETS_DIR, 'default_deck2.png'),
]

truck_images = [
	os.path.join(ASSETS_DIR, 'default_truck.png'),
	os.path.join(ASSETS_DIR, 'default_truck2.png'),
]


skateboard_brands = {
	'Element': ['Section', 'Seal', 'Quadrant'],
	'Santa Cruz': ['Classic Dot', 'Screaming Hand', 'Flame Dot'],
	'Powell Peralta': ['Ripper', 'Skull & Sword', 'Vato Rats'],
	'Baker': ['Brand Logo', 'OG Logo', 'Brand Name Red'],
	'Zero': ['Bold', 'Single Skull', 'Blood Skull'],
	'Enjoi': ['Panda', 'Whitey Panda', 'Half & Half'],
	'Globe': ['G1 Full On', 'G2 Ramones', 'G1 Argo'],
	'Blind': ['Reaper', 'Fresh Air', 'Matte OG'],
	'Almost': ['Double Impact', 'Youness Logo', 'Radiate'],
	'Plan B': ['Team OG', 'Joslin', 'Original Logo'],
}

skateboard_materials = [
	m[0] for m in CompleteSkateboard.DeckMaterials.choices
]

skateboard_variants = [
	(7.75, 31.25, 13),
	(8.0, 31.75, 14),
	(8.25, 32.0, 15),
]


deck_brands = {
	'Element': ['Section', 'Seal', 'Quadrant'],
	'Santa Cruz': ['Classic Dot', 'Screaming Hand', 'Flame Dot'],
	'Powell Peralta': ['Ripper', 'Skull & Sword', 'Vato Rats'],
	'Baker': ['Brand Logo', 'OG Logo', 'Brand Name Red'],
	'Zero': ['Bold', 'Single Skull', 'Blood Skull'],
	'Enjoi': ['Panda', 'Whitey Panda', 'Half & Half'],
	'Globe': ['G1 Full On', 'G2 Ramones', 'G1 Argo'],
	'Blind': ['Reaper', 'Fresh Air', 'Matte OG'],
	'Almost': ['Double Impact', 'Youness Logo', 'Radiate'],
	'Plan B': ['Team OG', 'Joslin', 'Original Logo'],
}

deck_materials = [
	m[0] for m in Deck.DeckMaterials.choices
]

deck_variants = [
	(7.75, 31.25, 13),
	(8.0, 31.75, 14),
	(8.25, 32.0, 15),
	(8.5, 32.25, 15),
]


truck_brands = {
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

truck_heights = ['Low', 'Mid', 'High']

truck_materials = [
	m[0] for m in Truck.TruckMaterials.choices
]

truck_colors = [
	'Black',
	'Silver',
	'White',
	'Raw',
	'Gold',
]

truck_variants = [
	(7.75, 8.0),
	(8.0, 8.25),
	(8.25, 8.5),
]


def get_brand(brand_name, image_index):
	brand, created = Brand.objects.get_or_create(
		name=brand_name
	)

	if created and image_index < len(brand_images):
		with open(brand_images[image_index], 'rb') as f:
			brand.image.save(
				os.path.basename(brand_images[image_index]),
				File(f),
				save=True
			)

	return brand


def create_attachments(item, image_paths):
	for image_path in image_paths:
		with open(image_path, 'rb') as f:
			Attachment.objects.create(
				item=item,
				image=File(
					f,
					name=os.path.basename(image_path)
				)
			)


def seed_skateboards():
	for i, (brand_name, models) in enumerate(skateboard_brands.items()):

		brand = get_brand(brand_name, i)

		print(f'Creating skateboards for {brand.name}...')

		for model_name in models:

			width, length, wheelbase = random.choice(
				skateboard_variants
			)

			skateboard, created = CompleteSkateboard.objects.get_or_create(
				parent_brand=brand,
				name=f'{model_name} Complete',
				defaults={
					'width': width,
					'length': length,
					'wheelbase': wheelbase,
					'material': random.choice(skateboard_materials),
					'price': Decimal(random.randint(70, 160)),
					'pdate': timezone.now(),
				}
			)

			if created:
				create_attachments(
					skateboard,
					skateboard_images
				)


def seed_decks():
	for i, (brand_name, models) in enumerate(deck_brands.items()):

		brand = get_brand(brand_name, i)

		print(f'Creating decks for {brand.name}...')

		for model_name in models:

			width, length, wheelbase = random.choice(
				deck_variants
			)

			deck, created = Deck.objects.get_or_create(
				parent_brand=brand,
				name=f'{model_name} Deck',
				defaults={
					'width': width,
					'length': length,
					'wheelbase': wheelbase,
					'material': random.choice(deck_materials),
					'price': Decimal(random.randint(50, 120)),
					'pdate': timezone.now(),
				}
			)

			if created:
				create_attachments(
					deck,
					deck_images
				)


def seed_trucks():
	for i, (brand_name, models) in enumerate(truck_brands.items()):

		brand = get_brand(brand_name, i)

		print(f'Creating trucks for {brand.name}...')

		for model_name in models:

			width, axle_width = random.choice(
				truck_variants
			)

			truck, created = Truck.objects.get_or_create(
				parent_brand=brand,
				name=f'{model_name} Trucks',
				defaults={
					'width': width,
					'axle_width': axle_width,
					'height': random.choice(truck_heights),
					'material': random.choice(truck_materials),
					'weight': round(random.uniform(280.0, 420.0),2),
					'price': Decimal(random.randint(40, 120)),
					'color': random.choice(truck_colors),
					'pdate': timezone.now(),
				}
			)

			if created:
				create_attachments(
					truck,
					truck_images
				)


if __name__ == '__main__':
	seed_skateboards()
	seed_decks()
	seed_trucks()

	print('Done!')