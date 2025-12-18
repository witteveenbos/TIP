import L from 'leaflet';
import { Marker } from 'react-leaflet';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    useInputTypeStore,
} from 'stores/calculateStore';

interface GeoJsonLabelProps {
    feature: {
        geometry: { coordinates: any };
        properties: {
            value?: any;
            label?: string;
            name?: string;
            gid: string;
            color?: string;
        };
    };
    currentZoom: number;
    getFeatureValue: (feature: any) => any;
    selectedDevelopment?: {
        unit?: string;
        key?: string;
    };
}

const GeoJsonLabel = ({ 
    feature, 
    currentZoom, 
    getFeatureValue, 
    selectedDevelopment 
}: GeoJsonLabelProps) => {
    const { inputType } = useInputTypeStore();
    const { changedContinuousDevelopments } = continuousDevelopmentsChangesStore();
    const { changedSectoralDevelopments } = sectoralDevelopmentsChangesStore();

    const center = L.polygon(feature.geometry.coordinates).getBounds().getCenter();
    const value = getFeatureValue(feature);
    const unit = selectedDevelopment?.unit || '%';
    const formattedValue = value !== undefined && value !== null ? 
        `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${unit}`.trim() : 
        'No data';
    const name = feature.properties.label || feature.properties.name || `Area ${feature.properties.gid}`;
    
    // Check for active developments (from EnergyBalanceLabel logic)
    const activeContinuousDevelopments = changedContinuousDevelopments.filter(
        (cd) =>
            cd.municipalityID === feature.properties.gid &&
            cd.devGroupKey == selectedDevelopment?.key
    );

    const activeSectoralDevelopments = changedSectoralDevelopments.filter(
        (sd) =>
            sd.municipalityID === feature.properties.gid &&
            sd.devGroupKey == selectedDevelopment?.key &&
            sd.isDefault === false
    );

    const hasActiveDevelopments = (
        (inputType === 'continuous' && activeContinuousDevelopments.length > 0) ||
        (inputType === 'sectoral' && activeSectoralDevelopments.length > 0)
    );

    // Only show label when zoomed in enough
    const minZoomLevel = 11;
    
    // SVG icon from original EnergyBalanceLabel
    const developmentSvg = `<svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 -960 960 960" width="24"><path fill="#000" d="M440-82q-76-8-141.5-41.5t-114-87Q136-264 108-333T80-480q0-91 36.5-168T216-780h-96v-80h240v240h-80v-109q-55 44-87.5 108.5T160-480q0 123 80.5 212.5T440-163v81Zm-17-214L254-466l56-56 113 113 227-227 56 57-283 283Zm177 196v-240h80v109q55-45 87.5-109T800-480q0-123-80.5-212.5T520-797v-81q152 15 256 128t104 270q0 91-36.5 168T744-180h96v80H600Z"/></svg>`;
    
    if (currentZoom < minZoomLevel) {
        // Show development indicator even when not zoomed in if there are active developments
        if (hasActiveDevelopments) {
            const checkmarkIcon = L.divIcon({
                html: `
                    <span title="${name}" style="border-color:${feature.properties.color || '#333'}">${developmentSvg}</span>
                `,
                className: 'map__text_icon',
                iconSize: [24, 24],
                iconAnchor: [12, 12]
            });

            return (
                <Marker
                    key={`dev-indicator-${feature.properties.gid}`}
                    position={[center.lng, center.lat] as L.LatLngExpression}
                    // @ts-expect-error - Leaflet icon type compatibility
                    icon={checkmarkIcon}
                />
            );
        }
        return null;
    }

    // When zoomed in, show detailed label with both development status and data
    const labelIcon = L.divIcon({
        html: `
            <div style="
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #003360;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                color: #333;
                white-space: nowrap;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                pointer-events: none;
                ${hasActiveDevelopments ? 'border-left: 4px solid #22c55e;' : ''}
            ">
                <div style="font-size: 11px; color: #666;">
                    ${hasActiveDevelopments ? developmentSvg : ''}${name}
                </div>
                <div style="font-size: 12px; font-weight: bold;">${formattedValue}</div>
            </div>
        `,
        className: 'zoom-based-label',
        iconSize: [120, 40],
        iconAnchor: [60, 20]
    });

    return (
        <Marker
            key={`label-${feature.properties.gid}`}
            position={[center.lng, center.lat] as L.LatLngExpression}
            // @ts-ignore - Leaflet icon type compatibility
            icon={labelIcon}
        />
    );
};

export default GeoJsonLabel;