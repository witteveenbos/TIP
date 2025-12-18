import { useEffect, useState, useMemo } from 'react';
import {
    Bar,
    BarChart,
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import { Checkbox } from '../ui/checkbox';
//types
import { GraphProps, GraphDataPoint } from '@/types/components/Graph';



export default function StartupDialogGraph({ scenario, data }: GraphProps) {
    console.log(scenario); // TODO Temporarly print scenario until it's used (to fix linter)
    console.log(data); // TODO Temporarly print data until it's used (to fix linter)
    const graphDataFromApi = data.graph.graphData;
    const metaDataFromApi = data.graph.metaData;

    const uniqueDragers = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.carrier)),
    ], [graphDataFromApi]);
    const uniqueSectors = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.sector)),
    ], [graphDataFromApi]);
    const uniqueBars = useMemo(() => [
        ...new Set(graphDataFromApi.map((item) => item.demandSupply)),
    ], [graphDataFromApi]);

    const [selectedDragers, setSelectedDragers] = useState(uniqueDragers);
    const [selectedSectors, setSelectedSectors] = useState(uniqueSectors);

    const [graphData, setGraphData] = useState([]);
    const [legendData, setLegendData] = useState([]);

    useEffect(() => {
        const graph = [];
        const legend = [];

        const graphData = graphDataFromApi.filter(
            (item) =>
                selectedDragers.includes(item.carrier) &&
                selectedSectors.includes(item.sector)
        );

        for (let i = 0; i < uniqueBars.length; i++) {
            const x: GraphDataPoint = {} as GraphDataPoint;
            x.name = uniqueBars[i];

            graphData
                .filter((item) => item.demandSupply === uniqueBars[i])
                .map((item) => {
                    x[item.carrier + ' - ' + item.sector] = item.value;
                    legend[item.carrier + ' - ' + item.sector] = item.color;
                });

            graph.push(x);
        }

        setGraphData(graph);
        setLegendData(legend);
    }, [selectedDragers, selectedSectors, data, graphDataFromApi, uniqueBars]);

    function getUniqueKeys() {
        const uniqueKeys = [];
        graphData.map((item) => {
            Object.keys(item).map((key) => {
                if (!uniqueKeys.includes(key)) {
                    uniqueKeys.push(key);
                }
            });
        });
        return uniqueKeys;
    }

    return (
        <div className="flex flex-col md:flex-row h-[250px] flex-1">
            <div className="">
                <h3 className="text-primary font-bold leading-6">Per drager</h3>
                {uniqueDragers.map((item) => (
                    <div key={item}>
                        <Checkbox
                            key={item}
                            id={item}
                            value={item}
                            defaultChecked={selectedDragers.includes(item)}
                            onCheckedChange={() => {
                                if (selectedDragers.includes(item)) {
                                    setSelectedDragers(
                                        selectedDragers.filter(
                                            (drager) => drager !== item
                                        )
                                    );
                                } else {
                                    setSelectedDragers([
                                        ...selectedDragers,
                                        item,
                                    ]);
                                }
                            }}></Checkbox>

                        <label className="ml-2" htmlFor={item}>
                            {item}
                        </label>
                    </div>
                ))}
                <hr />
                <h3 className="text-primary font-bold leading-6">Per sector</h3>
                {uniqueSectors.map((item) => (
                    <div key={item}>
                        <Checkbox
                            id={item}
                            key={item}
                            value={item}
                            defaultChecked={selectedSectors.includes(item)}
                            onCheckedChange={() => {
                                if (selectedSectors.includes(item)) {
                                    setSelectedSectors(
                                        selectedSectors.filter(
                                            (sector) => sector !== item
                                        )
                                    );
                                } else {
                                    setSelectedSectors([
                                        ...selectedSectors,
                                        item,
                                    ]);
                                }
                            }}></Checkbox>

                        <label htmlFor={item} className="ml-2">
                            {item}
                        </label>
                    </div>
                ))}
            </div>
            {graphData.length > 0 ? (
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
                                {`${metaDataFromApi.title} (${metaDataFromApi.unit})`}
                            </Label>
                        </YAxis>

                        <Tooltip />
                        <Legend align="left" />

                        {getUniqueKeys()
                            .filter((bar) => bar != 'name')
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
            ) : (
                'no data'
            )}
        </div>
    );
}
