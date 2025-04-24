import requests
import os
from flask import Flask, request, jsonify, render_template
from config import PLAN_PRICING, DevelopmentConfig, ProductionConfig

app = Flask(__name__)

# Dynamically select the config based on an env var or default to dev
if os.getenv("FLASK_ENV") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Get PayPal access token
def get_paypal_access_token():
    try:
        url = f"{app.config['PAYPAL_BASE_URL']}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        auth = (app.config['PAYPAL_CLIENT_ID'], app.config['PAYPAL_SECRET'])

        response = requests.post(url, headers=headers, data=data, auth=auth)
        response.raise_for_status()
        return response.json().get('access_token')

    except requests.RequestException as e:
        print(f"PayPal token error: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html", paypal_client_id=app.config['PAYPAL_CLIENT_ID'])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/env-check")
def env_check():
    return {
        "FLASK_ENV": os.getenv("FLASK_ENV"),
        "PAYPAL_CLIENT_ID": os.getenv("app.config['PAYPAL_CLIENT_ID']"),
        "CONFIG_CLASS": str(type(app.config))
    }

@app.route("/create_order", methods=["POST"])
def create_order():

    data = request.get_json()
    plan = data.get("plan")

    if plan not in PLAN_PRICING:
        return jsonify({"error": "Invalid plan selected."}), 400

    access_token = get_paypal_access_token()
    if not access_token:
        return jsonify({"error": "Failed to authenticate with PayPal."}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "description": PLAN_PRICING[plan]["description"],
            "amount": {
                "currency_code": "USD",
                "value": PLAN_PRICING[plan]["value"]
            }
        }]
    }

    url = f"{app.config['PAYPAL_BASE_URL']}/v2/checkout/orders"
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)

