import Header from '../components/layout/Header';
import ChartCard from '../components/common/ChartCard';
import KPICard from '../components/common/KPICard';
import BranchCompareChart from '../components/charts/BranchCompareChart';
import { mockBranchPerformance, mockKPI } from '../utils/mockData';
import { formatCurrencyFull, formatNumber } from '../utils/formatters';
import { GitBranch, Users, TrendingUp, Target } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, Radar, Legend,
} from 'recharts';

export default function BranchAnalyticsPage() {
  const branches = mockBranchPerformance;

  // Radar data for branch comparison
  const radarData = [
    { metric: 'Sales', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.total_sales / 1000])) },
    { metric: 'Customers', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.total_customers])) },
    { metric: 'Cash', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.cash_sales / 1000])) },
    { metric: 'Mobile', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.mobile_sales / 1000])) },
    { metric: 'Card', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.card_sales / 1000])) },
    { metric: 'Avg Txn', ...Object.fromEntries(branches.map(b => [b.branch_name.slice(0, 10), b.avg_transaction / 100])) },
  ];

  return (
    <div className="min-h-screen">
      <Header title="Branch Analytics" subtitle="Compare performance across all branches" />

      <div className="p-6 space-y-6">
        {/* Branch KPI cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <KPICard title="Total Branches" value={branches.length} change={0} icon={GitBranch}
            iconColor="#6366f1" iconBg="rgba(99,102,241,0.15)" isCurrency={false} delay={0} />
          <KPICard title="Combined Sales" value={branches.reduce((s, b) => s + b.total_sales, 0)} change={12.5} icon={TrendingUp}
            iconColor="#10b981" iconBg="rgba(16,185,129,0.15)" delay={80} />
          <KPICard title="Total Customers" value={branches.reduce((s, b) => s + b.total_customers, 0)} change={8.4} icon={Users}
            iconColor="#f59e0b" iconBg="rgba(245,158,11,0.15)" isCurrency={false} delay={160} />
          <KPICard title="Avg Transaction" value={mockKPI.avg_transaction_value} change={3.2} icon={Target}
            iconColor="#06b6d4" iconBg="rgba(6,182,212,0.15)" delay={240} />
        </div>

        {/* Branch Comparison Chart */}
        <ChartCard title="Branch Sales Comparison" subtitle="Stacked sales by payment channel">
          <BranchCompareChart data={branches} />
        </ChartCard>

        {/* Branch Rankings Table */}
        <div className="glass-card p-5">
          <h3 className="chart-title mb-4">Branch Rankings</h3>
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Branch</th>
                  <th>Total Sales</th>
                  <th>Customers</th>
                  <th>Cash Sales</th>
                  <th>Mobile Sales</th>
                  <th>Card Sales</th>
                  <th>Avg Transaction</th>
                </tr>
              </thead>
              <tbody>
                {branches
                  .sort((a, b) => b.total_sales - a.total_sales)
                  .map((branch, i) => (
                    <tr key={branch.branch_code}>
                      <td>
                        <span className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                          i === 0 ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' :
                          'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400'
                        }`}>
                          #{i + 1}
                        </span>
                      </td>
                      <td className="font-medium text-surface-800 dark:text-surface-200">{branch.branch_name}</td>
                      <td className="font-semibold text-surface-900 dark:text-white">{formatCurrencyFull(branch.total_sales)}</td>
                      <td>{formatNumber(branch.total_customers)}</td>
                      <td className="text-emerald-600 dark:text-emerald-400">{formatCurrencyFull(branch.cash_sales)}</td>
                      <td className="text-cyan-600 dark:text-cyan-400">{formatCurrencyFull(branch.mobile_sales)}</td>
                      <td className="text-brand-600 dark:text-brand-400">{formatCurrencyFull(branch.card_sales)}</td>
                      <td>{formatCurrencyFull(branch.avg_transaction)}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
