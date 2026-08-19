import os
import shutil

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Brand, Attachment


@receiver(post_delete, sender=Attachment)
def delete_attachment_file(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)

		dir_path = os.path.dirname(instance.image.path)

		if os.path.isdir(dir_path) and not os.listdir(dir_path):
			os.rmdir(dir_path)


@receiver(post_delete, sender=Brand)
def delete_brand_folder(sender, instance, **kwargs):
	brand_slug = instance.slug

	for brand_type in ['brands', 'skateboards', 'decks', 'trucks']:
		folder_path = os.path.join(
			settings.MEDIA_ROOT,
			brand_type,
			brand_slug,
		)

		if os.path.isdir(folder_path):
			shutil.rmtree(folder_path)