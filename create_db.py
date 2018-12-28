#!/usr/bin/env python
# -*- coding:utf-8 -*
# @Author   : Zhxu
# @Time     : 18-12-28 下午4:28

# create_db.py


from app import db
from models import Flaskx


# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()