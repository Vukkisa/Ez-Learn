# 📧 Email Configuration Guide for Ez-Learn

This guide helps you configure email sending for OTP verification in the Ez-Learn application.

## 🚨 IMPORTANT: Getting OTPs in Your Email

**To receive OTP emails in your actual email inbox**, you need to configure email credentials.

## 🚀 Quick Setup (Get Real Emails Working)

### Step 1: Gmail Setup (Recommended)
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Create a new app password for "Django"
   - Copy the 16-character password (like: `abcd efgh ijkl mnop`)

### Step 2: Configure Email Credentials
Run these commands in your terminal:

```bash
# Navigate to your project directory
cd /Users/vj/Desktop/Ez-Learn/Ez_Learn

# Set your email credentials (replace with your actual email)
export EMAIL_HOST_USER="your-gmail@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-character-app-password"

# Restart your Django server
python manage.py runserver
```

### Step 3: Test Email Sending
Use the setup script to test:
```bash
python ../setup_email.py
```

## 🔧 Alternative: Quick Environment File Setup

Create a `.env` file in your `Ez_Learn` directory:
```bash
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Then update your settings to load from `.env` file (optional but recommended).

## ⚠️ Current Development Mode

**Right now**, Ez-Learn is using console fallback because email credentials aren't configured.
- OTPs are shown in the Django console: `🔐 OTP for user@example.com: 123456`
- This works for testing but emails don't reach your inbox

## 📧 Production Email Setup

### Option 1: Gmail SMTP (Recommended for Development)

1. **Get Gmail App Password**:
   - Go to your Google Account settings
   - Enable 2-factor authentication
   - Generate an "App Password" for Django
   - Use this app password instead of your regular password

2. **Set Environment Variables**:
   ```bash
   export EMAIL_HOST_USER="your-gmail@gmail.com"
   export EMAIL_HOST_PASSWORD="your-app-password"
   export EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
   ```

### Option 2: Other SMTP Services

For services like Outlook, Yahoo, or custom SMTP:

```bash
export EMAIL_HOST="smtp.your-provider.com"
export EMAIL_PORT="587"  # or 465 for SSL
export EMAIL_HOST_USER="your-email@domain.com"
export EMAIL_HOST_PASSWORD="your-password"
export EMAIL_USE_TLS="True"
export EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
```

### Option 3: File-based Email (Development)

Save emails to files instead of sending:

```bash
export EMAIL_BACKEND="django.core.mail.backends.filebased.EmailBackend"
export EMAIL_FILE_PATH="/tmp/ez-learn-emails"
```

## 🐛 Troubleshooting

### Error: "Failed to send OTP"
This usually means:
1. **Email credentials not set**: Make sure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are configured
2. **Network issues**: Check your internet connection
3. **Firewall**: Ensure port 587 or 465 is not blocked

### For Development:
- Check the console output - the OTP is always displayed there
- The registration will still work even if email sending fails
- You can use the OTP from the console to complete registration

## 🔧 Current Configuration Status

Check your current email configuration by running:
```bash
cd Ez_Learn && python manage.py shell
>>> from django.conf import settings
>>> print(f"Email backend: {settings.EMAIL_BACKEND}")
>>> print(f"Email host: {settings.EMAIL_HOST}")
>>> print(f"Email user configured: {bool(settings.EMAIL_HOST_USER)}")
```

## 📱 Quick Test

1. Try registering a new user
2. Check the console output for the OTP
3. Use that OTP to complete registration

The system is designed to work even without email configuration, making development and testing easier!
