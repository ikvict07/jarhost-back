from rest_framework import serializers
from .models import Jar


class JarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jar
        fields = ['monoid', 'name', 'description']
