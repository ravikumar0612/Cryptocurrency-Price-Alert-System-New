import os
import logging
import requests
from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("EMAIL_USERNAME")
SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("EMAIL_USERNAME")

# Store alerts in memory (in a real application, you'd use a database)
alerts = {}

# Configure requests session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def get_crypto_price(crypto_symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data[crypto_symbol]['usd']
        logger.debug(f"Fetched price for {crypto_symbol}: ${price}")
        return price
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching price for {crypto_symbol}: {str(e)}")
        return None

def send_email_alert(recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    try:
        logger.info(f"Attempting to send email to {recipient}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            logger.info(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
            server.starttls()
            logger.info(f"Attempting to login with username: {SMTP_USERNAME}")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            logger.info("Login successful")
            server.send_message(msg)
            logger.info(f"Email alert sent to {recipient}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")

def check_alerts():
    logger.info("Starting to check alerts")
    logger.debug(f"Current alerts: {alerts}")
    for crypto_symbol, alert_data in alerts.items():
        current_price = get_crypto_price(crypto_symbol)
        if current_price is not None:
            for alert in alert_data:
                logger.debug(f"Checking alert for {crypto_symbol}: current price ${current_price}, upper bound ${alert['upper_bound']}, lower bound ${alert['lower_bound']}")
                if current_price > alert['upper_bound']:
                    alert_message = f"Alert: {crypto_symbol} price (${current_price}) is above ${alert['upper_bound']}"
                    logger.info(alert_message)
                    send_email_alert(alert['email'], "Crypto Price Alert", alert_message)
                elif current_price < alert['lower_bound']:
                    alert_message = f"Alert: {crypto_symbol} price (${current_price}) is below ${alert['lower_bound']}"
                    logger.info(alert_message)
                    send_email_alert(alert['email'], "Crypto Price Alert", alert_message)
    logger.info("Finished checking alerts")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_alert', methods=['POST'])
def set_alert():
    data = request.json
    logger.info(f"Received alert request: {data}")
    crypto_symbol = data['crypto_symbol'].lower()
    upper_bound = float(data['upper_bound'])
    lower_bound = float(data['lower_bound'])
    
    if upper_bound <= lower_bound:
        logger.warning(f"Invalid alert bounds: upper {upper_bound}, lower {lower_bound}")
        return jsonify({"status": "error", "message": "Upper bound must be greater than lower bound"}), 400
    
    if crypto_symbol not in alerts:
        alerts[crypto_symbol] = []
    alerts[crypto_symbol].append({
        'upper_bound': upper_bound,
        'lower_bound': lower_bound,
        'email': data['email']
    })
    logger.info(f"New alert set for {crypto_symbol}: Upper bound ${upper_bound}, Lower bound ${lower_bound}")
    logger.debug(f"Current alerts: {alerts}")
    return jsonify({"status": "success"})

@app.route('/test_email')
def test_email():
    try:
        send_email_alert(SMTP_USERNAME, "Test Email", "This is a test email from your Render app")
        return 'Email sent successfully'
    except Exception as e:
        logger.error(f"Error in test_email: {str(e)}")
        return f'Error sending email: {str(e)}'

if __name__ == '__main__':
    # Check if environment variables are set
    if not all([SMTP_USERNAME, SMTP_PASSWORD]):
        logger.error("SMTP credentials not set. Please check your .env file.")
        exit(1)
    
    logger.info(f"Email username: {SMTP_USERNAME}")
    logger.info(f"Email password is set: {'Yes' if SMTP_PASSWORD else 'No'}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_alerts, trigger="interval", seconds=30)
    scheduler.start()

    app.logger.info("Starting the Flask app on Render...")
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)