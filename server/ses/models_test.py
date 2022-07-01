import datetime

from ses.__init__ import db
from werkzeug.security import generate_password_hash


class Role(db.Model):
    """角色

    角色名称, 角色说明, 角色权限"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250))
    routes = db.Column(db.Text)
    # account = db.relationship('Account', back_populates='role')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Role %r>' % self.name

    @classmethod
    def add_admin_role(cls):
        roles = db.session.query(Role).all()
        if len(roles) is 0:
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
    # role = db.relationship('Role', back_populates='account')
    # backref=db.backref('accounts', lazy=True))
    # personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'),
    #                          nullable=False)
    personnel = db.relationship('Personnel', back_populates="account", uselist=False)

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

    # def to_json(self):
    #     dict = self.__dict__
    #     if "_sa_instance_state" in dict:
    #         del dict["_sa_instance_state"]
    #     return dict


class Personnel(db.Model):
    """人员

    人员名称, 工号/学号, 人员类型， 部门ID, 关联账号"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    personnel_code = db.Column(db.Integer, unique=True, nullable=False)
    # type = None
    # sex = None
    # age = None
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),
                              nullable=False)
    department = db.relationship('Department',
                                 backref=db.backref('personnel', lazy=True))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', back_populates='personnel')
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
    superior_department = db.relationship('Department', remote_side=[id])
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # backref=db.backref('Department', lazy=True))

    def __repr__(self):
        return '<Department %r>' % self.name
