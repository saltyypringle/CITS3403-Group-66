from SukiScan import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # <-- Comment this out when using Flask-Migrate!
    print("Database created (use Flask-Migrate for schema changes).")
