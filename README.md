# FormFlow Restructurer

This project, **FormFlow Restructurer**, is a Flask-based web application designed to modify JSON data format from WordPress Contact Form 7, restructure it, and send the data to Freshsales CRM. Additionally, it sends email notifications upon successful data processing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Systemd Service](#systemd-service)
- [uWSGI Configuration](#uwsgi-configuration)
- [License](#license)
- [Contact](#contact)

## Introduction

**FormFlow Restructurer** is a Flask web application that serves as an intermediary between WordPress Contact Form 7 and Freshsales CRM. The app listens for JSON payloads, restructures the data to meet Freshsales' API format, sends the data to Freshsales, and notifies relevant stakeholders via email.

## Features

- Receives JSON payloads from WordPress Contact Form 7.
- Restructures and formats JSON data.
- Sends the modified data to Freshsales CRM using its API.
- Sends email notifications upon successful processing.
- Configurable via `.ini` files and systemd service for production deployment.

## Requirements

- Python 3.7+
- Flask 2.3.3
- Requests 2.31.0
- uWSGI
- Email configuration (e.g., SMTP server details)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/formflow-restructurer.git
    cd formflow-restructurer
    ```

2. **Create a Virtual Environment and Install Dependencies**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Update Configuration**

   - Modify the `myapp.ini` file as needed.
   - Update email settings in the configuration file to ensure proper email notifications.

4. **Run the Application**

    ```bash
    uwsgi --ini myapp.ini
    ```

## Usage

Once the application is running, it listens for incoming JSON data from Contact Form 7, processes it, sends the transformed data to Freshsales CRM, and notifies the configured email addresses.

## Deployment

To deploy this application in a production environment:

1. **Install uWSGI**:

    ```bash
    pip install uwsgi
    ```

2. **Set Up systemd Service**:

    Create a service file `/etc/systemd/system/myapp.service`:

    ```ini
    [Unit]
    Description=my flask app
    After=network.target

    [Service]
    User=your-username
    Group=www-data
    WorkingDirectory=/path/to/your/app
    ExecStart=/usr/local/bin/uwsgi --ini /path/to/your/app/myapp.ini
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

3. **Enable and Start the Service**:

    ```bash
    sudo systemctl enable myapp
    sudo systemctl start myapp
    ```

4. **Check Status**:

    ```bash
    sudo systemctl status myapp
    ```

## uWSGI Configuration

The application uses uWSGI to serve the Flask app. Below is an example uWSGI configuration:

```ini
[uwsgi]
module = app:app
master = true
processes = <number_of_processes>
http-timeout = <timeout_duration>
socket = <socket_address>
protocol = http
chmod-socket = 660
vacuum = true
die-on-term = true
pythonpath = <path_to_your_app>
pidfile = <path_to_pidfile>
logto = <path_to_logfile>
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please reach out to:

- **Name:** Nishanth Fiona
- **Email:** fiona.nf12@gmail.com
- **GitHub:** [nishanth fiona](https://github.com/Nishanthfiona)
