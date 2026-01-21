export interface GraphApiData {
    graph: {
        graphData: Array<{
            carrier: string;
            sector: string;
            demandSupply: string;
            value: number;
            color: string;
        }>;
        metaData: {
            title: string;
            unit: string;
        };
    };
}

export interface GraphProps {
    scenario: string;
    data: GraphApiData;   
    };


// Type for individual graph data points
export type GraphDataPoint = {
    name: string;
    [key: string]: string | number;
};
export interface EnergyBalanceChartProps {
    graphData: GraphDataPoint[];
    legendData: Record<string, string>;
    metaData: {
        title: string;
        unit: string;
    };
}

export type ViewMode = 'dragers' | 'sectors';

export interface FilterItem {
    name: string;
    demandSupply: string;
}

export interface FilterSectionProps {
    title: string;
    items: FilterItem[];
    selectedItems: string[];
    onToggleItem: (item: string) => void;
    legendData: Record<string, string>;
}

