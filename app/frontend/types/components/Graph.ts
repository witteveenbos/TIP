export interface GraphProps {
    scenario: string;
    data: {
        graph: {
            graphData: {
                carrier: string;
                sector: string;
                demandSupply: string;
                value: number;
                color: string;
            }[];
            metaData: {
                title: string;
                unit: string;
                plotType: string;
                xGrouping?: string;
                yGrouping?: string;
                xLabelText?: string;
                yLabelText?: string;
            };
        };
    };
}

// Type for individual graph data points
export type GraphDataPoint = {
    name: string;
    [key: string]: string | number;
};