document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculateButton").addEventListener("click", sendSensorData);
});
function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}



//Первый запрос на сохранение датчиков в бд
function sendSensorData() {
    const data = {
        car_vin: document.getElementById('car_vin').value,
        // user_id: document.getElementById('user_id').value,
        // user_id: 1,
        engine_rpm: document.getElementById('engine_rpm').value,
        intake_air_temperature: document.getElementById('intake_air_temperature').value,
        mass_air_flow_sensor: document.getElementById('mass_air_flow_sensor').value,
        injection_duration: document.getElementById('injection_duration').value,
        throttle_position: document.getElementById('throttle_position').value,
        vehicle_speed: document.getElementById('vehicle_speed').value,
        manifold_absolute_pressure: document.getElementById('manifold_absolute_pressure').value
    };

    fetch('/sensors/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('responseMessage').innerText = "Ошибка: " + data.error;
        } else {
            document.getElementById('responseMessage').innerText = "Датчики добавлены успешно! ID записи: " + data.sensor_data_id;
            fetchSensorData(data.sensor_data_id);

        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('responseMessage').innerText = "Ошибка при отправке данных.";
    });
}

// Попытка сначала сделать PUT , он работает, но в случае если нет авто, то выдает Not Found: /cars/get_car_id/
// POST не работает
// function sendSensorData() {
//     const vinNumber = document.getElementById('car_vin').value;

//     // 1. Запрашиваем car_id по vin_number
//     fetch(`/cars/get_car_id/?vin_number=${vinNumber}`)
//     .then(response => response.json())
//     .then(carData => {
//         if (!carData.car_id) {
//             document.getElementById('responseMessage').innerText = "Ошибка: автомобиль не найден.";
//             return;
//         }

//         const car_id = carData.car_id;
//         const user_id = 1; // Здесь можно поставить реального пользователя, если он доступен в системе

//         // 2. Проверяем, есть ли уже запись в sensors_sensor
//         return fetch(`/sensors/check/?car_id=${car_id}&user_id=${user_id}`);
//     })
//     .then(response => response.json())
//     .then(sensorRecord => {
//         const sensorData = {
//             car_vin: vinNumber,
//             engine_rpm: document.getElementById('engine_rpm').value,
//             intake_air_temperature: document.getElementById('intake_air_temperature').value,
//             mass_air_flow_sensor: document.getElementById('mass_air_flow_sensor').value,
//             injection_duration: document.getElementById('injection_duration').value,
//             throttle_position: document.getElementById('throttle_position').value,
//             vehicle_speed: document.getElementById('vehicle_speed').value,
//             manifold_absolute_pressure: document.getElementById('manifold_absolute_pressure').value
//         };

//         if (sensorRecord && sensorRecord.sensor_data_id) {
//             // 3. Если запись есть → PUT-запрос
//             return fetch(`/sensors/update/${sensorRecord.sensor_data_id}/`, {
//                 method: 'PUT',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     "X-CSRFToken": getCSRFToken()
//                 },
//                 body: JSON.stringify(sensorData)
//             })
//             .then(response => response.json())
//             .then(updatedData => {
//                 document.getElementById('responseMessage').innerText = "Данные обновлены успешно! ID записи: " + updatedData.sensor_data_id;
//                 fetchSensorData(updatedData.sensor_data_id);
//             });
//         } else {
//             // 4. Если записи нет → POST-запрос
//             return fetch('/sensors/add/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     "X-CSRFToken": getCSRFToken()
//                 },
//                 body: JSON.stringify(sensorData)
//             })
//             .then(response => response.json())
//             .then(newData => {
//                 document.getElementById('responseMessage').innerText = "Датчики добавлены успешно! ID записи: " + newData.sensor_data_id;
//                 fetchSensorData(newData.sensor_data_id);
//             });
//         }
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         document.getElementById('responseMessage').innerText = "Ошибка при отправке данных.";
//     });
// }



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
    console.log("fetchSensorData вызвана с car_id:", car_id); 
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
            console.log(`Расчёты сохранены! ID: ${data.calculated_id}, Новая запись: ${data.created}`);
        }
    })
    .catch(error => console.error("Ошибка при сохранении данных:", error));
}







// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelector("form").addEventListener("submit", function (event) {
//         event.preventDefault(); // Остановить стандартную отправку формы

//         let formData = {
//             car_brand: document.getElementById("car_brand").value,
//             car_color: document.getElementById("car_color").value,
//             car_vin: document.getElementById("car_vin").value,
//             engine_rpm: parseFloat(document.getElementById("engine_rpm").value),
//             intake_air_temperature: parseFloat(document.getElementById("intake_air_temperature").value),
//             mass_air_flow_sensor: parseFloat(document.getElementById("mass_air_flow_sensor").value),
//             injection_duration: parseFloat(document.getElementById("injection_duration").value),
//             throttle_position: parseFloat(document.getElementById("throttle_position").value),
//             vehicle_speed: parseFloat(document.getElementById("vehicle_speed").value),
//             manifold_absolute_pressure: parseFloat(document.getElementById("manifold_absolute_pressure").value)
//         };

//         fetch("/sensors/save-sensor-data/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": getCookie("csrftoken") // CSRF-токен для Django
//             },
//             body: JSON.stringify(formData)
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.message) {
//                 alert("✅ " + data.message);
//             } else {
//                 alert("⚠ Ошибка: " + JSON.stringify(data));
//             }
//         })
//         .catch(error => console.error("Ошибка:", error));
//     });

//     // Функция для получения CSRF-токена
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== "") {
//             let cookies = document.cookie.split(";");
//             for (let i = 0; i < cookies.length; i++) {
//                 let cookie = cookies[i].trim();
//                 if (cookie.startsWith(name + "=")) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
// });
