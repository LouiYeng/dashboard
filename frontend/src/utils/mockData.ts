/**
 * Sample/mock data for the dashboard UI.
 * Used when backend is not connected. Realistic Kenyan retail data.
 */
import type { KPISummary, BranchPerformance, PaymentMethodBreakdown, DailySummary, SalesTrend } from '../types/api';

export const mockKPI: KPISummary = {
  total_sales: 2847350.50,
  total_purchases: 423800.00,
  total_expenses: 187650.00,
  gross_profit: 2423550.50,
  net_profit: 2235900.50,
  cash_in_hand: 1245780.25,
  customer_count: 1847,
  transaction_count: 312,
  avg_transaction_value: 9126.44,
  sales_change: 12.5,
  purchases_change: -3.2,
  profit_change: 15.8,
  customer_change: 8.4,
};

export const mockPaymentBreakdown: PaymentMethodBreakdown[] = [
  { method: 'Cash', amount: 1138940.20, percentage: 40.0, color: '#10b981' },
  { method: 'M-PESA', amount: 854205.15, percentage: 30.0, color: '#22c55e' },
  { method: 'Credit Card', amount: 427102.58, percentage: 15.0, color: '#6366f1' },
  { method: 'Airtel Money', amount: 142367.53, percentage: 5.0, color: '#ef4444' },
  { method: 'VOOMA', amount: 113894.02, percentage: 4.0, color: '#06b6d4' },
  { method: 'Loyalty', amount: 85420.52, percentage: 3.0, color: '#a855f7' },
  { method: 'Gift Voucher', amount: 56947.01, percentage: 2.0, color: '#14b8a6' },
  { method: 'CAP (Credit)', amount: 28473.51, percentage: 1.0, color: '#f97316' },
];

export const mockBranchPerformance: BranchPerformance[] = [
  {
    branch_code: 1, branch_name: 'Main Branch - Nairobi CBD',
    total_sales: 1652350.30, total_customers: 1073, total_sessions: 181,
    cash_sales: 660940.12, mobile_sales: 495705.09, card_sales: 247852.55, avg_transaction: 9128.18,
  },
  {
    branch_code: 2, branch_name: 'Westlands Branch',
    total_sales: 1195000.20, total_customers: 774, total_sessions: 131,
    cash_sales: 478000.08, mobile_sales: 358500.06, card_sales: 179250.03, avg_transaction: 9122.14,
  },
];

export const mockDailyTrends: DailySummary[] = Array.from({ length: 30 }, (_, i) => {
  const d = new Date();
  d.setDate(d.getDate() - (29 - i));
  const base = 80000 + Math.random() * 40000;
  const weekend = d.getDay() === 0 || d.getDay() === 6;
  const mult = weekend ? 1.3 : 1;
  return {
    date: d.toISOString().split('T')[0],
    total_sales: Math.round(base * mult * 100) / 100,
    cash_sales: Math.round(base * 0.4 * mult * 100) / 100,
    card_sales: Math.round(base * 0.15 * mult * 100) / 100,
    mobile_sales: Math.round(base * 0.35 * mult * 100) / 100,
    customers: Math.round(50 + Math.random() * 30 * (weekend ? 1.4 : 1)),
    transactions: Math.round(8 + Math.random() * 6),
  };
});

export const mockSalesTrends: SalesTrend[] = mockDailyTrends.map(d => ({
  period: d.date,
  total_sales: d.total_sales,
  cash_sales: d.cash_sales,
  card_sales: d.card_sales,
  mobile_sales: d.mobile_sales,
  other_sales: d.total_sales - d.cash_sales - d.card_sales - d.mobile_sales,
  customers: d.customers,
}));
