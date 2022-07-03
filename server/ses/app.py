from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from ses import config
from ses.models_test import *
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
CORS(app)

db.init_app(app)
migrate.init_app(app, db)

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST'
}


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data['username'], data['password']
    account = db.session.query(Account).filter(Account.username == username and
                                               Account.password == generate_password_hash(password)).first()
    if account is None:
        response = {
            'code': 60204,
            'message': '账号或密码错误'
        }
    else:
        response = {
            'code': 20000,
            'data': {
                'token': account.id
            }
        }
    return make_response((response, 200, headers))


@app.route('/api/user/info', methods=['GET'])
def info():
    # print(request.url)
    # account = db.session.query(Account).filter(Account.id == 1).first()
    # if account is None:
    #     response = {
    #         'code': 60204,
    #         'message': '账号或密码错误'
    #     }
    # else:
    #     response = {
    #         'code': 20000,
    #         'data': account.id
    #     }
    info = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    }
    return make_response(({'code': 20000, 'data': info}, 200, headers))


@app.route('/api/account/list')
def account_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = Account.id if request.args.get('sort') == '+id' else Account.id.desc()

    data_by_query = db.session.query(Account).order_by(sort).offset((page - 1) * limit).limit(limit).all()

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        role_name = db.session.query(Role).filter(Role.id == row.role_id).first().name
        row_dict['role_name'] = role_name
        result_data.append(row_dict)

    count = db.session.query(Account).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/account/create', methods=['POST'])
def account_create():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role_id = data['role']
    status = data['status']
    existing_account = db.session.query(Account).filter(Account.username == username).first()
    if existing_account is not None:
        return make_response(({
                                  'code': 40004,
                                  'message': '账号已存在'
                              }, 200, headers))

    new_account = Account(username=username, password=generate_password_hash(password),
                          role_id=role_id, status=status)
    db.session.add(new_account)
    db.session.commit()

    existing_account = db.session.query(Account).filter(Account.username == username).first()

    if existing_account is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '创建账号失败'
                              }, 200, headers))

    return make_response(({
                              'code': 20000,
                              'message': 'success'
                          }, 200, headers))


@app.route('/api/account/update', methods=['POST'])
def account_update():
    data = request.get_json()
    username = data['username']
    # password = data['password']
    # role_id = data['role']
    # status = data['status']
    existing_account = db.session.query(Account).filter(Account.username == username).first()
    if existing_account is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '账号不存在'
                              }, 200, headers))

    new_account = db.session.query(Account).filter(Account.username == username).update(data)
    db.session.commit()

    return make_response(({
                              'code': 20000,
                              'message': '账号信息更新成功'
                          }, 200, headers))


@app.route('/api/account/change_status')
def account_change_status():
    account_id = request.args.get('id')
    target_status = request.args.get('status')
    db.session.query(Account).filter(Account.id == account_id).update({'status': target_status})
    db.session.commit()
    # print(f'{account_id}, {target_status}')
    return make_response(({'code': 20000, 'message': '帐号状态改变成功'}, 200, headers))


@app.route('/api/account/delete/<int:id>')
def account_delete(id):
    account_id = id
    db.session.query(Account).filter(Account.id == account_id).delete()
    db.session.commit()
    # print(f'{account_id}, {target_status}')
    return make_response(({'code': 20000, 'message': '帐号删除改变成功'}, 200, headers))


@app.route('/api/role/list')
def role_list():
    data_by_query = db.session.query(Role).all()

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        result_data.append(row_dict)

    response = {
        'code': 20000,
        'data': {
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/department/list')
def department_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = Department.id if request.args.get('sort') == '+id' else Account.id.desc()

    data_by_query = db.session.query(Department).order_by(sort).offset((page - 1) * limit).limit(limit).all()

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        print(row.superior_department)
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        print(row.superior_department_id)
        if row.superior_department_id is None:
            superior_department_name = '无'
        else:
            superior_department = db.session.query(Department).filter(Department.superior_department == row.superior_department).first()
            superior_department_name = superior_department.name
        row_dict['superior_department_name'] = superior_department_name
        result_data.append(row_dict)

    count = db.session.query(Department).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))
