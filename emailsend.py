import requests
from flask import current_app as app

def send_email_otp(to_email, otp):
    """
    Send OTP to the user's email via Mailgun.
    """
    MAILGUN_API_KEY = app.config["MAILGUN_API_KEY"]
    MAILGUN_DOMAIN = app.config["MAILGUN_DOMAIN"]

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"MockBank <postmaster@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": "Your MockBank OTP",
            "text": f"Your OTP is {otp}. It is valid for 5 minutes."
        }
    )
    return response
