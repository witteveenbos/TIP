
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer,CartesianGrid, Tooltip } from 'recharts';
//import curve_graph from './curve_graph.json'

export default function EnergyProfileGraph() {
    const data = [
  {
    name: 'Page A',
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: 'Page B',
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: 'Page C',
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: 'Page D',
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: 'Page E',
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: 'Page F',
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: 'Page G',
    uv: 3490,
    pv: 4300,
    amt: 2100,
  }
];
    return (
        <div className="flex flex-col max-h-[550px] flex-1">
            <div className="text-center p-8">
                <h3 className="text-lg font-semibold mb-4">Energie Profiel</h3>
                <p className="text-gray-600">Energie profiel grafiek komt hier..</p>
        <ResponsiveContainer width="100%" height="100%">
           <AreaChart
    
     
       width={500}
                height={300}
      data={data}
      margin={{
        top: 20,
        right: 0,
        left: 0,
        bottom: 0,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis  />
      <Tooltip />
      <Area type="monotone" dataKey="uv" stackId="1" stroke="#8884d8" fill="#8884d8" />
      <Area type="monotone" dataKey="pv" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
      <Area type="monotone" dataKey="amt" stackId="1" stroke="#ffc658" fill="#ffc658" />
     
    </AreaChart>
    </ResponsiveContainer>
            </div>
        </div>
    );
}
