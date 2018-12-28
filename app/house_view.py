import os

from flask import Blueprint, render_template, request, session, jsonify

from app.models import House, Area, HouseImage, Facility, Order, User
from utils.settings import MEDIA_PATH

blue1 = Blueprint('house', __name__)


@blue1.route('/booking/',methods=['GET'])
def booking():
    return render_template('booking.html')


@blue1.route('/newhouse/',methods=['GET','POST'])

def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')

    if request.method == 'POST':
        params = request.form.to_dict()
        facility_ids=request.form.getlist('facility')
        house = House()
        house.user_id=session['user_id']
        house.title = request.form.get('title')
        house.price = request.form.get('price')
        house.area_id = request.form.get('area_id')
        house.address = request.form.get('address')
        house.room_count = request.form.get('room_count')
        house.acreage = request.form.get('acreage')
        house.unit = request.form.get('unit')
        house.capacity= request.form.get('capacity')
        house.beds= request.form.get('beds')
        house.deposit= request.form.get('deposit')
        house.min_days= request.form.get('min_days')
        house.max_days=request.form.get('max_days')
        if facility_ids:
            facility_list=Facility.query.filter(Facility.id.in_(facility_ids)).all()
            house.facilities=facility_list

        house.add_update()
        return jsonify({'code':200,'house_id':house.id})


@blue1.route('/house_images/', methods=['POST'])
def house_images():
    # 创建房屋图片
    house_id = request.form.get('house_id')
    image = request.files.get('house_image')

    # 保存图片  /static/media/upload/xxx.jpg
    save_url = os.path.join(MEDIA_PATH, image.filename)
    image.save(save_url)
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image.filename
    house_image.add_update()

    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image.filename
        house.add_update()
    return jsonify({'code':200,'image_url':image.filename})






@blue1.route('/detail/', methods=['GET'])
def detail():

    return render_template('detail.html')



@blue1.route('/detail/<int:id>/',methods=['GET'])
def house_detail(id):

    house=House.query.get(id)
    facility_list=house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    booking=1
    if 'user_id' in session:
        if house.user_id==session['user_id']:
            booking=0

    return jsonify(house=house.to_full_dict(),facility_list=facility_dict_list,booking=booking)


@blue1.route('/search/',methods=['GET'])
def search():
    return render_template('search.html')




@blue1.route('/my_search/', methods=['GET'])
def search_house():

    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    # 过滤区域信息
    house = House.query.filter(House.area_id==aid)
    # 过滤登录用户发布房屋信息
    if 'user_id' in session:
        hlist = house.filter(House.user_id != session['user_id'])
    # 查询不满足条件的房屋id
    order1 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
    order3 = Order.query.filter(Order.begin_date >= sd, Order.begin_date <= ed)
    order4 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    house_ids1 = [order.house_id for order in order1]
    house_ids2 = [order.house_id for order in order2]
    house_ids3 = [order.house_id for order in order3]
    house_ids4 = [order.house_id for order in order4]

    house_ids = list(set(house_ids1 + house_ids2 + house_ids3 + house_ids4))
    # 最终展示的房屋信息
    houses = hlist.filter(House.id.notin_(house_ids))

    if sk == 'booking':
        houses = houses.order_by('order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')
    else:
        houses = houses.order_by('-id')

    houses_dict = [house.to_dict() for house in houses]

    return jsonify({'code':200,'houses_dict':houses_dict})


@blue1.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()

    areas_json = [area.to_dict() for area in areas]
    facilitys_json = [facility.to_dict() for facility in facilitys ]

    return jsonify({'code':'200','areas':areas_json,'facilitys':facilitys_json})




@blue1.route('/hindex/', methods=['GET'])
def my_index():
    user_id = session.get('user_id')
    # 验证用户的登录情况
    if user_id:
        user = User.query.get(user_id)
        username = user.name
    else:
        username = ''
    # 返回轮播图
    houses =House.query.filter(House.index_image_url != '')[:3]
    houses_image = [house.to_dict() for house in houses]

    return jsonify({'code':200,'username':username,'houses_image':houses_image})
