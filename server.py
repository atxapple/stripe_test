import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ---------------------------------------
# ROUTES
# ---------------------------------------

@app.route("/")
def home():
    return "Stripe Backend is running!"

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json()
    price_id = data.get("price_id", PRICE_6_MONTH)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {"price": price_id, "quantity": 1}
            ],
            success_url="https://google.com",
            cancel_url="https://google.com",
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify(error=str(e)), 400

# ---------------------------------------
# WEBHOOK HANDLER
# ---------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except Exception as e:
        print("❌ Webhook signature error:", e)
        return "Bad signature", 400

    # Log event type
    print(f"🔔 Received event: {event['type']}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("🎉 Payment succeeded!")
        print("Customer:", session.get("customer_details"))
        print("Amount:", session.get("amount_total"))

    return "OK", 200

# ---------------------------------------
# START SERVER (Railway compatible)
# ---------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4242))
    app.run(host="0.0.0.0", port=port)
