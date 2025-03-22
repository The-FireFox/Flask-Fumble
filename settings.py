

SECRET_KEY = 'hardpassword' # Because who needs an easy one?

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{host}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'main_root',
        password = 'welcome',
        host = 'localhost',
        database = 'api4noobs'
    )