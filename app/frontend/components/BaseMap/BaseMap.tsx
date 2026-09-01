import { useRef } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import type { LatLngBoundsExpression } from 'leaflet';
const BaseMap = () => {
    const mapContainerRef = useRef(null);
    const bounds: LatLngBoundsExpression = [
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
                 <TileLayer
                    attribution='Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a>'
                    url="https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/grijs/EPSG:3857/{z}/{x}/{y}{r}.png"
                    subdomains="abcd"
                    maxZoom={20}
                />
            </MapContainer>
        </div>
    ) : null;
};

export default BaseMap;
