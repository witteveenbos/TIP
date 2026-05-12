import dynamic from 'next/dynamic';
import { EnergyProfileChartProps } from '@/types/components/EnergyProfileGraph';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function EnergyProfileChart({ graphData, graphMeta }: EnergyProfileChartProps) {
    const traces = graphMeta.xTickLabels
        ? graphData.data.map(trace => ({ ...trace, x: graphMeta.xTickLabels }))
        : graphData.data;

    const layout = {
        ...graphData.layout,
        title: { text: graphMeta.title },
        autosize: true,
        margin: { t: 40, r: 20, b: 60, l: 60 },
        legend: { orientation: 'v' as const },
    };

    return (
        <div className="w-full h-full min-h-[400px]">
            <Plot
                data={traces as Plotly.Data[]}
                layout={layout}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler
                config={{ responsive: true, displayModeBar: true }}
            />
        </div>
    );
}
