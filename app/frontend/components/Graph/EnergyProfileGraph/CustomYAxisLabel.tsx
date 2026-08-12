interface CustomYAxisLabelProps {
    viewBox?: {
        x: number;
        y: number;
        width: number;
        height: number;
    };
    metadata?: { yLabelText?: string } | null;
    // Allow any additional props that Recharts might pass
    [key: string]: any;
}

export default function CustomYAxisLabel({ viewBox, metadata, ...props }: CustomYAxisLabelProps) {
    // Use viewBox from props if passed directly, otherwise extract from Recharts props
    const actualViewBox = viewBox || props.viewBox;
    
    if (!actualViewBox) {
        return null;
    }
    
    const { x, y, width, height } = actualViewBox;
    const centerY = y + height / 2;
    
    return (
        <g>
            {/* Main Y-axis label (Vermogen) - rotated on the left */}
            <text
                x={x - 10}
                y={centerY}
                textAnchor="middle"
                dominantBaseline="central"
                transform={`rotate(-90, ${x - 10}, ${centerY})`}
                style={{ fontSize: '16px', fill: '#666', fontWeight: 'bold' }}
            >
                {metadata?.yLabelText || 'Waarde'}
            </text>
            
            {/* Aanbod label - right side, upper area */}
            <text
                x={x + width - 50}
                y={y + height * 0.25}
                textAnchor="start"
                dominantBaseline="central"
                transform={`rotate(-90, ${x + width - 50}, ${y + height * 0.25})`}
                style={{ fontSize: '14px', fill: '#666', fontWeight: 'bold' }}
            >
                Aanbod
            </text>
            
            {/* Vraag label - right side, lower area */}
            <text
                x={x + width - 50}
                y={y + height * 0.75}
                textAnchor="start"
                dominantBaseline="central"
                transform={`rotate(-90, ${x + width - 50}, ${y + height * 0.75})`}
                style={{ fontSize: '14px', fill: '#666', fontWeight: 'bold' }}
            >
                Vraag
            </text>
        </g>
    );
}