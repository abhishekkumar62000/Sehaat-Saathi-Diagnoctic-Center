# 🔑 **ENVIRONMENT VARIABLES - COMPLETE GUIDE**

## ✅ **REQUIRED ENVIRONMENT VARIABLES**

### 1. **Django Configuration**

#### SECRET_KEY
```
Name: SECRET_KEY
Value: [Generate new strong key]
Required: YES ✅
Example: django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

How to Generate:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Or copy-paste a 50+ character random string:
dj-4k_9$x@2m#p&8z*5!j%q^3v~6n(7)w&2x_8y+4z-1a@b
```

#### DEBUG
```
Name: DEBUG
Value: False
Required: YES ✅
Note: ALWAYS False in production!
```

#### ALLOWED_HOSTS
```
Name: ALLOWED_HOSTS
Value: your-app.railway.app,yourdomain.com,www.yourdomain.com
Required: YES ✅
Example: sehaat-saathi.railway.app,sehaat-saathi.com,www.sehaat-saathi.com
```

---

### 2. **Database Configuration**

#### DATABASE_URL
```
Name: DATABASE_URL
Value: [Auto-set by Railway/Heroku]
Required: YES ✅
Status: AUTOMATIC - Railway/Heroku provides this
Format: postgresql://user:password@host:5432/dbname
Leave BLANK when setting up - platform fills automatically!
```

---

### 3. **Email Configuration (Gmail)**

#### EMAIL_HOST
```
Name: EMAIL_HOST
Value: smtp.gmail.com
Required: YES ✅
```

#### EMAIL_HOST_USER
```
Name: EMAIL_HOST_USER
Value: your-email@gmail.com
Required: YES ✅
Example: abhishek@gmail.com
```

#### EMAIL_HOST_PASSWORD
```
Name: EMAIL_HOST_PASSWORD
Value: [16-character Gmail App Password]
Required: YES ✅

HOW TO GET:
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in (use 2-factor authentication)
3. Select "Mail" and "Windows Computer"
4. Google generates 16-character password
5. Copy entire password (with spaces)

Example: abcd efgh ijkl mnop
```

#### EMAIL_PORT
```
Name: EMAIL_PORT
Value: 587
Required: YES ✅
```

#### EMAIL_USE_TLS
```
Name: EMAIL_USE_TLS
Value: True
Required: YES ✅
```

---

## 📦 **OPTIONAL BUT RECOMMENDED**

### 4. **AWS S3 Configuration (File Uploads)**

#### AWS_ACCESS_KEY_ID
```
Name: AWS_ACCESS_KEY_ID
Value: [Your AWS Access Key]
Required: NO (optional)
Status: If you want to use S3 for file uploads

HOW TO GET:
1. Create free AWS account: https://aws.amazon.com/free/
2. Go to AWS Console → IAM Dashboard
3. Create New User (e.g., "sehaat-saathi-user")
4. Assign Permissions:
   - AmazonS3FullAccess
   - AmazonTranscribeFullAccess
5. Create Access Key
6. Copy and save Access Key ID
7. Copy and save Secret Access Key

Example: AKIAIOSFODNN7EXAMPLE
```

#### AWS_SECRET_ACCESS_KEY
```
Name: AWS_SECRET_ACCESS_KEY
Value: [Your AWS Secret Key]
Required: NO (optional)

⚠️ KEEP THIS SECRET!
⚠️ NEVER share or commit to GitHub

Example: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

#### MY_REGION
```
Name: MY_REGION
Value: us-east-1
Required: NO (optional)
Default: us-east-1
Other options: us-west-2, eu-west-1, ap-south-1, etc.
```

#### BUCKET_NAME
```
Name: BUCKET_NAME
Value: [Your S3 Bucket Name]
Required: NO (optional)

HOW TO GET:
1. Go to AWS Console → S3
2. Click "Create Bucket"
3. Name: sehaat-saathi-uploads (must be unique worldwide)
4. Select region: us-east-1
5. Create bucket
6. Copy bucket name

Example: sehaat-saathi-uploads
```

---

### 5. **OpenAI Configuration (AI Features)**

#### OPENAI_API_KEY
```
Name: OPENAI_API_KEY
Value: [Your OpenAI API Key]
Required: NO (optional)
Status: If you want AI chatbot features

HOW TO GET:
1. Go to: https://platform.openai.com/api-keys
2. Sign in (create account if needed)
3. Click "Create new secret key"
4. Copy entire key
5. Save securely (can't see again!)

Format: sk-proj-...
Example: sk-proj-ABC123...rest of key...

⚠️ KEEP THIS SECRET!
⚠️ NEVER share this key!
```

---

## 📋 **COMPLETE ENVIRONMENT VARIABLES LIST**

### **FOR RAILWAY DEPLOYMENT**

Copy these into Railway Dashboard → Variables:

```
SECRET_KEY=your-generated-secret-key-here-change-this-50+ characters
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-gmail-app-password

AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
MY_REGION=us-east-1
BUCKET_NAME=your-s3-bucket-name

OPENAI_API_KEY=sk-your-openai-api-key
```

**Note**: DATABASE_URL is added automatically by Railway when you add PostgreSQL!

---

### **FOR HEROKU DEPLOYMENT**

Use Heroku CLI:

```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app.herokuapp.com,yourdomain.com'
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
heroku config:set AWS_ACCESS_KEY_ID=your-key
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret
heroku config:set MY_REGION=us-east-1
heroku config:set BUCKET_NAME=your-bucket
heroku config:set OPENAI_API_KEY=sk-your-key
```

**Note**: Add PostgreSQL add-on (Heroku auto-sets DATABASE_URL)

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

---

### **FOR PYTHONANYWHERE DEPLOYMENT**

Create .env file in web app directory:

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com,yourdomain.com
DATABASE_URL=sqlite:////home/username/db.sqlite3

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
MY_REGION=us-east-1
BUCKET_NAME=your-bucket

OPENAI_API_KEY=sk-your-key
```

---

## 🎯 **STEP-BY-STEP SETUP GUIDE**

### **Step 1: Generate SECRET_KEY**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (looks like: `django-insecure-a1b2c3d4...`)

---

### **Step 2: Get Gmail App Password**

1. Open: https://myaccount.google.com/app-passwords
2. Sign in (use 2-factor authentication if needed)
3. Select: **Mail** and **Windows Computer**
4. Google generates 16-character password
5. Copy it (including spaces)

---

### **Step 3: Get AWS Credentials (Optional)**

1. Create AWS account: https://aws.amazon.com/free/
2. Go to IAM Dashboard
3. Create new User
4. Assign: AmazonS3FullAccess + AmazonTranscribeFullAccess
5. Create Access Key
6. Save both keys securely

---

### **Step 4: Get OpenAI API Key (Optional)**

1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy immediately (can't see again)
4. Store securely

---

## ⚠️ **SECURITY BEST PRACTICES**

### ✅ DO:
- ✅ Use strong, random SECRET_KEY
- ✅ Use Gmail app-specific password (not regular password)
- ✅ Keep all keys in environment variables (not in code)
- ✅ Never commit .env file to GitHub
- ✅ Rotate keys periodically
- ✅ Use HTTPS/SSL everywhere

### ❌ DON'T:
- ❌ Don't share these keys with anyone
- ❌ Don't put keys in code or comments
- ❌ Don't use weak passwords
- ❌ Don't commit .env to GitHub
- ❌ Don't use same key for multiple apps
- ❌ Don't hardcode secrets

---

## 🧪 **TESTING ENVIRONMENT VARIABLES**

After setting variables, verify in Django shell:

```bash
python manage.py shell

# Check if variables are loaded:
from decouple import config
print(config('SECRET_KEY'))           # Should show your key
print(config('DEBUG'))                 # Should show False
print(config('EMAIL_HOST_USER'))       # Should show your email
```

If all show correct values, setup is successful! ✅

---

## 📊 **QUICK REFERENCE TABLE**

| Variable | Required | Value | Source |
|----------|----------|-------|--------|
| SECRET_KEY | YES | 50+ char string | Generate new |
| DEBUG | YES | False | Type exactly |
| ALLOWED_HOSTS | YES | domain.com | Your domain |
| DATABASE_URL | YES | Auto-set | Platform provides |
| EMAIL_HOST | YES | smtp.gmail.com | Static |
| EMAIL_PORT | YES | 587 | Static |
| EMAIL_USE_TLS | YES | True | Static |
| EMAIL_HOST_USER | YES | you@gmail.com | Your Gmail |
| EMAIL_HOST_PASSWORD | YES | 16-char | Gmail app password |
| AWS_ACCESS_KEY_ID | NO | your-key | AWS IAM |
| AWS_SECRET_ACCESS_KEY | NO | your-secret | AWS IAM |
| MY_REGION | NO | us-east-1 | Your choice |
| BUCKET_NAME | NO | bucket-name | AWS S3 |
| OPENAI_API_KEY | NO | sk-... | OpenAI platform |

---

## ✅ **FINAL CHECKLIST**

Before deploying:

- [ ] Generated new SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Added ALLOWED_HOSTS with your domain
- [ ] Got Gmail app-specific password
- [ ] Added EMAIL variables
- [ ] (Optional) Got AWS credentials and created S3 bucket
- [ ] (Optional) Got OpenAI API key
- [ ] Verified DATABASE_URL will be auto-set by platform
- [ ] Tested all variables in Django shell
- [ ] Ready to deploy!

---

## 🚀 **READY TO DEPLOY!**

Once you have all these variables set in your deployment platform:

1. **Railway**: Go to Variables section, add each variable
2. **Heroku**: Use `heroku config:set` commands
3. **PythonAnywhere**: Create .env file in app directory
4. **Render**: Add in environment section

Then deploy! Your app will be live in minutes! 🎉

---

**Questions?** Check:
- RAILWAY_DEPLOYMENT.md (for Railway)
- DEPLOYMENT_GUIDE.md (for all platforms)
- PRODUCTION_SETTINGS.md (for Django config)
