import { type LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { useCountUp } from '../../hooks/useCountUp';
import { formatCurrency, formatNumber } from '../../utils/formatters';
import {
  LineChart, Line, ResponsiveContainer,
} from 'recharts';

interface KPICardProps {
  title: string;
  value: number;
  change: number;
  icon: LucideIcon;
  iconColor: string;
  iconBg: string;
  isCurrency?: boolean;
  sparkData?: number[];
  delay?: number;
}

export default function KPICard({
  title, value, change, icon: Icon,
  iconColor, iconBg, isCurrency = true, sparkData, delay = 0,
}: KPICardProps) {
  const animatedValue = useCountUp(value, 1200);

  const isPositive = change >= 0;
  const TrendIcon = isPositive ? TrendingUp : TrendingDown;
  const trendClass = isPositive ? 'kpi-trend-up' : 'kpi-trend-down';

  // Generate sparkline data
  const sparkline = sparkData || Array.from({ length: 7 }, () => Math.random() * 100);
  const chartData = sparkline.map((v, i) => ({ v, i }));

  return (
    <div
      className="kpi-card animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start justify-between mb-3">
        <div
          className="kpi-icon"
          style={{ backgroundColor: iconBg }}
        >
          <Icon size={20} style={{ color: iconColor }} />
        </div>
        <div className={trendClass}>
          <TrendIcon size={14} />
          <span>{isPositive ? '+' : ''}{change.toFixed(1)}%</span>
        </div>
      </div>

      <p className="kpi-label mb-1">{title}</p>
      <p className="kpi-value text-surface-900 dark:text-white">
        {isCurrency
          ? formatCurrency(animatedValue)
          : formatNumber(Math.round(animatedValue))
        }
      </p>

      {/* Mini Sparkline */}
      <div className="mt-3 h-8 -mx-1">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <Line
              type="monotone"
              dataKey="v"
              stroke={isPositive ? '#10b981' : '#f43f5e'}
              strokeWidth={1.5}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
