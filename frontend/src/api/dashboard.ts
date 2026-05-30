import client from './client';
import type { KPISummary, BranchPerformance, PaymentMethodBreakdown, DailySummary } from '../types/api';

interface DashboardFilters {
  date_from?: string;
  date_to?: string;
  branch_code?: number;
}

export const dashboardApi = {
  getSummary: (filters?: DashboardFilters) =>
    client.get<KPISummary>('/dashboard/summary', { params: filters }).then(r => r.data),

  getPaymentBreakdown: (filters?: DashboardFilters) =>
    client.get<PaymentMethodBreakdown[]>('/dashboard/payment-breakdown', { params: filters }).then(r => r.data),

  getTrends: (filters?: DashboardFilters & { days?: number }) =>
    client.get<DailySummary[]>('/dashboard/trends', { params: filters }).then(r => r.data),

  getBranchPerformance: (filters?: DashboardFilters) =>
    client.get<BranchPerformance[]>('/dashboard/branch-performance', { params: filters }).then(r => r.data),
};
