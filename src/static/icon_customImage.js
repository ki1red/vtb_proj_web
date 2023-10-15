var myMap;
var clusterer;

async function sendGetRequest(latitude, longitude, radius, requiredServices) {
    const url = `http://0.0.0.0:5000/atm_filter?latitude=${latitude}&longitude=${longitude}&radius=${radius}&required=${requiredServices}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

function showAtm() {
    myMap = new ymaps.Map('map', {
        center: [55.751574, 37.573856],
        zoom: 9
    }, {
        searchControlProvider: 'yandex#map'
    });

    var MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
    );

    clusterer = new ymaps.Clusterer({
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: true,
        clusterBalloonContentLayout: 'cluster#balloonAccordion'
    });

    response = fetchATMData();
    response.then(data => {
        var atms = data.atms;

        for (var i = 0; i < atms.length; i++) {
            var atm = atms[i];
            var coordinates = [atm.latitude, atm.longitude];
            var servicesContent = '';

            for (var service in atm.services) {
                if (atm.services[service].serviceActivity === "AVAILABLE") {
                    servicesContent += service + '<br>';
                }
            }


            var placemark = new ymaps.Placemark(coordinates, {
                clusterCaption: atm.address,
                hintContent: 'Банкомат',
                balloonContent: 'Доступные услуги:<br>' + servicesContent + '<br>'
            }, {
                iconLayout: 'default#imageWithContent',
                iconImageHref: 'https://pngicon.ru/file/uploads/geometka.png',
                iconImageSize: [16, 16],
                iconImageOffset: [-24, -24],
                iconContentOffset: [15, 15],
                iconContentLayout: MyIconContentLayout
            });

            clusterer.add(placemark); // Добавляем точку в кластеризатор

            console.log("Placemark added.");
        }

        myMap.geoObjects.add(clusterer); // Добавляем кластеризатор на карту
    });
};

ymaps.ready(showAtm)
// банки сами
function show_office() {
    var MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="color: #ff0000; font-weight: bold;">$[properties.iconContent]</div>'
    );

    clusterer = new ymaps.Clusterer({
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: true,
        clusterBalloonContentLayout: 'cluster#balloonAccordion'
    });

    response = fetchOfficeData();
    response.then(data => {
        var offices = data.office; // Изменил название переменной на множественное число
        for (var i = 0; i < offices.length; i++) {
            var currentOffice = offices[i]; // Изменил название переменной

            // Остальной код без изменений...

            var coordinates = [currentOffice.latitude, currentOffice.longitude];
            var placemark = new ymaps.Placemark(coordinates, {
                clusterCaption: currentOffice.address,
                hintContent: 'Отделение банка',
                balloonContent: currentOffice.salePointName,
            }, {
                iconLayout: 'default#imageWithContent',
                iconImageHref: 'https://pngicon.ru/file/uploads/geometka.png',
                iconImageSize: [16, 16],
                iconImageOffset: [-24, -24],
                iconContentOffset: [15, 15],
                iconContentLayout: MyIconContentLayout
            });

            clusterer.add(placemark);
            console.log("Placemark added.");
        }

        myMap.geoObjects.add(clusterer);
    });

};





async function fetchATMData() {
    try {
        const response = await fetch('http://0.0.0.0:5000/atm');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Произошла ошибка:', error);
    }
}


async function fetchOfficeData() {
    try {
        const response = await fetch('http://0.0.0.0:5000/office');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Произошла ошибка:', error);
    }
}

async function get_atm_radius() {
    // функция позволяет получить банкоматы в радиусе
    latitude = 55.756192;
    longitude = 37.594665;
    radius = 5;
    try {
        const response = await fetch('http://0.0.0.0:5000/atm_filter?latitude=55.756192&longitude=37.594665&radius=2');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Произошла ошибка:', error);
    }
}

function clearMap() {
    myMap.geoObjects.removeAll(); // Удаляем все объекты с карты
    clusterer.removeAll(); // Очищаем кластеризатор
}



export { sendGetRequest };