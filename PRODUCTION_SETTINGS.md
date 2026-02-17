# Production Settings Update Guide

## 🔒 CRITICAL: Update checkup/settings.py for Production

Replace lines 16-20 in your settings.py with:

```python
# SECURITY WARNING: keep the secret key used in production secret!
from decouple import config
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure--kl%km2!6d57(-uqq4hu(s^2k*%%m+_l!l+zlbxbn-&s5=a122'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
```

---

## 📝 Complete Production Settings

Add this at the end of checkup/settings.py:

```python
# ===== Production Configuration =====

import dj_database_url

# Use PostgreSQL in production
if not DEBUG:
    # Database from environment
    DATABASES['default'] = dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
    
    # SSL/HTTPS Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Content Security
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
        "script-src": ("'self'", "cdn.jsdelivr.net", "kit.fontawesome.com"),
        "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
        "img-src": ("'self'", "data:", "https:"),
    }

# Static Files (already configured with Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AWS S3 Configuration (for file uploads)
USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    import storages
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Django Extensions
INSTALLED_APPS += ['django_extensions']  # Optional, for helpful commands
```

---

## ✨ Create .env File Locally

Create a file named `.env` in your project root:

```
# Django Configuration
SECRET_KEY=your-very-long-random-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1

# Database (for development, otherwise use cloud provider)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (Gmail App Password)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
EMAIL_USE_TLS=True

# AWS S3 Configuration (if you want file uploads to cloud)
USE_S3=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Optional: OpenAI API (if using GPT features)
OPENAI_API_KEY=your-openai-api-key

# Optional: Sentry Error Tracking
SENTRY_DSN=
```

---

## 🔑 How to Get Required Keys

### 1. Generate Strong SECRET_KEY
```python
# Run this in Python:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Copy output to SECRET_KEY in .env
```

### 2. Gmail App Password
```
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Copy 16-character password
4. Use as EMAIL_HOST_PASSWORD
```

### 3. AWS S3 (for file uploads)
```
1. Create Free AWS Account: https://aws.amazon.com/free/
2. Go to IAM Dashboard
3. Create New User
4. Assign S3 and Transcribe Permissions
5. Create Access Key
6. Copy Access Key ID and Secret Key
```

### 4. OpenAI API (for AI features)
```
1. Go to: https://platform.openai.com/api-keys
2. Create new API key
3. Copy to OPENAI_API_KEY
```

---

## 🧪 Test Locally Before Deploying

```bash
# Create .env file with DEBUG=True
# Install dependencies
pip install -r requirements.txt

# Test with production settings locally
# Change DEBUG to False to test security settings
DEBUG=False python manage.py runserver

# Check for any issues
# Test static file serving
# Test email sending
# Test database connections
```

---

## 🚀 Deploy Steps

### For Railway:
1. Add all .env variables as "Variables" in Railway dashboard
2. Push code to GitHub
3. Railway auto-deploys
4. Check logs: `railway logs`

### For Heroku:
```bash
heroku config:set SECRET_KEY='your-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='yourdomain.com'
# ... add other variables

git push heroku main
heroku run python manage.py migrate
```

### For PythonAnywhere:
1. Upload .env file (replace values in Web app settings)
2. Reload web app
3. Check error logs

---

## 🔍 Verify Production Setup

After deployment, check:

```bash
# Check static files are served
curl https://yourdomain.com/static/front/neon_theme.css

# Check admin panel works
# https://yourdomain.com/admin/

# Check migrations ran
# Check database is not empty

# Monitor logs for errors
# Test each feature:
# - User registration
# - Disease prediction
# - Image upload
# - Email sending
# - Video call
```

---

## ⚠️ Security Checklist

- [ ] SECRET_KEY is unique and strong (30+ characters)
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS includes your domain
- [ ] Database credentials in .env (not in code)
- [ ] Email credentials in .env (not in code)
- [ ] AWS credentials in .env (not in code)
- [ ] HTTPS enabled (automatic on most platforms)
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] Regular backups enabled
- [ ] Error monitoring setup (Sentry)

---

## 📞 Troubleshooting

### "BadRequest: Invalid HTTP_HOST"
```
Solution: Check ALLOWED_HOSTS includes your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### "Psycopg2 Import Error"
```
Solution: Install PostgreSQL adapter
pip install psycopg2-binary
```

### "Static Files 404"
```
Solution: Run collectstatic
python manage.py collectstatic --noinput

Check STATIC_ROOT and STATIC_URL paths
```

### "Connection refused" on Email
```
Solution: Use app-specific Gmail password
Enable "Less secure apps" if on personal account
Check EMAIL_HOST_PASSWORD is correct
```

---

## 🎯 Recommended Production Stack

**Best Option: Railway + PostgreSQL + Cloudflare**

- Railway: $5/month (includes PostgreSQL)
- Cloudflare: Free (CDN + SSL)
- Sentry: Free tier (error tracking)
- **Total**: ~$5/month for professional setup

This gives you:
- ✅ Automatic deployments
- ✅ PostgreSQL database
- ✅ Free SSL/HTTPS
- ✅ CDN (faster loading)
- ✅ Error tracking
- ✅ Professional email monitoring
