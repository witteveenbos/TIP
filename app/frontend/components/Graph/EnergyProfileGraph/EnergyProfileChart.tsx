import dynamic from 'next/dynamic';
import { EnergyProfileChartProps } from '@/types/components/EnergyProfileGraph';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function EnergyProfileChart({ graphData, graphMeta }: EnergyProfileChartProps) {
    // Apply overrides to specific traces based on their name or stackgroup - this will be removed later, as this will be implemented in the backend
    const applyOverrides = (trace: (typeof graphData.data)[number]) => {
        const t = trace as any;
        const originalStackgroup: string | undefined = t.stackgroup;
        let result = t;

        if (t.name === 'Basislast elektriciteitsvraag') {
            const { stackgroup, ...rest } = t;
            result = { ...rest, fill: 'none', line: { ...rest.line, dash: 'dot' } };
        }

        if (originalStackgroup === 'two') {
            const y = Array.isArray(result.y) ? result.y.map((v: number) => -v) : result.y;
            result = { ...result, y };
        }

        const legendGroupMap: Record<string, string> = { one: 'Aanbod', two: 'Vraag' };
        const legendgroup = originalStackgroup ? legendGroupMap[originalStackgroup] ?? originalStackgroup : undefined;
        if (legendgroup) {
            result = { ...result, legendgroup, legendgrouptitle: { text: legendgroup } };
        }

        return result;
    };

    const traces = graphMeta.xTickLabels
        ? graphData.data.map(trace => applyOverrides({ ...trace, x: graphMeta.xTickLabels }))
        : graphData.data.map(applyOverrides);

    const layout = {
        ...graphData.layout,
        title: { text: graphMeta.title },
        autosize: true,
        margin: { t: 40, r: 20, b: 60, l: 60 },
        legend: { orientation: 'v' as const },
        hovermode: 'x unified' as const,
        xaxis: { ...(graphData.layout as any)?.xaxis, hoverformat: '%d-%m-%Y %H:%M' },
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
