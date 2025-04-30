import os
import requests

def send_simple_message():
    # Your Mailgun API Key (use the one you just found)
    api_key = "dc98b46572b4b7f0958ca762ed3a26bb-67bd41c2-38f2d24a"  # Your API key
    domain = "sandbox0c3f6cd80fbf4f91aba9d94eed5cf5fd.mailgun.org"  # Your sandbox domain

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Mailgun Sandbox <postmaster@{domain}>",
            "to": "Bhushan Acharekar <bhushanacharekar1725@gmail.com>",  # Replace with recipient email
            "subject": "Hello Kazuki",
            "text": "Congratulations Kazuki, you just sent an email with Mailgun! You are truly awesome!"
        }
    )

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage
send_simple_message()
