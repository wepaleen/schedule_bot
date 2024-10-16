
TOKEN='7413059401:AAEdBL7cCPcoqjSTT3CKvn-LeFytuseruAI'
# Список ID администраторов
admin_ids = [820372096]  # Замените на реальные ID администраторов
# Подключение к БД

def db_connection():
    address = f"postgresql://{username}:{password}@{localhost}/{dbname}"
    return address

# имя пользователя БД
username = "admin"
# Пароль к БД
password = "234dfgdf"
# Адрес хоста с БД
localhost = "45.151.30.108"
# Имя БД
dbname = "tg_db_postgres"