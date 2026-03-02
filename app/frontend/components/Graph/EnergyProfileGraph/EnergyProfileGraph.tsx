
import React, { useState } from 'react';
import Loader from '@/components/Loader/Loader';
import { EnergyProfileGraphProps } from '@/types/components/EnergyProfileGraph';
import { useEnergyProfileData } from '@/hooks/useEnergyProfileData';
import FilterSection from '../FilterSection';
import EnergyProfileChart from './EnergyProfileChart';
import { GraphDataPoint } from '@/types/components/Graph';

export default function EnergyProfileGraph({ 
    enabled = true 
}: EnergyProfileGraphProps) {
    const { data, metadata, loading, error } = useEnergyProfileData({ enabled });

    // State for selected items (initially empty, will be set when data loads)
    const [selectedItems, setSelectedItems] = useState<string[]>([]);

    // Update selectedItems when data changes
    React.useEffect(() => {
        if (data.length > 0) {
            const newDataKeys = Object.keys(data[0]).filter(key => key !== 'name');
            setSelectedItems(newDataKeys);
        }
    }, [data]);

    const toggleItem = (item: string) => {
        setSelectedItems(prev => 
            prev.includes(item)
                ? prev.filter(i => i !== item)
                : [...prev, item]
        );
    };

    const chartData = data.length > 0 ? data : [];
    const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];
    
    // Transform data to include proper x-axis labels from metadata
    const finalChartData: GraphDataPoint[] = chartData.map((dataPoint, index) => {
        return {
            ...dataPoint,
            name: String(metadata?.xTickLabels?.[index] || dataPoint.name || `Day ${index + 1}`)
        };
    });
    
    // Get all data keys except 'name' for the areas
    const allDataKeys = chartData.length > 0 
        ? Object.keys(chartData[0]).filter(key => key !== 'name')
        : [];
    
    // Filter data keys based on selected items and separate 'Basislast elektriciteit' from other keys
    const dataKeys = allDataKeys.filter(key => key !== 'Basislast elektriciteitsvraag' && selectedItems.includes(key));
    const hasBasislast = allDataKeys.includes('Basislast elektriciteitsvraag') && selectedItems.includes('Basislast elektriciteitsvraag');
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
                
                {!loading && !error && (
                  <div className="flex flex-col md:flex-row flex-1 min-h-[300px] max-h-[110%]">
              <div className="min-w-[200px] max-w-[250px] pr-4">
                        <FilterSection
                            title="Selecteer energieprofielen"
                            items={metadata ? (() => {
                                const entries = Object.entries(metadata.properties);
                                const aanbodItems = entries
                                    .filter(([key, value]) => value.demandSupply === 'Aanbod')
                                    .map(([key, value]) => ({
                                        name: key,
                                        demandSupply: value.demandSupply,
                                    }));
                                const vraagItems = entries
                                    .filter(([key, value]) => value.demandSupply === 'Vraag')
                                    .map(([key, value]) => ({
                                        name: key,
                                        demandSupply: value.demandSupply,
                                    }));
                                return [...aanbodItems, ...vraagItems];
                            })() : []}
                            selectedItems={selectedItems}
                            onToggleItem={toggleItem} // Toggle functionality implemented
                            legendData={metadata ? Object.fromEntries(Object.entries(metadata.properties).map(([key, value], index) => [key, value.color || colors[index % colors.length]])) : {}}
                            reverseOrder={{
                                "Vraag": false,
                                "Aanbod": true,
                            }}
                        />
                    </div>
                    <div className="flex-1 min-h-0">
                        <EnergyProfileChart
                            chartData={finalChartData}
                            metadata={metadata}
                            dataKeys={dataKeys}
                            hasBasislast={hasBasislast}
                            colors={colors}
                        />
                    </div>
                     </div>
                )}
            </div>
        </div>
    );
}
