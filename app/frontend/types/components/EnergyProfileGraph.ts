import { GraphDataPoint } from "./Graph";
export interface EnergyProfileGraphProps {
    enabled?: boolean;
}

export interface GraphData {
    [key: string]: number | string;
}

export interface GraphMetadata {
    title: string;
    unit: string;
    yLabelText: string;
    xTickLabels?: string[];
    properties?: { [key: string]: { [key: string]: string } };
}

export interface GraphResponse {
    metaData: GraphMetadata;
    graphData: GraphData[];
}

export interface EnergyProfileChartProps {
    chartData: GraphDataPoint[];
    metadata: GraphMetadata;
    dataKeys: string[];
    hasBasislast: boolean;
    colors: string[];
}