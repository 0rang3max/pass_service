import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Настраиваем и подымаем Flask
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Разрешенные символы
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'

symbols = list(letters) + list(letters.upper()) + list(numbers)
col_symbols = 4


class Keys(db.Model):
    # таблица с ключами
    key = db.Column(db.String, primary_key=True)
    used = db.Column(db.Boolean, default=False)


@app.route('/create_key')
def create_key():
    """
    Выдача уникальных ключей. По обращению к сервису происходит выдача ключа клиенту
    """

    key = ''
    left_symbols = symbols[:]

    while len(key) < col_symbols:
        # Пока длинна собираемого ключа меньше необходимой

        # Берем случайный символ из тех которые еще не пробовали
        symbol = left_symbols[random.randint(0, len(left_symbols) - 1)]
        possible_key = f"{key}{symbol}" # Начало генерируемого ключа

        # Количество возможных ключей с таким началом
        possible_combos = len(symbols) ** (col_symbols - len(possible_key))

        #Количество существующих ключей начинающихся так же
        existing_combos = Keys.query.filter(Keys.key.like(f"{possible_key}%")).count()

        # Если все ключи с таким сочетанием в начале еще НЕ сгенерированы
        if existing_combos < possible_combos:
            key = str(possible_key)
            left_symbols = symbols[:]
        else:
            # Иначе убираем символ из набора
            left_symbols.remove(symbol)

            if len(left_symbols) == 0:
                # если больше нечего пробовать
                return 'Ключей больше не осталось!'

    #Добавляем ключ
    db.session.add(Keys(key=key))
    db.session.commit()

    return key


@app.route('/use_key/<string:key>')
def use_key(key):
    """
    Погашение ключа. Помечает ключ как использованный. Повторно погасить ключ нельзя. Нельзя погасить ключ, если он не был предварительно выдан клиенту.
    """
    stored_key = Keys.query.filter_by(key=key).first()
    if stored_key:
        if stored_key.used:
            return 'Уже погашен'

        stored_key.used = True
        db.session.commit()

        return f'Ключ {key} погашен'

    return 'Не выдан'


@app.route('/check_key/<string:key>')
def check_key(key):
    """
    Проверка ключа. Возвращает информацию информацию о ключе: не выдан, выдан, погашен.
    """
    stored_key = Keys.query.filter_by(key=key).first()
    if stored_key:
        return 'Погашен' if stored_key.used else 'Выдан'
    return 'Не выдан'


@app.route('/left_keys')
def left_keys():
    """
    Информация о количестве оставшихся, не выданных ключей
    """
    possible_combos = len(symbols) ** col_symbols
    existing_combos = Keys.query.count()
    return str(possible_combos - existing_combos)
