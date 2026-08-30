# Movie-Ticket-Booking-Management-System

Movie Ticket Booking Management System for booking movies, checking seat availability, calculating costs, confirming or cancelling tickets, allocating seats, generating tickets, notifications, SLA management, and show-based routing, with PDF documents as a knowledge base.

##  Project Overview

The **Movie Ticket Booking Management System** is a digital application designed to manage movie ticket booking requests.

The system allows customers to select a movie, theatre, show date and time, and number of tickets. It checks seat availability, calculates the booking cost, allows the customer to review and confirm or cancel the booking, processes the ticket booking, allocates seats, and sends a booking confirmation.

The project is designed around a structured booking workflow with data objects, case management, validation, routing, SLA handling, and notifications.

---

##  Project Objectives

The main objectives of this project are:

* Allow customers to submit movie ticket booking requests.
* Check show and seat availability.
* Calculate the total booking cost.
* Allow customers to review booking details.
* Provide Confirm and Cancel options.
* Process confirmed ticket bookings.
* Allocate seats and update availability.
* Generate ticket/booking information.
* Notify customers after successful booking.
* Maintain movie and show information.
* Route booking requests based on show type.
* Define an SLA for processing booking requests.

---

##  Application Workflow

```text
                    Customer
                       │
                       ▼
              Submit Booking Request
                       │
                       ▼
              Check Show Availability
                       │
                       ▼
                Calculate Cost
                       │
                       ▼
             Review Booking Details
                       │
                       ▼
              Confirm / Cancel
                 │          │
              Cancel      Confirm
                 │          │
                 ▼          ▼
             CLOSED    Process Booking
                            │
                            ▼
                      Allocate Seats
                            │
                            ▼
                      Generate Ticket
                            │
                            ▼
                    Send Notification
                            │
                            ▼
                         CLOSED
```

---

##  Main Features

### 1. Movie Ticket Request

Customers can enter:

* Customer Name
* Email
* Phone Number
* Movie
* Theatre
* Show Date
* Show Time
* Number of Tickets

A new booking request is created after submission.

### 2. Show Availability

The system checks whether enough seats are available for the requested show.

Example:

```text
Available Seats = 5
Requested Tickets = 2

5 >= 2
```

The booking can continue.

If:

```text
Available Seats = 1
Requested Tickets = 2
```

The booking cannot continue.

### 3. Booking Cost Calculation

The total booking cost is calculated using:

```text
Total Cost = Number of Tickets × Ticket Price
```

Example:

```text
Tickets = 3
Ticket Price = ₹200

Total Cost = 3 × ₹200
           = ₹600
```

### 4. Review Booking

Before confirmation, customers can review:

```text
Customer
Movie
Theatre
Show Date
Show Time
Number of Tickets
Ticket Price
Total Cost
```

### 5. Confirm or Cancel

The customer can choose:

* **Confirm** → Continue with booking
* **Cancel** → Booking status becomes Cancelled

### 6. Ticket Processing

After confirmation, the system:

1. Verifies availability.
2. Allocates seats.
3. Updates available seats.
4. Generates booking/ticket information.
5. Changes the booking status to Confirmed.

### 7. Notifications

After successful booking, the customer receives booking confirmation containing information such as:

```text
Booking ID
Movie
Theatre
Show
Number of Tickets
Total Amount
```

### 8. Movie and Show Management

Staff/Admin can maintain:

* Movies
* Theatres
* Shows
* Show times
* Ticket prices
* Available seats
* Show status

### 9. SLA Management

The project includes an SLA for processing booking requests.

Example:

```text
Booking Request
      ↓
SLA Timer Starts
      ↓
Request Processing
      ↓
Booking Completed
```

The requirements provide **30 minutes** as an example processing deadline.

### 10. Work Queue Routing

Booking requests can be automatically routed according to show type.

```text
                 Booking Request
                       │
                       ▼
                  Show Type
                 /    |     \
                /     |      \
          Regular    VIP    Special
             │        │        │
             ▼        ▼        ▼
          Regular    VIP     Special
          Queue     Queue     Queue
```

---

##  Data Objects

The application uses the following main data objects.

### Customer

```text
Customer Name
Email
Phone Number
```

### Movie

```text
Movie Name
Language
Genre
Duration
```

### Theatre

```text
Theatre Name
Location
```

### Show

```text
Movie
Theatre
Show Date
Show Time
Total Seats
Available Seats
Ticket Price
```

### Booking

```text
Customer
Movie
Theatre
Show
Number of Tickets
Total Cost
Booking Status
```

---

##  Knowledge Base / PDF Documents

The project also includes a `documents` folder containing PDF documents that can be used as a project reference or AI/RAG knowledge base.

```text
documents/
│
├── 01_Movie_Ticket_Booking_Requirements.pdf
├── 02_Movie_Booking_Policy.pdf
├── 03_Cancellation_Refund_Policy.pdf
├── 04_Seat_Booking_Rules.pdf
├── 05_Payment_and_Pricing_Policy.pdf
├── 06_Theatre_and_Show_Information.pdf
└── 07_Customer_FAQ.pdf
```

These documents contain information about booking requirements, booking rules, cancellation, seat availability, pricing, theatre/show information and customer FAQs.

> **Note:** The supplied requirements do not define specific refund percentages, payment gateway behavior, taxes, discounts, or refund timelines. Such information should only be added if it is officially defined for the application.

##  Testing

The application should be tested using different scenarios.

### Test Case 1 — Successful Booking

```text
Select Movie
      ↓
Select Theatre
      ↓
Select Show
      ↓
Select Tickets
      ↓
Check Availability
      ↓
Calculate Cost
      ↓
Confirm
      ↓
Booking Successful
      ↓
Notification
```

### Test Case 2 — Insufficient Seats

```text
Requested Tickets = 5
Available Seats = 2

Result:
Booking cannot continue
```

### Test Case 3 — Customer Cancellation

```text
Booking Request
      ↓
Review Details
      ↓
Cancel
      ↓
Booking Status = Cancelled
```

### Test Case 4 — SLA

Verify that the booking case has the configured SLA.

### Test Case 5 — Routing

Submit different show types and verify that each request is routed to the appropriate work queue.


## 🛠️ Technology / Platform

The original application requirements are designed for implementation using:

* **Pega App Studio**
* **Pega Blueprint**
* Pega Case Management
* Data Objects
* Business Processes
* Work Queues
* SLA
* Notifications

The PDF documents can additionally serve as a knowledge source if an AI/RAG component is added.


##  Project Structure

```text
movie-ticket-booking/
│
├── README.md
│
├── documents/
│   ├── 01_Movie_Ticket_Booking_Requirements.pdf
│   ├── 02_Movie_Booking_Policy.pdf
│   ├── 03_Cancellation_Refund_Policy.pdf
│   ├── 04_Seat_Booking_Rules.pdf
│   ├── 05_Payment_and_Pricing_Policy.pdf
│   ├── 06_Theatre_and_Show_Information.pdf
│   └── 07_Customer_FAQ.pdf
│
├── frontend/
│
├── backend/
│
├── data/
│
└── screenshots/
```


##  Future Enhancements

Possible future improvements include:

* Online payment integration
* QR-code ticket generation
* Email/SMS notifications
* Real-time seat selection
* User authentication
* Booking history
* Admin dashboard
* Movie search and filtering
* AI-powered customer support
* PDF-based RAG chatbot
* Analytics and reporting

---

##  Project Status

**Status:** In Development

The project workflow, data objects, booking process, validation, notification, SLA, routing and testing requirements have been defined.


##  License

This project is developed for educational and project demonstration purposes.
