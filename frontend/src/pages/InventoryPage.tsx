import Header from '../components/layout/Header';
import { Package, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react';

export default function InventoryPage() {
  return (
    <div className="min-h-screen">
      <Header title="Inventory Analytics" subtitle="Stock levels and movement analysis" />
      <div className="p-6">
        <div className="glass-card p-12 text-center">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-amber-500/20 to-amber-600/20 flex items-center justify-center mb-4">
            <Package size={32} className="text-amber-500" />
          </div>
          <h2 className="text-xl font-bold text-surface-900 dark:text-white mb-2">Inventory Module</h2>
          <p className="text-surface-500 dark:text-surface-400 max-w-md mx-auto mb-6">
            Connect your Stock and Product tables to enable inventory analytics including
            stock value, low stock alerts, and product movement analysis.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 max-w-2xl mx-auto">
            {[
              { icon: Package, label: 'Current Stock Value', color: 'brand' },
              { icon: AlertTriangle, label: 'Low Stock Alerts', color: 'amber' },
              { icon: TrendingUp, label: 'Fast Moving Items', color: 'emerald' },
              { icon: TrendingDown, label: 'Slow Moving Items', color: 'rose' },
            ].map((item, i) => (
              <div key={i} className="glass-card p-4 text-center opacity-50">
                <item.icon size={24} className={`mx-auto mb-2 text-${item.color}-500`} />
                <p className="text-xs text-surface-500">{item.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
