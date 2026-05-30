import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend, Cell,
} from 'recharts';
import type { BranchPerformance } from '../../types/api';
import { formatCurrency } from '../../utils/formatters';

interface BranchCompareChartProps {
  data: BranchPerformance[];
}

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#a855f7'];

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card p-3 !rounded-lg text-xs min-w-[180px]">
      <p className="font-semibold text-surface-800 dark:text-white mb-2">{label}</p>
      {payload.map((entry: any, i: number) => (
        <div key={i} className="flex justify-between gap-4 mb-1">
          <span className="text-surface-500 dark:text-surface-400">{entry.name}</span>
          <span className="font-medium text-surface-800 dark:text-white">
            {formatCurrency(entry.value)}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function BranchCompareChart({ data }: BranchCompareChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
        <XAxis
          dataKey="branch_name"
          tick={{ fontSize: 11, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => v.length > 15 ? v.slice(0, 15) + '…' : v}
        />
        <YAxis
          tick={{ fontSize: 11, fill: '#94a3b8' }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => `${(v / 1000).toFixed(0)}K`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: '11px' }} />
        <Bar
          dataKey="cash_sales"
          name="Cash"
          stackId="a"
          fill="#10b981"
          radius={[0, 0, 0, 0]}
          animationDuration={1200}
        />
        <Bar
          dataKey="mobile_sales"
          name="Mobile"
          stackId="a"
          fill="#06b6d4"
          animationDuration={1200}
          animationBegin={200}
        />
        <Bar
          dataKey="card_sales"
          name="Card"
          stackId="a"
          fill="#6366f1"
          radius={[6, 6, 0, 0]}
          animationDuration={1200}
          animationBegin={400}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
