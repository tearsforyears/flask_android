from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    passwordsalt = Column(String(), nullable=False)
    phone = Column(Integer(), nullable=False)
    image_src = Column(String(), default=None)
    email = Column(String())
    sign = Column(String(), default="这个人很懒,什么也没有说")
    rights = Column(String(), default=1)  # 权利 0为游客 1为普通 2为管理员
    create_time = Column(String(), default=datetime.datetime.now())
    last_login_time = Column(String(), onupdate=datetime.datetime.now(), default=datetime.datetime.now())


class Items(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True)
    itemname = Column(String(), unique=True, nullable=False)
    description = Column(String(), nullable=False)
    amount = Column(Integer, nullable=False)
    _user_id = Column(Integer, ForeignKey("users.user_id"))


class UseRecord(Base):
    __tablename__ = "use_record"
    record_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.item_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    last_use_time = Column(String, default=datetime.datetime.now())
    state = Column(Integer, default=0)


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from app.api.function_implements import insert_item
    import os

    engine = create_engine('sqlite:///' + os.path.dirname(__file__) + '/db.sqlite3.db')
    # Base.metadata.create_all(engine)

    sess = sessionmaker(bind=engine)()  # 建立会话对象
    re = UseRecord()
    re.item_id = 2
    re.user_id = 1
    re.state = 1
    sess.add(re)
    # insert_item(sess, {'username': 'root', 'itemname': '物品1', 'descripton': '易燃易爆炸', 'amount': '200'})
    # print(len(sess.query(Users).filter_by(username="root", passwordsalt="4f156b738070a78b4136a6400e824ba3").all()))
    sess.commit()
    sess.close()
