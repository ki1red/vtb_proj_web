var myMap;
var clusterer;

ymaps.ready(function () {
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

    response = get_atm_radius();
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
});


// банки сами
function show_office() {
    var MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
    );

    clusterer = new ymaps.Clusterer({
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: true,
        clusterBalloonContentLayout: 'cluster#balloonAccordion'
    });

    response = fetchOfficeData();
    response.then(data => {
        var office = data.office;

        for (var i = 0; i < office.length; i++) {
            var office = office[i];
            var coordinates = [office.latitude, office.longitude];

            var placemark = new ymaps.Placemark(coordinates, {
                clusterCaption: office.address,
                hintContent: 'Отделение банка',
                balloonContent: 'Тут будет описание'
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