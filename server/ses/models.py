import datetime

import sqlalchemy
from werkzeug.security import generate_password_hash

from ses.routes import db


class Role(db.Model):
    """角色

    角色名称, 角色说明, 角色权限"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250))
    routes = db.Column(db.Text)
    account = sqlalchemy.orm.relationship('Account')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Role %r>' % self.name

    @classmethod
    def add_admin_role(cls):
        roles = db.session.query(Role).all()
        if len(roles) == 0:
            role = Role(name='admin')
            db.session.add(role)
            db.session.commit()


class Account(db.Model):
    """账户

    用户名, 密码, 角色ID, 人员ID, 账户状态"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer)  # 0:禁用 1:启用 9:已删除
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                        nullable=False)
    # personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
    #                          nullable=False)
    # personnel = db.relationship('Personnel', back_populates="account", uselist=False)

    # backref=db.backref('accounts', lazy=True))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Account %r>' % self.username

    @classmethod
    def add_admin(cls):
        user = db.session.query(Account).filter(Account.username == 'admin').first()
        admin_role = db.session.query(Role).filter(Role.name == 'admin').first()
        if user is None:
            user = Account(username='admin', password=generate_password_hash('123456'), status=1, role_id=admin_role.id)
            db.session.add(user)
            db.session.commit()


class Personnel(db.Model):
    """人员

    人员名称, 工号/学号, 人员类型， 部门ID, 关联账号"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    personnel_code = db.Column(db.Integer, unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),
                              nullable=False)
    # department = db.relationship('Department',
    #                              backref=db.backref('personnel', lazy=True))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = sqlalchemy.orm.relationship('Account', backref=sqlalchemy.orm.backref("personnel", uselist=False))

    score_record = sqlalchemy.orm.relationship('ScoreRecord')

    is_student = db.Column(db.Integer, default=0, nullable=False)

    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Personnel %r>' % self.name


class Department(db.Model):
    """部门(组织)

    部门名称, 上一级组织ID, 组织说明"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250))
    # 自引关系
    superior_department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    # superior_department = sqlalchemy.orm.relationship('Department', remote_side=[id])
    personnel = sqlalchemy.orm.relationship('Personnel')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # backref=db.backref('Department', lazy=True))

    def __repr__(self):
        return '<Department %r>' % self.name


class ScoreRecord(db.Model):
    """成绩记录

    学生ID, 分数类型ID, 分值, 评分依据, 获得学期"""
    __tablename__ = "score_record"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
                           nullable=False)
    score_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer)
    evaluation_material_id = db.Column(db.Integer, db.ForeignKey('evaluation_material.id'))
    # evaluation_material = sqlalchemy.orm.relationship(
    #     "EvaluationMaterial", )  # backref=sqlalchemy.orm.backref("score_record", uselist=False))
    status = db.Column(db.Integer)  # 0:拒绝 1:审核通过 9:审核中
    description = db.Column(db.Text)
    gain_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 获得时间

    def __repr__(self):
        return '<ScoreRecord %r>' % self.name


class EvaluationMaterial(db.Model):
    """评价材料

    材料路径"""
    __tablename__ = "evaluation_material"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text, nullable=False)
    # score_record_id = db.Column(db.Integer, db.ForeignKey('score_record.id'))

    def __repr__(self):
        return '<EvaluationMaterial %r>' % self.name


class EvaluationRecord(db.Model):
    """评优记录

    奖项名称, 获得日期, 获得者ID"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    release_datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
                             nullable=False)

    gain_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 获得时间

    # rule_id = db.Column(db.Integer, db.ForeignKey('evaluation_rule.id'),
    #                     nullable=False)
    # rule = db.Column(db.String(300))

    def __repr__(self):
        return '<EvaluationRecord %r>' % self.name
