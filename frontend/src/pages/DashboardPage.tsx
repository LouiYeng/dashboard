import {
  DollarSign, ShoppingCart, TrendingDown, TrendingUp,
  Wallet, Users, Receipt, ArrowUpDown,
} from 'lucide-react';
import Header from '../components/layout/Header';
import KPICard from '../components/common/KPICard';
import ChartCard from '../components/common/ChartCard';
import SalesTrendChart from '../components/charts/SalesTrendChart';
import PaymentMethodChart from '../components/charts/PaymentMethodChart';
import BranchCompareChart from '../components/charts/BranchCompareChart';
import CustomerTrendChart from '../components/charts/CustomerTrendChart';
import {
  mockKPI, mockPaymentBreakdown,
  mockBranchPerformance, mockDailyTrends,
} from '../utils/mockData';
import { formatCurrencyFull } from '../utils/formatters';

export default function DashboardPage() {
  const kpi = mockKPI;

  const kpiCards = [
    {
      title: 'Total Sales',
      value: kpi.total_sales,
      change: kpi.sales_change,
      icon: DollarSign,
      iconColor: '#6366f1',
      iconBg: 'rgba(99, 102, 241, 0.15)',
    },
    {
      title: 'Total Purchases',
      value: kpi.total_purchases,
      change: kpi.purchases_change,
      icon: ShoppingCart,
      iconColor: '#06b6d4',
      iconBg: 'rgba(6, 182, 212, 0.15)',
    },
    {
      title: 'Gross Profit',
      value: kpi.gross_profit,
      change: kpi.profit_change,
      icon: TrendingUp,
      iconColor: '#10b981',
      iconBg: 'rgba(16, 185, 129, 0.15)',
    },
    {
      title: 'Net Profit',
      value: kpi.net_profit,
      change: kpi.profit_change,
      icon: ArrowUpDown,
      iconColor: '#22d3ee',
      iconBg: 'rgba(34, 211, 238, 0.15)',
    },
    {
      title: 'Cash in Hand',
      value: kpi.cash_in_hand,
      change: 5.3,
      icon: Wallet,
      iconColor: '#f59e0b',
      iconBg: 'rgba(245, 158, 11, 0.15)',
    },
    {
      title: 'Customers',
      value: kpi.customer_count,
      change: kpi.customer_change,
      icon: Users,
      iconColor: '#a855f7',
      iconBg: 'rgba(168, 85, 247, 0.15)',
      isCurrency: false,
    },
  ];

  return (
    <div className="min-h-screen">
      <Header title="Executive Dashboard" subtitle="Overview of today's performance" />

      <div className="p-6 space-y-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {kpiCards.map((card, i) => (
            <KPICard
              key={card.title}
              {...card}
              isCurrency={card.isCurrency !== false}
              delay={i * 80}
            />
          ))}
        </div>

        {/* Charts Row 1: Sales Trend + Payment Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ChartCard
            title="Sales Trend"
            subtitle="Last 30 days performance"
            className="lg:col-span-2"
          >
            <SalesTrendChart data={mockDailyTrends} />
          </ChartCard>

          <ChartCard title="Payment Methods" subtitle="Revenue by channel">
            <PaymentMethodChart data={mockPaymentBreakdown} />
          </ChartCard>
        </div>

        {/* Charts Row 2: Branch Performance + Customer Trend */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ChartCard title="Branch Performance" subtitle="Sales comparison by branch">
            <BranchCompareChart data={mockBranchPerformance} />
          </ChartCard>

          <ChartCard title="Customer Traffic" subtitle="Daily customer count">
            <CustomerTrendChart data={mockDailyTrends} />
          </ChartCard>
        </div>

        {/* Recent Sessions Table */}
        <div className="glass-card p-5">
          <h3 className="chart-title mb-4">Recent Till Sessions</h3>
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Till</th>
                  <th>Cashier</th>
                  <th>Cash Sales</th>
                  <th>M-PESA</th>
                  <th>Card Sales</th>
                  <th>Total Sales</th>
                  <th>Customers</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { date: '2026-05-30', till: 1, user: 'JOY', cash: 52340, mpesa: 28450, card: 12800, total: 98750, customers: 67 },
                  { date: '2026-05-30', till: 2, user: 'MERCY', cash: 48120, mpesa: 31200, card: 9450, total: 94230, customers: 58 },
                  { date: '2026-05-30', till: 3, user: 'BRIAN', cash: 61500, mpesa: 22800, card: 15600, total: 105400, customers: 73 },
                  { date: '2026-05-30', till: 4, user: 'ALICE', cash: 39800, mpesa: 35100, card: 8900, total: 89200, customers: 51 },
                  { date: '2026-05-29', till: 1, user: 'JOY', cash: 55200, mpesa: 26300, card: 11200, total: 97500, customers: 64 },
                  { date: '2026-05-29', till: 2, user: 'MERCY', cash: 43100, mpesa: 29800, card: 10300, total: 88700, customers: 55 },
                ].map((row, i) => (
                  <tr key={i}>
                    <td className="text-surface-600 dark:text-surface-300">{row.date}</td>
                    <td>
                      <span className="badge-info">Till {row.till}</span>
                    </td>
                    <td className="font-medium text-surface-800 dark:text-surface-200">{row.user}</td>
                    <td className="text-emerald-600 dark:text-emerald-400">{formatCurrencyFull(row.cash)}</td>
                    <td className="text-green-600 dark:text-green-400">{formatCurrencyFull(row.mpesa)}</td>
                    <td className="text-brand-600 dark:text-brand-400">{formatCurrencyFull(row.card)}</td>
                    <td className="font-semibold text-surface-900 dark:text-white">{formatCurrencyFull(row.total)}</td>
                    <td className="text-surface-600 dark:text-surface-300">{row.customers}</td>
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
