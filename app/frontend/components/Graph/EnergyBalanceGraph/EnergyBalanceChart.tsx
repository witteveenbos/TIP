import {
    Bar,
    BarChart,
    CartesianGrid,
    Label,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import { EnergyBalanceChartProps } from '@/types/components/Graph';


export default function EnergyBalanceChart({
    graphData,
    legendData,
    metaData,
}: EnergyBalanceChartProps) {
    const getUniqueKeys = () => {
        const uniqueKeys = [];
        graphData.map((item) => {
            Object.keys(item).map((key) => {
                if (!uniqueKeys.includes(key)) {
                    uniqueKeys.push(key);
                }
            });
        });
        return uniqueKeys;
    };

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            // Reverse the payload order to match the visual stacking order
            const reversedPayload = [...payload].reverse();
            
            return (
                <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
                    <p className="font-medium">{`${label}`}</p>
                    {reversedPayload.map((entry: any, index: number) => (
                        <p key={index} >
                            {`${entry.name}: ${entry.value.toFixed(2)}`}
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    if (graphData.length === 0) {
        return (
            <div className="flex items-center justify-center h-full text-gray-500">
                Geen data beschikbaar
            </div>
        );
    }

    return (
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
                        {`${metaData.title} (${metaData.unit})`}
                    </Label>
                </YAxis>
                <Tooltip content={<CustomTooltip />} />
                {getUniqueKeys()
                    .filter((bar) => bar !== 'name')
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
    );
}