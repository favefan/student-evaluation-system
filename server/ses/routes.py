from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ses import app, db
from ses.models import Account, Role, Department, ScoreRecord, EvaluationRecord

# db = SQLAlchemy()
# migrate = Migrate()
#
# app = Flask(__name__, instance_relative_config=True)
# app.config.from_object(config)
#
# db.init_app(app)
# migrate.init_app(app, db)

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST'
}


@app.route('/api/routes')
def routes_list():
    pass


"""登录模块
* 登录
* 登出
"""


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data['username'], data['password']
    account = db.session.query(Account).filter(Account.username == username).first()

    if account is None:
        response = {
            'code': 60204,
            'message': '账号不存在'
        }
    elif check_password_hash(account.password, password):
        response = {
            'code': 20000,
            'data': {
                'token': account.id
            }
        }
    else:
        response = {
            'code': 60204,
            'message': '账号或密码错误'
        }
    return make_response((response, 200, headers))


@app.route('/api/logout', methods=['POST'])
def logout():
    pass


"""角色管理模块
* 角色分页查询
* 角色创建
* 角色修改
* 角色删除
"""


@app.route('/api/role/list')
def role_list():
    """角色分页查询"""
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


@app.route('/api/role/create', methods=['POST'])
def role_create():
    pass


@app.route('/api/role/update', methods=['POST'])
def role_update():
    pass


@app.route('/api/role/delete')
def role_delete():
    pass


"""账户管理模块
* 账号分页查询
* 账号信息查询(通过id/token)
* 账号创建
* 账号修改
* 账号状态切换
* 账号删除
"""


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


@app.route('/api/account/info')
def account_info():
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


@app.route('/api/account/state', methods=['PUT'])
def account_state():
    account_id = request.args.get('id')
    target_status = request.args.get('status')
    db.session.query(Account).filter(Account.id == account_id).update({'status': target_status})
    db.session.commit()
    return make_response(({'code': 20000, 'message': '帐号状态改变成功'}, 200, headers))


@app.route('/api/account/delete/<int:id>')
def account_delete(id):
    account_id = id
    db.session.query(Account).filter(Account.id == account_id).delete()
    db.session.commit()
    return make_response(({'code': 20000, 'message': '帐号删除改变成功'}, 200, headers))


"""人员管理模块
* 人员分页查询
* 人员创建
* 人员修改
* 人员删除
"""


@app.route('/api/personnel/list')
def personnel_list():
    pass


@app.route('/api/personnel/create', methods=['POST'])
def personnel_create():
    pass


@app.route('/api/personnel/update', methods=['POST'])
def personnel_update():
    pass


@app.route('/api/personnel/delete')
def personnel_delete():
    pass


"""部门管理模块
* 部门分页查询
* 部门创建
* 部门修改
* 部门删除
"""


@app.route('/api/department/list')
def department_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = Department.id if request.args.get('sort') == '+id' else Department.id.desc()

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
            superior_department = db.session.query(Department).filter(
                Department.superior_department == row.superior_department).first()
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


@app.route('/api/department/create', methods=['POST'])
def department_create():
    pass


@app.route('/api/department/update', methods=['POST'])
def department_update():
    pass


@app.route('/api/department/delete')
def department_delete():
    pass


"""成绩管理模块
* 成绩分页查询
* 成绩创建
* 成绩修改
* 成绩删除
"""


@app.route('/api/score/list')
def score_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = ScoreRecord.id if request.args.get('sort') == '+id' else ScoreRecord.id.desc()

    data_by_query = db.session.query(ScoreRecord).order_by(sort).offset((page - 1) * limit).limit(limit).all()

    print([u.__dict__ for u in data_by_query])

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        em_list = []
        for r in row.evaluation_material:
            r_dict = r.__dict__
            if '_sa_instance_state' in r_dict:
                del r_dict['_sa_instance_state']
            em_list.append((r_dict))
        row_dict['evaluation_material_list'] = em_list
        result_data.append(row_dict)
    print(result_data)

    count = db.session.query(ScoreRecord).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/score/create', methods=['POST'])
def score_create():
    pass


@app.route('/api/score/update', methods=['POST'])
def score_update():
    pass


@app.route('/api/score/delete')
def score_delete():
    pass


@app.route('/api/score/apply')
def score_apply():
    pass


@app.route('/api/score/audit')
def score_audit():
    pass


@app.route('/api/score/import')
def score_import():
    pass


"""评优记录管理模块
* 评优分页查询
* 评优生成
* 评优修改
* 评优删除
"""


@app.route('/api/evaluation/list')
def evaluation_list():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = EvaluationRecord.id if request.args.get('sort') == '+id' else EvaluationRecord.id.desc()

    data_by_query = db.session.query(EvaluationRecord).order_by(sort).offset((page - 1) * limit).limit(limit).all()

    print([u.__dict__ for u in data_by_query])

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        em_list = []
        for r in row.evaluation_material:
            r_dict = r.__dict__
            if '_sa_instance_state' in r_dict:
                del r_dict['_sa_instance_state']
            em_list.append((r_dict))
        row_dict['evaluation_material_list'] = em_list
        result_data.append(row_dict)
    print(result_data)

    count = db.session.query(EvaluationRecord).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/evaluation/create', methods=['POST'])
def evaluation_create():
    pass


@app.route('/api/evaluation/update', methods=['POST'])
def evaluation_update():
    pass


@app.route('/api/evaluation/delete')
def evaluation_delete():
    pass

@app.route('/api/evaluation/export')
def evaluation_export():
    pass







