import nested_admin
from django.contrib import admin
from .models import SkateboardBrand, CompleteSkateboard, DeckBrand, Deck, TruckBrand, Truck, AttachmentSkateboard, AttachmentDeck, AttachmentTruck

class AttachmentSkateboardInline(nested_admin.NestedTabularInline):
	model = AttachmentSkateboard
	extra = 1

class AttachmentDeckInline(nested_admin.NestedTabularInline):
	model = AttachmentDeck
	extra = 1

class AttachmentTruckInline(nested_admin.NestedTabularInline):
	model = AttachmentTruck
	extra = 1

class SkateboardInline(nested_admin.NestedTabularInline): 
	model = CompleteSkateboard
	fields = ('parent_brand', 'name', 'pdate', 'width', 'length', 'material', 'wheelbase', 'price')
	extra = 1
	inlines = [AttachmentSkateboardInline]  

@admin.register(SkateboardBrand)
class SkateboardBrandAdmin(nested_admin.NestedModelAdmin):
	list_display = ('name', 'logo_display')
	inlines = [SkateboardInline]
	fields = ('name', 'image')  

	def logo_display(self, obj):
		if obj.image:
			return f'<img src="{obj.image.url}" alt="{obj.name}">'
		return "No Image"
	logo_display.allow_tags = True
	logo_display.short_description = "Logo"

class DeckInline(admin.TabularInline): 
	model = Deck
	fields = ('parent_brand', 'name', 'pdate', 'width', 'length', 'material', 'wheelbase', 'price')
	extra = 1
	inlines = [AttachmentDeckInline]  
	
@admin.register(DeckBrand)
class DeckBrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'logo_display')
	inlines = [DeckInline]
	fields = ('name', 'image')  

	def logo_display(self, obj):
		if obj.image:
			return f'<img src="{obj.image.url}" alt="{obj.name}">'
		return "No Image"
	logo_display.allow_tags = True
	logo_display.short_description = "Logo"

class TruckInline(admin.TabularInline): 
	model = Truck
	fields = ('parent_brand', 'name', 'pdate', 'width', 'axle_width', 'height', 'material', 'weight', 'color', 'price')
	extra = 1
	inlines = [AttachmentTruckInline]  
	
@admin.register(TruckBrand)
class TruckBrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'logo_display')
	inlines = [TruckInline]
	fields = ('name', 'image')  

	def logo_display(self, obj):
		if obj.image:
			return f'<img src="{obj.image.url}" alt="{obj.name}">'
		return "No Image"
	logo_display.allow_tags = True
	logo_display.short_description = "Logo"

