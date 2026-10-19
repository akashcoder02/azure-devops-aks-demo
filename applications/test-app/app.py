import os
import time

import pymysql
from flask import Flask, jsonify, request
from html import escape


app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "persistent-app")
DB_HOST = os.getenv("DB_HOST", APP_NAME + "-mysql")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.environ["DB_PASSWORD"]


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        autocommit=True,
    )


def initialize_database():
    last_error = None

    for _ in range(60):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        item VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            connection.close()
            return
        except Exception as exc:
            last_error = exc
            time.sleep(2)

    raise RuntimeError(f"Database initialization failed: {last_error}")


@app.get("/")
def home():
    name = escape(APP_NAME)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} - Persistent Bucket List</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 760px;
           margin: 40px auto; padding: 0 20px; }}
    input, button {{ padding: 10px; }}
    input {{ width: 65%; }}
    li {{ margin: 12px 0; }}
    .status {{ background: #eee; padding: 12px; }}
  </style>
</head>
<body>
  <h1>{name}</h1>
  <p>Flask + MySQL application with persistent Kubernetes storage.</p>
  <p class="status">Application generated through Backstage.</p>

  <form id="item-form">
    <input id="item" maxlength="255"
           placeholder="Add a bucket-list item" required>
    <button type="submit">Add item</button>
  </form>

  <h2>Saved items</h2>
  <ul id="items"></ul>
  <p id="message"></p>

  <script>
    const prefix = window.location.pathname.endsWith('/') ? window.location.pathname : window.location.pathname + '/';
    const endpoint = prefix + 'api/items';
    const list = document.getElementById('items');
    const message = document.getElementById('message');

    async function loadItems() {{
      try {{
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error('Could not load items');
        const items = await response.json();
        list.replaceChildren();

        for (const item of items) {{
          const li = document.createElement('li');
          li.textContent = item.item;
          list.appendChild(li);
        }}
      }} catch (error) {{
        message.textContent = 'Application is waiting for its database.';
      }}
    }}

    document.getElementById('item-form').addEventListener('submit',
      async (event) => {{
        event.preventDefault();
        const input = document.getElementById('item');

        const response = await fetch(endpoint, {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{item: input.value}})
        }});

        if (response.ok) {{
          input.value = '';
          message.textContent = 'Item saved.';
          await loadItems();
        }} else {{
          message.textContent = 'Unable to save item.';
        }}
      }}
    );

    loadItems();
  </script>
</body>
</html>"""


@app.get("/api/items")
def list_items():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, item, created_at FROM items ORDER BY id DESC"
            )
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        connection.close()


@app.post("/api/items")
def add_item():
    payload = request.get_json(silent=True) or {}
    item = str(payload.get("item", "")).strip()

    if not item or len(item) > 255:
        return jsonify({"error": "Item must contain 1-255 characters"}), 400

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO items (item) VALUES (%s)", (item,))
        return jsonify({"message": "Item saved"}), 201
    finally:
        connection.close()


@app.get("/health")
def health():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        finally:
            connection.close()

        return jsonify({"status": "healthy", "database": "connected"})
    except Exception:
        return jsonify({"status": "unhealthy", "database": "unavailable"}), 503


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5001)
