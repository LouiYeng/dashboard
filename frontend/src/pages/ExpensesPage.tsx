import Header from '../components/layout/Header';
import { Receipt } from 'lucide-react';

export default function ExpensesPage() {
  return (
    <div className="min-h-screen">
      <Header title="Expense Analytics" subtitle="Expense breakdown and trends" />
      <div className="p-6">
        <div className="glass-card p-12 text-center">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-rose-500/20 to-rose-600/20 flex items-center justify-center mb-4">
            <Receipt size={32} className="text-rose-500" />
          </div>
          <h2 className="text-xl font-bold text-surface-900 dark:text-white mb-2">Expense Module</h2>
          <p className="text-surface-500 dark:text-surface-400 max-w-md mx-auto">
            Connect your Expenses table to enable expense breakdown by category,
            monthly trends, and cost analysis across branches.
          </p>
        </div>
      </div>
    </div>
  );
}
