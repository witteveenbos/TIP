import dynamic from 'next/dynamic';
import { EnergyProfileChartProps } from '@/types/components/EnergyProfileGraph';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function EnergyProfileChart({ graphData, graphMeta }: EnergyProfileChartProps) {
    const stackgroupOrder: Record<string, number> = { one: 0, two: 1 };
    const traces = (graphMeta.xTickLabels
        ? graphData.data.map(trace => ({ ...trace, x: graphMeta.xTickLabels }))
        : graphData.data
    ).sort((a, b) => {
        const aOrder = stackgroupOrder[(a as any).stackgroup] ?? 99;
        const bOrder = stackgroupOrder[(b as any).stackgroup] ?? 99;
        return aOrder - bOrder;
    });

    const gridStyle = { gridcolor: '#d1d5db', griddash: 'dot' as const, gridwidth: 1 };

    const sharedAnnotationStyle = {
        xref: 'paper' as const,
        xanchor: 'right' as const,
        showarrow: false,
        textangle: -90,
    };

    const yAxisAnnotations = [
        {
            ...sharedAnnotationStyle,
            x: -0.06,
            text: 'Vermogen (MW)',
            font: { size: 16,  color: '#374151', weight: 'bold'},
            yref: 'y' as const,
            y: 0,
            yanchor: 'middle' as const,
            
        },
        {
            ...sharedAnnotationStyle,
            x: -0.04,
            text: 'Aanbod',
            font: { size: 14,  color: '#374151', weight: 'bold'},
            yref: 'paper' as const,
            y: 0.75,
            yanchor: 'middle' as const,
           
        },
        {
            ...sharedAnnotationStyle,
            x: -0.04,
            text: 'Vraag',
            font: { size: 14,  color: '#374151', weight: 'bold'},
            yref: 'paper' as const,
            y: 0.25,
            yanchor: 'middle' as const,
            
        },
    ];

    const layout = {
        ...graphData.layout,
        title: undefined,
        autosize: true,
        margin: { t: 10, r: 10, b: 60, l: 0 },
        legend: { orientation: 'v' as const, font: { size: 14 }, title: { text: 'Selecteer energieprofielen' }, x: -0.2, xanchor: 'right' as const, y: 1, groupclick: 'toggleitem' as const },
        hovermode: 'x unified' as const,
        paper_bgcolor: '#ffffff',
        plot_bgcolor: '#ffffff',
        xaxis: { ...(graphData.layout as any)?.xaxis, hoverformat: '%d-%m-%Y %H:%M', ...gridStyle },
        yaxis: { ...(graphData.layout as any)?.yaxis, ...gridStyle },
        annotations: yAxisAnnotations,
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
