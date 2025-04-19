import requests
from flask import Flask, request, jsonify, render_template
from config import PAYPAL_SECRET, PAYPAL_CLIENT_ID

app = Flask(__name__)

# Get PayPal access token
def get_paypal_access_token():
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    response = requests.post(url, headers=headers, data=data, auth=auth)
    return response.json().get('access_token')

@app.route("/")
def index():
    return render_template("index.html", paypal_client_id=PAYPAL_CLIENT_ID)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.get_json()
    plan = data.get("plan")

    # Plan prices hardcoded server-side (secure)
    plan_pricing = {
        "standard": {"description": "Standard Plan Subscription", "value": "0.99"},
        "premium": {"description": "Premium Plan Subscription", "value": "4.99"},
        "business": {"description": "Business Plan Subscription", "value": "9.99"},
    }

    if plan not in plan_pricing:
        return jsonify({"error": "Invalid plan selected."}), 400

    access_token = get_paypal_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "description": plan_pricing[plan]["description"],
            "amount": {
                "currency_code": "USD",
                "value": plan_pricing[plan]["value"]
            }
        }]
    }

    url = "https://api.sandbox.paypal.com/v2/checkout/orders"
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
