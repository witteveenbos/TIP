import { useEffect, useState, useMemo } from 'react';
import {
    Bar,
    BarChart,
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import { Checkbox } from '../ui/checkbox';
//types
import { GraphProps, GraphDataPoint } from '@/types/components/Graph';

type ViewMode = 'dragers' | 'sectors';

export default function EnergyBalanceGraph({ scenario, data }: GraphProps) {
    console.log(scenario); // TODO Temporarly print scenario until it's used (to fix linter)
    console.log(data); // TODO Temporarly print data until it's used (to fix linter)
    const graphDataFromApi = data.graph.graphData;
    const metaDataFromApi = data.graph.metaData;

    const uniqueDragers = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.carrier)),
    ], [graphDataFromApi]);
    const uniqueSectors = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.sector)),
    ], [graphDataFromApi]);
    const uniqueBars = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.demandSupply)),
    ], [graphDataFromApi]);

    const [viewMode, setViewMode] = useState<ViewMode>('dragers');
    const [selectedDragers, setSelectedDragers] = useState(uniqueDragers);
    const [selectedSectors, setSelectedSectors] = useState(uniqueSectors);

    const [graphData, setGraphData] = useState([]);
    const [legendData, setLegendData] = useState([]);

    // Define consistent colors for sectors
    const sectorColors = useMemo(() => {
        const colors = [
            '#5D7929', // Forest Green (similar to Biogene brandstoffen)
            '#4169E1', // Royal Blue (similar to Elektriciteit)
            '#854321', // Brown (similar to Olie)
            '#FF8400', // Orange (similar to Geothermisch)
            '#8B0000', // Dark Red (similar to Warmte)
            '#87CEEB', // Sky Blue (similar to Waterstof)
            '#CCCCCC', // Gray (similar to Netwerkgas)
            '#333333', // Dark Gray (similar to Kolen)
            '#FFD900', // Yellow (similar to Zonthermie)
            '#1ce6d6', // Cyan (similar to Ammoniak)
        ];
        
        const colorMap = {};
        uniqueSectors.forEach((sector, index) => {
            colorMap[sector] = colors[index % colors.length];
        });
        return colorMap;
    }, [uniqueSectors]);

    useEffect(() => {
        const graph = [];
        const legend = [];

        const filteredData = graphDataFromApi.filter(
            (item) =>
                selectedDragers.includes(item.carrier) &&
                selectedSectors.includes(item.sector)
        );

        if (viewMode === 'dragers') {
            // Group by demandSupply (x-axis), show carriers as different bars
            for (let i = 0; i < uniqueBars.length; i++) {
                const x: GraphDataPoint = {} as GraphDataPoint;
                x.name = uniqueBars[i];

                filteredData
                    .filter((item) => item.demandSupply === uniqueBars[i])
                    .forEach((item) => {
                        if (x[item.carrier]) {
                            x[item.carrier] += item.value;
                        } else {
                            x[item.carrier] = item.value;
                            legend[item.carrier] = item.color;
                        }
                    });

                graph.push(x);
            }
        } else {
            // Group by demandSupply (x-axis), show sectors as different bars
            for (let i = 0; i < uniqueBars.length; i++) {
                const x: GraphDataPoint = {} as GraphDataPoint;
                x.name = uniqueBars[i];

                filteredData
                    .filter((item) => item.demandSupply === uniqueBars[i])
                    .forEach((item) => {
                        if (x[item.sector]) {
                            x[item.sector] += item.value;
                        } else {
                            x[item.sector] = item.value;
                            legend[item.sector] = sectorColors[item.sector];
                        }
                    });

                graph.push(x);
            }
        }

        setGraphData(graph);
        setLegendData(legend);
    }, [selectedDragers, selectedSectors, viewMode, data, graphDataFromApi, uniqueBars]);

    function getUniqueKeys() {
        const uniqueKeys = [];
        graphData.map((item) => {
            Object.keys(item).map((key) => {
                if (!uniqueKeys.includes(key)) {
                    uniqueKeys.push(key);
                }
            });
        });
        return uniqueKeys;
    }

    return (
        <div className="flex flex-col h-[350px] flex-1">
             {/* View Mode Toggle */}
                <div className="mb-4">
                    <h3 className="text-primary font-bold leading-6 mb-2">Weergave</h3>
                    <div className="flex gap-4">
                        <label className="flex items-center">
                            <input
                                type="radio"
                                name="viewMode"
                                value="dragers"
                                checked={viewMode === 'dragers'}
                                onChange={(e) => setViewMode(e.target.value as ViewMode)}
                                className="mr-2"
                            />
                            Dragers
                        </label>
                        <label className="flex items-center">
                            <input
                                type="radio"
                                name="viewMode"
                                value="sectors"
                                checked={viewMode === 'sectors'}
                                onChange={(e) => setViewMode(e.target.value as ViewMode)}
                                className="mr-2"
                            />
                            Sectoren
                        </label>
                    </div>
                </div>
                <hr className="mb-4" />
        <div className="flex flex-col md:flex-row flex-1">{/* Removed fixed height h-[250px] */}
            <div className="">
               

                {/* Conditional Checkbox Sections */}
                {viewMode === 'sectors' && (
                    <>
                        <h3 className="text-primary font-bold leading-6">Filter sectoren</h3>
                        {uniqueSectors.map((item) => (
                            <div key={item}>
                                <Checkbox
                                    id={item}
                                    key={item}
                                    value={item}
                                    defaultChecked={selectedSectors.includes(item)}
                                    onCheckedChange={() => {
                                        if (selectedSectors.includes(item)) {
                                            setSelectedSectors(
                                                selectedSectors.filter(
                                                    (sector) => sector !== item
                                                )
                                            );
                                        } else {
                                            setSelectedSectors([
                                                ...selectedSectors,
                                                item,
                                            ]);
                                        }
                                    }}></Checkbox>

                                <label htmlFor={item} className="ml-2">
                                    {item}
                                </label>
                            </div>
                        ))}
                    </>
                )}

                {viewMode === 'dragers' && (
                    <>
                        <h3 className="text-primary font-bold leading-6">Filter dragers</h3>
                        {uniqueDragers.map((item) => (
                            <div key={item}>
                                <Checkbox
                                    key={item}
                                    id={item}
                                    value={item}
                                    defaultChecked={selectedDragers.includes(item)}
                                    onCheckedChange={() => {
                                        if (selectedDragers.includes(item)) {
                                            setSelectedDragers(
                                                selectedDragers.filter(
                                                    (drager) => drager !== item
                                                )
                                            );
                                        } else {
                                            setSelectedDragers([
                                                ...selectedDragers,
                                                item,
                                            ]);
                                        }
                                    }}></Checkbox>

                                <label className="ml-2" htmlFor={item}>
                                    {item}
                                </label>
                            </div>
                        ))}
                    </>
                )}
            </div>
            {graphData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        width={500}
                        height={300}
                        data={graphData}
                        margin={{
                            top: 20,
                            right: 30,
                            left: 20,
                            bottom: 5,
                        }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis>
                            <Label angle={-90} dx={-20}>
                                {`${metaDataFromApi.title} (${metaDataFromApi.unit})`}
                            </Label>
                        </YAxis>

                        <Tooltip 
                            formatter={(value: number, name: string) => [
                                value.toFixed(2), 
                                name
                            ]}
                        />
                        <Legend align="left" />

                        {getUniqueKeys()
                            .filter((bar) => bar != 'name')
                            .map((item, index) => (
                                <Bar
                                    key={index}
                                    isAnimationActive={false}
                                    dataKey={item}
                                    stackId="a"
                                    fill={legendData[item]}
                                />
                            ))}
                    </BarChart>
                </ResponsiveContainer>
            ) : (
                'Geen data beschikbaar'
            )}
        </div>
        </div>
    );
}
