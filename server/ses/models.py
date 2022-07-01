import datetime

from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Role(db.Model):
    """角色
    
    角色名称, 角色说明, 角色权限"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250))
    permission = None
    account = db.relationship('Account', back_populates='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Account(db.Model):
    """账户
    
    用户名, 密码, 角色ID, 人员ID, 账户状态"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer)  # 0:禁用 1:启用 9:已删除
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                        nullable=False)
    role = db.relationship('Role', back_populates='accounts_role')
                           # backref=db.backref('accounts', lazy=True))
    # personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
    #                          nullable=False)
    personnel = db.relationship('Personnel', back_populates="account", uselist=False)
                                # backref=db.backref('accounts', lazy=True))

    def __repr__(self):
        return '<Account %r>' % self.username


class Personnel(db.Model):
    """人员
    
    人员名称, 工号/学号, 人员类型， 部门ID, 关联账号"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    personnel_code = db.Column(db.Integer, unique=True, nullable=False)
    type = None
    sex = None
    age = None
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),
                              nullable=False)
    department = db.relationship('Department',
                                 backref=db.backref('personnel', lazy=True))

    account_id = db.Column(db.Integer, db.ForeignKey('account_id'))
    account = db.relationship('Account', back_populates='personnel')

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
    superior_department = db.relationship('Department', remote_side=[id])
                                          #backref=db.backref('Department', lazy=True))

    def __repr__(self):
        return '<Department %r>' % self.name


class ScoreRecord(db.Model):
    """成绩记录

    学生ID, 分数类型ID, 分值, 评分依据, 获得学期"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
                           nullable=False)
    score_type_id = None
    score = db.Column(db.Integer)
    material_id = db.Column(db.Integer, db.ForeignKey('evaluation_material.id'),
                            nullable=False)

    def __repr__(self):
        return '<ScoreRecord %r>' % self.name


# class ScoreType(db.Model):
#     """分数类型"""
#     id = db.Column(db.Integer, primary_key=True)
#
#     def __repr__(self):
#         return '<ScoreType %r>' % self.name


# class EvaluationRule(db.Model):
#     """评价规则
#
#     规则名称, 规则表达式"""
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     rule = db.Column(db.String(250))
#
#     def __repr__(self):
#         return '<EvaluationRule %r>' % self.name


class EvaluationMaterial(db.Model):
    """评价材料

    材料路径"""
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(300))

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
    # rule_id = db.Column(db.Integer, db.ForeignKey('evaluation_rule.id'),
    #                     nullable=False)
    # rule = db.Column(db.String(300))

    def __repr__(self):
        return '<EvaluationRecord %r>' % self.name
