import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, TrendingUp, GitBranch, Package,
  ShoppingCart, Receipt, Users, ChevronLeft, ChevronRight,
  BarChart3, LogOut
} from 'lucide-react';
import { useState } from 'react';

// Mock user for unauthenticated access
const defaultUser = { full_name: 'Administrator', role: 'super_admin' };

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/branches', label: 'Branch Analytics', icon: GitBranch },
  { path: '/sales', label: 'Sales Analytics', icon: TrendingUp },
  { path: '/inventory', label: 'Inventory', icon: Package },
  { path: '/purchases', label: 'Purchases', icon: ShoppingCart },
  { path: '/expenses', label: 'Expenses', icon: Receipt },
  { path: '/users', label: 'User Activity', icon: Users },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const user = defaultUser;
  const location = useLocation();

  const roleLabels: Record<string, string> = {
    super_admin: 'Super Admin',
    branch_manager: 'Branch Manager',
    accountant: 'Accountant',
    auditor: 'Auditor',
  };

  return (
    <aside
      className={`glass-sidebar h-screen flex flex-col transition-all duration-300 ease-in-out ${
        collapsed ? 'w-[72px]' : 'w-64'
      } fixed left-0 top-0 z-40`}
    >
      {/* Logo / Brand */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-surface-200 dark:border-surface-800">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
          <BarChart3 size={20} className="text-white" />
        </div>
        {!collapsed && (
          <div className="animate-fade-in">
            <h1 className="text-sm font-bold gradient-text">BI Dashboard</h1>
            <p className="text-[10px] text-surface-500 dark:text-surface-400">Analytics Portal</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={isActive ? 'nav-item-active' : 'nav-item'}
              title={collapsed ? item.label : undefined}
            >
              <item.icon size={20} className="flex-shrink-0" />
              {!collapsed && (
                <span className="animate-fade-in truncate">{item.label}</span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* User Info */}
      <div className="border-t border-surface-200 dark:border-surface-800 p-3">
        {!collapsed && user && (
          <div className="flex items-center gap-3 mb-2 px-2 animate-fade-in">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
              {user.full_name.charAt(0)}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium truncate text-surface-800 dark:text-surface-200">
                {user.full_name}
              </p>
              <p className="text-[10px] text-brand-500 dark:text-brand-400 font-medium">
                {roleLabels[user.role] || user.role}
              </p>
            </div>
          </div>
        )}

        <div className="flex items-center gap-2">
          <a
            href="/login"
            className="btn-ghost flex-1 flex items-center gap-2 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/20 justify-center"
            title="Login"
          >
            <LogOut size={16} />
            {!collapsed && <span className="text-xs">Login</span>}
          </a>
        </div>
      </div>

      {/* Collapse Toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-20 w-6 h-6 rounded-full bg-brand-500 text-white flex items-center justify-center shadow-lg hover:bg-brand-600 transition-colors z-50"
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>
    </aside>
  );
}
