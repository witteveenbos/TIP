import { useMapEvents } from 'react-leaflet';

interface ZoomHandlerProps {
    setCurrentZoom: (zoom: number) => void;
}

const ZoomHandler = ({ setCurrentZoom }: ZoomHandlerProps) => {
    useMapEvents({
        zoom: (e) => {
            setCurrentZoom(e.target.getZoom());
        },
        zoomend: (e) => {
            setCurrentZoom(e.target.getZoom());
        },
        zoomstart: (e) => {
            setCurrentZoom(e.target.getZoom());
        }
    });
    return null;
};

export default ZoomHandler;