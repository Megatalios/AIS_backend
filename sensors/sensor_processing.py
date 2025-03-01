# Функции для работы с расчетом массового расхода воздуха и длительностью впрыска
#----------------------------------
from users.models import User # Импорт модели User из приложения users


def process_sensor_data_for_user(user_id, sensor_data):
    try:
        user = User.objects.get(id=user_id) # Получаем пользователя по ID, используя Django ORM
        # ... (дальнейшая обработка sensor_data, связанная с user) ...
        print(f"Обрабатываем данные датчиков для пользователя: {user.name}")
    except User.DoesNotExist:
        print(f"Пользователь с ID {user_id} не найден.")

def estimate_mass_air_flow(engine_rpm, intake_air_temperature_c):
    """
    Оценка массового расхода воздуха (MAF) на основе оборотов двигателя и температуры воздуха.

    Args:
        engine_rpm: Обороты двигателя (об/мин).
        intake_air_temperature_c: Температура воздуха на впуске (°C).

    Returns:
        float: Оцененный MAF в г/с, или None в случае ошибки.
        str: Сообщение об ошибке, если есть.
    """
    if not isinstance(engine_rpm, (int, float)) or not isinstance(intake_air_temperature_c, (int, float)):
        return None, "Ошибка: обороты и температура должны быть числами."
    if engine_rpm < 0 or intake_air_temperature_c < -50: # Минимальные разумные значения
        return None, "Ошибка: недопустимые значения оборотов или температуры."

    # Упрощенная модель: MAF пропорционален оборотам и обратно пропорционален температуре (приблизительно)
    # Коэффициенты (42.0, 273.15, 20) подобраны очень приблизительно и требуют калибровки под конкретный двигатель!
    base_maf = 42.0  # Базовое значение MAF при определенных условиях (требуется калибровка)
    temperature_kelvin = intake_air_temperature_c + 273.15 # Перевод в Кельвины
    estimated_maf = base_maf * (engine_rpm / 1000) * (293.15 / temperature_kelvin) # 293.15K = 20°C - опорная температура

    return estimated_maf, None


def estimate_injection_duration(mass_air_flow_gs, engine_rpm):
    """
    Оценка длительности впрыска топлива на основе массового расхода воздуха и оборотов двигателя.
    Модель упрощена. Реальная длительность впрыска зависит от множества факторов.

    Args:
        mass_air_flow_gs: Массовый расход воздуха (г/с).
        engine_rpm: Обороты двигателя (об/мин).

    Returns:
        float: Оцененная длительность впрыска в мс, или None в случае ошибки.
        str: Сообщение об ошибке, если есть.
    """
    if not isinstance(mass_air_flow_gs, (int, float)) or not isinstance(engine_rpm, (int, float)):
        return None, "Ошибка: MAF и обороты должны быть числами."
    if mass_air_flow_gs < 0 or engine_rpm < 0:
        return None, "Ошибка: недопустимые значения MAF или оборотов."

    # Упрощенная модель: Длительность впрыска пропорциональна MAF и обратно пропорциональна оборотам (приблизительно)
    # Коэффициенты (0.08, 1000) очень приблизительные и требуют калибровки!
    
    base_injection_duration = 0.08 # Базовая длительность впрыска (требуется калибровка)
    estimated_duration_ms = base_injection_duration * (mass_air_flow_gs / (engine_rpm / 1000)) # Приведение RPM к тысячам

    return estimated_duration_ms, None
