# 🔑 ENVIRONMENT VARIABLES - QUICK COPY-PASTE

## ⚡ MINIMUM REQUIRED (For Basic App)

```
SECRET_KEY=django-insecure-[generate-new-50-char-string]
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=[16-char-gmail-app-password]
```

**Getting Values:**
- SECRET_KEY: Run `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- EMAIL_HOST_PASSWORD: https://myaccount.google.com/apppasswords (select Mail + Windows Computer)
- DATABASE_URL: Railway/Heroku sets automatically when you add PostgreSQL

---

## 🚀 COMPLETE SET (Recommended)

```
# Django
SECRET_KEY=your-50-char-random-string
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,sehaat-saathi.com,www.sehaat-saathi.com

# Database (AUTO-SET by platform - leave blank)
# DATABASE_URL=auto-set-by-railway-or-heroku

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx

# AWS S3
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
MY_REGION=us-east-1
BUCKET_NAME=sehaat-saathi-uploads

# OpenAI
OPENAI_API_KEY=sk-proj-ABC123...rest...
```

---

## 🔗 WHERE TO GET EACH VALUE

### SECRET_KEY
```bash
# Run this command:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the output (50+ characters starting with "django-insecure-")
```

### EMAIL_HOST_PASSWORD
```
1. Go: https://myaccount.google.com/apppasswords
2. Sign in (use 2FA if prompted)
3. Select "Mail" and "Windows Computer"
4. Copy 16-character password (with spaces)
Example: abcd efgh ijkl mnop
```

### AWS Keys (Optional)
```
1. AWS Account: https://aws.amazon.com/console/
2. IAM Dashboard
3. Create User → Create Access Key
4. Download credentials
5. Copy Access Key ID and Secret Key
```

### OPENAI_API_KEY (Optional - for AI features)
```
1. Go: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy immediately
Example: sk-proj-ABC123XYZ789...
```

---

## 📍 HOW TO SET VARIABLES

### Railway
```
1. Your Project → Variables
2. Click "New Variable"
3. Name: SECRET_KEY
4. Value: your-key
5. Add Secret
6. Repeat for all variables
```

### Heroku
```bash
heroku config:set SECRET_KEY='your-key'
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
# etc.
```

### PythonAnywhere
```
Create file: .env in your app directory
Add all variables as shown above
```

### Render.com
```
1. Environment section
2. Add variable
3. Name-value pairs
```

---

## ✅ VALIDATE SETUP

After setting variables, run:

```bash
python manage.py shell

from decouple import config

# Check each variable
print("SECRET_KEY:", config('SECRET_KEY')[:20] + "...")
print("DEBUG:", config('DEBUG'))
print("EMAIL_HOST_USER:", config('EMAIL_HOST_USER'))
print("ALLOWED_HOSTS:", config('ALLOWED_HOSTS'))
```

All should show without errors ✅

---

## 🎯 MINIMAL SETUP (Testing Only)

For local testing before deployment:

```
SECRET_KEY=django-insecure-test-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=test@gmail.com
EMAIL_HOST_PASSWORD=test-password
DATABASE_URL=sqlite:///db.sqlite3
```

---

## ⚠️ SECURITY REMINDERS

- 🔒 NEVER share these values
- 🔒 NEVER commit .env to GitHub
- 🔒 NEVER use weak passwords
- 🔒 NEVER hardcode in app code
- 🔒 Use environment variables only!

---

## 📱 FULL STEP-BY-STEP FOR RAILWAY

1. **Generate SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Get Gmail App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select Mail + Windows Computer
   - Copy 16-character password

3. **Set in Railway**
   - Go to: https://railway.app → Your Project → Variables
   - Add each variable from list above

4. **Add PostgreSQL**
   - Click "Add" → Select PostgreSQL
   - DATABASE_URL auto-added ✅

5. **Deploy**
   - Click "Deploy" button
   - Wait 5-10 minutes
   - Your app live! 🎉

---

## 🎓 COMPLETE GUIDE

For detailed explanations, see: `ENVIRONMENT_VARIABLES_GUIDE.md`

For platform-specific help, see:
- `RAILWAY_DEPLOYMENT.md` (Railway)
- `DEPLOYMENT_GUIDE.md` (all platforms)
- `PRODUCTION_SETTINGS.md` (Django config)

---

**Status**: ✅ Ready to Deploy!
