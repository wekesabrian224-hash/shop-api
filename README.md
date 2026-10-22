# Duka API

A small Amazon-style shop backend built with Flask while learning at Moringa School.
It currently stores products in memory, and a database arrives in Week 2.

## Setup

1. Clone the repository and enter the folder.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac, Linux or WSL: `python3 -m venv venv` then `source venv/bin/activate`
3. Install the packages: `pip install -r requirements.txt`
4. Run the server: `flask --app app run --debug`
5. Open http://127.0.0.1:5000/

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/about` | About the author |
| GET | `/api/products` | List all products |
| GET | `/api/products/<id>` | Get one product |
| POST | `/api/products` | Create a product |
| PATCH | `/api/products/<id>` | Update a product |
| DELETE | `/api/products/<id>` | Delete a product |

## Example request

```
POST /api/products
{"name": "Charger", "price": 1200, "stock": 15}
```

## Status

Week 1 of 4 complete. Next: database, users, cart, orders.