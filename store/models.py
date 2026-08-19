import os
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from functools import partial
from django.utils.text import slugify


def attachment_upload_path(instance, filename):
    item = instance.item

    return os.path.join(
        item.brand_type,
        item.parent_brand.slug,
        item.slug,
        filename,
    )

def upload_to_brand():
	return partial(_upload_to_brand)

def _upload_to_brand(instance, filename):
	return os.path.join('brands', instance.slug, filename)

class Brand(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(unique=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)

		super().save(*args, **kwargs)

	image = models.ImageField(upload_to=upload_to_brand(), blank=True, null=True)

class Item(models.Model):
	parent_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='items')

	def __str__(self):
		return self.name
	
	@property
	def brand_type(self):
		return self.parent_brand.type

	@property
	def brand_name(self):
		return self.parent_brand.name

	slug = models.SlugField(blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)

		super().save(*args, **kwargs)

	pdate = models.DateTimeField('date')
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=7, decimal_places=2)


class CompleteSkateboard(Item):
	def __str__(self):
		return self.name

	@property
	def brand_type(self):
		return 'skateboards'

	@property
	def brand_name(self):
		return self.parent_brand.name

	width = models.FloatField(validators=[
		MinValueValidator(6.0),
		MaxValueValidator(11.0)],
		help_text='Width of the skateboard deck in inches (6.0 to 11.0).'
	)
	length = models.FloatField(validators=[
		MinValueValidator(26.0),
		MaxValueValidator(35.0)],
		help_text='Length of the skateboard deck in inches (26.0 to 35.0).'
)
	
	class DeckMaterials(models.TextChoices):
		MAPLE_7PLY = '7-Ply Maple'
		MAPLE_8PLY = '8-Ply Maple'
		BAMBOO_MAPLE = 'Bamboo / Maple Composite'
		CARBON_REINFORCED = 'Carbon Reinforced Maple'
		FIBERGLASS_REINFORCED = 'Fiberglass Reinforced Maple'

	material = models.CharField(choices=DeckMaterials.choices, max_length=30)
	wheelbase = models.IntegerField(validators=[
		MinValueValidator(12),
		MaxValueValidator(16)],
		help_text='Distance between the trucks (wheelbase) in inches (12 to 16).')
	
class Deck(Item):
	def __str__(self):
		return self.name
	
	@property
	def brand_type(self):
		return 'decks'

	@property
	def brand_name(self):
		return self.parent_brand.name

	width = models.FloatField(validators=[
		MinValueValidator(7.0),
		MaxValueValidator(9.0)],
		help_text='Width of the skateboard deck in inches (7.0 to 9.0).'
)
	length = models.FloatField(validators=[
		MinValueValidator(26.0),
		MaxValueValidator(35.0)],
		help_text='Length of the skateboard deck in inches (26.0 to 35.0).')
	
	class DeckMaterials(models.TextChoices):
		MAPLE_7PLY = '7-Ply Maple'
		MAPLE_8PLY = '8-Ply Maple'
		BAMBOO_MAPLE = 'Bamboo / Maple Composite'
		CARBON_REINFORCED = 'Carbon Reinforced Maple'
		FIBERGLASS_REINFORCED = 'Fiberglass Reinforced Maple'

	material = models.CharField(choices=DeckMaterials.choices, max_length=30)
	wheelbase = models.IntegerField(validators=[
			MinValueValidator(12),
			MaxValueValidator(16)],
		help_text='Distance between the trucks (wheelbase) in inches (typically 12 to 16).'
	)

class Truck(Item):
	def __str__(self):
		return self.name
	
	@property
	def brand_type(self):
		return 'trucks'

	@property
	def brand_name(self):
		return self.parent_brand.name
	
	width = models.FloatField(
		validators=[
			MinValueValidator(7.0),
			MaxValueValidator(10.0)],
		help_text='Width of the truck hanger in inches (7.0 to 10.0)'
	) 
	axle_width = models.FloatField(
		validators=[
			MinValueValidator(7.0),
			MaxValueValidator(10.0)],
		help_text='Width of the axle in inches (7.0 to 10.0)'
	)
	height = models.CharField(
		max_length=30,
		choices=[
			('Low', 'Low'),
			('Mid', 'Mid'),
			('High', 'High')],
		default='Mid',
		help_text='Truck height'
	)

	class TruckMaterials(models.TextChoices):
		ALUMINUM = 'Aluminum'
		STEEL = 'Steel'
		TITANIUM = 'Titanium'
		MAGNESIUM = 'Magnesium'

	material = models.CharField(
		choices=TruckMaterials.choices,
		default=TruckMaterials.ALUMINUM)

	weight = models.FloatField(validators=[
			MinValueValidator(200.0),
			MaxValueValidator(500.0)],
		help_text='Weight of a single truck in grams (200.0 to 500.0)'
	)
	color = models.CharField(max_length=30, blank=True, null=True)

class BaseAttachment(models.Model):
    image = models.ImageField(upload_to=attachment_upload_path)

    class Meta:
        abstract = True

class Attachment(BaseAttachment):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='attachments',
    )

class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_items')

    original_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorited_by')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'original_item'],
                name='unique_user_favorite_item',
            )
        ]