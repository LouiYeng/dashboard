import Header from '../components/layout/Header';
import { ShoppingCart } from 'lucide-react';

export default function PurchasesPage() {
  return (
    <div className="min-h-screen">
      <Header title="Purchase Analytics" subtitle="Purchase trends and supplier performance" />
      <div className="p-6">
        <div className="glass-card p-12 text-center">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-cyan-500/20 to-cyan-600/20 flex items-center justify-center mb-4">
            <ShoppingCart size={32} className="text-cyan-500" />
          </div>
          <h2 className="text-xl font-bold text-surface-900 dark:text-white mb-2">Purchase Module</h2>
          <p className="text-surface-500 dark:text-surface-400 max-w-md mx-auto">
            Connect your Purchase Orders, GRN, and Supplier tables to enable
            purchase trend analysis, supplier performance metrics, and GRN reports.
          </p>
        </div>
      </div>
    </div>
  );
}
