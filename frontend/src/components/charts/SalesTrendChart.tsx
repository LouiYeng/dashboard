import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend,
} from 'recharts';
import type { DailySummary } from '../../types/api';
import { formatCurrency } from '../../utils/formatters';

interface SalesTrendChartProps {
  data: DailySummary[];
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card p-3 !rounded-lg text-xs min-w-[160px]">
      <p className="font-semibold text-surface-800 dark:text-white mb-2">{label}</p>
      {payload.map((entry: any, i: number) => (
        <div key={i} className="flex items-center justify-between gap-4 mb-1">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
            <span className="text-surface-500 dark:text-surface-400">{entry.name}</span>
          </div>
          <span className="font-medium text-surface-800 dark:text-white">
            {formatCurrency(entry.value)}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function SalesTrendChart({ data }: SalesTrendChartProps) {
  const chartData = data.map(d => ({
    ...d,
    date: d.date.slice(5), // MM-DD format
  }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <AreaChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="gradTotal" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="gradCash" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#10b981" stopOpacity={0.2} />
            <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="gradMobile" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.2} />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 11, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          tick={{ fontSize: 11, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => `${(v / 1000).toFixed(0)}K`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }}
        />
        <Area
          type="monotone"
          dataKey="total_sales"
          name="Total Sales"
          stroke="#6366f1"
          strokeWidth={2}
          fill="url(#gradTotal)"
          animationDuration={1500}
        />
        <Area
          type="monotone"
          dataKey="cash_sales"
          name="Cash"
          stroke="#10b981"
          strokeWidth={1.5}
          fill="url(#gradCash)"
          animationDuration={1500}
          animationBegin={200}
        />
        <Area
          type="monotone"
          dataKey="mobile_sales"
          name="Mobile"
          stroke="#06b6d4"
          strokeWidth={1.5}
          fill="url(#gradMobile)"
          animationDuration={1500}
          animationBegin={400}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
