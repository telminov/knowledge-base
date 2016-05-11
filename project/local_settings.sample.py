SECRET_KEY = '123'


#
# For mysql in python3.5, uncomment if you will Use MySQL database driver
# import pymysql
# pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite',
        'NAME': 'db.sqlite3',
    }
}
