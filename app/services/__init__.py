# package marker for services
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    # register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.job_routes import job_bp
    from app.routes.application_routes import application_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(job_bp, url_prefix="/jobs")
    app.register_blueprint(application_bp, url_prefix="/applications")

    # --- Test route ---
    @app.route("/ping")
    def ping():
        return "pong", 200

    return app
