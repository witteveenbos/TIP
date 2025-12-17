import { useEffect, useRef, useState } from 'react';
import { GeoJSON, MapContainer, TileLayer } from 'react-leaflet';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    selectedDevelopmentStore,
    useAreaDivisionStore,
    useGeoJsonDataStore,
    useInputTypeStore,
    useMunicipalityScenariosStore,
    useScenarioStore,
    useSelectedGeoIdStore,
} from 'stores/calculateStore';
import {
    useDragersStore,
    useFutureVisionsDialogStore,
} from 'stores/headerTogglesStore';
import FutureVisionDialog from '../FutureVisionDialog';
import { Button } from '../ui/button';
import s from './EnergyBalance.module.css';
import { EnergyBalanceAsideDevelopments } from './EnergyBalanceAsideDevelopments';
import EnergyBalanceDialogGraph from './EnergyBalanceDialogGraph';
import EnergyBalanceLabel from './EnergyBalanceLabel';
import EnergyBalanceLegend from './EnergyBalanceLegend';

export default function EnergyBalance({ geojson }: { geojson: any }) {
    const [hoverGeoId, setHoverGeoId] = useState('');
    const [hoverTooltip, setHoverTooltip] = useState({ show: false, x: 0, y: 0, value: null, name: '' });
    const { selectedGeoId, setSelectedGeoId } = useSelectedGeoIdStore();
    const [dialogOpen, setDialogOpen] = useState({ open: false, type: null });
    const [graphData, setGraphData] = useState(null);

    const mapContainerRef = useRef(null);

    const { selectedScenario } = useScenarioStore();
    const { geoJsonData, setGeoJsonData } = useGeoJsonDataStore();
    const { futureVisionDialog, setFutureVisionDialog } =
        useFutureVisionsDialogStore();
    const { selectedAreaDivision, setSelectedAreaDivision } =
        useAreaDivisionStore();
    const { selectedDevelopment } = selectedDevelopmentStore();
    const { inputType, setInputType } = useInputTypeStore();

    const { continuousDevelopmentDefaults, changedContinuousDevelopments } =
        continuousDevelopmentsChangesStore();
    const { sectoralDevelopmentDefaults, changedSectoralDevelopments } =
        sectoralDevelopmentsChangesStore();
    const { original } = useDragersStore();

    const changedDevelopments =
        inputType == 'sectoral'
            ? changedSectoralDevelopments
            : changedContinuousDevelopments;
    const developmentsDefaults =
        inputType == 'sectoral'
            ? sectoralDevelopmentDefaults
            : continuousDevelopmentDefaults;
    const backupColors = [
        '#7896c1',
        '#bdc6d7',
        '#faf5f4',
        '#e1b9b6',
        '#c67875',
    ];

    {
        /*TODO: volgens mij kan deze eruit -> dit gebeurd allemaal in energyBalanceAsideDevelopments
    useEffect(() => {
        getMetaData();
    }, [geojson, selectedAreaDivision]); */
    }

    useEffect(() => {
        if (futureVisionDialog.open) {
            setDialogOpen({
                open: true,
                type: 'futureVision',
            });
        }
    }, [futureVisionDialog]);

    //Legend colors come from the metadata of the geoJsonData, these are used everywhere
    const legendColors = geoJsonData?.metadata?.legendLabels
        ? geoJsonData.metadata.legendLabels.map((label) => label.color)
        : backupColors;

    const createLegendValues = (min, max, colors) => {
        const step = (max - min) / colors.length;
        const values = [];
        for (let i = 0; i < colors.length + 1; i++) {
            values.push(Math.round(min + i * step));
        }
        return values;
    };

    const setColor = (value, min, max) => {
        const values = createLegendValues(min, max, backupColors);
        let colorIndex = 0;
        for (let i = 1; i < values.length; i++) {
            if (value < values[i]) {
                break;
            }
            colorIndex++;
        }
        if (colorIndex === values.length - 1 && value >= values[colorIndex]) {
            colorIndex = values.length - 2;
        }
        return backupColors[colorIndex];
    };

    const getFeatureValue = (feature) => {
        if (
            selectedDevelopment &&
            Object.keys(developmentsDefaults).length !== 0
        ) {
            const changedCd = changedDevelopments.filter(
                (cd) =>
                    cd.municipalityID === feature.properties.gid &&
                    cd.devGroupKey == selectedDevelopment.key
            );

            const gid = changedCd.length
                ? changedCd
                : developmentsDefaults[feature.properties.gid];

            let value;

            //if there are changes, calculate the value based on the changes
            if (changedCd.length && gid.length) {
                value = gid
                    .map((gid) => gid.changes)
                    .flat()
                    .reduce(
                        (partialSum, a) =>
                            parseFloat(partialSum) + parseFloat(a.value),
                        0
                    );
            } else {
                const gidValue = gid?.find(
                    (feature) => feature.key === selectedDevelopment?.key
                );
                value = gidValue
                    ? gidValue.inputs.reduce(
                          (partialSum, a) =>
                              parseFloat(partialSum) + parseFloat(a.default),
                          0
                      )
                    : undefined;
            }
            return value;
        } else {
            return feature.properties.value;
        }
    };

    const setStyle = (feature) => {
        let fillColor;
        const value = getFeatureValue(feature);
        
        if (
            selectedDevelopment &&
            Object.keys(developmentsDefaults).length !== 0
        ) {
            fillColor = setColor(
                value,
                selectedDevelopment.min,
                selectedDevelopment.max
            );
        } else {
            fillColor = feature.properties.color;
        }

        const fillOpacity = fillColor
            ? feature.properties.gid === selectedGeoId?.gid
                ? 0.8
                : 0.2
            : 0;

        const style = {
            fillColor: fillColor,
            fillOpacity: fillOpacity,
            color:
                feature.properties.gid === selectedGeoId?.gid
                    ? '#AA0067'
                    : fillColor,
            opacity: feature.properties.gid === selectedGeoId?.gid ? 1 : 0.5,
            dashArray: feature.properties.gid === selectedGeoId?.gid ? 10 : 0,
        };

        return style;
    };

    function getBounds() {
        // function to automatically calculate the bounds of the map
        const x = [];
        const newCoords = { ...geojson[selectedAreaDivision] };
        const bounds = newCoords.features.map((feature) =>
            feature.geometry.coordinates.flat(3)
        );

        for (let i = 0; i < bounds.length; i++) {
            x.push(...bounds[i]);
        }
        const lats = x.map((x) => x[0]);
        const longs = x.map((x) => x[1]);

        return [
            [Math.min(...longs), Math.min(...lats)],
            [Math.max(...longs), Math.max(...lats)],
        ];
    }
    function updateHover(geoid) {
        setHoverGeoId(geoid);
    }
    // Function to bind popup to the geoJason data.
    function clickOnFeature(feature, layer) {
        layer
            .on('mouseover', function (e) {
                updateHover(feature.properties);
                const value = getFeatureValue(feature);
                const unit = selectedDevelopment?.unit || '%';
                const formattedValue = value !== undefined && value !== null ? `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${unit}`.trim() : 'No data';
                
                setHoverTooltip({
                    show: true,
                    x: e.containerPoint.x,
                    y: e.containerPoint.y,
                    value: formattedValue,
                    name: feature.properties.label || feature.properties.name || `Area ${feature.properties.gid}`
                });
            })
            .on('mouseout', function (e) {
                updateHover('');
                setHoverTooltip({ show: false, x: 0, y: 0, value: null, name: '' });
            })
            .on('click', function (e) {
                setSelectedGeoId(feature.properties);
            });
    }

    // Function to close the dialog
    const closeDialog = () => {
        setDialogOpen({ open: false, type: null });
        if (futureVisionDialog.open) {
            setFutureVisionDialog({ open: false, type: 'none' });
        }
    };

    // Function to change zoom level
    const changeZoomLevel = (zoomLevel) => {
        if (mapContainerRef.current) {
            mapContainerRef.current.setZoom(zoomLevel);
        }
    };
    const bounds = [
        [50.5, 3.5], // whole of the Netherlands
        [53.5, 7.108],
    ]; 

    return (
        <>
            {dialogOpen.open &&
                (dialogOpen.type === 'energyBalance' ? (
                    <EnergyBalanceDialogGraph
                        graphData={graphData}
                        region={selectedGeoId}
                        closeDialog={closeDialog}
                    />
                ) : dialogOpen.type === 'futureVision' ? (
                    <FutureVisionDialog
                        closeDialog={closeDialog}
                        dialogType={futureVisionDialog.type}
                        scenario={selectedScenario}
                        changeZoomLevel={changeZoomLevel}
                    />
                ) : null)}

            <MapContainer
                className="energy-balance-map"
                ref={mapContainerRef}
                bounds={bounds}
                scrollWheelZoom={true}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                    subdomains="abcd"
                    maxZoom={20}
                />
                {geoJsonData.geoJSON && (
                    <>
                        <GeoJSON
                            key={`${JSON.stringify(geoJsonData.geoJSON)}-${selectedDevelopment?.key || 'none'}`}
                            onEachFeature={clickOnFeature}
                            data={geoJsonData.geoJSON}
                            style={setStyle}
                        />

                        {!original &&
                            geoJsonData.geoJSON.features.map(
                                (feature: {
                                    label: string;
                                    geometry: { coordinates: any };
                                    properties: {
                                        value: any;
                                        label: string;
                                        color: string;
                                        gid: string;
                                    };
                                }) => {
                                    return (
                                        <EnergyBalanceLabel
                                            key={feature.label}
                                            coords={
                                                feature.geometry.coordinates
                                            }
                                            value={feature.properties.value}
                                            text={feature.properties.label}
                                            color={feature.properties.color}
                                            gid={feature.properties.gid}
                                        />
                                    );
                                }
                            )}

                        <EnergyBalanceLegend
                            map={mapContainerRef}
                            colors={
                                selectedDevelopment
                                    ? backupColors
                                    : legendColors
                            }
                            labels={
                                selectedDevelopment
                                    ? createLegendValues(
                                          selectedDevelopment.min,
                                          selectedDevelopment.max,
                                          backupColors
                                      )
                                    : geoJsonData?.metadata?.legendLabels?.map(
                                          (label) => label.label
                                      )
                            }
                            unit={selectedDevelopment?.unit}
                            title={
                                selectedDevelopment
                                    ? selectedDevelopment.name
                                    : geoJsonData?.metadata?.legendTitle
                            }
                            metadata={geoJsonData.metadata}
                            selectedDevelopment={selectedDevelopment}
                        />
                    </>
                )}
            </MapContainer>

            {/* Hover tooltip */}
            {hoverTooltip.show && (
                <div
                    style={{
                        position: 'absolute',
                        left: hoverTooltip.x + 10,
                        top: hoverTooltip.y - 10,
                        backgroundColor: 'rgba(239, 239, 240)',
                        color: 'white',
                        padding: '8px 12px',
                        borderRadius: '4px',
                        fontSize: '12px',
                        pointerEvents: 'none',
                        zIndex: 1000,
                        whiteSpace: 'nowrap',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                    }}
                >
                    <div style={{ fontWeight: 'bold', color: 'white !important' }}>{hoverTooltip.name}: {hoverTooltip.value}</div>
                   
                </div>
            )}

            <aside className={s.EnergyBalanceAside}>
                <div className={s.EnergyBalanceAside__inner}>
                    <EnergyBalanceAsideDevelopments
                        hovergeoid={hoverGeoId}
                        geojson={geojson}
                        setGraphData={setGraphData}>
                        <Button
                            disabled={selectedAreaDivision !== 'GM'}
                            size="sm"
                            className="border-primary ml-auto"
                            variant="outline"
                            onClick={() =>
                                setDialogOpen({
                                    open: true,
                                    type: 'energyBalance',
                                })
                            }>
                            energiebalans
                        </Button>
                    </EnergyBalanceAsideDevelopments>
                </div>
            </aside>
        </>
    );
}
