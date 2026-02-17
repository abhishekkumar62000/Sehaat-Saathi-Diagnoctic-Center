from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DiabetesRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.IntegerField()
    prediction = models.CharField(max_length=50) # "Diabetic" or "Not Diabetic"

    def __str__(self):
        return f"{self.user.username} - Diabetes - {self.date}"

class HeartRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    chest_pain_type = models.CharField(max_length=50)
    resting_bp = models.FloatField()
    cholesterol = models.FloatField()
    fasting_bs = models.CharField(max_length=10)
    resting_ecg = models.CharField(max_length=50)
    max_hr = models.FloatField()
    exercise_angina = models.CharField(max_length=10)
    old_peak = models.FloatField()
    st_slope = models.CharField(max_length=50)
    prediction = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Heart - {self.date}"

class LiverRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    total_bilirubin = models.FloatField()
    direct_bilirubin = models.FloatField()
    alkaline_phosphatase = models.FloatField()
    alamine_aminotransferase = models.FloatField()
    aspartate_aminotransferase = models.FloatField()
    total_proteins = models.FloatField()
    albumin = models.FloatField()
    albumin_and_globulin_ratio = models.FloatField()
    prediction = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Liver - {self.date}"

class CancerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # Storing 30+ features as a JSON string to avoid excessive columns
    features = models.TextField() 
    prediction = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Cancer - {self.date}"

class ImagePredictionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    disease_type = models.CharField(max_length=50) # Malaria, Covid, Alzheimer, BrainTumor, Glaucoma
    image_path = models.CharField(max_length=500)
    prediction = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.disease_type} - {self.date}"
