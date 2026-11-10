import os

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    db.create_all()
    # Auto-seed an empty database so the UI has data on first run.
    if os.environ.get("AUTO_SEED", "1") == "1":
        from seed import seed

        seed()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
