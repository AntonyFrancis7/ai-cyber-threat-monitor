from flask import Flask
from honeypot.routes import honeypot_bp
from analytics.dashboard_routes import analytics_bp

app = Flask(__name__)
app.register_blueprint(honeypot_bp)
app.register_blueprint(analytics_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
