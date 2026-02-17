import os
import django
import random
import json
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkup.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import DiabetesRecord, HeartRecord, LiverRecord, CancerRecord, ImagePredictionRecord

def create_dummy_data():
    print("Creating dummy data...")

    # 1. Create or Get Test User
    username = "testuser"
    password = "password123"
    email = "test@example.com"
    
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
        print(f"Created user: {username} (Password: {password})")
    else:
        user.set_password(password)
        user.save()
        print(f"Using existing user: {username}")

    # 2. Create Diabetes Records
    print("Generating Diabetes Records...")
    for _ in range(5):
        DiabetesRecord.objects.create(
            user=user,
            pregnancies=random.randint(0, 10),
            glucose=random.uniform(70, 200),
            blood_pressure=random.uniform(60, 100),
            skin_thickness=random.uniform(10, 50),
            insulin=random.uniform(0, 300),
            bmi=random.uniform(18, 40),
            diabetes_pedigree_function=random.uniform(0.1, 2.0),
            age=random.randint(20, 80),
            prediction=random.choice(["Diabetic", "Not Diabetic"])
        )

    # 3. Create Heart Records
    print("Generating Heart Records...")
    for _ in range(5):
        HeartRecord.objects.create(
            user=user,
            age=random.randint(30, 80),
            gender=random.choice(["Male", "Female"]),
            chest_pain_type=random.choice(["ATA", "NAP", "ASY", "TA"]),
            resting_bp=random.uniform(90, 180),
            cholesterol=random.uniform(100, 400),
            fasting_bs=random.choice(["0", "1"]),
            resting_ecg=random.choice(["Normal", "ST", "LVH"]),
            max_hr=random.randint(60, 200),
            exercise_angina=random.choice(["Y", "N"]),
            old_peak=random.uniform(0, 6),
            st_slope=random.choice(["Up", "Flat", "Down"]),
            prediction=random.choice(["Presence", "Absence"])
        )

    # 4. Create Liver Records
    print("Generating Liver Records...")
    for _ in range(5):
        LiverRecord.objects.create(
            user=user,
            age=random.randint(20, 80),
            gender=random.choice(["Male", "Female"]),
            total_bilirubin=random.uniform(0.1, 10.0),
            direct_bilirubin=random.uniform(0.1, 5.0),
            alkaline_phosphatase=random.uniform(50, 500),
            alamine_aminotransferase=random.uniform(10, 200),
            aspartate_aminotransferase=random.uniform(10, 200),
            total_proteins=random.uniform(2.0, 10.0),
            albumin=random.uniform(1.0, 6.0),
            albumin_and_globulin_ratio=random.uniform(0.1, 3.0),
            prediction=random.choice(["1", "2"]) # 1: Liver Disease, 2: No Liver Disease
        )

    # 5. Create Cancer Records
    print("Generating Cancer Records...")
    for _ in range(5):
        # Generate 30 random features usually found in breast cancer datasets
        features = [random.uniform(0, 50) for _ in range(30)]
        CancerRecord.objects.create(
            user=user,
            features=json.dumps(features),
            prediction=random.choice(["Malignant", "Benign"])
        )
        
    print(f"\nSUCCESS: Dummy data generated for user '{username}'.")
    print(f"Login with -> Username: {username} | Password: {password}")

if __name__ == "__main__":
    create_dummy_data()
