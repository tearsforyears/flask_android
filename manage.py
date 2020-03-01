# from flask_script import Manager, Shell
# from app import create_app,db
# from flask_migrate import Migrate, MigrateCommand, upgrade
#
from app.run import create_app
app = create_app()

if __name__ == "__main__":
    from werkzeug.contrib.fixers import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
#     # manager.run()
