
import { ComposedChart, Area, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip } from 'recharts';
import { useEffect, useState } from 'react';
import { postUserInputs } from 'api/api';
import type { PostUserInputRequest } from 'types/api/postUserInput';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    useAreaDivisionStore,
    useInputTypeStore,
    useSelectedGeoIdStore,
    useMunicipalityScenariosStore,
    useScenarioStore,
} from 'stores/calculateStore';
import { useDragersStore } from 'stores/headerTogglesStore';
import Loader from '@/components/Loader/Loader';

interface EnergyProfileGraphProps {
    enabled?: boolean;
}

interface GraphData {
    [key: string]: number | string;
}

interface GraphMetadata {
    title: string;
    unit: string;
    yLabelText: string;
    properties?: { [key: string]: { [key: string]: string } };
}

interface GraphResponse {
    metaData: GraphMetadata;
    graphData: GraphData[];
}

export default function EnergyProfileGraph({ 
    enabled = true 
}: EnergyProfileGraphProps) {
    const [data, setData] = useState<GraphData[]>([]);
    const [metadata, setMetadata] = useState<GraphMetadata | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Access stores directly
    const { selectedGeoId } = useSelectedGeoIdStore();
    const { selectedAreaDivision } = useAreaDivisionStore();
    const { inputType } = useInputTypeStore();
    const { energyCarrier, balance, original } = useDragersStore();
    const { municipalityScenarios } = useMunicipalityScenariosStore();
    const { changedContinuousDevelopments } = continuousDevelopmentsChangesStore();
    const { changedSectoralDevelopments } = sectoralDevelopmentsChangesStore();
      const { selectedScenario } = useScenarioStore();

    useEffect(() => {
        if (!enabled || !selectedGeoId || !selectedAreaDivision || !selectedScenario) {
            console.log('EnergyProfileGraph: Missing required data', {
                enabled,
                selectedGeoId,
                selectedAreaDivision,
                selectedScenario
            });
            return;
        }

        const fetchGraphData = async () => {
            setLoading(true);
            setError(null);

            try {
                // Construct the user input request directly from stores
                const userInputRequest: PostUserInputRequest = {
                    viewSettings: {
                        areaDivision: selectedAreaDivision,
                        energyCarrier: energyCarrier,
                        balance: balance,
                        original: original,
                        developmentType: inputType,
                        mapType: 'energy_balance',
                        graphType: 'energybalance_curve',
                        graphFocus: selectedGeoId?.gid,
                    },
                    userSettings: {
                        municipalityScenarios: municipalityScenarios,
                        continuousDevelopments: changedContinuousDevelopments,
                        sectoralDevelopments: changedSectoralDevelopments,
                        selectedScenario: selectedScenario,
                    }
                };

                const response = await postUserInputs(userInputRequest);

                console.log('EnergyProfileGraph API request:', userInputRequest);
                console.log('EnergyProfileGraph API response:', response);

                
                if (response && response.graph) {
                    const graphResponse = response.graph as GraphResponse;
                    if (graphResponse.graphData && Array.isArray(graphResponse.graphData) && graphResponse.graphData.length > 0) {
                        setData(graphResponse.graphData);
                        setMetadata(graphResponse.metaData);
                    } else {
                        console.warn('EnergyProfileGraph: Empty graphData received', graphResponse);
                        setError('Geen grafiekdata beschikbaar - lege dataset');
                    }
                } else if (response && response.msgs) {
                    const graphMsg = response.msgs.find(msg => msg.component === 'graph');
                    if (graphMsg) {
                        console.warn('EnergyProfileGraph: Graph error message', graphMsg.msg);
                        setError(`Grafiekfout: ${graphMsg.msg}`);
                    } else {
                        setError('Onverwacht API-antwoord - geen grafiekdata gevonden');
                    }
                } else {
                    console.warn('EnergyProfileGraph: No valid response received', response);
                    setError('Geen grafiekdata beschikbaar');
                }
            } catch (err) {
                console.error('Error fetching energy profile data:', err);
                setError('Er is een fout opgetreden bij het laden van de data');
            } finally {
                setLoading(false);
            }
        };

        fetchGraphData();
    }, [enabled, selectedGeoId, selectedAreaDivision, energyCarrier, balance, original, inputType, municipalityScenarios, changedContinuousDevelopments, changedSectoralDevelopments, selectedScenario]);


    const chartData = data.length > 0 ? data : [];
    const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];
    
    // Get all data keys except 'name' for the areas
    const allDataKeys = chartData.length > 0 
        ? Object.keys(chartData[0]).filter(key => key !== 'name')
        : [];
    
    // Transform data to make 'Vraag' values negative
    const transformedChartData = chartData.map(dataPoint => {
        const transformed = { ...dataPoint };
        allDataKeys.forEach(key => {
            const demandSupply = metadata?.properties?.[key]?.demandSupply;
            if (demandSupply === 'Vraag' && typeof transformed[key] === 'number') {
                transformed[key] = -Math.abs(transformed[key]);
            }
        });
        return transformed;
    });
    
    // Separate 'Basislast elektriciteit' from other keys
    const dataKeys = allDataKeys.filter(key => key !== 'Basislast elektriciteitsvraag');
    const hasBasislast = allDataKeys.includes('Basislast elektriciteitsvraag');
    return (
        <div className="flex flex-col h-[550px] flex-1">
            <div className="text-center p-8 flex-1 flex flex-col">
                <h3 className="text-lg font-semibold mb-4">
                    {metadata?.title || 'Energie Profiel'}
                </h3>
                
                {loading && (
                    <div className="flex-1 flex flex-col gap-4 items-center justify-center">
                      <p>De grafiek wordt geladen, dit kan even duren...</p>
                        <Loader />
                    </div>
                )}
                
                {error && (
                    <div className="flex-1 flex items-center justify-center">
                        <p className="text-red-500">{error}</p>
                    </div>
                )}
                
                {!loading && !error && (
                    <div className="flex-1 min-h-0">
                        <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart
                                data={transformedChartData}
                                margin={{
                                    top: 20,
                                    right: 30,
                                    left: 20,
                                    bottom: 5,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis label={{ value: metadata?.yLabelText || 'Waarde', angle: -90, position: 'insideLeft' }} />
                                <Tooltip />
                                {dataKeys.map((key, index) => {
                                    const demandSupply = metadata?.properties?.[key]?.demandSupply;
                                    const stackId = demandSupply === 'Vraag' ? 'demand' : 'supply';
                                    
                                    return (
                                        <Area 
                                            key={key}
                                            type="monotone" 
                                            dataKey={key} 
                                            stackId={stackId}
                                            stroke={metadata?.properties?.[key]?.color || colors[index % colors.length]} 
                                            fill={metadata?.properties?.[key]?.color || colors[index % colors.length]} 
                                        />
                                    );
                                })}
                                {hasBasislast && (
                                    <Line
                                        type="monotone"
                                        dataKey="Basislast elektriciteitsvraag"
                                        stroke={metadata?.properties?.['Basislast elektriciteitsvraag']?.color || '#ff0000'}
                                        strokeWidth={1}
                                        dot={false}
                                    />
                                )}
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>
        </div>
    );
}
