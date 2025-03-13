document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculateButton").addEventListener("click", sendSensorData);
});
function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}
function sendSensorData() {
    // Первый запрос на сохранение датчиков в бд
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
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('responseMessage').innerText = "Ошибка при отправке данных.";
    });
}


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addCarButton").addEventListener("click", sendCar);
});
function sendCar() {
    //Второй запрос на создание машины
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
