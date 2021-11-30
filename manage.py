from flask_script import Manager, Command, Option
from flask_migrate import MigrateCommand, Migrate
from src import db, app
from src.Config.Backup import DatabaseBackup


manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)
manager.add_command('backup', DatabaseBackup)


if __name__ == '__main__':
    manager.run()