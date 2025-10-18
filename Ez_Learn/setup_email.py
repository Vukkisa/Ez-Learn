#!/usr/bin/env python3
"""
Quick Email Setup Script for Ez-Learn
Run this script to test and configure email settings
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ez_Learn.settings')
django.setup()

def setup_email():
    print("🔧 Ez-Learn Email Configuration Setup")
    print("=" * 50)
    
    # Get current settings
    from django.conf import settings
    print(f"Current EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"Current EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"Current EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD configured: {bool(settings.EMAIL_HOST_PASSWORD)}")
    print()
    
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        print("✅ Email credentials are configured!")
        print("Let's test sending an email...")
        
        # Test email sending
        from website.views import sending_mail
        test_email = input("Enter your email address to test: ").strip()
        if test_email:
            result = sending_mail("Test email from Ez-Learn setup", "123456", test_email)
            if result:
                print("✅ Test email sent successfully!")
            else:
                print("❌ Test email failed. Check the error messages above.")
    else:
        print("⚠️ Email credentials are not configured.")
        print("\nTo configure email, set these environment variables:")
        print("export EMAIL_HOST_USER=\"your-email@gmail.com\"")
        print("export EMAIL_HOST_PASSWORD=\"your-app-password\"")
        print()
        print("For Gmail setup:")
        print("1. Enable 2-factor authentication on your Google account")
        print("2. Generate an App Password (not your regular password)")
        print("3. Use that App Password in EMAIL_HOST_PASSWORD")
        print()
        
        # Let's try to set up Gmail interactively
        setup_gmail = input("Would you like to set up Gmail now? (y/n): ").strip().lower()
        if setup_gmail == 'y':
            gmail_user = input("Enter your Gmail address: ").strip()
            gmail_password = input("Enter your Gmail App Password: ").strip()
            
            if gmail_user and gmail_password:
                # Set environment variables for this session
                os.environ['EMAIL_HOST_USER'] = gmail_user
                os.environ['EMAIL_HOST_PASSWORD'] = gmail_password
                
                print("Testing Gmail configuration...")
                from website.views import sending_mail
                test_result = sending_mail("Gmail test from Ez-Learn", "999999", gmail_user)
                if test_result:
                    print("✅ Gmail configuration successful!")
                    print(f"Add these to your environment or .env file:")
                    print(f"EMAIL_HOST_USER={gmail_user}")
                    print(f"EMAIL_HOST_PASSWORD={gmail_password}")
                else:
                    print("❌ Gmail test failed. Please check your credentials.")

if __name__ == "__main__":
    setup_email()
