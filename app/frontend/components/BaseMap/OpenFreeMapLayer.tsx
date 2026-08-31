import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import { maplibreGL } from '@maplibre/maplibre-gl-leaflet';
import * as maplibregl from 'maplibre-gl';

const OPENFREEMAP_POSITRON_STYLE =
    'https://tiles.openfreemap.org/styles/positron';

const OpenFreeMapLayer = () => {
    const map = useMap();

    useEffect(() => {
        maplibregl.setWorkerUrl('/maplibre-gl-csp-worker.js');

        const layer = maplibreGL({
            style: OPENFREEMAP_POSITRON_STYLE,
        });

        layer.addTo(map);

        return () => {
            map.removeLayer(layer);
        };
    }, [map]);

    return null;
};

export default OpenFreeMapLayer;