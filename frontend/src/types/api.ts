/* API response types matching backend schemas */

export interface KPISummary {
  total_sales: number;
  total_purchases: number;
  total_expenses: number;
  gross_profit: number;
  net_profit: number;
  cash_in_hand: number;
  customer_count: number;
  transaction_count: number;
  avg_transaction_value: number;
  sales_change: number;
  purchases_change: number;
  profit_change: number;
  customer_change: number;
}

export interface BranchPerformance {
  branch_code: number;
  branch_name: string;
  total_sales: number;
  total_customers: number;
  total_sessions: number;
  cash_sales: number;
  mobile_sales: number;
  card_sales: number;
  avg_transaction: number;
}

export interface PaymentMethodBreakdown {
  method: string;
  amount: number;
  percentage: number;
  color: string;
}

export interface DailySummary {
  date: string;
  total_sales: number;
  cash_sales: number;
  card_sales: number;
  mobile_sales: number;
  customers: number;
  transactions: number;
}

export interface SalesTrend {
  period: string;
  total_sales: number;
  cash_sales: number;
  card_sales: number;
  mobile_sales: number;
  other_sales: number;
  customers: number;
}

export interface BranchComparison {
  branch_code: number;
  branch_name: string;
  total_sales: number;
  total_purchases: number;
  total_customers: number;
  cash_sales: number;
  mobile_sales: number;
  card_sales: number;
  cash_in_hand: number;
  sessions_count: number;
}

export interface BranchRanking {
  rank: number;
  branch_code: number;
  branch_name: string;
  metric_value: number;
  metric_name: string;
}

export interface BranchListItem {
  branch_code: number;
  branch_name: string;
  branch_name_short?: string;
}
