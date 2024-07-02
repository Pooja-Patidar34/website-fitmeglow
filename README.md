<h1 align="center">Skincare E-Commerce Platform</h1>

A comprehensive e-commerce platform for Korean skincare products built with Django. Features include user authentication, product management, shopping cart, wishlist, advanced filtering by product type, skin type, and skin concern, sorting by prices, and secure checkout with Stripe integration.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Key Features](#key-features)
3. [Setup Instructions](#setup-instructions)

## Technologies Used
- [Django](https://www.djangoproject.com/) (Python web framework)
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Stripe API](https://stripe.com/docs/api) (for payment processing)
- [SQLite](https://www.sqlite.org/) (lightweight database for development)

## Key Features
- **User Authentication**: Implemented secure user registration and login functionality.
- **Product Management**: CRUD operations managed through Django admin.
- **Shopping Cart**: Developed a shopping cart feature that allows users to add, remove, and update items.
- **Wishlist**: Added functionality for users to save products to a wishlist for future reference.
- **Filtering and Sorting**: Implemented advanced filtering and sorting features using Django's ORM.
- **Checkout Process**: Integrated Stripe for secure payment processing during checkout.
- **Dashboard**: Access to user account details and order history.
- **Contact Section**: Provided a dedicated contact page or form for user inquiries and support.

## Setup Instructions

### Prerequisites

 **Install Python**:
    - Download and install Python from the [official Python website](https://www.python.org/downloads/). 

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/chrispsang/Beauty-Skincare.git
    cd Beauty-Skincare
    ```

2. **Install dependencies**:
    ```sh
    pip3 install -r requirements.txt
    ```

3. **Set up environment variables for Stripe**:
    - Create a `.env` file in the root of the project and add your Stripe API keys:
        ```plaintext
        STRIPE_SECRET_KEY=
        STRIPE_PUBLISHABLE_KEY=
        ```

4. **Start the development server**:
    ```sh
    python3 manage.py runserver
    ```

5. **Access the application**:
    - Visit `http://127.0.0.1:8000` in your browser for the main site.

6. **Testing with Stripe Payment**:
    - Debit or Credit Card Number: 4242 4242 4242 4242
    - Expiry Date: Any future date
    - CVC: Any 3 digits
    - ZIP Code: Any 5 digits 

