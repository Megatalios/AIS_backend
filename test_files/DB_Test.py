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


# Необходимые для объемного тестирования методы
def add_new_user(l):
    data =  {
        "name": "test_name", 
        "email": generate_vin() + "@mail.test"
        }
    l.client.post("/users/add/", json=data)


def add_new_car(l):
    data={
        "vin_number": generate_vin(),
        "color": "Red",   
        "brand": "Toyota",   
        "owner_id": 1
        }
    l.client.post("/cars/add/", json=data)


    
class DataBaseUser(HttpUser):
    @task(1)
    def add_new_user(self):
        add_new_user(self)
    
    @task(2)
    def add_new_car(self):
        add_new_car(self)
    
    min_wait = 5000
    max_wait = 9000