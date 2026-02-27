from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import phone_regex, gender_choices, marital_status, education, days_of_week, status
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    sex = models.CharField(choices=gender_choices, max_length=10)
    weight = models.FloatField()
    height = models.FloatField()

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    sex = models.CharField(choices=gender_choices, max_length=10)
    marital_status = models.CharField(choices=marital_status, max_length=20)
    education = models.CharField(choices=education, max_length=50)
    date_of_hire = models.DateField()
    date_of_dismissal = models.DateField(blank=True, null=True)

class Diagnosis_Guide(models.Model):
    name = models.CharField(max_length=255)

class Analysis_Guide(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)

class Medicine_Guide(models.Model):
    name = models.CharField(max_length=255)

class Service_Guide(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)

class Position(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=50, unique=True)


class Work_Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day_of_week = models.CharField(choices=days_of_week, max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Medical_History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_arrival = models.DateField()
    date_departure = models.DateField(blank=True, null=True)
    diagnosis = models.ForeignKey(Diagnosis_Guide, on_delete=models.CASCADE)
    conclusion = models.TextField()

class Prescribed_Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    analysis = models.ForeignKey(Analysis_Guide, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='doctor_prescribed_analyses')
    laboratory_assistant = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='lab_assistant_prescribed_analyses')
    date_prescribed = models.DateField()
    result = models.FileField(upload_to='analysis_results/', blank=True, null=True)
    status = models.CharField(choices=status, max_length=20)

class Prescribed_Medicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine_Guide, on_delete=models.CASCADE)
    date_prescribed = models.DateField()
    recipe = models.TextField()

class Prescribed_Service(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service_Guide, on_delete=models.CASCADE)
    date_prescribed = models.DateField()
    status = models.CharField(choices=status, max_length=20)

class Position_Service(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    service = models.ForeignKey(Service_Guide, on_delete=models.CASCADE)

class Response(models.Model):
    prescribed_service = models.ForeignKey(Prescribed_Service, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_created = models.DateTimeField(auto_now_add=True)



