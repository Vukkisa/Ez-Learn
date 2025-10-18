# Payment Gateway Configuration Guide

## Razorpay Setup

### 1. Get Razorpay API Keys

1. Visit [Razorpay Dashboard](https://dashboard.razorpay.com/app/keys)
2. Create an account or log in
3. Go to **Settings > API Keys**
4. Generate API Keys:
   - For testing: Use **Test Mode** keys (start with `rzp_test_`)
   - For production: Use **Live Mode** keys (start with `rzp_live_`)

### 2. Quick Setup (RECOMMENDED)

**Option A: Direct Configuration in settings.py**

1. Open `Ez_Learn/Ez_Learn/settings.py`
2. Find the section `# DIRECT RAZORPAY CONFIGURATION`
3. Replace the empty strings with your Razorpay keys:

```python
RAZORPAY_KEY_ID_DIRECT = "rzp_test_your_key_id_here"  # Your test key ID
RAZORPAY_KEY_SECRET_DIRECT = "your_test_secret_here"  # Your test secret
```

4. Restart your Django server

**Option B: Environment Variables**

Create a `.env` file in the project root with:

```bash
# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_your_key_id_here
RAZORPAY_KEY_SECRET=your_secret_key_here

# Optional: Webhook secret for production
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret_here
```

### 3. Django Settings

The payment gateway is configured in `settings.py` with automatic fallbacks:

```python
# Direct configuration (takes priority if set)
RAZORPAY_KEY_ID_DIRECT = "rzp_test_your_key_id_here"
RAZORPAY_KEY_SECRET_DIRECT = "your_test_secret_here"

# Environment variables (production recommended)
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID") or RAZORPAY_KEY_ID_DIRECT
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET") or RAZORPAY_KEY_SECRET_DIRECT

# Auto-initialized client
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
```

### 4. Features Included

✅ **Order Creation**: Automatic Razorpay order generation
✅ **Payment Verification**: Signature verification for security
✅ **Error Handling**: Fallback modes for different scenarios
✅ **Development Mode**: Test payments without real gateway
✅ **Multiple Payment Methods**: Cards, Net Banking, UPI, Wallets
✅ **Webhook Support**: Ready for production webhooks

### 5. Testing

#### Development Mode
- Without Razorpay keys: Uses development orders (can be marked as paid in UI)
- Test keys: Full Razorpay integration with sandbox

#### Production Mode
- Live Razorpay keys required
- Automatic signature verification
- Real payment processing

### 6. Security Features

- ✅ Signature verification using HMAC SHA256
- ✅ CSRF protection
- ✅ Secure environment variable handling
- ✅ Error logging and monitoring
- ✅ Development/production mode detection

### 7. Payment Flow

1. User clicks "Purchase to Access" → Enhanced purchase page
2. User confirms payment → Razorpay order created
3. User completes payment → Razorpay gateway redirects back
4. Payment verification → Signature validation
5. Course access activated → User gains premium access

### 8. Troubleshooting

**Issue**: Payment gateway not configured
**Solution**: Set `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` environment variables

**Issue**: Signature verification failed
**Solution**: Ensure webhook secret matches Razorpay dashboard

**Issue**: Development orders not working
**Solution**: Check console logs for order creation status

### 9. Production Checklist

- [ ] Replace test keys with live keys
- [ ] Set up webhook endpoint for real-time updates
- [ ] Configure proper error handling and logging
- [ ] Test payment flow end-to-end
- [ ] Set up monitoring for failed payments
