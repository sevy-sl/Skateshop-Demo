import nested_admin
from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, CompleteSkateboard, Deck, Truck, Attachment

class AttachmentInline(nested_admin.NestedTabularInline):
	model = Attachment
	extra = 1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	fields = ('name', 'image')

@admin.register(CompleteSkateboard)
class CompleteSkateboardAdmin(nested_admin.NestedModelAdmin):
	list_display = ('name', 'parent_brand', 'price')
	inlines = [AttachmentInline]

@admin.register(Deck)
class DeckAdmin(nested_admin.NestedModelAdmin):
	list_display = ('name', 'parent_brand', 'price')
	inlines = [AttachmentInline]

@admin.register(Truck)
class TruckAdmin(nested_admin.NestedModelAdmin):
	list_display = ('name', 'parent_brand', 'price')
	inlines = [AttachmentInline]