# Vanessa Loans - Mini Loan Request Platform

Welcome to **Vanessa Loans** — a simple Django-based backend API designed to handle user registrations and loan requests, including basic loan status management and integration with a credit scoring webhook.

## Project Overview

This project provides a RESTful API for managing users and their loan requests. Key features include:

- User creation and listing
- Creating, viewing, and deleting loan requests
- Validations to ensure valid loan amounts and prevent duplicate pending requests
- Integration with a mocked external credit scoring API via a webhook to update loan statuses asynchronously
- Admin panel access for easy data management

## Tech Stack

- Python 3.10.12
- Django 5.2.5
- Django REST Framework
- SQLite 

## Features

- **User Management:** Create and list users with fields like name, email, and phone number.
- **Loan Requests:** Create loans with amount validation and status tracking (Pending, Approved, Rejected).
- **Webhook Integration:** Accept callbacks from a credit scoring service to update loan status and add reasons.
- **Admin Panel:** Full Django admin interface with custom list displays and filters for users and loans.

## Getting Started

Clone the repository and create a Python virtual environment:

- git clone https://github.com/Rukorio-Vanessa/Loan-Interview
- cd loan_request_platform
- python3 -m venv venv
- source venv/bin/activate

## Apply migrations and create a superuser:
- python manage.py migrate
- python manage.py createsuperuser

## Run the development server:
python manage.py runserver at http://127.0.0.1:8000/

## API Endpoints
### User APIs:

    POST /users/ — Create a user

    GET /users/list/ — List users

### Loan APIs:

    POST /loan-request/ — Create a loan request

    GET /loans/<id>/ — View loan and their details

    DELETE /loans/<id>/delete/ — Delete a loan

    POST /loans/webhook/credit-score/ — Webhook to update loan statuses from credit scoring API

# API Usage with curl
## Create a new user
    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Vanessa", "email_address": "vanessa@example.com", "phone_number":0735750473}'

## Create a new loan request
    curl -X POST http://127.0.0.1:8000/loan-request/ -H "Content-Type: application/json" -d '{"user_id": 1, "amount": 500}'

## View loan details
    curl http://127.0.0.1:8000/loans/1/

## Delete a loan
    curl -X DELETE http://127.0.0.1:8000/loans/1/delete/

## Update loan request with atatus using webhook callback
    curl -X POST http://127.0.0.1:8000/loans/webhook/credit-score/ \
    -H "Content-Type: application/json" \
    -d '{
        "loan_id": 1,
        "status": "APPROVED",
        "reason": "Good credit history"
    }'


## Author
This repository is created and maintained by:

- [Vanessa Rukorio](https://github.com/Rukorio-Vanessa)
