
import { ComposedChart, Area, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';
import Loader from '@/components/Loader/Loader';
import { EnergyProfileGraphProps } from '@/types/components/EnergyProfileGraph';
import CustomYAxisLabel from './CustomYAxisLabel';
import { useEnergyProfileData } from '@/hooks/useEnergyProfileData';
import FilterSection from '../FilterSection';

export default function EnergyProfileGraph({ 
    enabled = true 
}: EnergyProfileGraphProps) {
    const { data, metadata, loading, error } = useEnergyProfileData({ enabled });

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            // Group payload by demandSupply type
            const groupedPayload = payload.reduce((acc: any, entry: any) => {
                const demandSupply = metadata?.properties?.[entry.dataKey]?.demandSupply || '';
                if (!acc[demandSupply]) {
                    acc[demandSupply] = [];
                }
                acc[demandSupply].push(entry);
                return acc;
            }, {});
            
            return (
                <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
                    <p className="font-medium">{label}</p>
                    {/* Show Aanbod first */}
                    {groupedPayload['Aanbod'] && (
                        <>
                            <p className="font-medium text-sm mt-2">Aanbod</p>
                            {groupedPayload['Aanbod'].map((entry: any, index: number) => (
                                <p key={`aanbod-${index}`} className="ml-2">
                                    {`${entry.dataKey}: ${entry.value?.toFixed(2) || 0} ${metadata?.unit || ''}`}
                                </p>
                            ))}
                        </>
                    )}
                    {/* Then show Vraag */}
                    {groupedPayload['Vraag'] && (
                        <>
                            <p className="font-medium text-sm mt-2">Vraag</p>
                            {groupedPayload['Vraag'].map((entry: any, index: number) => (
                                <p key={`vraag-${index}`} className="ml-2">
                                    {`${entry.dataKey}: ${entry.value?.toFixed(2) || 0} ${metadata?.unit || ''}`}
                                </p>
                            ))}
                        </>
                    )}
                </div>
            );
        }
        return null;
    };


    const chartData = data.length > 0 ? data : [];
    const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];
    
    // Transform data to include proper x-axis labels from metadata
    const finalChartData = chartData.map((dataPoint, index) => {
        return {
            ...dataPoint,
            name: metadata?.xTickLabels?.[index] || dataPoint.name || `Day ${index + 1}`
        };
    });
    
    // Get all data keys except 'name' for the areas
    const allDataKeys = chartData.length > 0 
        ? Object.keys(chartData[0]).filter(key => key !== 'name')
        : [];
    
    // Separate 'Basislast elektriciteit' from other keys
    const dataKeys = allDataKeys.filter(key => key !== 'Basislast elektriciteitsvraag');
    const hasBasislast = allDataKeys.includes('Basislast elektriciteitsvraag');
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
                            selectedItems={dataKeys}
                            onToggleItem={() => {}} // No toggle functionality for now
                            legendData={metadata ? Object.fromEntries(Object.entries(metadata.properties).map(([key, value], index) => [key, value.color || colors[index % colors.length]])) : {}}
                            reverseOrder={false}
                        />
                    </div>
                    <div className="flex-1 min-h-0">
                        <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart
                                data={finalChartData}
                                margin={{
                                    top: 20,
                                    right: 30,
                                    left: 20,
                                    bottom: 5,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis 
                                    dataKey="name" 
                                    interval={Math.floor(finalChartData.length / 12)} // Show every Nth tick for ~12 labels
                                    tick={{ fontSize: 14 }}
                                />  
                                <YAxis label={(props: any) => <CustomYAxisLabel {...props} metadata={metadata} />}  tick={{ fontSize: 14 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <ReferenceLine y={0} stroke="#666" strokeWidth={1} />
                              
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
                                        strokeWidth={3}
                                        strokeDasharray="3 3"
                                        dot={false}
                                    />
                                )}
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                     </div>
                )}
            </div>
        </div>
    );
}
