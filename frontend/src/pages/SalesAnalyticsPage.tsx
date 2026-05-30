import { useState } from 'react';
import Header from '../components/layout/Header';
import ChartCard from '../components/common/ChartCard';
import SalesTrendChart from '../components/charts/SalesTrendChart';
import PaymentMethodChart from '../components/charts/PaymentMethodChart';
import { mockDailyTrends, mockPaymentBreakdown, mockSalesTrends } from '../utils/mockData';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, Legend,
} from 'recharts';
import { formatCurrency } from '../utils/formatters';

export default function SalesAnalyticsPage() {
  const [period, setPeriod] = useState<'daily' | 'weekly' | 'monthly'>('daily');

  // Weekly aggregation from daily data
  const weeklyData = [];
  for (let i = 0; i < mockDailyTrends.length; i += 7) {
    const chunk = mockDailyTrends.slice(i, i + 7);
    weeklyData.push({
      date: `Week ${Math.floor(i / 7) + 1}`,
      total_sales: chunk.reduce((s, d) => s + d.total_sales, 0),
      cash_sales: chunk.reduce((s, d) => s + d.cash_sales, 0),
      card_sales: chunk.reduce((s, d) => s + d.card_sales, 0),
      mobile_sales: chunk.reduce((s, d) => s + d.mobile_sales, 0),
      customers: chunk.reduce((s, d) => s + d.customers, 0),
      transactions: chunk.reduce((s, d) => s + d.transactions, 0),
    });
  }

  const trendData = period === 'daily' ? mockDailyTrends :
    period === 'weekly' ? weeklyData : mockDailyTrends;

  return (
    <div className="min-h-screen">
      <Header title="Sales Analytics" subtitle="Detailed sales performance analysis" />

      <div className="p-6 space-y-6">
        {/* Period Toggle */}
        <div className="flex items-center gap-2">
          {(['daily', 'weekly', 'monthly'] as const).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                period === p
                  ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/25'
                  : 'glass-card text-surface-600 dark:text-surface-400 hover:text-surface-900 dark:hover:text-white'
              }`}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>

        {/* Sales Trend */}
        <ChartCard title={`${period.charAt(0).toUpperCase() + period.slice(1)} Sales Trend`} subtitle="Sales performance over time">
          <SalesTrendChart data={trendData} />
        </ChartCard>

        {/* Row: Payment Methods + Transaction Volume */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ChartCard title="Payment Methods" subtitle="Revenue distribution by payment channel">
            <PaymentMethodChart data={mockPaymentBreakdown} />
          </ChartCard>

          <ChartCard title="Transaction Volume" subtitle="Number of transactions over time">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={trendData.map(d => ({ date: d.date.toString().slice(5), txns: d.transactions }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(30,41,59,0.9)', border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px', fontSize: '12px', color: '#f1f5f9',
                  }}
                />
                <Bar dataKey="txns" name="Transactions" fill="#6366f1" radius={[4, 4, 0, 0]} animationDuration={1200} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Top Products Placeholder */}
        <ChartCard title="Top Selling Products" subtitle="Awaiting Products table integration">
          <div className="flex flex-col items-center justify-center h-48 text-surface-400">
            <p className="text-sm">This section will be available once the Products table is connected.</p>
            <p className="text-xs mt-1">Sales by item and category breakdown will appear here.</p>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}
