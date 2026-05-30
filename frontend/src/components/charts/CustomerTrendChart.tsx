import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer,
} from 'recharts';
import type { DailySummary } from '../../types/api';

interface CustomerTrendChartProps {
  data: DailySummary[];
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card p-3 !rounded-lg text-xs">
      <p className="font-semibold text-surface-800 dark:text-white">{label}</p>
      <p className="text-surface-500 dark:text-surface-400 mt-1">
        {payload[0]?.value?.toLocaleString()} customers
      </p>
    </div>
  );
}

export default function CustomerTrendChart({ data }: CustomerTrendChartProps) {
  const chartData = data.map(d => ({
    date: d.date.slice(5),
    customers: d.customers,
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 10, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          tick={{ fontSize: 10, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip content={<CustomTooltip />} />
        <Line
          type="monotone"
          dataKey="customers"
          stroke="#f59e0b"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: '#f59e0b' }}
          animationDuration={1500}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
