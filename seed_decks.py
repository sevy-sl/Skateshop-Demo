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
	Deck,
	DeckBrand,
	AttachmentDeck,
)

ASSETS_DIR = os.path.join(BASE_DIR, 'seed_assets')

brand_images = [
	os.path.join(ASSETS_DIR, f'{i}.jpg')
	for i in range(1, 11)
]

image_paths = [
	os.path.join(ASSETS_DIR, 'default_deck.png'),
	os.path.join(ASSETS_DIR, 'default_deck2.png'),
]

brands_data = {
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

materials = [m[0] for m in Deck.DeckMaterials.choices]

variants = [
	(7.75, 31.25, 13),
	(8.0, 31.75, 14),
	(8.25, 32.0, 15),
	(8.5, 32.25, 15),
]

for i, (brand_name, models) in enumerate(brands_data.items()):

	brand, created = DeckBrand.objects.get_or_create(name=brand_name)

	if created and i < len(brand_images):
		with open(brand_images[i], 'rb') as f:
			brand.image.save(os.path.basename(brand_images[i]), File(f), save=True)

	print(f'Creating decks for {brand.name}...')

	for model_name in models:

		width, length, wheelbase = random.choice(variants)

		deck, created = Deck.objects.get_or_create(
			parent_brand=brand,
			name=f'{model_name} Deck',
			defaults={
				'width': width,
				'length': length,
				'wheelbase': wheelbase,
				'material': random.choice(materials),
				'price': Decimal(random.randint(50, 120)),
				'pdate': timezone.now(),
			}
		)

		if created:
			for img_path in image_paths:
				with open(img_path, 'rb') as f:
					AttachmentDeck.objects.create(
						deck=deck,
						image=File(f, name=os.path.basename(img_path))
					)