from app import app  
from utils.db import db
import config
from dotenv import load_dotenv

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
