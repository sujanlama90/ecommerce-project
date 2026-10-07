# E-Commerce Store

A modern Django-based e-commerce application for browsing products, managing a cart, creating user accounts, handling profile settings, and contacting the store.

This project includes category-based product browsing, custom user authentication, social login support, media uploads through Cloudinary, rich product descriptions with CKEditor, and an admin dashboard enhanced with Jazzmin.

## Features

- Product catalog with category and subcategory filtering
- Featured homepage offers and promotional sections
- Product detail pages with reviews and ratings
- Session-based shopping cart
- User registration, login, logout, and password reset flow
- Profile management and dashboard features
- Social authentication with Google sign-in
- Contact form and store information pages
- Admin management with Django admin and Jazzmin
- Cloudinary media handling for product and profile images

## Tech Stack

- Python 3.x
- Django 6.1
- PostgreSQL
- Bootstrap-based frontend templates
- Cloudinary for media storage
- django-ckeditor-5 for rich text editing
- django-allauth and social-auth-app-django
- django-jazzmin for admin UI
- python-decouple for environment configuration

## Project Overview

The application is structured as a typical Django storefront with separate apps for storefront logic, user accounts, payments, and cart handling.

### User Journey

1. A customer visits the homepage and browses featured products and categories.
2. They filter or explore subcategories to narrow results.
3. They open a product page to view details, variants, and reviews.
4. They add items to the cart and proceed to checkout-related flows.
5. Registered users can manage their profile, update settings, and reset their password.
6. Admin users can manage products, categories, offers, reviews, and contacts from the admin panel.

## Project Structure

```text
.
├── LICENSE
├── README.md
├── shop/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── accounts/
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── pipeline.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── main/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── templates/
│   ├── payments/
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── shop/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── static/
│   ├── templates/
│   └── media/
└── venv/
```

## Main Applications

### `main`

Handles the storefront experience, including:

- homepage
- product listings
- category and subcategory filtering
- product detail pages
- cart interactions
- contact form and about page

### `accounts`

Responsible for authentication and account management:

- registration and login
- logout and session handling
- password reset flow
- profile updates and dashboard
- Google social login integration

### `payments`

Contains order and checkout-related logic, including:

- order models
- item tracking
- payment flow integration points

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+ installed
- PostgreSQL installed and running locally or remotely
- A virtual environment tool such as `venv`
- Access to a Gmail account for email sending, if using the default SMTP config
- Cloudinary credentials for media uploads
- Google OAuth credentials for social login

## Environment Configuration

Create a `.env` file in the project root or inside the `shop/` folder, depending on your local setup. Use the following variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

cloud_name=your-cloudinary-cloud-name
api_key=your-cloudinary-api-key
api_secret=your-cloudinary-api-secret
secure=True

SOCIAL_AUTH_URL_NAMESPACE=social
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret
```

> This project reads environment variables using `python-decouple` in the Django settings configuration.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/e-commerce.git
cd e-commerce
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install project dependencies:

```bash
pip install -r shop/requirements.txt
```

4. Create the PostgreSQL database and ensure your database credentials match the values in `.env`.

5. Run database migrations:

```bash
cd shop
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Admin Access

Create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Running the Project

After setup, you can:

- browse the storefront at the homepage
- register an account and log in
- update profile information
- add products to the cart
- manage orders and payment-related features through the configured UI
- use the admin panel to manage products, offers, and content

## Notes

- The application is configured for local development with environment variables.
- Cloudinary is required for media uploads in the default setup.
- Social login and email features require valid API credentials.
- If you are deploying to production, review the Django security settings and replace the default local configuration with your production environment values.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
