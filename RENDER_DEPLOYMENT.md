# 🚀 Render Deployment Guide for Ez-Learn

## Prerequisites
1. GitHub repository with your code
2. Render account (sign up at https://render.com)
3. Razorpay account for payments (optional for testing)

## Step-by-Step Deployment

### 1. Prepare Your Repository
Make sure your code is committed and pushed to GitHub with these files:
- `requirements.txt` ✅
- `Procfile` ✅
- `runtime.txt` ✅
- `.gitignore` ✅
- `Ez_Learn/settings.py` (updated for Render) ✅

### 2. Create Render Account & Web Service

1. **Sign up** at https://render.com using your GitHub account
2. **Click** "New +" → "Web Service"
3. **Connect** your GitHub repository
4. **Select** your Ez-Learn repository

### 3. Configure Render Settings

**Basic Settings:**
- **Name**: `ez-learn-app` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your main branch)

**Build & Deploy Settings:**
- **Root Directory**: `/Ez_Learn` (important!)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: (Leave empty - uses Procfile)

**Instance Type:**
- Start with **Free** tier for testing
- Upgrade to **Starter** ($7/month) for production use

### 4. Environment Variables

Add these environment variables in Render dashboard:

#### Required Variables:
```
SECRET_KEY=your-unique-secret-key-here-very-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

#### Database (Optional - Render provides PostgreSQL):
```
DATABASE_URL=postgresql://... # Auto-provided by Render
```

#### Email Configuration:
```
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

#### Razorpay (for payments):
```
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_test_secret
```

### 5. Database Setup

**Option A: Free PostgreSQL (Recommended)**
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it `ez-learn-db`
3. Copy the `DATABASE_URL` and set it as environment variable
4. Render will automatically run migrations on deploy

**Option B: SQLite (Free but limited)**
- No additional setup needed
- Uses the built-in SQLite database

### 6. Deploy

1. **Click** "Create Web Service"
2. **Wait** for build to complete (5-10 minutes)
3. **Check** build logs for any errors
4. **Visit** your app at `https://your-app-name.onrender.com`

## Post-Deployment Steps

### 1. Create Admin User
If your app includes Django admin, you'll need to create a superuser:
1. In Render dashboard, go to your service
2. Click "Shell" tab
3. Run: `python manage.py createsuperuser`

### 2. Test Your Application
- ✅ Homepage loads
- ✅ User registration works
- ✅ Admin panel accessible
- ✅ Payments work (if configured)
- ✅ Static files load properly

### 3. Custom Domain (Optional)
1. In Render dashboard, go to your service
2. Click "Settings" → "Custom Domains"
3. Add your domain and follow DNS instructions

## Troubleshooting

### Common Issues:

**Build Fails:**
- Check `requirements.txt` syntax
- Ensure all dependencies are listed
- Check build logs for specific errors

**Static Files Not Loading:**
- Verify WhiteNoise is installed and configured
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Run `python manage.py collectstatic` in shell

**Database Issues:**
- Ensure `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Verify migrations ran successfully

**Email Not Working:**
- Verify email credentials in environment variables
- Check Gmail app password setup
- Test email sending in shell

### Environment Variables Reference:

```bash
# Security
SECRET_KEY=your-secret-key
DEBUG=False

# Hosts
ALLOWED_HOSTS=your-app.onrender.com

# Database (Render auto-provides)
DATABASE_URL=postgresql://user:pass@host:port/db

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Razorpay
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=your-secret
```

## Cost Estimation

**Free Tier:**
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- SQLite database
- Perfect for testing and small projects

**Starter Plan ($7/month):**
- Always-on
- 0.1 CPU, 256MB RAM
- PostgreSQL database included
- Custom domains

**Standard Plan ($25/month):**
- 0.5 CPU, 512MB RAM
- Better performance
- Multiple environments

## Security Notes

⚠️ **Important Security Updates:**
1. Never commit sensitive data to Git
2. Use strong, random `SECRET_KEY`
3. Enable HTTPS (Render does this automatically)
4. Keep dependencies updated
5. Use environment variables for all secrets

## Support

If you encounter issues:
1. Check Render build/deploy logs
2. Review Django logs in Render dashboard
3. Test locally with production settings
4. Consult Render documentation: https://render.com/docs

---

**Good luck with your deployment! 🚀**
