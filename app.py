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
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Example route to create an order (payment request)
@app.route("/create_order", methods=["POST"])
def create_order():
    access_token = get_paypal_access_token()
    url = "https://api.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "10.00"  # The price of the product
            }
        }]
    }
    response = requests.post(url, json=data, headers=headers)
    order = response.json()
    return jsonify(order)

if __name__ == "__main__":
    app.run(debug=True)
