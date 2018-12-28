import os
import re

from werkzeug.security import generate_password_hash
from io import BytesIO
from utils.functions import is_login
from app.captcha import Captcha

from flask import Blueprint, request, render_template, make_response, jsonify, session
from app.models import User, House
from utils.settings import MEDIA_PATH

blue = Blueprint('user', __name__)


@blue.route('/register/',methods=['GET','POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        passwd = request.form.get('passwd')
        passwd2 = request.form.get('passwd2')

        if not all([mobile,passwd,passwd2]):
            return jsonify({'code':1001,'msg':'参数不完整'})

        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify({'code':1002,'msg':'请输入正确的电话号码'})

        if passwd != passwd2:
            return jsonify({'code':1003,'msg':'两次密码输入不一致'})

        if User.query.filter(User.phone == mobile).count():
            # 数据库中已存在
            return jsonify({'code':1004,'msg':'用户名已存在'})
        user = User()
        user.phone = mobile
        user.password = passwd
        user.name = mobile
        user.add_update()

        return jsonify({'code':200})
    else:
        return render_template('register.html')


@blue.route('/captcha/')
def graph_captcha():
   text, image = Captcha.gen_graph_captcha()
   out = BytesIO()
   image.save(out, 'png')
   out.seek(0)
   resp = make_response(out.read())
   resp.content_type = 'image/png'
   return resp


@blue.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        passwd = request.form.get('passwd')

        if not all([mobile,passwd]):
            return jsonify({'code':10001,'msg':'参数不完整'})

        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify({'code':1002,'msg':'请输入正确的电话号码'})

        user = User.query.filter(User.phone == mobile).first()

        if user:
            if user.check_pwd(passwd):
                session['user_id'] = user.id
                return jsonify({'code':200,})
            else:
                return jsonify({'code':1003,'msg':'密码错误'})
        else:
            return jsonify({'code':1005,'msg':'用户不存在'})


@blue.route('/index/',methods=['GET'])
def index():
    if request.method == 'GET':

        return render_template('index.html')



@blue.route('/my/',methods=['GET'])
@is_login
def my():
    if request.method == 'GET':

        return render_template('my.html')


@blue.route('/my_info/',methods=['GET'])
@is_login
def my_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    my_info = user.to_basic_dict()
    return jsonify({'code':200, 'my_info':my_info})


@blue.route('/profile/',methods=['GET','PATCH'])
@is_login
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

    if request.method == 'PATCH':
        avatar = request.files.get('avatar')
        name = request.form.get('name')
        if avatar:
            path = os.path.join(MEDIA_PATH, avatar.filename)
            avatar.save(path)
            user = User.query.get(session['user_id'])
            user.avatar = avatar.filename
            user.add_update()
            return jsonify({'code':200})
        if name:
            if User.query.filter(User.name==name).count():
                return jsonify({'code':1006,'msg':'用户名已存在'})
            user = User.query.get(session['user_id'])
            user.name = name
            user.add_update()
            return jsonify({'code': 200})


@blue.route('/auth/',methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')

    if request.method == 'POST':
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')
        if not re.match(r'^[\u4E00-\u9FA5]+$', id_name):
            return jsonify({'code':1010,'msg':'请输入正确的中文'})
        if not re.match(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', id_card):
            return jsonify({'code':1011,'msg':'请输入正确的身份证号码'})
        user = User.query.get(session['user_id'])
        user.id_name = id_name
        user.id_card = id_card
        user.add_update()
        return jsonify({'code':200,'id_name':id_name,'id_card':id_card})


@blue.route('/auth_info/',methods=['GET'])
def user_info():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify({'code':200,'user':user})


@blue.route('/myhouse/',methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@blue.route('/house_info/',methods=['GET'])
def house_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    user1 = user.to_auth_dict()
    if user.id_name:
        house_list = House.query.filter(House.user_id==user_id).order_by(House.id.asc())
        house_info = [house.to_dict() for house in house_list]
        return jsonify({'code':200,'house_info':house_info,'user1':user1})
    else:
        return jsonify({'code':1007,'msg':'用户未实名认证'})


@blue.route('/logout/',methods=['GET'])
def logout():
    return render_template('login.html')


