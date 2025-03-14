document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculateButton").addEventListener("click", sendSensorData);
});
function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}


function getUserId() {
    return fetch('/sensors/get_user_info/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            return data.user_id;
        });
}

// Первый запрос на сохранение датчиков в бд
// Сначала пробуем обновить (PUT), если не найдено, то создаем (POST)
function sendSensorData() {
    const vinNumber = document.getElementById('car_vin').value;
    getUserId()
    .then(userId => {
        if (!userId) throw new Error("User ID is missing");
        
        return fetch(`/cars/get_car_id/?vin_number=${vinNumber}`)
            .then(response => response.json())
            .then(carData => {
                if (!carData.car_id) throw new Error("Car ID not found for VIN " + vinNumber);
                return { userId, carId: carData.car_id };
            });
    })
    .then(({ userId, carId }) => {
        return fetch(`/sensors/check/?car_id=${carId}&user_id=${userId}`)
            .then(response => response.json())
            .then(sensorCheck => {
                return { userId, carId, sensorCheck };
            });
    })
    .then(({ userId, carId, sensorCheck }) => {
        const engineRpm = document.getElementById('engine_rpm').value;
        if (!engineRpm) throw new Error("Engine RPM is missing");

        const sensorData = {
            car_vin: vinNumber,
            user_id: userId,
            engine_rpm: engineRpm,
            intake_air_temperature: document.getElementById('intake_air_temperature').value,
            mass_air_flow_sensor: document.getElementById('mass_air_flow_sensor').value,
            injection_duration: document.getElementById('injection_duration').value,
            throttle_position: document.getElementById('throttle_position').value,
            vehicle_speed: document.getElementById('vehicle_speed').value,
            manifold_absolute_pressure: document.getElementById('manifold_absolute_pressure').value
        };


        const url = sensorCheck.exists
            ? `/sensors/update/${sensorCheck.sensor_data_id}/`
            : `/sensors/add/`;
        const method = sensorCheck.exists ? 'PUT' : 'POST';

        return fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify(sensorData)
        });
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('responseMessage').innerText = "Ошибка: " + data.error;
        } else {
            document.getElementById('responseMessage').innerText = `Данные ${data.sensor_data_id ? "обновлены" : "добавлены"} успешно! ID записи: ${data.sensor_data_id}`;
            fetchSensorData(data.sensor_data_id);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('responseMessage').innerText = "Ошибка: " + error.message;
    });
}



// Второй запрос на создание машины
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addCarButton").addEventListener("click", sendCar);
});
function sendCar() {
    const data_cars = {
        vin_number: document.getElementById('car_vin_2').value,
        brand: document.getElementById('car_brand_2').value,
        color: document.getElementById('car_color_2').value
    };


    fetch('/cars/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data_cars)
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.error) {
            document.getElementById('responseMessageCar').innerText = "Ошибка: " + data.error;
        } else {
            document.getElementById('responseMessageCar').innerText = "Автомобиль добавлен успешно! ID записи: " + data.car_id;
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('responseMessageCar').innerText = "Ошибка при отправке данных.";
    });
}

function fetchSensorData(car_id) {
    fetch(`/sensors/calculate/${car_id}`)
    .then(response => response.json())
    .then(sensorData => {
        if (sensorData.error) {
            document.getElementById('sensorResponse').innerText = "Ошибка: " + sensorData.error;
        } else {
            document.getElementById('sensorContainer').style.display = "block"; // Показываем блок
            document.getElementById('sensorResponse').innerHTML = `
                <strong>Sensor Data ID:</strong> ${sensorData.sensor_data_id} <br>
                <strong>Estimate Mass Air Flow:</strong> ${sensorData.estimate_mass_air_flow.toFixed(4)} <br>
                <strong>Estimate Injection Duration:</strong> ${sensorData.estimate_injection_duration} <br>
                <strong>User ID:</strong> ${sensorData.user_id} <br>
                <strong>Car ID:</strong> ${sensorData.car_id}
            `;
            // После получения данных вызываем сохранение в БД
            saveSensorCalculation(sensorData);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('sensorResponse').innerText = "Ошибка при получении данных датчиков.";
    });
}


function saveSensorCalculation(sensorData) {
    fetch(`/sensors/calculate/save/${sensorData.sensor_data_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Ошибка:", data.error);
        } else {
            // console.log(`Расчёты сохранены! ID: ${data.calculated_id}, Новая запись: ${data.created}`);
        }
    })
    .catch(error => console.error("Ошибка при сохранении данных:", error));
}
