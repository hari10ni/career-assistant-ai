import markdown
from flask import Flask
from database.db import initialize_database

app = Flask(__name__)

app.jinja_env.filters["markdown"] = lambda text: markdown.markdown(text)

app.secret_key = "career_assistant_secret_key"
initialize_database()

# Import Blueprints
from routes.main import main
from routes.auth import auth
from routes.chat import chat
from routes.resume import resume

# Register Blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(chat)
app.register_blueprint(resume)

if __name__ == "__main__":
    app.run(debug=True)