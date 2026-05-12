
import Loader from '@/components/Loader/Loader';
import { EnergyProfileGraphProps } from '@/types/components/EnergyProfileGraph';
import { useEnergyProfileData } from '@/hooks/useEnergyProfileData';
import EnergyProfileChart from './EnergyProfileChart';

export default function EnergyProfileGraph({ 
    enabled = true 
}: EnergyProfileGraphProps) {
    const { graphData, graphMeta, loading, error } = useEnergyProfileData({ enabled });

    return (
        <div className="flex flex-col h-[550px] flex-1">
            <div className="text-left p-8 flex-1 flex flex-col">
                {loading && (
                    <div className="flex-1 flex flex-col gap-4 items-center justify-center">
                        <p>De energie profiel grafiek wordt geladen, dit kan even duren...</p>
                        <Loader />
                    </div>
                )}

                {error && (
                    <div className="flex-1 flex items-center justify-center">
                        <p className="text-red-500">{error}</p>
                    </div>
                )}

                {!loading && !error && graphData && graphMeta && (
                    <div className="flex-1 min-h-[300px]">
                        <EnergyProfileChart graphData={graphData} graphMeta={graphMeta} />
                    </div>
                )}
            </div>
        </div>
    );
}
