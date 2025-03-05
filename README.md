# Daraja M-Pesa API Integration

A robust Django-based API integrating Safaricom's Daraja M-Pesa services for real-time payment processing.
Overview
This project provides a custom implementation of Safaricom's Daraja M-Pesa API, focusing on Customer-to-Business (C2B) transactions. Built with Django and Python, it handles authentication, endpoint routing, and real-time payment callbacks efficiently. Whether you're building a payment gateway or experimenting with M-Pesa integrations, this project offers a solid foundation.
Features
C2B Register URL: Successfully registers callback URLs with M-Pesa for real-time transaction updates.

Dynamic Routing: Clean and scalable URL routing with Django’s urls.py configuration.

Real-Time Processing: Handles payment requests and responses instantly.

Flexible Design: Modular structure for easy extension (e.g., adding B2C or STK Push).

Error Handling: Resolves common issues like 404 errors with synced endpoints.

## Prerequisites

Python 3.8+

Django 4.x

Requests library (pip install requests)

Safaricom Daraja API credentials (Consumer Key, Consumer Secret)

## Installation

Clone the Repository  
bash

git clone https://github.com/yourusername/daraja-api-project.git
cd daraja-api-project

Set Up a Virtual Environment  
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install Dependencies

bash

pip install -r requirements.txt

Configure Environment Variables
Create a .env file in the root directory and add your M-Pesa credentials:
plaintext

MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=your_shortcode

Run Migrations  
bash

python manage.py migrate

Start the Server  
bash

python manage.py runserver

## Usage

Registering Callback URLs
Send a POST request to /api/v1/c2b/register/ to register your validation and confirmation URLs with M-Pesa.
bash

curl -X POST http://localhost:8000/api/v1/c2b/register/ \
-H "Content-Type: application/json" \
-d '{"validation_url": "https://yourdomain.com/validate", "confirmation_url": "https://yourdomain.com/confirm"}'

## Testing Endpoints

C2B Register: GET /api/v1/c2b/register/ (for testing purposes)

Transaction Callback: Configure your server to handle POST requests from M-Pesa at your callback URLs.

## Project Structure

daraja-api-project/
├── api/                # API views and logic
│   ├── urls.py         # Routing configuration
│   └── views.py        # API endpoints
├── daraja/             # Django project settings
├── .env                # Environment variables
├── requirements.txt    # Project dependencies
└── README.md           # This file

## Contributing

Feel free to fork this repo, submit issues, or send pull requests. All contributions are welcome!
License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

Safaricom Daraja API Documentation

Django and Python communities


