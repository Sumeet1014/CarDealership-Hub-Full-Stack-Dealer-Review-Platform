import sys
path='dealership/settings.py'
with open(path) as f:
    s=f.read()
if 'corsheaders' not in s and 'import os' not in s:
    s = s.replace('from pathlib import Path\n', 'from pathlib import Path\nimport os\n')
old = \"INSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n]\"
new = \"INSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'rest_framework',\n    'corsheaders',\n    'api',\n    'dealership_app',\n]\"
if old in s and 'api' not in s:
    s=s.replace(old,new)
oldm = \"MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.middleware.common.CommonMiddleware',\n    'django.middleware.csrf.CsrfViewMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware',\n    'django.contrib.messages.middleware.MessageMiddleware',\n    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n]\"
newm = \"MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',\n    'django.middleware.security.SecurityMiddleware',\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.middleware.common.CommonMiddleware',\n    'django.middleware.csrf.CsrfViewMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware',\n    'django.contrib.messages.middleware.MessageMiddleware',\n    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n]\"
if 'corsheaders.middleware' not in s:
    s=s.replace(oldm,newm)
s=s.replace(\"ALLOWED_HOSTS = []\", \"ALLOWED_HOSTS = ['*']\")
if 'CORS_ALLOW_ALL_ORIGINS' not in s:
    s += \"\n\nCORS_ALLOW_ALL_ORIGINS = True\nCORS_ALLOW_CREDENTIALS = True\n\nREST_FRAMEWORK = { 'DEFAULT_AUTHENTICATION_CLASSES': [] }\n\nSTATIC_URL = '/static/'\nSTATIC_ROOT = BASE_DIR / 'staticfiles'\nMEDIA_URL = '/media/'\nMEDIA_ROOT = BASE_DIR / 'media'\n\"
with open(path,'w') as f:
    f.write(s)
print('done')
