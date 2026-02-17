# 🎯 STEP-BY-STEP DEPLOYMENT INSTRUCTIONS

## 🚀 OPTION 1: RAILWAY (RECOMMENDED - EASIEST)

### Step 1: Prepare Your Code
```bash
cd "c:\Users\DELL\Downloads\Sehaat Saathi Diagnoctic Center"

# Initialize git if not already done
git init
git add .
git commit -m "Ready for Railway deployment"

# Push to GitHub (Railway connects to GitHub)
# If you don't have GitHub, create account at github.com
git remote add origin https://github.com/YOUR-USERNAME/sehaat-saathi.git
git push -u origin main
```

### Step 2: Create Railway Account
```
1. Go to: https://railway.app
2. Click "Start a new project"
3. Sign up with GitHub (or Email)
4. Authorize GitHub access
```

### Step 3: Create New Project
```
1. Click "Create New" button
2. Select "GitHub Repo"
3. Select "Sehaat Saathi" repository
4. Railway auto-detects Django
5. Click "Deploy"
```

### Step 4: Configure Environment Variables
```
In Railway Dashboard:

1. Click on Your Project
2. Go to "Variables" tab
3. Add these variables:

SECRET_KEY = (generate new: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG = False
ALLOWED_HOSTS = your-domain.com,www.your-domain.com
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-specific-password
AWS_ACCESS_KEY_ID = your-aws-key
AWS_SECRET_ACCESS_KEY = your-aws-secret
AWS_STORAGE_BUCKET_NAME = your-bucket-name
```

### Step 5: Setup Database
```
1. In Railway Dashboard, click "Add"
2. Select "PostgreSQL"
3. Railway auto-adds DATABASE_URL variable
4. Database is ready!
```

### Step 6: Run Migrations
```
In Railway Dashboard:

1. Click "Deploy" (if not auto-deploying)
2. Click "View Logs" to monitor
3. Once build succeeds, migrations run automatically
4. If not, run:
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
```

### Step 7: Test Your App
```
1. Railway gives you a URL like: sehaat-saathi.railway.app
2. Click the link
3. Your app is live! 🎉
4. Test all features
```

### Step 8: Add Custom Domain (Optional)
```
1. Buy domain from GoDaddy, Namecheap, etc.
2. In Railway: Project → Settings → Domains
3. Add your domain
4. Update DNS records (Railway shows instructions)
5. Wait 24 hours for DNS propagation
```

**Total Time: 10-15 minutes**

---

## 🚀 OPTION 2: HEROKU (CLASSIC)

### Step 1: Install Heroku CLI
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Or use chocolatey:
choco install heroku-cli

# Verify
heroku --version
heroku login  # Opens browser to login
```

### Step 2: Prepare Repository
```bash
cd "c:\Users\DELL\Downloads\Sehaat Saathi Diagnoctic Center"

git init
git add .
git config user.email "your-email@gmail.com"
git config user.name "Your Name"
git commit -m "Initial commit for Heroku"
```

### Step 3: Create Heroku App
```bash
# Create new Heroku app
heroku create sehaat-saathi-app

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Verify DATABASE_URL was created
heroku config | grep DATABASE_URL
```

### Step 4: Set Environment Variables
```bash
heroku config:set SECRET_KEY='your-new-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='sehaat-saathi-app.herokuapp.com,yourdomain.com'
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-app-password'
heroku config:set AWS_ACCESS_KEY_ID='your-key'
heroku config:set AWS_SECRET_ACCESS_KEY='your-secret'
heroku config:set AWS_STORAGE_BUCKET_NAME='your-bucket'

# Verify all variables set
heroku config
```

### Step 5: Deploy
```bash
# Deploy code to Heroku
git push heroku main

# Watch deployment logs
heroku logs --tail

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app in browser
heroku open
```

### Step 6: Monitor and Troubleshoot
```bash
# View logs
heroku logs --tail

# Check free dyno hours remaining
heroku ps

# Restart app if needed
heroku restart

# View errors
heroku logs --source app
```

**Cost**: Starting at $7/month (Eco Dynos)

**Total Time: 20-30 minutes**

---

## 🚀 OPTION 3: PYTHONANYWHERE (EASIEST FOR BEGINNERS)

### Step 1: Create Account
```
1. Go to: https://www.pythonanywhere.com
2. Click "Pricing" → "Start now" (free)
3. Create free account
4. Verify email
```

### Step 2: Upload Your Code
```
1. In Dashboard, go to "Files" tab
2. Click "Upload a file"
3. Zip your project: Right-click → Send to → Compressed folder
4. Upload the ZIP
5. Unzip: In console, "unzip your-file.zip"
```

Or use Git:
```bash
# In PythonAnywhere Bash console:
git clone https://github.com/YOUR-USERNAME/sehaat-saathi.git
cd Sehaat-Saathi
pip install -r requirements.txt
```

### Step 3: Create Web App
```
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Python 3.9"
4. Choose "Django"
5. Point to: /home/username/Sehaat-Saathi/checkup/settings.py
```

### Step 4: Configure WSGI File
```
1. In Web app config, click on WSGI file link
2. Replace content with:

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'checkup.settings'
path = '/home/username/Sehaat-Saathi'
if path not in sys.path:
    sys.path.append(path)

application = get_wsgi_application()
```

### Step 5: Setup Environment Variables
```
1. Create .env file in your app directory
2. Add all required variables:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=username.pythonanywhere.com,yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=sqlite:////home/username/Sehaat-Saathi/db.sqlite3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

### Step 6: Configure Static Files
```
In Web app "Static files" section:

URL: /static/
Directory: /home/username/Sehaat-Saathi/static

Then in Bash console:
cd ~/Sehaat-Saathi
python manage.py collectstatic --noinput
```

### Step 7: Setup Database
```
In Bash console:

python manage.py migrate
python manage.py createsuperuser
```

### Step 8: Reload App
```
1. In Web tab, click "Reload" button
2. Your app is live at: https://username.pythonanywhere.com
3. Admin at: https://username.pythonanywhere.com/admin/
```

**Cost**: Free or $5/month

**Total Time: 20-25 minutes**

---

## 🚀 OPTION 4: RENDER.COM (MODERN)

### Step 1: Create Account
```
1. Go to: https://render.com
2. Sign up with GitHub
3. Authorize GitHub
```

### Step 2: Create Web Service
```
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repo
4. Select Sehaat Saathi repository
```

### Step 3: Configure
```
Name: sehaat-saathi
Environment: Python 3
Build Command:
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

Start Command:
gunicorn checkup.wsgi:application

Instance Type: Free (512MB RAM)
```

### Step 4: Add Environment Variables
```
In Settings → Environment:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=sehaat-saathi.onrender.com,yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=postgresql://...
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

### Step 5: Create Database
```
1. Click "New +"
2. Select "PostgreSQL"
3. Connect to your Web Service
4. Render auto-adds DATABASE_URL
```

### Step 6: Deploy
```
1. Click "Deploy"
2. Render auto-deploys on git push
3. Wait 5-10 minutes for build
4. Your app is live!
```

**Cost**: Free tier (with limitations) or $7/month

**Total Time: 10-15 minutes**

---

## 🚀 OPTION 5: DIGITALOCEAN (FULL CONTROL)

### Step 1: Create Droplet
```
1. Go to: https://www.digitalocean.com
2. Click "Create" → "Droplets"
3. Choose: Ubuntu 22.04 LTS
4. Size: Basic ($6/month)
5. Add SSH key (recommended)
6. Click "Create Droplet"
```

### Step 2: SSH into Server
```powershell
# On Windows, use PuTTY or WSL:
ssh root@your_droplet_ip

# First login password sent via email
# Change password when prompted
```

### Step 3: Setup Environment
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# Create app directory
mkdir /var/www/sehaat-saathi
cd /var/www/sehaat-saathi
git clone https://github.com/YOUR-USERNAME/sehaat-saathi.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL
```bash
# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE sehaat_db;
CREATE USER sehaat_user WITH PASSWORD 'use-a-strong-password';
ALTER ROLE sehaat_user SET client_encoding TO 'utf8';
ALTER ROLE sehaat_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sehaat_user SET default_transaction_deferrable TO on;
ALTER ROLE sehaat_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sehaat_db TO sehaat_user;
\q
```

### Step 5: Update Django Settings
```bash
# Edit settings.py
nano checkup/settings.py

# Update DATABASE section:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sehaat_db',
        'USER': 'sehaat_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Save (Ctrl+X, then Y)
```

### Step 6: Run Migrations
```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Setup Gunicorn
```bash
# Create gunicorn service file
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn application server
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/sehaat-saathi
ExecStart=/var/www/sehaat-saathi/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/sehaat-saathi/gunicorn.sock \
          checkup.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### Step 8: Setup Nginx
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/sehaat
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://unix:/var/www/sehaat-saathi/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/sehaat-saathi/staticfiles/;
    }

    location /media/ {
        alias /var/www/sehaat-saathi/media/;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/sehaat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup HTTPS (SSL)
```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal already configured
```

**Cost**: $6/month

**Total Time: 30-45 minutes**

---

## ✅ POST-DEPLOYMENT VERIFICATION

For ANY deployment choice:

```bash
# 1. Test homepage loads
curl https://yourdomain.com

# 2. Check admin panel
https://yourdomain.com/admin/

# 3. Test API endpoints
curl https://yourdomain.com/api/predictions/

# 4. Check CSS/JS loading
# Check browser console for errors

# 5. Test user registration
# Test disease prediction
# Test appointment booking
# Test email sending

# 6. Check static files
https://yourdomain.com/static/front/neon_theme.css
https://yourdomain.com/static/front/SehaatSaathi.png

# 7. Monitor logs for errors
# Check any 500 errors
# Check database connectivity
```

---

## 🎯 RECOMMENDED DEPLOYMENT ORDER

1. **First Time**: Try Railway or PythonAnywhere (easiest)
2. **Success Verification**: Test all features work
3. **Custom Domain**: Add your domain name
4. **Scale Up**: Move to DigitalOcean if needed

---

## 💡 QUICK REFERENCE COMMANDS

```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Test Django settings
python manage.py check

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Django shell
python manage.py shell

# Check environment variables
# Linux/Mac: env | grep DEBUG
# Windows: set
```

---

**You're all set to deploy! Choose your platform and follow the steps.** 🚀
