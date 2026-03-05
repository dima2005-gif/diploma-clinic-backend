from rest_framework import serializers
from ....models import Patient
from datetime import date

class PatientDashboardSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'age', 'phone_number', 'email', 'address', 'sex', 'weight', 'height', 'bmi', 'blood_group']
    
    def get_age(self, obj):
        if obj.date_of_birth:
            today = date.today()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None
     
    def get_bmi(self, obj):
        if obj.weight and obj.height:
            height_in_meters = obj.height / 100
            bmi = obj.weight / (height_in_meters ** 2)
            return round (bmi, 2)
        return None
