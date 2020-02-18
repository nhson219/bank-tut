from .. import db, flask_bcrypt

class UserAccount(db.Model):
    __tablename__ = 'user_accounts'

    AccountId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(100))

    @property
    def password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User Account '{}'>".format(self.username)

