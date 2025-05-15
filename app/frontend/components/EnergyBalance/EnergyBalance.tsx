import dynamic from 'next/dynamic';
import React, { useCallback, useEffect, useState } from 'react';
import {
    getAreaDivisionOptions,
    getGeoJSONs,
    getMunicipalityScenarios,
} from '../../api/api';
import {
    useAllAreasStore,
    useAreaDivisionStore,
    useMunicipalityScenariosStore,
    useScenarioStore,
} from '../../stores/calculateStore';

const EnergyBalanceMapComponent = dynamic(() => import('./EnergyBalanceMap'), {
    ssr: false,
});

const EnergyBalance = ({
    handleMapLoading,
}: {
    handleMapLoading: (showLoading: boolean) => void;
}) => {
    const [errorMessage, setErrorMessage] = useState('');
    const { selectedScenario } = useScenarioStore();
    const { setAreaDivision } = useAreaDivisionStore();
    const { municipalityScenarios, setMunicipalityScenarios } =
        useMunicipalityScenariosStore();
    const [geoJsonData, setGeoJsonData] = useState(null);

    const { setAllAreas } = useAllAreasStore();

    useEffect(() => {
        const fetchData = async () => {
            handleMapLoading(true); // Set loading state to true

            if (municipalityScenarios.length === 0) {
                try {
                    const res = await getMunicipalityScenarios({
                        dataLink: selectedScenario,
                    });
                    if (res) {
                        setMunicipalityScenarios(res);
                    }
                } catch (error) {
                    setErrorMessage(
                        "Er is iets fout gegaan bij het ophalen van de gemeentelijke scenario's."
                    );
                }
            }

            try {
                const areaDivisionRes = await getAreaDivisionOptions();
                if (areaDivisionRes) {
                    setAreaDivision(areaDivisionRes);
                    const geoJsonRes = await getGeoJSONs();
                    if (geoJsonRes) {
                        setGeoJsonData(geoJsonRes);
                        const areasData = getAllAreas(geoJsonRes);
                        setAllAreas(areasData);
                    } else {
                        setErrorMessage(
                            'Er is iets fout gegaan bij het ophalen van de kaartlagen.'
                        );
                    }
                } else {
                    setErrorMessage(
                        'Er is iets fout gegaan in het ophalen van de beschikbare ruimtelijke indelingen. Probeer het later opnieuw.'
                    );
                }
            } catch (error) {
                setErrorMessage(
                    'Er is iets fout gegaan bij het ophalen van de gegevens.'
                );
            } finally {
                handleMapLoading(false); // Stop loading
            }
        };

        fetchData();
    }, [selectedScenario]);

    const getAllAreas = useCallback((geojson) => {
        const areaData = {};
        for (const key in geojson) {
            if (geojson.hasOwnProperty(key)) {
                const features = geojson[key].features;
                areaData[key] = [];
                features.forEach((feature) => {
                    const { gid, label } = feature.properties;
                    areaData[key].push({ gid, label });
                });
            }
        }
        return areaData;
    }, []);

    return (
        <>
            {errorMessage && (
                <p className="text-red-700 block m-1">{errorMessage}</p>
            )}
            {geoJsonData && <EnergyBalanceMapComponent geojson={geoJsonData} />}
        </>
    );
};

export default React.memo(EnergyBalance, (prevProps, nextProps) => {
    return prevProps.handleMapLoading === nextProps.handleMapLoading;
});
