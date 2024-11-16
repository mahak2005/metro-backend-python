from flask_cors import CORS

def configure_cors(app):
    # CORS configuration to allow specific origins and methods
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "https://delhimetro.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Origin", "X-Requested-With", "Content-Type", "Accept", "Authorization"],
            "supports_credentials": True
        }
    })
