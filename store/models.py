import os
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from functools import partial

def attachment_upload_path(instance, filename):

	if hasattr(instance, 'skateboard') and instance.skateboard:
		obj = instance.skateboard
		folder = 'skateboards'

	elif hasattr(instance, 'deck') and instance.deck:
		obj = instance.deck
		folder = 'decks'

	elif hasattr(instance, 'truck') and instance.truck:
		obj = instance.truck
		folder = 'trucks'

	else:
		return os.path.join('others', filename)

	brand = obj.parent_brand.name.replace(' ', '_').lower()
	name = obj.name.replace(' ', '_').lower()

	return os.path.join(f'{folder}/{brand}/{name}', filename)

def upload_to_brand(folder):
	return partial(_upload_to_brand, folder=folder)

def _upload_to_brand(instance, filename, folder):
	brand_name = instance.name.replace(" ", "_").lower()
	return os.path.join(f'{folder}/{brand_name}/', filename)

class BaseAttachment(models.Model):
	image = models.ImageField(upload_to=attachment_upload_path)

	class Meta:
		abstract = True 

class AttachmentSkateboard(BaseAttachment):
	skateboard = models.ForeignKey("CompleteSkateboard", on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)

class AttachmentDeck(BaseAttachment):
	deck = models.ForeignKey("Deck", on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)

class AttachmentTruck(BaseAttachment):
	truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)

class SkateboardBrand(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length=30, primary_key=True)
	image = models.ImageField(upload_to=upload_to_brand(folder='skateboards'), blank=True, null=True)

class CompleteSkateboard(models.Model):
	def __str__(self):
		return self.name

	@property
	def brand_type(self):
		return 'skateboards'

	@property
	def brand_name(self):
		return self.parent_brand.name

	parent_brand = models.ForeignKey(SkateboardBrand, on_delete=models.CASCADE)
	pdate = models.DateTimeField('date')
	name = models.CharField(max_length=50)
	width = models.FloatField(validators=[
		MinValueValidator(6.0),
		MaxValueValidator(11.0)],
		help_text="Width of the skateboard deck in inches (6.0 to 11.0)."
	)
	length = models.FloatField(validators=[
		MinValueValidator(26.0),
		MaxValueValidator(35.0)],
		help_text="Length of the skateboard deck in inches (26.0 to 35.0)."
)
	
	class DeckMaterials(models.TextChoices):
		MAPLE_WOOD = 'Maple Wood'
		BAMBOO = 'Bamboo'
		CARBON_FIBER = 'Carbon Fiber'
		FIBERGLASS = 'Fiberglass'

	material = models.CharField(choices=DeckMaterials.choices, max_length=30)
	wheelbase = models.IntegerField(validators=[
		MinValueValidator(12),
		MaxValueValidator(16)],
		help_text='Distance between the trucks (wheelbase) in inches (12 to 16).')

	price = models.DecimalField(max_digits=7, decimal_places=2)
	favorites = models.ManyToManyField(User, through='FavoriteSkateboard', related_name='favorite_skateboards', blank=True)

class FavoriteSkateboard(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	original_item = models.ForeignKey(CompleteSkateboard, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'original_item')

class DeckBrand(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length=30, primary_key=True)
	image = models.ImageField(upload_to=upload_to_brand(folder='decks'), blank=True, null=True)

class Deck(models.Model):
	def __str__(self):
		return self.name
	
	@property
	def brand_type(self):
		return 'decks'

	@property
	def brand_name(self):
		return self.parent_brand.name

	parent_brand = models.ForeignKey(DeckBrand, on_delete=models.CASCADE)
	pdate = models.DateTimeField('date')
	name = models.CharField(max_length=30)
	width = models.FloatField(validators=[
		MinValueValidator(7.0),
		MaxValueValidator(9.0)],
		help_text="Width of the skateboard deck in inches (7.0 to 9.0)."
)
	length = models.FloatField(validators=[
		MinValueValidator(26.0),
		MaxValueValidator(35.0)],
		help_text='Length of the skateboard deck in inches (26.0 to 35.0).')
	
	class DeckMaterials(models.TextChoices):
		MAPLE_WOOD = 'Maple Wood'
		BAMBOO = 'Bamboo'
		CARBON_FIBER = 'Carbon Fiber'
		FIBERGLASS = 'Fiberglass'

	material = models.CharField(choices=DeckMaterials.choices, max_length=30)
	wheelbase = models.IntegerField(validators=[
			MinValueValidator(12),
			MaxValueValidator(16)],
		help_text="Distance between the trucks (wheelbase) in inches (typically 12 to 16)."
	)

	price = models.DecimalField(max_digits=7, decimal_places=2)
	favorites = models.ManyToManyField(User, through='FavoriteDeck', related_name='favorite_decks', blank=True)

class FavoriteDeck(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	original_item = models.ForeignKey(Deck, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'original_item')

class TruckBrand(models.Model):
	def __str__(self):
		return self.name 

	name = models.CharField(max_length=30, primary_key=True)
	image = models.ImageField(upload_to=upload_to_brand(folder='trucks'), blank=True, null=True)

class Truck(models.Model):
	def __str__(self):
		return self.name
	
	@property
	def brand_type(self):
		return 'trucks'

	@property
	def brand_name(self):
		return self.parent_brand.name

	parent_brand = models.ForeignKey(TruckBrand, on_delete=models.CASCADE)
	pdate = models.DateTimeField('date')
	name = models.CharField(max_length=50)
	width = models.FloatField(
		validators=[
			MinValueValidator(7.0),
			MaxValueValidator(10.0)],
		help_text="Width of the truck hanger in inches (7.0 to 10.0)"
	) 
	axle_width = models.FloatField(
		validators=[
			MinValueValidator(7.0),
			MaxValueValidator(10.0)],
		help_text="Width of the axle in inches (7.0 to 10.0)"
	)
	height = models.CharField(
		max_length=30,
		choices=[
			("Low", "Low"),
			("Mid", "Mid"),
			("High", "High")],
		default="Mid",
		help_text="Truck height"
	)
	material = models.CharField(
		max_length=30,
		choices=[
			("Aluminum", "Aluminum"),
			("Steel", "Steel"),
			("Titanium", "Titanium"),
			("Magnesium", "Magnesium")],
		default="Aluminum"
	)
	weight = models.FloatField(validators=[
			MinValueValidator(200.0),
			MaxValueValidator(500.0)],
		help_text="Weight of a single truck in grams (200.0 to 500.0)"
	)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	color = models.CharField(max_length=30, blank=True, null=True)
	favorites = models.ManyToManyField(User, through='FavoriteTruck', related_name='favorite_trucks', blank=True)

class FavoriteTruck(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	original_item = models.ForeignKey(Truck, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'original_item')
