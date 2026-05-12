export interface EnergyProfileGraphProps {
    enabled?: boolean;
}

export interface PlotlyTrace {
    name: string;
    type: string;
    mode?: string;
    x?: (string | number)[];
    y?: (string | number)[];
    line?: { color?: string; [key: string]: any };
    stackgroup?: string;
    fill?: string;
    fillcolor?: string;
    [key: string]: any;
}

export interface PlotlyLayout {
    template?: {
        data?: Record<string, any>;
        layout?: Record<string, any>;
    };
    [key: string]: any;
}

export interface PlotlyGraphData {
    data: PlotlyTrace[];
    layout: PlotlyLayout;
}

export interface GraphMeta {
    title: string;
    plotType: string;
    xTickLabels?: string[];
}

export interface GraphResponse {
    graphData: PlotlyGraphData;
    graphMeta: GraphMeta;
}

export interface EnergyProfileChartProps {
    graphData: PlotlyGraphData;
    graphMeta: GraphMeta;
}