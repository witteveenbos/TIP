import { useRef } from 'react';
import { MapContainer } from 'react-leaflet';
import OpenFreeMapLayer from './OpenFreeMapLayer';

const BaseMap = () => {
    const mapContainerRef = useRef(null);
    const bounds = [
        [51.8, 3.2], // whole of the Netherlands
        [53.6, 6.2],
    ];
    return typeof window !== 'undefined' ? (
        <div className="z-20 relative h-screen">
            <MapContainer
                className="energy-balance-map"
                ref={mapContainerRef}
                bounds={bounds}
                scrollWheelZoom={false}>
                <OpenFreeMapLayer />
            </MapContainer>
        </div>
    ) : null;
};

export default BaseMap;
