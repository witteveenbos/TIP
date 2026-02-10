import { useState } from 'react';
import { GraphProps } from '@/types/components/Graph';
import { useEnergyBalanceData } from '@/hooks/useEnergyBalanceData';
import RadioOption from '../../ui/radioButtonOption';
import FilterSection from './FilterSection';
import EnergyBalanceChart from './EnergyBalanceChart';
import { ViewMode } from '@/types/components/Graph';


export default function EnergyBalanceGraph({ data }: GraphProps) {
    const metaDataFromApi = data.graph.metaData;
    
    // Extract initial unique values for filters
    const initialDragers = [...new Set(data.graph.graphData.map((item) => item.carrier))];
    const initialSectors = [...new Set(data.graph.graphData.map((item) => item.sector))];
    
    // State management
    const [viewMode, setViewMode] = useState<ViewMode>('dragers');
    const [selectedDragers, setSelectedDragers] = useState(initialDragers);
    const [selectedSectors, setSelectedSectors] = useState(initialSectors);

    const toggleDrager = (drager: string) => {
        if (selectedDragers.includes(drager)) {
            setSelectedDragers(selectedDragers.filter((d) => d !== drager));
        } else {
            setSelectedDragers([...selectedDragers, drager]);
        }
    };

    const toggleSector = (sector: string) => {
        if (selectedSectors.includes(sector)) {
            setSelectedSectors(selectedSectors.filter((s) => s !== sector));
        } else {
            setSelectedSectors([...selectedSectors, sector]);
        }
    };
    
    // Use custom hook for data processing
    const {
        graphData,
        legendData,
        uniqueDragers,
        uniqueSectors,
    } = useEnergyBalanceData(data, viewMode, selectedDragers, selectedSectors);

    return (
        <div className="flex flex-col max-h-[550px] flex-1">
            {/* View Mode Toggle */}
            <div className="flex justify-start items-center mb-4 gap-8">
                <h3 className="text-primary font-bold leading-6">Weergave</h3>
                <div className="flex">
                    <RadioOption
                        label="Dragers"
                        value="dragers"
                        selectedOption={viewMode}
                        onSelect={(value) => setViewMode(value as ViewMode)}
                    />
                    <RadioOption
                        label="Sectoren"
                        value="sectors"
                        selectedOption={viewMode}
                        onSelect={(value) => setViewMode(value as ViewMode)}
                    />
                </div>
            </div>
            <hr className="mb-4" />
            <div className="flex flex-col md:flex-row flex-1 min-h-[300px] max-h-[110%]">
                <div className="min-w-[200px] max-w-[250px] pr-4">
                    {viewMode === 'sectors' ? (
                        <FilterSection
                            title="Filter sectoren"
                            items={uniqueSectors}
                            selectedItems={selectedSectors}
                            onToggleItem={toggleSector}
                            legendData={legendData}
                        />
                    ) : (
                        <FilterSection
                            title="Filter dragers"
                            items={uniqueDragers}
                            selectedItems={selectedDragers}
                            onToggleItem={toggleDrager}
                            legendData={legendData}
                        />
                    )}
                </div>
                <div className="flex-1 min-h-0">
                    <EnergyBalanceChart
                        graphData={graphData}
                        legendData={legendData}
                        metaData={metaDataFromApi}
                    />
                </div>
            </div>
        </div>
    );
}
