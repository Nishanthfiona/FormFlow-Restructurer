import requests
from flask import Flask, request, jsonify
import re
import html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Define your secret token for authentication (keep this secret)
SECRET_TOKEN = ""

# Define your CRM Authorization Token
CRM_AUTH_TOKEN = ""

# Define your CRM URL
CRM_URL = ""  # Replace with your actual CRM API endpoint URL

# Email configuration
SMTP_SERVER = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_FROM = ""
EMAIL_TO = ""

def send_email(subject, message, is_html=False):
    try:
        # Create a connection to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        if is_html:
            # If it's an HTML email, set the content type and attach the HTML message
            msg.attach(MIMEText(message, 'html'))
        else:
            # Plain text email
            msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        # Close the SMTP server connection
        server.quit()
    except Exception as e:
        print("Failed to send email:", str(e))

def sanitize_data(input_data):
    # Implement sanitization logic here
    # Remove HTML tags and escape HTML special characters
    sanitized_data = html.escape(re.sub(r'<[^>]+>', '', input_data))
    return sanitized_data.strip()

def format_data(data):
    # Extract and clean the fields from the JSON data
    custom_field_courses = sanitize_data(data.get('cf_courses', ''))
    first_name = sanitize_data(data.get('first_name', ''))
    mobile_number = sanitize_data(data.get('mobile_number', ''))
    emails = sanitize_data(data.get('emails', ''))
    phone_numbers = sanitize_data(data.get('phone_numbers', ''))
    cf_age_range = sanitize_data(data.get('cf_age_range', ''))
    cf_message = sanitize_data(data.get('cf_message', ''))
    ip = sanitize_data(data.get('ip', ''))
    page = sanitize_data(data.get('page', ''))
    lead_source_id = sanitize_data(data.get('lead_source_id', ''))
    cf_status_of_lead = sanitize_data(data.get('cf_status_of_lead', ''))

    # Reformat the extracted data as needed
    reformatted_data = {
        'unique_identifier': {
            'emails': emails,
        },
        'contact': {
            'first_name': first_name,
            'mobile_number': mobile_number,
            'phone_numbers': phone_numbers,
            'lead_source_id': lead_source_id,
        
        'custom_field': {
            'cf_age_range': cf_age_range,
            
            'cf_courses': custom_field_courses,
            'cf_message': cf_message,
            'cf_status_of_lead': cf_status_of_lead,
        },
        'ip': ip,
        'page': page,
        'status_of_api': 'success',
        },
    }

    return reformatted_data

def generate_html_error_message(error_data):
    try:
        # Try to parse error_data as a dictionary
        error_data_dict = eval(error_data)

        # Check if error_data_dict is a dictionary
        if isinstance(error_data_dict, dict):
            # Extract the 'contact' and 'custom_field' dictionaries
            contact_data = error_data_dict.get('contact', {})
            custom_field_data = error_data_dict.get('custom_field', {})

            # Create a formatted HTML message without quotes and curly braces
            error_message = f"""
<html>
  <body>
    <p>Failed to send data to CRM</p>
    <p>Data:</p>
    <pre>
      'contact': {{
        'first_name': {contact_data.get('first_name', '')},
        'mobile_number': {contact_data.get('mobile_number', '')},
        'phone_numbers': {contact_data.get('phone_numbers', '')},
      }},
      'custom_field': {{
        
        'cf_age_range': {custom_field_data.get('cf_age_range', '')},
        'cf_courses': {custom_field_data.get('cf_courses', '')},
        'cf_message': {custom_field_data.get('cf_message', '')},
      }}
    </pre>
  </body>
</html>
"""
            return error_message
        else:
            # If error_data is not a dictionary, handle accordingly
            return f"""
<html>
  <body>
    <p>Failed to send data to CRM</p>
    <p>Data:</p>
    <pre>{error_data}</pre>
  </body>
</html>
"""
    except Exception as e:
        # Handle any exceptions that may occur during the parsing attempt
        return f"""
<html>
  <body>
    <p>Failed to send data to CRM</p>
    <p>Error parsing data:</p>
    <pre>{str(e)}</pre>
    <p>Data:</p>
    <pre>{error_data}</pre>
  </body>
</html>
"""

@app.before_request
def check_auth_token():
    # Check if the 'Authorization' header is present in the request
    auth_header = request.headers.get('Authorization')

    # Verify the token
    if auth_header != f"Bearer {SECRET_TOKEN}":
        return jsonify({'status_of_api': 'error', 'message': 'Unauthorized'}), 401

@app.route('/collectchat_webhook', methods=['POST', 'GET'])
def collectchat_webhook():
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = request.json

            # Clean and format the data
            reformatted_data = format_data(data)

            # Send the reformatted data to the CRM URL with Authorization header
            headers = {
                'Authorization': f'Token token={CRM_AUTH_TOKEN}',
                'Content-Type': 'application/json'
            }

            response = requests.post(CRM_URL, json=reformatted_data, headers=headers)

                        # Log the CRM API response for debugging
            app.logger.info(f'CRM API Response - Status Code: {response.status_code}, Content: {response.text}')

            # Check if the request was successful
            if response.status_code == 200:
                return jsonify({'status_of_api': 'success', 'data': reformatted_data})
            else:
                error_data = {
                    
                    'contact': {
                        'first_name': data.get('first_name', ''),
                        'mobile_number': data.get('mobile_number', ''),
                        'phone_numbers': data.get('phone_numbers', ''),
                        
                    },
                    'custom_field': {
                        
                        'cf_age_range': data.get('cf_age_range', ''),
                        'cf_courses': data.get('cf_courses', ''),
                        'cf_message': data.get('cf_message', ''),
                        'cf_status_of_lead': data.get('cf_status_of_lead', ''),
                    },
                }

                error_message = generate_html_error_message(str(error_data))

                # Send the error email with the HTML message
                send_email('CollectChat Data Not Sent To CRM', error_message, is_html=True)

                return jsonify({'status_of_api': 'error', 'message': 'Failed to send data to CRM', })

        except Exception as e:
            app.logger.error(f'Error processing request: {str(e)}')

            error_data = {
                'unique_identifier': {
                    'emails': data.get('emails', ''),
                },
                'contact': {
                    'first_name': data.get('first_name', ''),
                    'mobile_number': data.get('mobile_number', ''),
                    'phone_numbers': data.get('phone_numbers', ''),
                    'lead_source_id': data.get('lead_source_id', ''),
                
                'custom_field': {
                    
                    'cf_age_range': data.get('cf_age_range', ''),
                    'cf_courses': data.get('cf_courses', ''),
                    'cf_message': data.get('cf_message', ''),
                    'cf_status_of_lead': data.get('cf_status_of_lead', ''),
                },
                'ip': data.get('ip', ''),
                'page': data.get('page', ''),
                'status_of_api': 'error',
                'error_message': str(e),
                },
            }

            error_message = generate_html_error_message(str(error_data))

            # Send the error email with the HTML message
            send_email('Flask App Error', error_message, is_html=True)

            return jsonify({'status_of_api': 'error', 'message': 'Failed to send data to CRM', 'message': error_message })

    elif request.method == 'GET':
        # Handle GET requests (if needed)
        # Add code to handle GET requests here, if necessary
        return jsonify({'status_of_api': 'success', 'message': 'GET request received'})

if __name__ == '__main__':
    app.run(debug=True)
