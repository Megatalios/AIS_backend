import random
import string
from locust import HttpUser, TaskSet, task

def generate_vin():
    """Генерирует случайный VIN-номер."""
    # Символы, которые могут использоваться в VIN-номере
    allowed_chars = string.ascii_uppercase + string.digits
    forbidden_chars = "I", "O", "Q"
    # Длина VIN-номера
    vin_length = 17
    # Генерируем VIN-номер
    vin = "".join(random.choice([char for char in allowed_chars if char not in forbidden_chars]) for _ in range(vin_length))
    return vin

# Необходимые для нагрузочного тестирования методы
def get_all_users(l):
    l.client.get("/users/all/")

def get_all_cars(l):
    l.client.get("/cars/all/")








class WebsiteUser(HttpUser):
    @task(2)
    def get_users(self):
        get_all_users(self)

    @task(1)
    def get_cars(self):
        get_all_cars(self)

    min_wait = 5000
    max_wait = 9000




