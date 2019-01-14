from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel


class Items(TimeStampedModel):

    name = models.CharField(max_length = 25, verbose_name = 'Name')
    image = models.CharField(max_length = 100, verbose_name = 'Image URL')
    category = models.CharField(max_length = 15, verbose_name = 'Category')
    comment = models.CharField(max_length = 250, verbose_name = 'Comment')
    imageFile = CloudinaryField('imageFile')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name']
        # ordering = ['-name']
