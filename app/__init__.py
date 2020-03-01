# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import config
#
# db = SQLAlchemy()
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config)
#     db.init_app(app)
#   '''
#     这里省去了部分代码。最基本的就是上边的几条语句。
#     包括初始化数据库的对象，引入配置信息。
#   '''
#
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint, static_folder='static')
#
#     return app