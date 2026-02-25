import { ComposedChart, Area, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';
import CustomYAxisLabel from './CustomYAxisLabel';
import { EnergyProfileChartProps } from '@/types/components/EnergyProfileGraph';


export default function EnergyProfileChart({
    chartData,
    metadata,
    dataKeys,
    hasBasislast,
    colors
}: EnergyProfileChartProps) {
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
                    <p className="font-semibold">{label}</p>
                    {/* Show Aanbod first */}
                    {groupedPayload['Aanbod'] && (
                        <>
                            <p className="font-semibold text-sm mt-2">Aanbod</p>
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
                            <p className="font-semibold text-sm mt-2">Vraag</p>
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

    return (
        <ResponsiveContainer width="100%" height="100%">
            <ComposedChart
                data={chartData}
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
                    interval={Math.floor(chartData.length / 12)} // Show every Nth tick for ~12 labels
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
    );
}
