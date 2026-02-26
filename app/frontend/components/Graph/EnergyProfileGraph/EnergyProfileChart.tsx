import { ComposedChart, Area, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip, ReferenceLine, Brush } from 'recharts';
import { useState, useMemo, useCallback } from 'react';
import React from 'react';
import CustomYAxisLabel from './CustomYAxisLabel';
import { EnergyProfileChartProps } from '@/types/components/EnergyProfileGraph';


export default function EnergyProfileChart({
    chartData,
    metadata,
    dataKeys,
    hasBasislast,
    colors
}: EnergyProfileChartProps) {
    // State for brush-based zooming with monthly segments
    const [selectedMonthRange, setSelectedMonthRange] = useState<{ startMonth: number; endMonth: number } | null>(null);
    
    const isZoomed = selectedMonthRange !== null;

    // Create 12-month brush data for better performance and UX
    const monthlyBrushData = useMemo(() => {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return months.map((month, index) => ({
            name: month,
            month: index,
            // Add a representative value for visual feedback in brush
            value: index + 1 
        }));
    }, []);

    // Calculate actual data indices from month selection
    const actualDataIndices = useMemo(() => {
        if (!selectedMonthRange) return null;
        
        const pointsPerMonth = Math.floor(chartData.length / 12);
        const startIndex = selectedMonthRange.startMonth * pointsPerMonth;
        const endIndex = selectedMonthRange.endMonth === 11 
            ? chartData.length - 1 
            : (selectedMonthRange.endMonth + 1) * pointsPerMonth - 1;
            
        return { startIndex, endIndex };
    }, [selectedMonthRange, chartData.length]);

    // Handle brush change - map from month indices to actual data
    const handleBrushChange = useCallback((e: any) => {
        if (e && 
            typeof e.startIndex === 'number' && 
            typeof e.endIndex === 'number' && 
            e.startIndex >= 0 && 
            e.endIndex >= 0 &&
            e.startIndex <= 11 &&
            e.endIndex <= 11 &&
            e.startIndex <= e.endIndex) {
                
            console.log('Month range selected:', { start: e.startIndex, end: e.endIndex });
            setSelectedMonthRange({ 
                startMonth: e.startIndex, 
                endMonth: e.endIndex 
            });
        } else {
            console.log('Clearing month selection');
            setSelectedMonthRange(null);
        }
    }, []);

    // Reset zoom function
    const resetZoom = useCallback(() => {
        setSelectedMonthRange(null);
    }, []);

    // Calculate display data based on month selection
    const displayData = useMemo(() => {
        if (!actualDataIndices) return chartData;
        
        return chartData.slice(actualDataIndices.startIndex, actualDataIndices.endIndex + 1);
    }, [chartData, actualDataIndices]);

    // Calculate X-axis interval for better performance
    const xAxisInterval = useMemo(() => {
        return Math.max(1, Math.floor(displayData.length / 12));
    }, [displayData.length]);

    const CustomTooltip = useCallback(({ active, payload, label }: any) => {
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
    }, [metadata?.unit]);

    return (
        <div className="w-full h-full min-h-[400px] flex flex-col">
           
            
            <div className="flex-1 min-h-[350px] max-h-[600px]">
                <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart
                        data={displayData}
                        margin={{
                            top: 20,
                            right: 30,
                            left: 20,
                            bottom: 60, // Space for brush component
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                            dataKey="name" 
                            interval={xAxisInterval}
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
                    
                        {/* Monthly brush with 12 segments for yearly data */}
                        <Brush 
                            key={`monthly-brush-${chartData.length}`}
                            data={monthlyBrushData}
                            dataKey="name"
                            height={60}
                            stroke="#003461"
                            fill="rgba(0, 52, 97, 0.2)"
                            onChange={handleBrushChange}
                            startIndex={selectedMonthRange?.startMonth ?? undefined}
                            endIndex={selectedMonthRange?.endMonth ?? undefined}
                            tickFormatter={(value) => value} // Shows month names directly
                            travellerWidth={8}
                        />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
