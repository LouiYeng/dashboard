export interface DateRange {
  startDate: string;
  endDate: string;
}

export interface FilterState {
  dateRange: DateRange;
  branchId: string | null;
  category: string | null;
  period: 'daily' | 'weekly' | 'monthly';
}

export type DatePreset = 
  | 'today'
  | 'yesterday'
  | 'last7days'
  | 'last30days'
  | 'thisMonth'
  | 'lastMonth'
  | 'custom';

export interface DatePresetOption {
  label: string;
  value: DatePreset;
  getRange: () => DateRange;
}
