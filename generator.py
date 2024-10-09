import sqlite3
import random
from datetime import datetime, timedelta

# Подключение к базе данных SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Создание таблицы заказов, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS apps_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_fio TEXT,
    client_phone TEXT,
    client_tg TEXT,
    product_name TEXT,
    quantity INTEGER,
    sell_price REAL,
    address TEXT,
    description TEXT,
    priority TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
)
''')

# Функция для генерации случайной даты в этом году
def random_date():
    start_date = datetime(datetime.now().year, 1, 1, 0, 0, 0, 0)
    end_date = datetime.now()
    random_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
        microseconds=random.randint(0, 999999)
    )
    return random_date.strftime("%Y-%m-%d %H:%M:%S.%f")

# Списки для генерации случайных данных
products = [(1, 450), (2, 420), (3, 350)]
client_tg = ['@client_tg_1', '@client_tg_2', '@client_tg_3', '@client_tg_4', '@client_tg_5']
client_phone = ['+79001234567', '+79001234568', '+79001234569', '+79001234570', '+79001234571']
client_fio = ['Клиент 1', 'Клиент 2', 'Клиент 3', 'Клиент 4', 'Клиент 5']
priorities = ['Низкий', 'Средний', 'Высокий']
statuses = ['Новый', 'В обработке', 'Выполнен', 'Отменен']

# Генерация 1000 заказов
for _ in range(1000):
    product, price = random.choice(products)
    quantity = random.randint(1, 10)
    cost_price = price * quantity
    markup = random.uniform(1.3, 1.4)  # 30-40% наценка
    sell_price = round(cost_price * markup)
    date = random_date()

    cursor.execute('''
    INSERT INTO apps_orders (client_fio, client_phone, client_tg, product_id, quantity, sell_price, address, description, priority, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        random.choice(client_fio),
        random.choice(client_phone),
        random.choice(client_tg),
        product,
        quantity,
        sell_price,
        f"{random.randint(1, 10)}",
        f"{random.randint(1, 10)}",
        random.choice(priorities),
        random.choice(statuses),
        date,
        date
    ))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Успешно создано 1000 заказов в базе данных SQLite.")