from sqladmin import Admin
from mysite.database.db import engine


def create_admin(app) -> Admin:
    admin = Admin(app, engine, title="admin")
    return admin
