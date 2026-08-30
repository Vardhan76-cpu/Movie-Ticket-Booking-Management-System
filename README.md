# 🎬 Movie Ticket Booking Management System

A full-stack movie ticket booking application built with **Python Flask, SQLite, HTML, CSS and JavaScript**.

## Features
- Movie, theatre and show selection
- Seat availability checking
- Automatic cost calculation
- Booking confirmation and cancellation
- Seat restoration after cancellation
- Unique booking ID
- QR-code ticket
- Booking lookup
- PDF knowledge-base documents

## Architecture
Browser → HTML/CSS/JavaScript → Flask REST API → SQLite Database

## Project Structure
```text
movie-ticket-booking/
├── backend/app.py
├── backend/requirements.txt
├── frontend/index.html
├── frontend/style.css
├── frontend/script.js
├── documents/
├── data/
├── tickets/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```
Open `http://127.0.0.1:5000`.

## Booking Logic
`Total Cost = Number of Tickets × Ticket Price`

A booking is accepted only when:
`Available Seats >= Requested Tickets`

## PDF Knowledge Base
The `documents/` folder contains requirements, booking policy, cancellation/refund policy, seat rules, pricing, theatre/show information and FAQs. These PDFs can later be connected to a RAG/AI chatbot.

## API
- GET `/api/health`
- GET `/api/movies`
- GET `/api/theatres`
- GET `/api/shows`
- POST `/api/bookings`
- GET `/api/bookings/<booking_id>`
- POST `/api/bookings/<booking_id>/cancel`

## Note
This is an educational MVP. Production deployment should add authentication, HTTPS, secure secrets, a production WSGI server, stronger validation and a production database/payment service.
