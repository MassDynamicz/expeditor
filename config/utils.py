# config/utils.py

# хэширования паролей
from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

# форматирование даты
from datetime import datetime
def format_date(date_str):
    if date_str == '' or not isinstance(date_str, str):
        return None
    date_formats = [
        "%d.%m.%Y",  # формат "01.06.2024"
        "%Y-%m-%d %H:%M:%S",  # формат "2024-06-01 07:45:00"
        "%d.%m.%Y, %H:%M",  # формат "09.06.2024, 04:17"
        "%d.%m.%Y, %H:%M:%S"  # формат "17.06.2024, 20:57:38"
    ]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Невозможно распознать формат даты: {date_str}")