/**
 * Format a number as KES currency.
 */
export function formatCurrency(value: number): string {
  if (Math.abs(value) >= 1_000_000) {
    return `KES ${(value / 1_000_000).toFixed(2)}M`;
  }
  if (Math.abs(value) >= 1_000) {
    return `KES ${(value / 1_000).toFixed(1)}K`;
  }
  return `KES ${value.toFixed(2)}`;
}

/**
 * Format a number as full KES currency (no abbreviation).
 */
export function formatCurrencyFull(value: number): string {
  return `KES ${value.toLocaleString('en-KE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/**
 * Format a large number with commas.
 */
export function formatNumber(value: number): string {
  return value.toLocaleString('en-KE');
}

/**
 * Format a percentage change with sign and arrow.
 */
export function formatChange(value: number): { text: string; isPositive: boolean } {
  const isPositive = value >= 0;
  return {
    text: `${isPositive ? '+' : ''}${value.toFixed(1)}%`,
    isPositive,
  };
}
