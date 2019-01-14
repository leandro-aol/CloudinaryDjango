from cloudinary.templatetags import cloudinary
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone
from rest_framework import serializers
from .models import Items
from dateutil.parser import parse

class ItemsSerializer(serializers.ModelSerializer):

    image = serializers.CharField(required=False)

    class Meta:
        model = Items
        fields = ('id', 'name', 'image', 'category', 'comment', 'created')
        # fields = '__all__'

    def to_representation(self, instance):
        representation = super(ItemsSerializer, self).to_representation(instance)
        
        # imagemURL = cloudinary.utils.cloudinary_url(instance.image, width = 100, height = 150, crop = 'fill', quality = '30')
        # imagemURL = cloudinary.utils.cloudinary_url('DjangoAPI/' + instance.image)
        # representation['image'] = imagemURL[0]
        
        date = parse(representation['created'], ignoretz = True)
        representation['created'] = naturalday(date)
        
        return representation

    def get_validation_exclusions(self):
        exclusions = super(ItemsSerializer, self).get_validation_exclusions()
        return exclusions + ['image']
