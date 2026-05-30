import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend,
} from 'recharts';
import type { PaymentMethodBreakdown } from '../../types/api';
import { formatCurrency } from '../../utils/formatters';

interface PaymentMethodChartProps {
  data: PaymentMethodBreakdown[];
}

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const item = payload[0];
  return (
    <div className="glass-card p-3 !rounded-lg text-xs">
      <p className="font-semibold text-surface-800 dark:text-white">{item.name}</p>
      <p className="text-surface-500 dark:text-surface-400 mt-1">
        {formatCurrency(item.value)} ({item.payload.percentage}%)
      </p>
    </div>
  );
}

function CustomLegend({ payload }: any) {
  return (
    <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 mt-2">
      {payload?.map((entry: any, i: number) => (
        <div key={i} className="flex items-center gap-2 text-xs">
          <span
            className="w-2.5 h-2.5 rounded-full flex-shrink-0"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-surface-600 dark:text-surface-400 truncate">
            {entry.value}
          </span>
          <span className="text-surface-800 dark:text-surface-200 font-medium ml-auto">
            {entry.payload?.percentage}%
          </span>
        </div>
      ))}
    </div>
  );
}

export default function PaymentMethodChart({ data }: PaymentMethodChartProps) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={95}
            paddingAngle={3}
            dataKey="amount"
            nameKey="method"
            animationDuration={1200}
            animationBegin={200}
          >
            {data.map((entry, i) => (
              <Cell
                key={i}
                fill={entry.color}
                stroke="transparent"
                className="transition-opacity duration-200 hover:opacity-80"
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
      <CustomLegend
        payload={data.map(d => ({
          value: d.method,
          color: d.color,
          payload: d,
        }))}
      />
    </div>
  );
}
