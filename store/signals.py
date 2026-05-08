import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import SkateboardBrand, DeckBrand, TruckBrand, AttachmentSkateboard, AttachmentDeck, AttachmentTruck


@receiver(post_delete, sender=AttachmentSkateboard)
@receiver(post_delete, sender=AttachmentDeck)
@receiver(post_delete, sender=AttachmentTruck)
def delete_attachment_file(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)
		dir_path = os.path.dirname(instance.image.path)
		if os.path.isdir(dir_path) and not os.listdir(dir_path):
			os.rmdir(dir_path)


@receiver(post_delete, sender=SkateboardBrand)
def delete_skateboard_brand_folder(sender, instance, **kwargs):
	delete_folder('skateboards', instance.name)


@receiver(post_delete, sender=DeckBrand)
def delete_deck_brand_folder(sender, instance, **kwargs):
	delete_folder('decks', instance.name)


@receiver(post_delete, sender=TruckBrand)
def delete_truck_brand_folder(sender, instance, **kwargs):
	delete_folder('trucks', instance.name)


def delete_folder(base, brand_name):
	brand_name = brand_name.replace(" ", "_").lower()
	folder_path = os.path.join(settings.MEDIA_ROOT, base, brand_name)

	if os.path.isdir(folder_path):
		shutil.rmtree(folder_path)