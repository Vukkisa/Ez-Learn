#!/usr/bin/env python3
"""
Quick Email Test Script for Ez-Learn
Run this after setting EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent / 'Ez_Learn'
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ez_Learn.settings')
django.setup()

def test_email_setup():
    print("🧪 Ez-Learn Email Configuration Test")
    print("=" * 50)
    
    from django.conf import settings
    
    # Check configuration
    print("📧 Configuration Status:")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or 'NOT SET'}")
    print(f"  EMAIL_HOST_PASSWORD: {'SET' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print()
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("❌ EMAIL CREDENTIALS NOT CONFIGURED!")
        print("\n🔧 TO FIX, run these commands:")
        print("export EMAIL_HOST_USER='your-gmail@gmail.com'")
        print("export EMAIL_HOST_PASSWORD='your-app-password'")
        print("python manage.py runserver")
        return False
    
    # Test email sending
    print("📤 Testing email sending...")
    from website.views import sending_mail
    
    test_email = input("Enter email address to test with: ").strip()
    if not test_email:
        test_email = settings.EMAIL_HOST_USER  # Use same email if no input
    
    print(f"Sending test email to: {test_email}")
    result = sending_mail("Ez-Learn Email Test", "999999", test_email)
    
    if result == True:
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print(f"Check {test_email} for the test email with OTP: 999999")
        return True
    elif result == "console":
        print("⚠️ Email sent to console fallback")
        print("This means SMTP failed but console worked")
        return False
    else:
        print("❌ EMAIL SENDING FAILED")
        return False

if __name__ == "__main__":
    test_email_setup()
