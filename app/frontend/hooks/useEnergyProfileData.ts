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
import { PlotlyGraphData, GraphMeta, GraphResponse } from '@/types/components/EnergyProfileGraph';

interface UseEnergyProfileDataProps {
    enabled?: boolean;
}

export function useEnergyProfileData({ enabled = true }: UseEnergyProfileDataProps) {
    const [graphData, setGraphData] = useState<PlotlyGraphData | null>(null);
    const [graphMeta, setGraphMeta] = useState<GraphMeta | null>(null);
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

            if (response && response.graph) {
                const graphResponse = response.graph as GraphResponse;
                if (graphResponse.graphData?.data?.length > 0) {
                    setGraphData(graphResponse.graphData);
                    setGraphMeta(graphResponse.graphMeta);
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

    useEffect(() => {
        if (!enabled || !selectedGeoId || !selectedAreaDivision || !selectedScenario) {
            return;
        }

        fetchGraphData();
    }, [enabled, selectedGeoId, selectedAreaDivision, energyCarrier, balance, original, inputType, municipalityScenarios, changedContinuousDevelopments, changedSectoralDevelopments, selectedScenario]);

    return {
        graphData,
        graphMeta,
        loading,
        error,
        refetch: fetchGraphData
    };
}