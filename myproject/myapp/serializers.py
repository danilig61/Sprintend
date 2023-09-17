from rest_framework import serializers
from .models import Pass, Photo
from .models import SubmitData

class SubmitDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitData
        fields = '__all__'

class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = ['coordinates', 'height', 'name', 'user_name', 'user_email', 'user_phone']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']