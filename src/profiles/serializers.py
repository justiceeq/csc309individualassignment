from django.forms import widgets
from rest_framework import serializers
from profiles.models import *


class StartUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartUpIdea
        fields = ('name', 'pub_date', 'description', 'likes', 'category')