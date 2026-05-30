import { Sun, Moon, Bell, Download, Calendar } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useState } from 'react';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  const { isDark, toggle } = useTheme();
  const [dateRange, setDateRange] = useState('today');

  const datePresets = [
    { label: 'Today', value: 'today' },
    { label: '7 Days', value: '7d' },
    { label: '30 Days', value: '30d' },
    { label: 'This Month', value: 'month' },
    { label: 'This Year', value: 'year' },
  ];

  return (
    <header className="glass-header sticky top-0 z-30 px-6 py-3">
      <div className="flex items-center justify-between">
        {/* Title */}
        <div>
          <h1 className="text-lg font-bold text-surface-900 dark:text-white">{title}</h1>
          {subtitle && (
            <p className="text-xs text-surface-500 dark:text-surface-400">{subtitle}</p>
          )}
        </div>

        {/* Right Side Controls */}
        <div className="flex items-center gap-2">
          {/* Date Range Quick Selector */}
          <div className="hidden md:flex items-center gap-1 bg-surface-100 dark:bg-surface-800 rounded-xl p-1">
            {datePresets.map((preset) => (
              <button
                key={preset.value}
                onClick={() => setDateRange(preset.value)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  dateRange === preset.value
                    ? 'bg-brand-500 text-white shadow-sm'
                    : 'text-surface-600 dark:text-surface-400 hover:text-surface-900 dark:hover:text-white'
                }`}
              >
                {preset.label}
              </button>
            ))}
          </div>

          {/* Date Picker Button */}
          <button className="btn-ghost p-2" title="Custom Date Range">
            <Calendar size={18} />
          </button>

          {/* Export Button */}
          <button className="btn-ghost p-2" title="Export">
            <Download size={18} />
          </button>

          {/* Notifications */}
          <button className="btn-ghost p-2 relative" title="Notifications">
            <Bell size={18} />
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-rose-500" />
          </button>

          {/* Theme Toggle */}
          <button
            onClick={toggle}
            className="btn-ghost p-2"
            title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            {isDark ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
