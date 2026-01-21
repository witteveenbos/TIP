import { useMemo, useEffect, useState } from 'react';
import { GraphDataPoint } from '@/types/components/Graph';
import { GraphApiData, ViewMode } from '@/types/components/Graph';



export function useEnergyBalanceData(
    data: GraphApiData,
    viewMode: ViewMode,
    selectedDragers: string[],
    selectedSectors: string[]
) {
    const [graphData, setGraphData] = useState([]);
    const [legendData, setLegendData] = useState({});

    const graphDataFromApi = data.graph.graphData;

    const uniqueDragers = useMemo(() => {
        const dragerMap = new Map();
        graphDataFromApi.forEach((item) => {
            if (!dragerMap.has(item.carrier)) {
                dragerMap.set(item.carrier, {
                    name: item.carrier,
                    demandSupply: item.demandSupply
                });
            }
        });
        return Array.from(dragerMap.values());
    }, [graphDataFromApi]);

    const uniqueSectors = useMemo(() => {
        const sectorMap = new Map();
        graphDataFromApi.forEach((item) => {
            if (!sectorMap.has(item.sector)) {
                sectorMap.set(item.sector, {
                    name: item.sector,
                    demandSupply: item.demandSupply
                });
            }
        });
        return Array.from(sectorMap.values());
    }, [graphDataFromApi]);

    const uniqueBars = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.demandSupply)),
    ], [graphDataFromApi]);

    // Define consistent colors for sectors
    const sectorColors = useMemo(() => {
        const colors = [
            '#5D7929', '#4169E1', '#854321', '#FF8400', '#8B0000',
            '#87CEEB', '#CCCCCC', '#333333', '#FFD900', '#1ce6d6',
        ];
        
        const colorMap = {};
        uniqueSectors.forEach((sector, index) => {
            colorMap[sector.name] = colors[index % colors.length];
        });
        return colorMap;
    }, [uniqueSectors]);

    useEffect(() => {
        const graph = [];
        const legend = {};

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
    }, [selectedDragers, selectedSectors, viewMode, data, graphDataFromApi, uniqueBars, sectorColors]);

    return {
        graphData,
        legendData,
        uniqueDragers,
        uniqueSectors,
        uniqueBars,
    };
}