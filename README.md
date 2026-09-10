# What to Order — Dubai

Search Dubai restaurants and see what to order if you are watching your weight. Clients log in with email and password first.

```bash
cd "C:\Users\Nageen\Desktop\Nutrition cv\dubai-eat-out"
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5055/ — create an account, then the guides open.

On Render, set `SECRET_KEY`. Add a PostgreSQL database and `DATABASE_URL` if you want client accounts to survive restarts (SQLite on Render is wiped when the server sleeps).
