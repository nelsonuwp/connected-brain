from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

from flask import Flask

from routes.cpq import cpq_bp
from routes.profitability import profitability_bp
from routes.renewals import renewals_bp
from routes.settings import settings_bp

app = Flask(__name__)
app.register_blueprint(cpq_bp)
app.register_blueprint(profitability_bp)
app.register_blueprint(renewals_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
