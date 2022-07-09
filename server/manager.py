from flask_migrate import MigrateCommand, Migrate, upgrade
from flask_script import Manager, Server

from ses.routes import app
from ses.models import *

from flask_cors import CORS

manager = Manager(app)
migrate = Migrate(app, db)
# 子命令  MigrateCommand 包含三个方法 init migrate upgrade
manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(host="0.0.0.0", port=8000, use_debugger=True))  # 创建启动命令


@manager.command
def deploy():
    upgrade()
    Role.add_admin_role()
    Account.add_admin()


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    manager.run()
