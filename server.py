import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")  # MUST be set in Railway

@app.route("/")
def home():
    return "Stripe backend is running."

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.get_json()

        if not data or "price_id" not in data:
            return jsonify({"error": "Missing price_id"}), 400

        price_id = data["price_id"]

        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            success_url="https://google.com",
            cancel_url="https://google.com",
        )

        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import json

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        print("❌ Webhook signature failed:", str(e))
        return "Webhook signature failed", 400

    print("\n🎉 Webhook received:", event["type"])
    print("──────────────────────────────────────────────")
    print(json.dumps(event, indent=4))
    print("──────────────────────────────────────────────\n")

    # Optional: handle specific events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("Checkout Session ID:", session["id"])
        print("Customer Email:", session.get("customer_details", {}).get("email"))
        print("Payment Status:", session["payment_status"])
        print("Amount Total:", session["amount_total"])
        print("Currency:", session["currency"])

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
