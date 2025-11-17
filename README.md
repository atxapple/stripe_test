# Stripe Backend (Railway Deployment)

This is a minimal production-ready Stripe backend for Railway.

## Features
- Checkout session creation
- Stripe webhooks (production HTTPS)
- Railway-ready (gunicorn + dynamic PORT)
- CORS enabled
- REST API for front-end consumption

---

## 🚀 Deployment Steps

### 1. Add environment variables in Railway:
- `STRIPE_SECRET_KEY=sk_test_xxx`
- `STRIPE_WEBHOOK_SECRET=whsec_xxx`
- `PRICE_6_MONTH=price_xxx`
- `PRICE_1_MONTH=price_xxx`

### 2. Deploy to Railway
- Push this repo to GitHub
- Create a Railway project
- Connect GitHub repo
- Deploy

### 3. Set up Stripe Webhook
In Stripe Dashboard → Developers → Webhooks:

Add this endpoint:

https://<railway-app-url>.railway.app/webhook


Subscribe to:
- checkout.session.completed
- payment_intent.succeeded
- payment_intent.payment_failed

---

## API Endpoints

### POST /create-checkout-session
Create a payment session.

Body:
```json
{
  "price_id": "price_xxx"
}

{
  "url": "https://checkout.stripe.com/..."
}