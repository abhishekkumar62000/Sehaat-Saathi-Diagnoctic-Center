from django.contrib import admin
from main.models import DiabetesRecord, HeartRecord, LiverRecord, CancerRecord, ImagePredictionRecord

# Register your models here.
admin.site.register(DiabetesRecord)
admin.site.register(HeartRecord)
admin.site.register(LiverRecord)
admin.site.register(CancerRecord)
admin.site.register(ImagePredictionRecord)