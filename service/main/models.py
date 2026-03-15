from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import (
    phone_regex,
    gender_choices,
    marital_status,
    education,
    days_of_week,
    status,
    blood_group,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from django_cryptography.fields import encrypt
from simple_history.models import HistoricalRecords


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = encrypt(models.CharField(max_length=30))
    last_name = encrypt(models.CharField(max_length=30))
    middle_name = encrypt(models.CharField(max_length=30))
    date_of_birth = models.DateField()
    phone_number = encrypt(models.CharField(validators=[phone_regex], max_length=16))
    email = encrypt(models.EmailField())
    address = encrypt(models.CharField(max_length=255))
    sex = models.CharField(choices=gender_choices, max_length=10)
    weight = encrypt(models.FloatField())
    height = encrypt(models.FloatField())
    blood_group = encrypt(models.CharField(choices=blood_group, max_length=100))

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = encrypt(models.CharField(max_length=30))
    last_name = encrypt(models.CharField(max_length=30))
    middle_name = encrypt(models.CharField(max_length=30))
    position = models.ForeignKey("Position", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = encrypt(models.CharField(validators=[phone_regex], max_length=16))
    address = encrypt(models.CharField(max_length=255))
    email = encrypt(models.EmailField())
    sex = models.CharField(choices=gender_choices, max_length=10)
    marital_status = encrypt(models.CharField(choices=marital_status, max_length=20))
    education = models.CharField(choices=education, max_length=50)
    date_of_hire = models.DateField()
    date_of_dismissal = models.DateField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position.name}"


class Diagnosis_Guide(models.Model):
    name = encrypt(models.CharField(max_length=255))

    def __str__(self):
        return self.name


class Analysis_Guide(models.Model):
    name = encrypt(models.CharField(max_length=255))
    description = encrypt(models.TextField())
    price = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=10, decimal_places=2
    )

    def __str__(self):
        return self.name


class Medicine_Guide(models.Model):
    name = encrypt(models.CharField(max_length=255))

    def __str__(self):
        return self.name


class Service_Guide(models.Model):
    name = encrypt(models.CharField(max_length=255))
    description = encrypt(models.TextField())
    price = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=10, decimal_places=2
    )

    def __str__(self):
        return self.name


class Code(models.Model):
    name = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Work_Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day_of_week = models.CharField(choices=days_of_week, max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = [["employee", "day_of_week"]]


class Prescribed_Service(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service_Guide, on_delete=models.CASCADE)
    date_prescribed = models.DateTimeField()
    status = models.CharField(choices=status, max_length=20)

    history = HistoricalRecords()


class Medical_History(models.Model):
    prescribed_service = models.OneToOneField(
        Prescribed_Service, on_delete=models.CASCADE, null=True, blank=True
    )
    date_departure = models.DateField(blank=True, null=True)
    diagnosis = models.ForeignKey(Diagnosis_Guide, on_delete=models.CASCADE)
    conclusion = encrypt(models.TextField())

    history = HistoricalRecords()


class Prescribed_Analysis(models.Model):
    medical_history = models.ForeignKey(
        Medical_History, on_delete=models.CASCADE, null=True, blank=True
    )
    analysis = models.ForeignKey(Analysis_Guide, on_delete=models.CASCADE)
    laboratory_assistant = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="lab_assistant_prescribed_analyses",
    )
    date_prescribed = models.DateTimeField()
    result = models.FileField(upload_to="analysis_results/", blank=True, null=True)
    status = models.CharField(choices=status, max_length=20)

    history = HistoricalRecords()


class Prescribed_Medicine(models.Model):
    medical_history = models.ForeignKey(
        Medical_History, on_delete=models.CASCADE, null=True, blank=True
    )
    medicine = models.ForeignKey(Medicine_Guide, on_delete=models.CASCADE)
    recipe = encrypt(models.TextField())

    history = HistoricalRecords()


class Position_Service(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    service = models.ForeignKey(Service_Guide, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["position", "service"]]


class Response(models.Model):
    prescribed_service = models.ForeignKey(Prescribed_Service, on_delete=models.CASCADE)
    comment = encrypt(models.CharField(max_length=200))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    date_created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
