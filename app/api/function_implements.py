from app.models import *


def get_items(sess):
    return sess.query(Items).all()


def get_records(sess):
    return sess.query(UseRecord).all()


def insert_item(sess, param_dict):
    _user_id = get_user(sess, param_dict["username"]).user_id
    item = Items()
    item._user_id = int(_user_id)
    item.itemname = param_dict["itemname"]
    item.description = param_dict["description"]
    item.amount = int(param_dict["amount"])
    sess.add(item)
    sess.commit()


def insert_records(sess, param_dict):
    record = UseRecord()
    record.state = int(param_dict["state"])
    record.item_id = int(get_item_id_by_name(sess, param_dict["itemname"]))
    record.user_id = int(get_user_id_by_name(sess, param_dict["username"]))
    sess.add(record)
    sess.commit()
    # 除了添加记录之外还得改变 物品数量
    item = sess.query(Items).filter_by(itemname=param_dict["itemname"]).first()
    if param_dict["state"] == "0":
        item.amount = item.amount - 1
    elif param_dict["state"] == "1":
        item.amount = item.amount + 1
    sess.commit()


def update_user(sess, param_dict):
    if "newpasswordsalt" in param_dict.keys() and "oldpasswordsalt" in param_dict.keys():
        user = get_user(sess, param_dict["username"])
        user.passwordsalt = param_dict["newpasswordsalt"]
        sess.commit()
    else:
        user = get_user(sess, param_dict["username"])
        if param_dict.get("email") is not None:
            user.email = param_dict["email"]
        else:
            user.email = ""
        if param_dict.get("sign") is not None:
            user.sign = param_dict["sign"]
        else:
            user.sign = ""
        sess.commit()


def update_user_image(sess, username, file_name):
    user = get_user(sess, username)
    user.image_src = file_name
    sess.commit()


def exists_user(sess, username, passwordsalt=None):
    if passwordsalt:
        res = sess.query(Users).filter_by(username=username, passwordsalt=passwordsalt).all()
    else:
        res = sess.query(Users).filter_by(username=username).all()
    if len(res) > 0:
        return True
    else:
        return False


def insert_user(sess, param_dict):
    u = Users()
    if "phone" in param_dict.keys():
        u.phone = int(param_dict["phone"])
    if "rights" in param_dict.keys():
        u.rights = param_dict["rights"]
    if "sign" in param_dict.keys():
        u.sign = param_dict["sign"]
    if "passwordsalt" in param_dict.keys():
        u.passwordsalt = param_dict["passwordsalt"]
    if "email" in param_dict.keys():
        u.email = param_dict["email"]
    if "username" in param_dict.keys():
        u.username = param_dict["username"]
    try:
        sess.add(u)
        sess.commit()
    except Exception:
        raise Exception("insert error")


def get_user(sess, username):
    return sess.query(Users).filter_by(username=username).first()


def get_username_by_id(sess, user_id):
    return sess.query(Users).filter_by(user_id=user_id).first().username


def get_itemname_by_id(sess, item_id):
    return sess.query(Items).filter_by(item_id=item_id).first().itemname


def get_user_id_by_name(sess, username):
    return sess.query(Users).filter_by(username=username).first().user_id


def get_item_id_by_name(sess, itemname):
    return sess.query(Items).filter_by(itemname=itemname).first().item_id
