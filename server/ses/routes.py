import sqlalchemy
from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import xlrd

from ses import app, db
from ses.models import Account, Role, Department, ScoreRecord, EvaluationRecord, Personnel, EvaluationMaterial

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
    return make_response(({}, 200, headers))


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
    return make_response(({'code': 20000, 'message': 'success'}, 200, headers))


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
    username = request.args.get('username', None)
    if username is None:
        data_by_query = db.session.query(Account).order_by(sort).offset((page - 1) * limit).limit(limit).all()
    else:
        data_by_query = db.session.query(Account).filter(Account.username.like(f'%{username}%')) \
            .order_by(sort).offset((page - 1) * limit).limit(limit).all()

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
    original_username = data['original_username']
    existing_account = db.session.query(Account).filter(Account.username == original_username).first()
    if existing_account is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '账号不存在'
                              }, 200, headers))

    new_account = db.session.query(Account).filter(Account.username == original_username) \
        .update({'username': data['username'], 'password': generate_password_hash(data['password']),
                 'status': data['status'], 'role_id': data['role_id']})
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
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    sort = Personnel.id if request.args.get('sort') == '+id' else Personnel.id.desc()
    name = request.args.get('name', None)
    if name is None:
        data_by_query = db.session.query(Personnel).order_by(sort).offset((page - 1) * limit).limit(limit).all()
    else:
        data_by_query = db.session.query(Personnel).filter(Personnel.name.like(f'%{name}%')) \
            .order_by(sort).offset((page - 1) * limit).limit(limit).all()

    # all_accounts = db.session.query(Account).all()
    # all_department = db.session.query(Department).all()

    result_data = []
    for row in data_by_query:
        row_dict = row.__dict__
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        account_username = db.session.query(Account).filter(Account.id == row.account_id).first().username
        account_status = db.session.query(Account).filter(Account.id == row.account_id).first().status
        department_name = db.session.query(Department).filter(Department.id == row.department_id).first().name
        row_dict['account_username'] = account_username
        row_dict['account_status'] = account_status
        row_dict['department_name'] = department_name
        result_data.append(row_dict)

    count = db.session.query(Personnel).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/personnel/create', methods=['POST'])
def personnel_create():
    data = request.get_json()
    name = data['name']
    personnel_code = data['personnel_code']
    department_id = data['department']
    account_status = data['account_status']
    is_student = data['is_student']
    existing_personnel = db.session.query(Personnel).filter(Personnel.personnel_code == personnel_code).first()
    if existing_personnel is not None:
        return make_response(({
                                  'code': 40004,
                                  'message': '人员已存在'
                              }, 200, headers))

    new_account = Account(username=personnel_code, password=generate_password_hash(personnel_code),
                          role_id=1, status=account_status)
    db.session.add(new_account)
    db.session.commit()

    existing_account = db.session.query(Account).filter(Account.username == personnel_code).first()

    new_personnel = Personnel(name=name, personnel_code=personnel_code,
                              department_id=department_id, account_id=existing_account.id, is_student=is_student)

    db.session.add(new_personnel)
    db.session.commit()

    existing_personnel = db.session.query(Personnel).filter(Personnel.personnel_code == personnel_code).first()

    if existing_account is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '创建人员失败'
                              }, 200, headers))

    return make_response(({
                              'code': 20000,
                              'message': '创建人员成功'
                          }, 200, headers))


@app.route('/api/personnel/update', methods=['POST'])
def personnel_update():
    data = request.get_json()
    id = data['id']
    account_id = data['account_id']
    existing_personnel = db.session.query(Personnel).filter(Personnel.id == id).first()
    if existing_personnel is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '人员不存在'
                              }, 200, headers))

    new_account = db.session.query(Account).filter(Account.id == account_id) \
        .update({'status': data['account_status']})
    db.session.commit()

    new_personnel = db.session.query(Personnel).filter(Personnel.id == existing_personnel.id) \
        .update({'name': data['name'], 'personnel_code': data['personnel_code'],
                 'department_id': data['department']})
    db.session.commit()

    return make_response(({
                              'code': 20000,
                              'message': '人员信息更新成功'
                          }, 200, headers))


@app.route('/api/personnel/delete/<int:id>')
def personnel_delete(id):
    personnel_id = id
    existing_personnel = db.session.query(Personnel).filter(Personnel.id == personnel_id).first()
    account_id = existing_personnel.account_id
    existing_score_record = db.session.query(ScoreRecord).filter(
        ScoreRecord.student_id == existing_personnel.id).first()
    if existing_score_record is not None:
        ems = db.session.query(EvaluationMaterial).filter(
            EvaluationMaterial.score_record_id == existing_score_record.id)
        ems.delete() if ems is not None else None
    srs = db.session.query(ScoreRecord).filter(ScoreRecord.student_id == existing_personnel.id)
    srs.delete() if srs is not None else None
    ers = db.session.query(EvaluationRecord).filter(EvaluationRecord.personnel_id == existing_personnel.id)
    ers.delete() if ers is not None else None
    db.session.query(Personnel).filter(Personnel.id == personnel_id).delete()
    db.session.query(Account).filter(Account.id == account_id).delete()
    db.session.commit()
    return make_response(({'code': 20000, 'message': '人员及惯量账号删除成功'}, 200, headers))


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/personnel/upload', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        file = request.files.get('file')
        f = file.read()
        clinic_file = xlrd.open_workbook(file_contents=f)
        # sheet1
        table = clinic_file.sheet_by_index(0)
        nrows = table.nrows
        for i in range(2, nrows):
            # new = RenyuanQuanxian()
            row_data = table.row_values(i)
            print(row_data)
            # print(row_date)
            # new.账户 = str(row_date[1])
            # new.密码 = str(row_date[2])
            # db.session.add(new)
            # db.session.commit()
            # db.session.close()
    return make_response(({}, 200, headers))


@app.route('/api/personnel/upload_content/<int:is_student>', methods=['POST'])
def upload_excel_content(is_student):
    data = request.get_json()
    for row in data:
        existing_personnel = db.session.query(Personnel).filter(Personnel.personnel_code == row['工号']).first()
        if existing_personnel is not None:
            return make_response(({
                                      'code': 40004,
                                      'message': '人员已存在'
                                  }, 200, headers))

        new_account = Account(username=row['工号'], password=generate_password_hash(str(row['工号'])),
                              role_id=1, status=row['帐号状态'])
        db.session.add(new_account)
        db.session.commit()

        existing_account = db.session.query(Account).filter(Account.username == str(row['工号'])).first()

        existing_department = db.session.query(Department).filter(Department.name == row['部门']).first()

        new_personnel = Personnel(name=row['姓名'], personnel_code=row['工号'],
                                  department_id=existing_department.id, account_id=existing_account.id, is_student=is_student)

        db.session.add(new_personnel)
        db.session.commit()

        existing_personnel = db.session.query(Personnel).filter(Personnel.personnel_code == row['工号']).first()

        if existing_account is None:
            return make_response(({
                                      'code': 40004,
                                      'message': f'{row["姓名"]}创建人员失败'
                                  }, 200, headers))

    return make_response(({
                              'code': 20000,
                              'message': '所有创建人员成功'
                          }, 200, headers))


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
        # print(row.superior_department)
        if '_sa_instance_state' in row_dict:
            del row_dict['_sa_instance_state']
        print(row.superior_department_id)
        if row.superior_department_id is None:
            superior_department_name = '无'
        else:
            for d in data_by_query:
                if d.id == row.superior_department_id:
                    superior_department_name = d.name
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
    data = request.get_json()
    name = data['name']
    superior_department_id = data.get('superiorDepartment', None)
    description = data['description']
    existing_department = db.session.query(Department).filter(Department.name == name).first()
    if existing_department is not None:
        return make_response(({
                                  'code': 40004,
                                  'message': '账号已存在'
                              }, 200, headers))

    new_department = Department(name=name, superior_department_id=superior_department_id,
                                description=description)
    db.session.add(new_department)
    db.session.commit()

    existing_department = db.session.query(Department).filter(Department.name == name).first()

    if existing_department is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '创建账号失败'
                              }, 200, headers))

    return make_response(({
                              'code': 20000,
                              'message': 'success'
                          }, 200, headers))


@app.route('/api/department/update', methods=['POST'])
def department_update():
    data = request.get_json()
    id = data['id']
    existing_department = db.session.query(Department).filter(Department.id == id).first()
    if existing_department is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '账号不存在'
                              }, 200, headers))

    new_department = db.session.query(Department).filter(Department.name == existing_department.name) \
        .update({'name': data['name'], 'description': data['description'],
                 'superior_department_id': data['superior_department_id']})
    db.session.commit()

    return make_response(({
                              'code': 20000,
                              'message': '组织信息更新成功'
                          }, 200, headers))


@app.route('/api/department/delete/<int:id>')
def department_delete(id):
    department_id = id
    try:
        db.session.query(Department).filter(Department.id == department_id).delete()
    except sqlalchemy.exc.IntegrityError as e:
        return make_response(({'code': 50000, 'message': str(e)}, 500, headers))
    else:
        db.session.commit()
    return make_response(({'code': 20000, 'message': '组织删除成功'}, 200, headers))


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
        student = db.session.query(Personnel).filter(Personnel.id == row.student_id).first()
        row_dict['student_name'] = student.name
        row_dict['personnel_code'] = student.personnel_code
        result_data.append(row_dict)


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
    data = request.get_json()
    name = data['name']
    personnel_code = data['personnel_code']
    score_type = data['score_type']
    score = data['score']
    gain_time = data['gain_time']

    student = db.session.query(Personnel).filter(Personnel.personnel_code == personnel_code).first()

    new_record = ScoreRecord(name=name, student_id=student.id,
                             score_type=score_type, score=score, gain_time=gain_time, status=1)

    db.session.add(new_record)
    db.session.commit()

    # existing_personnel = db.session.query(Personnel).filter(Personnel.personnel_code == personnel_code).first()
    #
    # if existing_account is None:
    #     return make_response(({
    #                               'code': 40004,
    #                               'message': '创建人员失败'
    #                           }, 200, headers))

    return make_response(({
                              'code': 20000,
                              'message': '创建人员成功'
                          }, 200, headers))


@app.route('/api/score/update', methods=['POST'])
def score_update():
    data = request.get_json()
    id = data['id']
    existing_record = db.session.query(ScoreRecord).filter(ScoreRecord.id == id).first()
    if existing_record is None:
        return make_response(({
                                  'code': 40004,
                                  'message': '成绩记录不存在'
                              }, 200, headers))

    student = db.session.query(Personnel).filter(Personnel.personnel_code == data['personnel_code']).first()

    new_record = db.session.query(ScoreRecord).filter(ScoreRecord.id == existing_record.id) \
        .update({'name': data['name'], 'student_id': student.id,
                 'score_type': data['score_type'], 'score': data['score'], 'gain_time': data['gain_time']})
    db.session.commit()

    return make_response(({
                              'code': 20000,
                              'message': '成绩更新成功'
                          }, 200, headers))


@app.route('/api/score/delete/<int:id>')
def score_delete(id):
    try:
        db.session.query(ScoreRecord).filter(ScoreRecord.id == id).delete()
    except sqlalchemy.exc.IntegrityError as e:
        return make_response(({'code': 50000, 'message': str(e)}, 500, headers))
    else:
        db.session.commit()
    return make_response(({'code': 20000, 'message': '成绩删除成功'}, 200, headers))


@app.route('/api/score/apply')
def score_apply():
    pass


@app.route('/api/score/audit')
def score_audit():
    pass


@app.route('/api/score/import', methods=['POST'])
def score_import():
    data = request.get_json()
    for row in data:
        student = db.session.query(Personnel).filter(Personnel.personnel_code == row['学号']).first()

        new_record = ScoreRecord(name=row['成绩名称'], student_id=student.id, score_type=row['分数类型'],
                                 score=row['分数'], status=1)
        db.session.add(new_record)

        db.session.commit()


    return make_response(({
                              'code': 20000,
                              'message': '所有成绩添加成功'
                          }, 200, headers))


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
        result_data.append(row_dict)

    count = db.session.query(EvaluationRecord).count()

    response = {
        'code': 20000,
        'data': {
            'total': count,
            'items': result_data
        }
    }

    return make_response((response, 200, headers))


@app.route('/api/evaluation/create')
def evaluation_create():
    all_students = db.session.query(Personnel).filter(Personnel.is_student == 1).all()
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
