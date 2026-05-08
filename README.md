# SkateShop Demo Project

A Django-based demo project for skateboarding equipment, including complete skateboards, decks and trucks. The project simulates a full shopping experience with cart, favorites, orders and a fake checkout/payment flow.

---

## Features

- Product catalog for skateboards, decks and trucks
- Brand-based browsing system
- Product detail pages with attributes and images
- Shopping cart with quantity support
- Favorite (wishlist) system per user
- Order creation from cart
- Fake checkout/payment flow (no real payment provider)
- Search functionality across all products
- User authentication system
- Seed scripts for generating demo data

---

## Tech Stack

- Python 3
- Django
- SQLite
- HTML, CSS, JavaScript
- Pillow

---

## Project Structure

store → products, brands, product logic  
cart → shopping cart system  
orders → checkout and order handling  
user → profile, favorites, user pages  
seed_assets → images used for database seeding  

---

## Installation

### 1. Clone repository

```
git clone https://github.com/sevy-sl/Skateshop-Demo.git
cd Skateshop-Demo
```

### 2. Create virtual environment

```
python3 -m venv venv  
source venv/bin/activate  # Windows: venv\Scripts\activate  
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Environment variables

Create a .env file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

To create a key:

```
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7. Apply migrations

```
python3 manage.py migrate
```

### 6. (Optional) Seed database

```
python3 seed_skateboards.py  
python3 seed_decks.py  
python3 seed_trucks.py  
```

### 7. Create admin user

```
python3 manage.py createsuperuser
```

### 8. Run server

```
python3 manage.py runserver
```

---

## Fake Checkout System

The checkout flow simulates a payment process:

- Cart items are converted into an order
- Order items are saved separately
- Cart is cleared after checkout
- A success message is shown to the user

No real payment provider is integrated.

---

## Notes

- This is a demo project, not production-ready
- Images are stored locally in `media/`
- Designed for learning Django architecture
