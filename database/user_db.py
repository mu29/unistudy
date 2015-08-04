# -*- coding: utf-8 -*-

import MySQLdb
import hashlib
from flask import *
from database.db import *

class UserDB:

    def __init__(self):
        self.connection = db.get_mysql().connect()
        self.connection.autocommit(True)

    def login(self, email, password):
        # 아이디와 비밀번호로 유저 검색
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `users` WHERE `email` = '" + email +
                       "' AND `password` = '" + hashlib.sha224(password).hexdigest() + "';")

        # 유저가 없을 경우
        if cursor.rowcount == 0:
            cursor.close()
            return u'아이디와 비밀번호를 확인하세요.'

        # 유저를 얻자
        userdata = cursor.fetchone()

        # 인증이 안된 경우
        if userdata['verify'] == 0:
            cursor.close()
            return u'가입 인증 메일을 확인해주세요.'

        # 밴 된 아이디일 경우
        if userdata['ban'] == 1:
            cursor.close()
            return u'차단된 계정입니다.'

        # 로그인 성공
        session['nickname'] = userdata['nickname']
        session['email'] = userdata['email']
        cursor.close()
        return None

    def register(self, email, password, nickname):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `users` WHERE `email` = '" + email + "';")
        if cursor.rowcount > 0:
            cursor.close()
            return u'이미 가입된 메일 주소입니다.'

        # 닉네임 중복 확인
        cursor.close()
        cursor = db.execute("SELECT * FROM `users` WHERE `nickname` = '" + nickname + "';")
        if cursor.rowcount > 0:
            cursor.close()
            return u'이미 존재하는 닉네임입니다.'

        # 가입 성공. 메일 보내자
        cursor.close()
        cursor = db.execute("INSERT INTO `users` SET `email` = '" + email +
                            "', `password` = '" + hashlib.sha224(password).hexdigest() +
                            "', `nickname` = '" + nickname + "';")

        cursor.close()
        return None

    def verify(self, email):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE `users` SET `verify` = '1' WHERE `email` = '" + email + "';")
        cursor.close()

user_db = UserDB()
