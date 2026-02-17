from django import forms

class LabReportForm(forms.Form):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    
    name = forms.CharField(label="Patient Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}))
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    
    # Hematology Section
    hemoglobin = forms.FloatField(label="Hemoglobin (g/dL)", required=False, 
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 14.2'}),
                                  help_text="Standard: Male (13.5-17.5), Female (12.0-15.5)")
    
    wbc = forms.FloatField(label="White Blood Cells (cells/mcL)", required=False, 
                           widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 6000'}),
                           help_text="Standard: 4,500 - 11,000")
    
    platelets = forms.FloatField(label="Platelets (cells/mcL)", required=False, 
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 250000'}),
                                 help_text="Standard: 150,000 - 450,000")
    
    # Metabolic Section
    glucose_fasting = forms.FloatField(label="Fasting Glucose (mg/dL)", required=False, 
                                       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 90'}),
                                       help_text="Standard: 70 - 100")
    
    cholesterol = forms.FloatField(label="Total Cholesterol (mg/dL)", required=False, 
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 180'}),
                                   help_text="Standard: < 200")
    
    creatinine = forms.FloatField(label="Creatinine (mg/dL)", required=False, 
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0.9'}),
                                   help_text="Standard: 0.7 - 1.3")

class RoadmapForm(forms.Form):
    GOAL_CHOICES = [
        ('General Health', 'Maintain General Health'),
        ('Weight Loss', 'Weight Loss'),
        ('Muscle Gain', 'Muscle Gain'),
        ('Diabetes Management', 'Diabetes Management'),
        ('Heart Health', 'Heart Health'),
    ]
    DIET_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Vegan', 'Vegan'),
    ]
    
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(label="Weight (kg)", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.FloatField(label="Height (cm)", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    goal = forms.ChoiceField(label="Health Goal", choices=GOAL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    diet_preference = forms.ChoiceField(label="Dietary Preference", choices=DIET_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

class MoodTrackerForm(forms.Form):
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Anxious', 'Anxious'),
        ('Neutral', 'Neutral'),
        ('Stressed', 'Stressed'),
    ]
    name = forms.CharField(label="Your Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    current_mood = forms.ChoiceField(choices=MOOD_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    journal_entry = forms.CharField(label="How are you feeling today?", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your thoughts here...'}))

class MedicalPassportForm(forms.Form):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ]
    
    full_name = forms.CharField(label="Full Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    blood_type = forms.ChoiceField(choices=BLOOD_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))
    allergies = forms.CharField(label="Allergies (if any)", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Peanuts, Penicillin...'}))
    existing_conditions = forms.CharField(label="Existing Conditions", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Asthma, Diabetes...'}))
    emergency_contact_name = forms.CharField(label="Emergency Contact Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_contact_phone = forms.CharField(label="Emergency Contact Phone", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PharmaCheckerForm(forms.Form):
    medication_1 = forms.CharField(label="Medication A", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Aspirin'}))
    medication_2 = forms.CharField(label="Medication B", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Warfarin'}))

