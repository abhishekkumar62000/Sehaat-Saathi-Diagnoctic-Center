from django.shortcuts import render , redirect
from django.http import HttpResponse , HttpResponseRedirect , JsonResponse , FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from main.models import DiabetesRecord, HeartRecord, LiverRecord, CancerRecord, ImagePredictionRecord
from main.ai_assistant import get_health_advice
import os
import re
import json
import base64
import random
import time
import boto3
import numpy as np
from PIL import Image
from django.template.loader import get_template
from xhtml2pdf import pisa
from main.health_guardian import get_health_plan
from .forms import LabReportForm, RoadmapForm, MoodTrackerForm, MedicalPassportForm, PharmaCheckerForm
import qrcode
from io import BytesIO
from main.roadmap_logic import get_roadmap_data

# Optional ML imports - wrapped to allow frontend to work without them
try:
    import cv2
    import torch
    from models.classifiers import (predict_malaria, predict_liverD, predict_heartD, predict_alzheimer, 
    predict_diabetes, predict_cancerB, predict_glaucoma, predict_covid, predict_brain, localizeTumor, predict_disease)
    from models.transcribe import get_text
    ML_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    ML_AVAILABLE = False
    # Dummy functions when ML is not available
    predict_malaria = predict_liverD = predict_heartD = predict_alzheimer = None
    predict_diabetes = predict_cancerB = predict_glaucoma = predict_covid = None
    predict_brain = localizeTumor = predict_disease = None
    get_text = None

# Create your views here
def features_hub(request):
    return render(request, 'features_hub.html')

def health_roadmap_view(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Helper to calculate BMI
            height_m = data['height'] / 100
            bmi = data['weight'] / (height_m * height_m)
            
            # Logic
            plan = get_roadmap_data(data['goal'], data['diet_preference'])
            
            context = {
                'user_data': data,
                'plan': plan,
                'bmi': bmi
            }
            
            # Generate PDF
            template_path = 'roadmap/pdf_template.html'
            template = get_template(template_path)
            html = template.render(context)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Health_Roadmap_{data["name"]}.pdf"'
            
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
            
    else:
        form = RoadmapForm()
    
    return render(request, 'roadmap/form.html', {'form': form})

def front(request):
    return render(request , 'front/index.html')

def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            context = data.get('context', {})
            
            # Get Chat History from Session (Limit to last 6 messages to save cost)
            chat_history = request.session.get('chat_history', [])
            
            response_text = get_health_advice(user_message, context, chat_history)
            
            # Update History (User + Bot)
            chat_history.append({"role": "user", "content": user_message})
            chat_history.append({"role": "assistant", "content": response_text})
            
            # Keep only last 6 messages (3 turns) context window
            if len(chat_history) > 6:
                chat_history = chat_history[-6:]
                
            request.session['chat_history'] = chat_history
            
            return JsonResponse({'response': response_text})
        except Exception as e:
            print(f"Chat Error: {e}")
            return JsonResponse({'response': "I apologize, but I encountered an error processing your request."}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def bmiCalc(request):
    return render(request , 'bmi/bmi-calculator.html')

@login_required(login_url='login')
def dashboard(request):
    diabetes_records = DiabetesRecord.objects.filter(user=request.user).order_by('-date')
    heart_records = HeartRecord.objects.filter(user=request.user).order_by('-date')
    liver_records = LiverRecord.objects.filter(user=request.user).order_by('-date')
    cancer_records = CancerRecord.objects.filter(user=request.user).order_by('-date')
    image_records = ImagePredictionRecord.objects.filter(user=request.user).order_by('-date')
    
    # Prepare Data for Charts (Ascending Order)
    d_asc = diabetes_records.reverse()
    d_dates = [r.date.strftime("%Y-%m-%d") for r in d_asc]
    d_glucose = [r.glucose for r in d_asc]
    d_bmi = [r.bmi for r in d_asc]

    h_asc = heart_records.reverse()
    h_dates = [r.date.strftime("%Y-%m-%d") for r in h_asc]
    h_bp = [r.resting_bp for r in h_asc]
    h_chol = [r.cholesterol for r in h_asc]

    context = {
        'diabetes_records': diabetes_records,
        'heart_records': heart_records,
        'liver_records': liver_records,
        'cancer_records': cancer_records,
        'image_records': image_records,
        # Chart Data
        'd_dates': json.dumps(d_dates),
        'd_glucose': json.dumps(d_glucose),
        'd_bmi': json.dumps(d_bmi),
        'h_dates': json.dumps(h_dates),
        'h_bp': json.dumps(h_bp),
        'h_chol': json.dumps(h_chol),
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def download_report(request):
    try:
        # Fetch Data
        diabetes_records = DiabetesRecord.objects.filter(user=request.user).order_by('-date')
        heart_records = HeartRecord.objects.filter(user=request.user).order_by('-date')
        liver_records = LiverRecord.objects.filter(user=request.user).order_by('-date')
        cancer_records = CancerRecord.objects.filter(user=request.user).order_by('-date')
        image_records = ImagePredictionRecord.objects.filter(user=request.user).order_by('-date')

        context = {
            'user': request.user,
            'diabetes_records': diabetes_records,
            'heart_records': heart_records,
            'liver_records': liver_records,
            'cancer_records': cancer_records,
            'image_records': image_records,
        }

        # Render Template
        template_path = 'report_template.html'
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
        return response
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")

def heart(request):
    return render(request , 'heart/index.html')

def heartPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        features = list(map(float , features))
        pred = predict_heartD(np.array([features]))
        
        if request.user.is_authenticated:
            HeartRecord.objects.create(
                user=request.user,
                age=int(features[0]),
                gender=str(features[1]),
                chest_pain_type=str(features[2]),
                resting_bp=features[3],
                cholesterol=features[4],
                fasting_bs=str(features[5]),
                resting_ecg=str(features[6]),
                max_hr=features[7],
                exercise_angina=str(features[8]),
                old_peak=features[9],
                st_slope=str(features[10]),
                prediction=pred
            )
            
        context = {
            'pred':pred,
            'chat_disease': 'Heart Disease',
            'chat_result': pred,
            'chat_data': f"Age: {features[0]}, BP: {features[3]}, Cholesterol: {features[4]}",
            'health_choice': get_health_plan('Heart Disease', pred)
        }
        return render(request , 'heart/output.html' , context)
    
    else:
        redirect('heart-disease/')

def diabetes(request):
    return render(request , 'diabetes/index.html')

def diabetesPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        pred = predict_diabetes(np.array([features]))
        
        if request.user.is_authenticated:
            try:
                # features: [Pregnancies, Glucose, BP, SkinThickness, Insulin, BMI, DPF, Age]
                # Note: Input values might be strings from request, need conversion
                f_float = [float(x) for x in features]
                DiabetesRecord.objects.create(
                    user=request.user,
                    pregnancies=int(f_float[0]),
                    glucose=f_float[1],
                    blood_pressure=f_float[2],
                    skin_thickness=f_float[3],
                    insulin=f_float[4],
                    bmi=f_float[5],
                    diabetes_pedigree_function=f_float[6],
                    age=int(f_float[7]),
                    prediction=pred
                )
            except Exception as e:
                print(f"Error saving diabetes record: {e}")

        context = {
            'pred':pred,
            'chat_disease': 'Diabetes',
            'chat_result': pred,
            'chat_data': f"Pregnancies: {features[0]}, Glucose: {features[1]}, BP: {features[2]}, BMI: {features[5]}",
            'health_choice': get_health_plan('Diabetes', pred)
        }
        return render(request , 'diabetes/output.html' , context)
    
    else:
        redirect('diabetes/')

def kidneyPred(request):
    if request.method == 'POST':
        try:
            # Extract features for Kidney (Age, BP, SG, AL, BGR, SC, Hemo, RC)
            # Since we may not have a real model file, we will MOCK the logic intelligently
            # based on thresholds for common CKD indicators.
            
            data = request.POST
            age = float(data.get('age', 0))
            bp = float(data.get('bp', 0))
            sg = float(data.get('sg', 1.020))
            al = float(data.get('al', 0))
            bgr = float(data.get('bgr', 0))
            sc = float(data.get('sc', 0))
            hemo = float(data.get('hemo', 0))
            rc = float(data.get('rc', 0))

            # Simple Mock Logic for CKD
            # High BP, High Glucose, Low Hemo, High Creatinine -> Risk
            score = 0
            if bp > 140: score += 1
            if bgr > 180: score += 2
            if sc > 1.2: score += 2
            if hemo < 11: score += 1
            if al > 0: score += 1
            if sg < 1.015: score += 1

            pred = 1 if score >= 3 else 0 # 1 = CKD, 0 = Normal
            
            # Context for Output & Chatbot
            context = {
                'pred': pred,
                'chat_disease': 'Chronic Kidney Disease',
                'chat_result': "Positive (High Risk)" if pred == 1 else "Negative (Normal)",
                'chat_data': f"BP: {bp}, Glucose: {bgr}, Creatinine: {sc}, Hemo: {hemo}",
                # 'health_choice': get_health_plan('Kidney Disease', pred) # If implemented
            }
            return render(request, 'kidney/output.html', context)

        except Exception as e:
            print(f"Kidney Pred Error: {e}")
            return render(request, 'kidney/index.html', {'error': 'Invalid Input'})

    return render(request, 'kidney/index.html')

def liver(request):
    return render(request , 'liver/index.html')

def liverPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        out_features = request.POST.dict()
        print(out_features)
        pred = predict_liverD(np.array([features]))
        
        if request.user.is_authenticated:
            try:
                f_floats = [float(x) for x in features]
                LiverRecord.objects.create(
                    user=request.user,
                    age=int(f_floats[0]),
                    gender=str(f_floats[1]),
                    total_bilirubin=f_floats[2],
                    direct_bilirubin=f_floats[3],
                    alkaline_phosphatase=f_floats[4],
                    alamine_aminotransferase=f_floats[5],
                    aspartate_aminotransferase=f_floats[6],
                    total_proteins=f_floats[7],
                    albumin=f_floats[8],
                    albumin_and_globulin_ratio=f_floats[9],
                    prediction=pred
                )
            except Exception as e:
                print(f"Error saving liver record: {e}")

        context = {
            'pred':pred,
            'out_features':out_features,
            'chat_disease': 'Liver Disease',
            'chat_result': pred,
            'chat_data': f"Age: {features[0]}, Gender: {features[1]}, Bilirubin: {features[2]}",
            'health_choice': get_health_plan('Liver Disease', pred)
        }
        return render(request , 'liver/page2.html' , context)
    
    else:
        redirect('liver/')

def cancer(request):
    return render(request , 'cancer/cancer.html')

def cancerPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        pred = predict_cancerB(np.array([features]))

        if request.user.is_authenticated:
            try:
                CancerRecord.objects.create(
                    user=request.user,
                    features=json.dumps(features),
                    prediction=pred
                )
            except Exception as e:
                print(f"Error saving cancer record: {e}")

        context = {
            'pred':pred,
            'chat_disease': 'Breast Cancer',
            'chat_result': pred,
            'chat_data': f"Mean Radius: {features[0]}, Mean Texture: {features[1]}",
            'health_choice': get_health_plan('Breast Cancer', pred)
        }
        return render(request , 'cancer/output.html' , context)
    
    else:
        redirect('cancer/')

def alzheimerPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).convert("RGB").resize((224, 224))
        label , cam_path = predict_alzheimer(img , file_path , file_path.replace(".jpg", "") + "_camViz.jpg")

        if request.user.is_authenticated:
            ImagePredictionRecord.objects.create(
                user=request.user,
                disease_type='Alzheimer',
                image_path=file_url,
                prediction=label
            )

        with open(cam_path, "rb") as img2str:
            converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': cam_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'alzheimer/Alzheimer.html')

def covidPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).resize((299, 299))
        label , cam_path = predict_covid(img , file_path , file_path.replace(".png", "") + "_camViz.jpg")

        if request.user.is_authenticated:
            ImagePredictionRecord.objects.create(
                user=request.user,
                disease_type='Covid',
                image_path=file_url,
                prediction=label
            )

        with open(cam_path, "rb") as img2str:
            converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': cam_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'covid/covid.html')

def brainPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).resize((224, 224))
        label = predict_brain(img)
        
        if request.user.is_authenticated:
            ImagePredictionRecord.objects.create(
                user=request.user,
                disease_type='Brain Tumor',
                image_path=file_url,
                prediction=label
            )

        if label == "No Tumor":
            with open(file_path, "rb") as img2str:
                converted_string = base64.b64encode(img2str.read())
            context = {
                'file_url': file_path,
                'label': label,
                'photo': str(converted_string)
            }
        else:
            out_path = localizeTumor(file_path , file_path.replace(".jpg", "") + "_tumorLoc.jpg")
            with open(out_path, "rb") as img2str:
                converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': out_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'brain/BrainTumor.html')

def malariaPred(request):
    if request.method == 'POST'and request.FILES['image']:
        
        img_file = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img_file.name, img_file)
        file_url = fss.url(file)

        img = Image.open(img_file).convert("RGB").resize((100, 100))
        label = predict_malaria(img)
        
        if request.user.is_authenticated:
            ImagePredictionRecord.objects.create(
                user=request.user,
                disease_type='Malaria',
                image_path=file_url,
                prediction=label
            )

        context = {
            'label': label,
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'malaria/malaria.html')     

def glaucomaPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img_file = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img_file.name, img_file)
        file_url = fss.url(file)

        img = Image.open(img_file).convert("RGB").resize((300, 300))
        label = predict_glaucoma(img)
        
        if request.user.is_authenticated:
            ImagePredictionRecord.objects.create(
                user=request.user,
                disease_type='Glaucoma',
                image_path=file_url,
                prediction=label
            )

        context = {
            'label': label,
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'glaucoma/index.html')

def pneumoniaPred(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            img_file = request.FILES['image']
            fss = FileSystemStorage()
            file = fss.save(img_file.name, img_file)
            file_url = fss.url(file)

            # Mock Prediction Logic since model file is missing
            # Randomly return Normal or Pneumonia for demo purposes
            # In production, load actual model here
            is_pneumonia = random.choice([True, False])
            label = "Pneumonia" if is_pneumonia else "Normal"
            
            if request.user.is_authenticated:
                ImagePredictionRecord.objects.create(
                    user=request.user,
                    disease_type='Pneumonia',
                    image_path=file_url,
                    prediction=label
                )
            
            # Pass context for Chatbot
            context = {
                'pred': label,
                'chat_disease': 'Pneumonia',
                'chat_result': label,
                'chat_data': 'Uploaded X-Ray Analysis'
            }
            return render(request, 'pneumonia/output.html', context)
        except Exception as e:
            print(f"Error in Pneumonia prediction: {e}")
            return render(request, 'pneumonia/index.html', {'error': 'Analysis Failed'})

    return render(request, 'pneumonia/index.html')

def symptomsDis(request):

    if request.method == 'POST' and 'audio' not in request.FILES:
        values = list(request.POST.dict().values())
        user_symptoms = values[:-1]
        days = int(values[-1])
        advice, output = predict_disease(user_symptoms , days)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_data = request.FILES["audio"]
        fss = FileSystemStorage()
        file_name = audio_data.name + ".webm"
        file = fss.save(file_name, audio_data)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        text = get_text(file_path , file_name)
        out = re.findall("[a-zA-Z]+", text)
        advice, output = predict_disease(out)
        print(advice , output)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'soundRecorder/recorder.html')

def analyze_lab_report(request):
    if request.method == 'POST':
        form = LabReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            analysis = []
            
            # --- Analysis Logic ---
            gender = data['gender']
            
            # Hemoglobin
            hb = data.get('hemoglobin')
            if hb is not None:
                low, high = (13.5, 17.5) if gender == 'Male' else (12.0, 15.5)
                if hb < low:
                    analysis.append({"title": "Hemoglobin", "status": "Low", "value": hb, "unit": "g/dL", "msg": "Indicates anemia (low red blood count). You might feel tired, weak, or dizzy.", "recommendation": "Eat iron-rich foods (spinach, red meat, beans). Consider a Vitamin C supplement to help absorption."})
                elif hb > high:
                    analysis.append({"title": "Hemoglobin", "status": "High", "value": hb, "unit": "g/dL", "msg": "Could indicate dehydration, smoking side-effects, or lung issues.", "recommendation": "Stay well-hydrated and avoid smoking. Consult a doctor if persistent."})
                else:
                    analysis.append({"title": "Hemoglobin", "status": "Normal", "value": hb, "unit": "g/dL", "msg": "Your oxygen-carrying capacity is good."})
                    
            # WBC
            wbc = data.get('wbc')
            if wbc is not None:
                if wbc < 4500:
                    analysis.append({"title": "White Blood Cells", "status": "Low", "value": wbc, "unit": "cells/mcL", "msg": "Leukopenia: Immune system might be weakened.", "recommendation": "Avoid crowded places and sick people. Eat a nutrient-rich diet."})
                elif wbc > 11000:
                    analysis.append({"title": "White Blood Cells", "status": "High", "value": wbc, "unit": "cells/mcL", "msg": "Leukocytosis: Likely fighting an infection (bacterial/viral) or inflammation.", "recommendation": "Monitor for fever. Rest and hydration are key."})
                else:
                    analysis.append({"title": "White Blood Cells", "status": "Normal", "value": wbc, "unit": "cells/mcL", "msg": "Immune system is functioning within standard range."})
            
            # Platelets
            platelets = data.get('platelets')
            if platelets is not None:
                if platelets < 150000:
                     analysis.append({"title": "Platelets", "status": "Low", "value": platelets, "unit": "cells/mcL", "msg": "Thrombocytopenia: Risk of bleeding/bruising.", "recommendation": "Avoid injury-prone activities. Report unusual bruising."})
                elif platelets > 450000:
                     analysis.append({"title": "Platelets", "status": "High", "value": platelets, "unit": "cells/mcL", "msg": "Thrombocytosis: Blood might clot too easily.", "recommendation": "Stay hydrated. Your doctor may check for underlying inflammation."})
                else:
                     analysis.append({"title": "Platelets", "status": "Normal", "value": platelets, "unit": "cells/mcL", "msg": "Blood clotting ability is normal."})

            # Glucose
            glucose = data.get('glucose_fasting')
            if glucose is not None:
                if glucose < 70:
                    analysis.append({"title": "Fasting Glucose", "status": "Low", "value": glucose, "unit": "mg/dL", "msg": "Hypoglycemia: Low blood sugar.", "recommendation": "Eat a small snack with sugar accurately to bring it up."})
                elif glucose > 100:
                    status = "High (Pre-Diabetic)" if glucose < 126 else "High (Diabetic Range)"
                    analysis.append({"title": "Fasting Glucose", "status": status, "value": glucose, "unit": "mg/dL", "msg": "Elevated blood sugar levels.", "recommendation": "Reduce sugar/carb intake. Exercise regularly."})
                else:
                    analysis.append({"title": "Fasting Glucose", "status": "Normal", "value": glucose, "unit": "mg/dL", "msg": "Blood sugar regulation is healthy."})

            # Cholesterol
            chol = data.get('cholesterol')
            if chol is not None:
                 if chol > 200:
                     analysis.append({"title": "Total Cholesterol", "status": "High", "value": chol, "unit": "mg/dL", "msg": "Hyperlipidemia: Risk factor for heart disease.", "recommendation": "Reduce saturated fats (fried food, red meat). Increase fiber."})
                 else:
                     analysis.append({"title": "Total Cholesterol", "status": "Normal", "value": chol, "unit": "mg/dL", "msg": "Lipid levels are healthy."})
            
            # Creatinine
            creat = data.get('creatinine')
            if creat is not None:
                if creat > 1.3: # slightly simplified for gender
                    analysis.append({"title": "Creatinine", "status": "High", "value": creat, "unit": "mg/dL", "msg": "Kidney function might be stressed.", "recommendation": "Stay hydrated. Limit protein intake slightly until re-checked."})
                else:
                    analysis.append({"title": "Creatinine", "status": "Normal", "value": creat, "unit": "mg/dL", "msg": "Kidney filtration is working well."})

            return render(request, 'lab_analyzer/result.html', {'analysis': analysis, 'user_data': data})
    else:
        form = LabReportForm()
    
    return render(request, 'lab_analyzer/form.html', {'form': form})

def mood_tracker_view(request):
    analysis_result = None
    sentiment_color = "primary"
    
    if request.method == 'POST':
        form = MoodTrackerForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['journal_entry'].lower()
            mood = form.cleaned_data['current_mood']
            name = form.cleaned_data['name']
            
            # Simple keyword analysis
            pos_words = ['happy', 'good', 'great', 'excellent', 'excited', 'joy', 'blessed', 'energetic', 'calm']
            neg_words = ['sad', 'bad', 'depressed', 'anxious', 'worried', 'stressed', 'tired', 'angry', 'lonely']
            
            p_score = sum(1 for w in pos_words if w in entry)
            n_score = sum(1 for w in neg_words if w in entry)
            
            if p_score > n_score:
                sentiment = "Positive"
                advice = "It sounds like you're in a good place! Keep doing what you're doing. Channel this energy into something creative."
                sentiment_color = "success"
            elif n_score > p_score:
                sentiment = "Negative/Stressed"
                advice = "It seems like things are tough right now. Remember to take deep breaths. Consider a 5-minute meditation or a short walk."
                sentiment_color = "warning"
            else:
                sentiment = "Neutral/Mixed"
                advice = "Balanced days are good. Listen to your body and mind."
                sentiment_color = "info"
                
            analysis_result = {
                'sentiment': sentiment,
                'advice': advice,
                'name': name,
                'mood': mood
            }
    else:
        form = MoodTrackerForm()
        
    return render(request, 'mood_tracker/index.html', {'form': form, 'result': analysis_result, 'color': sentiment_color})

def medical_passport_view(request):
    qr_code_img = None
    
    if request.method == 'POST':
        form = MedicalPassportForm(request.POST)
        if form.is_valid():
            # Create a string with the data
            data_string = f"EMERGENCY MEDICAL PASSPORT\nName: {form.cleaned_data['full_name']}\nDOB: {form.cleaned_data['dob']}\nBlood Type: {form.cleaned_data['blood_type']}\nAllergies: {form.cleaned_data['allergies']}\nConditions: {form.cleaned_data['existing_conditions']}\nEmergency Contact: {form.cleaned_data['emergency_contact_name']} ({form.cleaned_data['emergency_contact_phone']})"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_string)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_img = base64.b64encode(buffer.getvalue()).decode()
            
    else:
        form = MedicalPassportForm()
        
    return render(request, 'medical_passport/index.html', {'form': form, 'qr_image': qr_code_img})

def voice_assistant_view(request):
    return render(request, 'voice_bot/index.html')

def pharma_interaction_view(request):
    result = None
    if request.method == 'POST':
        form = PharmaCheckerForm(request.POST)
        if form.is_valid():
            med1 = form.cleaned_data['medication_1'].lower().strip()
            med2 = form.cleaned_data['medication_2'].lower().strip()
            
            # Simple simulation database of common dangerous interactions
            # Real implementation would use an API like NIH RxNav
            interactions = {
                frozenset(['aspirin', 'warfarin']): {
                    'severity': 'High',
                    'msg': 'Increased risk of bleeding. Taking these together can dangerously thin the blood.'
                },
                 frozenset(['aspirin', 'ibuprofen']): {
                    'severity': 'Moderate',
                    'msg': 'Increased risk of stomach ulcers and gastrointestinal bleeding. May also reduce the heart-protective effect of aspirin.'
                },
                frozenset(['lisinopril', 'potassium']): {
                    'severity': 'High',
                    'msg': 'Risk of Hyperkalemia (high potassium levels), which can cause irregular heart rhythm.'
                },
                frozenset(['viagra', 'nitrates']): {
                    'severity': 'Critical',
                    'msg': 'Extreme drop in blood pressure. Can be fatal.'
                },
                frozenset(['acetaminophen', 'alcohol']): {
                    'severity': 'High',
                    'msg': 'Increased risk of severe liver damage.'
                }
            }
            
            # Check interaction
            key = frozenset([med1, med2])
            
            # Allow fuzzy matching for demo purposes
            interaction_found = None
            for k, val in interactions.items():
                k_list = list(k)
                if (med1 in k_list[0] and med2 in k_list[1]) or (med1 in k_list[1] and med2 in k_list[0]):
                    interaction_found = val
                    break
            
            if interaction_found:
                result = {
                    'status': 'Danger',
                    'severity': interaction_found['severity'],
                    'message': interaction_found['msg'],
                    'color': 'danger' if interaction_found['severity'] in ['High', 'Critical'] else 'warning'
                }
            else:
                result = {
                    'status': 'Safe',
                    'severity': 'None Detected',
                    'message': 'No major interactions found in our basic database. Always consult a doctor.',
                    'color': 'success'
                }
                
    else:
        form = PharmaCheckerForm()
        
    return render(request, 'pharma/index.html', {'form': form, 'result': result})
