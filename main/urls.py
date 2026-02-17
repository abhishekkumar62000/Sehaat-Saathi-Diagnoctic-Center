from django.urls import path, include
from main import views

urlpatterns = [
    path('' , views.front , name = 'index'),
    path('features-hub/', views.features_hub, name='features-hub'),
    path('health-roadmap/', views.health_roadmap_view, name='roadmap-view'),
    path('chat-api/', views.chat_api, name='chat-api'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download-report/', views.download_report, name='download-report'),
    path('know-your-disease' , views.symptomsDis , name = 'know-your-disease'),

    path('calculate-bmi/' , views.bmiCalc , name = 'bmi-calculator'),

    path('alzheimer/' , views.alzheimerPred , name = 'alzheimer-predict'),

    path('cancer/' , views.cancer , name = 'cancer-view'),
    path('cancer-prediction/' , views.cancerPred , name = 'cancer-predict'),

    path('brain-tumor/' , views.brainPred , name = 'brain-tumor-predict'),

    path('covid/' , views.covidPred , name = 'covid-predict'),
    
    path('pneumonia/', views.pneumoniaPred, name='pneumonia-predict'),
    path('kidney-predict/', views.kidneyPred, name='kidney-predict'),

    path('diabetes/' , views.diabetes , name = 'diabetes-view'),
    path('diabetes-prediction/' , views.diabetesPred , name = 'diabetes-predict'),

    path('glaucoma/' , views.glaucomaPred , name = 'glaucoma-predict'),

    path('heart-disease/' , views.heart , name = 'heart-disease-view'),
    path('heart-disease-prediction/' , views.heartPred , name = 'heart-disease-predict'),

    path('liver/' , views.liver , name = 'liver-view'),
    path('liver-prediction/' , views.liverPred , name = 'liver-predict'),

    path('malaria/' , views.malariaPred , name = 'malaria-predict'),

    path('lab-analyzer/' , views.analyze_lab_report , name = 'lab-analyzer'),
    path('mood-tracker/', views.mood_tracker_view, name='mood-tracker'),
    path('medical-passport/', views.medical_passport_view, name='medical-passport'),
    path('voice-doctor/', views.voice_assistant_view, name='voice-doctor'),
    path('pharma-check/', views.pharma_interaction_view, name='pharma-check'),
]