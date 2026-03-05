from rest_framework import serializers
from main.models import Service_Guide

class DirectoryOfServicesSerializers(serializers.ModelSerializer):
    price=serializers.SerializerMethodField(); 

    class Meta:
        model = Service_Guide
        fields = ['id', 'name', 'description', 'price'] 

    def get_price(self, obj):
        return int(obj.price) 
