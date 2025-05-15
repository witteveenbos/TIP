import { useRef } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
const BaseMap = () => {
    const mapContainerRef = useRef(null);
    const bounds = [
        [51.643777887245896, 3.773675345120723],
        [52.33251094756909, 5.0314150015857],
    ];
    return typeof window !== 'undefined' ? (
        <div className="z-20 relative h-screen">
            <MapContainer
                className="energy-balance-map"
                ref={mapContainerRef}
                bounds={bounds}
                scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                    subdomains="abcd"
                    maxZoom={20}
                />
            </MapContainer>
        </div>
    ) : null;
};

export default BaseMap;
