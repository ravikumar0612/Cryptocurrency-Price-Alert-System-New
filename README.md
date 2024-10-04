# Crypto Price Alert System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Code Explanation](#code-explanation)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [Future Improvements](#future-improvements)
8. [Screen Shots](#Screen-Shots)
9. [Report of Brief: Adopted, Challenges](#Report-of-Brief-Adopted-Challenges)

## 1. System Overview
The Crypto Price Alert System is a Flask-based web application that allows users to set price alerts for various cryptocurrencies. When the price of a cryptocurrency crosses a user-defined threshold, the system sends an email alert to the user.

Key features:
- Set upper and lower price bounds for cryptocurrencies
- Periodic checking of cryptocurrency prices
- Email notifications when price thresholds are crossed
- Web interface for setting alerts

## 2. Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- A Gmail account for sending email alerts

## 3. Setup Instructions
1. Clone the repository or create a new directory for the project in Vs Code.
      ```
   Steps 1. Open VS Code

   Steps 2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) to open the Command Palette

   Steps 3. Type "Git: Clone" and select it

   Steps 4. Paste the GitHub repository URL and press Enter

   Steps 5. Choose a local folder for the cloned repository

   Steps 6. Click "Open" when prompted to open the cloned repository

   You're done! The repository is now cloned and open in VS Code.
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install required packages:
   ```
   pip install flask apscheduler requests python-dotenv
   ```
4. Create a `.env` file in the project root directory with the following content:
   ```
   EMAIL_USERNAME=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```
   Replace `your_email@gmail.com` with your Gmail address and `your_app_password` with an App Password generated for your Gmail account.
5. To generate an App Password for your Gmail account:
   - Go to your Google Account settings
   - Navigate to Security
   - Enable 2-Step Verification if not already enabled
   - Go back to Security and look for "App passwords"
   - Generate a new App password for your application
6. Create a file named `app.py` and copy the provided Python code into it.
7. Create a `templates` folder in the project directory and add an `index.html` file for the web interface.

## 4. Code Explanation

### Imports and Configuration
The key change here is in the import statement. We've replaced:

```python
from requests.packages.urllib3.util.retry import Retry
```

with:

```python
from urllib3.util.retry import Retry
```

This change reflects the current structure of the `urllib3` library, which is a dependency of `requests` but is now imported directly rather than through the `requests.packages` namespace.

To ensure everything works correctly, you may need to update your `requests` and `urllib3` libraries. You can do this by running:

```
pip install --upgrade requests urllib3
```

This will update both libraries to their latest versions, ensuring compatibility.

After making these changes, the "Import could not be resolved" error should be resolved. The rest of your code can remain the same, as the `Retry` class is used in the same way regardless of how it's imported.

If you encounter any other import issues or if Pylance is still showing warnings, you might want to check your Python environment and make sure all the required packages are installed correctly. You can do this by creating a `requirements.txt` file with all your dependencies and then installing them:

1. Create a `requirements.txt` file with the following content:

   ```
   flask
   apscheduler
   requests
   python-dotenv
   urllib3
   ```

2. Install all dependencies:

   ```
   pip install -r requirements.txt
   ```

This should ensure that all necessary packages are installed and up to date. After these steps, your script should run without any import errors.

The `app.py` file contains the main application code. Here's a breakdown of its key components:

### Imports and Configuration
- Flask for the web framework
- APScheduler for scheduling periodic tasks
- Requests for making HTTP requests to the cryptocurrency API
- Logging for error tracking and debugging
- python-dotenv for loading environment variables

### Global Variables
- `alerts`: A dictionary to store user-set alerts (in a production environment, this should be replaced with a database)
- `session`: A requests Session object configured with retries for improved reliability

### Functions
- `get_crypto_price(crypto_symbol)`: Fetches the current price of a given cryptocurrency from the CoinGecko API
- `send_email_alert(recipient, subject, body)`: Sends an email alert using the configured SMTP server
- `check_alerts()`: Periodically checks cryptocurrency prices against user-set alerts and sends notifications if thresholds are crossed

### Flask Routes
- `/`: Renders the main page
- `/set_alert`: Handles POST requests to set new alerts

### Main Execution
- Checks for proper configuration of environment variables
- Sets up the APScheduler to run `check_alerts()` every 5 minutes
- Starts the Flask application

## 5. Usage Guide
1. Start the application:
   ```
   python app.py
   ```
2. Open a web browser and navigate to `http://localhost:5000`
3. Use the web interface to set alerts by providing:
   - Cryptocurrency symbol (e.g., "bitcoin")
   - Upper price bound
   - Lower price bound
   - Email address for notifications
4. The system will check prices every 5 minutes and send email alerts when thresholds are crossed.

## 6. Troubleshooting
### Email Sending Issues
- Ensure your `.env` file contains the correct Gmail address and App Password
- Check that 2-Step Verification is enabled for your Google account
- Verify that the App Password is correctly generated and copied
- Review the application logs for specific error messages

### Incorrect Alert Thresholds
- Ensure that the upper bound is always set higher than the lower bound
- Verify that the frontend is sending correct values to the backend
- Check the `set_alert` function for proper validation of input values

### API Rate Limiting
- If you encounter rate limiting from the CoinGecko API, consider implementing caching or using a paid API plan for higher limits
...

## 7. Future Improvements
- Implement a database for storing alerts instead of in-memory storage
- Add user authentication to allow users to manage their own alerts
- Implement a more robust frontend with JavaScript for better user experience
- Add support for more cryptocurrencies and multiple fiat currencies
- Implement webhook notifications in addition to email alerts
- Add unit tests and integration tests for improved reliability

## 8. Screen Shots
   - # Backend Crypto Price Alert System Documentation
   - ![Backend Crypto Price Alter System](https://github.com/user-attachments/assets/620de5e8-52ea-4eac-8f98-0ec761f588a6)

     - # Frontend Crypto Price Alert System Documentation
     - ![Fontend Crypto Price Alter System](https://github.com/user-attachments/assets/91c5bb5f-420e-452e-80e9-49e96a95ad18)
    
     - # Result Crypto Price Alert System Documentation
     - ![Output Crypto Price Alter System](https://github.com/user-attachments/assets/1cc81774-b386-4994-901d-ef8419898be8)

## 9. Report of Brief: Adopted, Challenges
-  However, in making the Crypto Price Alert System, I wanted to create for an easy to use service where users can manage and monitor these cryptocurrency prices of their choice and get alerted if price crosses a user defined threshold. I used Flask for the web interface and APScheduler to periodically check the prices. I used the CoinGecko API to grab real-time data on crypto pricing and sent email alerts through SMTP with Gmail. The library project also uses Python's requests library for making reliable http requests, and has built-in automatic retries and error handling for robustness.
-  One of the main difficulties was to perform an efficient periodic price checking however keep the system responsive. To that end, they put APScheduler to use as a timed tasks handler and started checking current prices of animals every 5 minutes without locking the main application. Setting up the email alert system also had some initial hurdles in getting it to work with Gmail's 2-step verification and security settings, but we ultimately got that working too by using the python-dotenv library for storing the email credentials in a secure way. We notice that the system is well able to fulfill its objectives with respect to monitoring prices (triggering alerts) but there can still be areas of improvement like a more sophisticated frontend and an option for notification over various media.
