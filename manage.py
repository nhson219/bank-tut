import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user
from app.main.model import user_account
from app.main.model import customer
from app.main.model import payment_account
from app.main.model import customer_store
from app.main.model import payment_transaction
from app.main.model import payment_history
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# from app.main.model import user, blacklist

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()
app.config['JWT_SECRET_KEY'] = '123456@L'  # Change this!


manager = Manager(app)
jwt = JWTManager(app)

migrate = Migrate(app, db, compare_type=True)

manager.add_command('db', MigrateCommand)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'customer': identity,
    }

@manager.command
def run():
    app.run(debug=True)
    #app.run(host="localhost", port=8000, debug=True)



@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
