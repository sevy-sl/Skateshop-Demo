from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def content_type_id(obj):
    return ContentType.objects.get_for_model(obj).id

@register.filter(name='getattr', is_safe=True)
def getattr_filter(obj, attr):
	try:
		return getattr(obj, attr, '')
	except Exception:
		return ''

@register.filter
def is_float(value):
	try:
		return isinstance(float(value), float)
	except (ValueError, TypeError):
		return False