#!/usr/bin/env python
# coding=utf-8

"""
Файл для запуска управляющих команд из консоли.
"""

from flask_script import Manager
from app import app
from flask_migrate import MigrateCommand

manager = Manager(app)

manager.add_command('db', MigrateCommand)
"""
Команды для работы с базами данных
"""


@manager.command
def runserver(host='127.0.0.1', port='5000', debug='True'):
    """ Запуск отладочного сервера. """
    is_debug = debug == 'True'
    app.run(host=host, port=int(port), debug=is_debug)

if __name__ == "__main__":
    manager.run()
