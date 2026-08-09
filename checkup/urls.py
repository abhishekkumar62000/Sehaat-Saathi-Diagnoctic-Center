from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import FileResponse
import os

def service_worker(request):
    """Serve service worker from root scope for PWA"""
    sw_path = os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), 'front', 'sw.js')
    if not os.path.exists(sw_path):
        # Fallback: serve from staticfiles dirs
        sw_path = os.path.join(settings.BASE_DIR, 'static', 'front', 'sw.js')
    from django.http import HttpResponse
    try:
        with open(sw_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/javascript')
    except:
        return HttpResponse('// SW not found', content_type='application/javascript')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('main.urls')),
    path('auth/' , include('appointment.urls')),
    path('sw.js', service_worker, name='service_worker'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
