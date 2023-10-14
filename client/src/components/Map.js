import React from 'react';
import { YMaps, Map } from '@pbe/react-yandex-maps';


const BackgroundMap = () => {

    return (
        <YMaps>
            <Map defaultState={{ center: [55.751574, 37.573856], zoom: 12 }} width={window.screen.width} height={window.screen.height}/>
        </YMaps>
    )
}

export default BackgroundMap;