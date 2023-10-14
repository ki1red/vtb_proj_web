ymaps.ready(function () {
    var myMap = new ymaps.Map('map', {
        center: [55.751574, 37.573856],
        zoom: 9
    }, {
        searchControlProvider: 'yandex#search'
    });

    var MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
    );

    var clusterer = new ymaps.Clusterer({
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: true,
        clusterBalloonContentLayout: 'cluster#balloonAccordion'
    });

    response = fetchOfficeData();
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

            clusterer.add(placemark); // Добавляем точку в кластеризатор

            console.log("Placemark added.");
        }

        myMap.geoObjects.add(clusterer); // Добавляем кластеризатор на карту
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