ymaps.ready(function () {
    var myMap = new ymaps.Map('map', {
        center: [55.751574, 37.573856],
        zoom: 9
    }, {
        searchControlProvider: 'yandex#search'
    });

    // Создаём макет содержимого.
    var MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
    );

    // Получаем данные о банкоматах
    response = fetchOfficeData();
    response.then(data => {
        var atms = data.atms;

        for (var i = 0; i < atms.length; i++) {
            var atm = atms[i];
            var coordinates = [atm.latitude, atm.longitude];
            var servicesContent = ''; // Создаем строку для содержимого

            // Перебираем услуги банкомата
            for (var service in atm.services) {
                if (atm.services[service].serviceActivity === "AVAILABLE") {
                    servicesContent += service + '<br>'; // Добавляем услугу в строку
                }
            }

            // Создаем Placemark
            var placemark = new ymaps.Placemark(coordinates, {
                hintContent: 'Банкомат',
                balloonContent: 'Адрес: ' + atm.address + '<br>Доступные услуги:<br>' + servicesContent
            }, {
                iconLayout: 'default#imageWithContent',
                iconImageHref: 'https://pngicon.ru/file/uploads/geometka.png',
                iconImageSize: [16, 16],
                iconImageOffset: [-24, -24],
                iconContentOffset: [15, 15],
                iconContentLayout: MyIconContentLayout
            });

            myMap.geoObjects.add(placemark);
            console.log("Placemark added.");
        }
    });

});


async function fetchOfficeData() {
    try {
        const response = await fetch('http://0.0.0.0:5000/office');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Произошла ошибка:', error);
    }
}