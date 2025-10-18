from flask import Flask
from .extensions import db, login_manager,csrf #login manger use if needed
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__,template_folder='templates')

    app.config['SECRET_KEY'] = 'myfinance'  # change this in production!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    #import all blueprints and add them
    from finance.auth.routes import authbp
    from finance.dashboard.routes import dashboard
    from finance.budgets.routes import budgets
    from finance.transactions.routes import transbp
    from finance.aiandnews.routes import aiandnews

    # reg to app

    app.register_blueprint(authbp,url_prefix='/')
    app.register_blueprint(dashboard,url_prefix='/dashboard')
    app.register_blueprint(budgets,url_prefix='/budgets')
    app.register_blueprint(transbp,url_prefix='/transactions')
    app.register_blueprint(aiandnews,url_prefix='/aiandnews')


    migrate = Migrate(app,db)

    return app