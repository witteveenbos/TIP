import { postUserInputs } from '@/api/api';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import XMarkIcon from '@heroicons/react/24/outline/XMarkIcon';
import debounce from 'lodash.debounce';
import cloneDeep from 'lodash/cloneDeep';
import { useEffect, useState } from 'react';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    selectedDevelopmentStore,
    useAreaDivisionStore,
    useContinuousOptionsStore,
    useGeoJsonDataStore,
    useInputTypeStore,
    useMunicipalityScenariosStore,
    useScenarioStore,
    useSectoralOptionsStore,
    useSelectedGeoIdStore,
} from 'stores/calculateStore';
import { useDragersStore } from 'stores/headerTogglesStore';
import { PostUserInputRequest } from 'types/api/postUserInput';
import Loader from '../Loader/Loader';
import ContinuousDevelopments from './ContinuousDevelopments';
import SectoralDevelopments from './SectoralDevelopments';

export function EnergyBalanceAsideDevelopments({
    hovergeoid,
    geojson,
    setGraphData,
    children,
}) {
    const [isLoading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');
    const [sectoralAggregatedProjects, setSectoralAggregatedProjects] =
        useState([]);
    const { continuousOptions, setContinuousOptions } =
        useContinuousOptionsStore();
    const { sectoralOptions, setSectoralOptions } = useSectoralOptionsStore();
    const { setSelectedDevelopment } = selectedDevelopmentStore();
    const { inputType, setInputType } = useInputTypeStore();
    const { selectedScenario } = useScenarioStore();
    const { selectedAreaDivision } = useAreaDivisionStore();
    const { selectedGeoId, setSelectedGeoId } = useSelectedGeoIdStore();
    const {
        continuousDevelopmentDefaults,
        setContinuousDevelopmentDefaults,
        changedContinuousDevelopments,
    } = continuousDevelopmentsChangesStore();
    const {
        sectoralDevelopmentDefaults,
        setSectoralDevelopmentDefaults,
        setSectoralDevelopmentDefaultProjects,
        changedSectoralDevelopments,
        setChangedSectoralDevelopments,
    } = sectoralDevelopmentsChangesStore();
    const { setGeoJsonData } = useGeoJsonDataStore();
    const { municipalityScenarios } = useMunicipalityScenariosStore();
    const { energyCarrier, balance, original } = useDragersStore();

    const debouncedGetInputs = debounce((postData) => {
        getInputs(postData);
    }, 300);

    useEffect(() => {
        const postData = {
            viewSettings: {
                areaDivision: selectedAreaDivision,
                energyCarrier: energyCarrier,
                balance: balance,
                original: original,
                developmentType: inputType,
                graphType: 'energybalance_bar',
                graphFocus: selectedGeoId?.gid,
            },
            userSettings: {
                municipalityScenarios: municipalityScenarios,
                continuousDevelopments: changedContinuousDevelopments,
                sectoralDevelopments: changedSectoralDevelopments,
                selectedScenario: selectedScenario,
            },
        };

        debouncedGetInputs(postData);
    }, [
        selectedAreaDivision,
        selectedScenario,
        energyCarrier,
        balance,
        original,
        inputType,
        changedContinuousDevelopments,
        changedSectoralDevelopments,
        selectedGeoId, // TODO: it would be better to trigger the api call when clicking the button to show the graph
    ]);

    // Clean up the debounce function on component unmount
    useEffect(() => {
        return () => {
            debouncedGetInputs.cancel();
        };
    }, []);

    function saveDefaults(data, type) {
        const result = {};
        for (const key in data) {
            if (Array.isArray(data[key])) {
                result[key] = data[key].filter((item) => item.type === type);
            }
        }
        return result;
    }

    function createDefaultSectoralProjects(inputData) {
        const allDefaultProjects = [];

        for (const [municipalityID, developments] of Object.entries(
            inputData
        )) {
            developments.forEach((development) => {
                const changes = development.inputs.map((input) => ({
                    devKey: input.key,
                    value: input.default,
                }));

                // Check if all changes have a value of 0 - if so don't add a default project
                const allChangesZero = changes.every(
                    (change) => change.value === 0
                );

                if (!allChangesZero) {
                    const defaultProject = {
                        municipalityID: municipalityID,
                        devGroupKey: development.key,
                        changes: changes,
                        projectName: 'Bestaand',
                        projectId: `project-default-${development.key}-${municipalityID}`,
                        isDefault: true,
                    };

                    allDefaultProjects.push(defaultProject);
                }
            });
        }

        return allDefaultProjects;
    }

    function getInputs(postDataRequest: PostUserInputRequest) {
        setLoading(true);
        setErrorMessage('');

        postUserInputs(postDataRequest).then((res) => {
            if (res) {
                if (res.input) {
                    //set defaults and inputoptions of developments is not set yet
                    //this is only done once
                    if (inputType === 'continuous') {
                        const newDevelopments = saveDefaults(
                            res.input,
                            'continuous'
                        );
                        const merged = {
                            ...continuousDevelopmentDefaults,
                            ...newDevelopments,
                        };
                        setContinuousDevelopmentDefaults(merged);
                        const firstKey = Object.keys(res.input)[0];

                        const continuousOptions = res.input[firstKey].filter(
                            (option) => option.type === 'continuous'
                        );
                        setContinuousOptions(continuousOptions);
                        //do the same for sectoral only add one default project already for each location/development
                    } else if (inputType === 'sectoral') {
                        const newDevelopments = saveDefaults(
                            res.input,
                            'sectoral'
                        );
                        const merged = {
                            ...sectoralDevelopmentDefaults,
                            ...newDevelopments,
                        };
                        setSectoralDevelopmentDefaults(merged);
                        const firstKey = Object.keys(res.input)[0];
                        const sectoralOptions = res.input[firstKey].filter(
                            (option) => option.type === 'sectoral'
                        );
                        setSectoralOptions(sectoralOptions);
                        //create default projects for sectoral developments
                        if (
                            changedSectoralDevelopments.length === 0 &&
                            selectedAreaDivision === 'GM'
                        ) {
                            const defaultSectoralProjects =
                                createDefaultSectoralProjects(res.input);
                            setSectoralDevelopmentDefaultProjects(
                                cloneDeep(defaultSectoralProjects)
                            );
                            setChangedSectoralDevelopments(
                                defaultSectoralProjects
                            );
                        }
                        if (selectedAreaDivision !== 'GM') {
                            const aggregatedProjects =
                                createDefaultSectoralProjects(res.input);
                            setSectoralAggregatedProjects(aggregatedProjects);
                        }
                    }
                }
                if (res.graph) {
                    const { graph } = res;
                    setGraphData({ graph });
                }

                //update kaartlaag met nieuwe data
                if (res.map?.metadata) {
                    setGeoJsonData({
                        metadata: res.map.metadata,
                        geoJSON: {
                            ...geojson[selectedAreaDivision],
                            features: geojson[
                                selectedAreaDivision
                            ].features.map((feature) => {
                                return {
                                    ...feature,
                                    properties: {
                                        ...feature.properties,
                                        color: res.map.mapData[
                                            feature.properties.gid
                                        ]?.color,
                                        value: res.map.mapData[
                                            feature.properties.gid
                                        ]?.value,
                                    },
                                };
                            }),
                        },
                    });
                } else {
                    setGeoJsonData({
                        metadata: null,
                        geoJSON: {
                            ...geojson[selectedAreaDivision],
                            features: geojson[
                                selectedAreaDivision
                            ].features.map((feature) => {
                                return {
                                    ...feature,
                                    properties: {
                                        ...feature.properties,
                                        color: null,
                                        value: null,
                                    },
                                };
                            }),
                        },
                    });
                    res.msgs && setErrorMessage(res.msgs[0].msg);
                }
            } else {
                setErrorMessage(
                    'Er is iets fout gegaan in het ophalen van de inputvelden.'
                );
            }
            setLoading(false);
        });
    }

    function handleInputTypeChange(type) {
        setInputType(type);
        setSelectedDevelopment(null);
    }

    function loaderText(innerText) {
        return (
            <small className="absolute w-full h-full p-2 flex flex-col justify-center items-center bg-slate-700/50 cursor-progress">
                <Loader />
                <span>{innerText}</span>
            </small>
        );
    }

    function notificationNoAreaSelected() {
        return (
            <div className="p-2">
                <small className="bg-accent text-white block p-1 gap-2">
                    Selecteer een gebied op de kaart
                </small>
            </div>
        );
    }

    function genericTabHeader() {
        return (
            <div className="flex justify-between items-center p-2 gap-1">
                <strong>
                    {selectedGeoId
                        ? selectedGeoId.label
                        : hovergeoid
                          ? hovergeoid.label
                          : 'geen gebied'}{' '}
                </strong>
                {children}
                <Button
                    variant="outline"
                    className="border-primary"
                    size="icon"
                    onClick={() => {
                        setSelectedDevelopment(null), setSelectedGeoId(null);
                    }}>
                    <XMarkIcon className="h-4 w-4" />
                </Button>
            </div>
        );
    }

    return (
        <Tabs
            defaultValue="continuous"
            className="w-full h-full flex flex-col"
            id="side">
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger
                    value="continuous"
                    id="side-continous"
                    onClick={() => handleInputTypeChange('continuous')}>
                    Continue
                </TabsTrigger>
                <TabsTrigger
                    value="sectoral"
                    id="side-sectoral"
                    onClick={() => handleInputTypeChange('sectoral')}>
                    Sectoraal
                </TabsTrigger>
            </TabsList>
            <TabsContent
                value="continuous"
                className={
                    inputType == 'continuous' &&
                    `flex flex-col flex-1 relative mb-4`
                }>
                <div className="absolute w-full h-full flex flex-col">
                    {!selectedGeoId && notificationNoAreaSelected()}

                    {errorMessage && <p className="p-4">{errorMessage}</p>}
                    <>
                        {(selectedGeoId || hovergeoid) && genericTabHeader()}
                        {isLoading ? (
                            loaderText(
                                'Continue ontwikkelingen worden geladen...'
                            )
                        ) : (
                            <ContinuousDevelopments
                                gid={
                                    selectedGeoId
                                        ? selectedGeoId.gid
                                        : hovergeoid.gid
                                }
                                developments={
                                    selectedGeoId
                                        ? continuousDevelopmentDefaults[
                                              selectedGeoId.gid
                                          ]
                                        : hovergeoid
                                          ? continuousDevelopmentDefaults[
                                                hovergeoid.gid
                                            ]
                                          : continuousOptions
                                }
                                allExpandedRows={
                                    selectedGeoId || hovergeoid ? true : false
                                }
                            />
                        )}
                    </>
                </div>
            </TabsContent>
            <TabsContent
                value="sectoral"
                className={
                    inputType == 'sectoral' &&
                    `flex flex-col flex-1 relative mb-4`
                }>
                <div className="absolute w-full h-full flex flex-col">
                    {!selectedGeoId && notificationNoAreaSelected()}

                    {errorMessage && <p className="p-4">{errorMessage}</p>}
                    <>
                        {(selectedGeoId || hovergeoid) && genericTabHeader()}
                        {isLoading
                            ? loaderText(
                                  'Sectorale ontwikkelingen worden geladen...'
                              )
                            : sectoralDevelopmentDefaults && (
                                  <SectoralDevelopments
                                      gid={
                                          selectedGeoId
                                              ? selectedGeoId.gid
                                              : hovergeoid?.gid
                                      }
                                      developments={
                                          selectedGeoId
                                              ? sectoralDevelopmentDefaults[
                                                    selectedGeoId.gid
                                                ]
                                              : hovergeoid
                                                ? sectoralDevelopmentDefaults[
                                                      hovergeoid?.gid
                                                  ]
                                                : sectoralOptions
                                      }
                                      aggregatedProjects={
                                          sectoralAggregatedProjects
                                      }
                                      allExpandedRows={
                                          selectedGeoId || hovergeoid
                                              ? true
                                              : false
                                      }
                                  />
                              )}
                    </>
                </div>
            </TabsContent>
        </Tabs>
    );
}
