import Header from '../components/layout/Header';
import { Users, Shield, Clock, Activity } from 'lucide-react';

export default function UserActivityPage() {
  const users = [
    { id: 1, name: 'System Administrator', username: 'admin', role: 'super_admin', status: 'active', lastLogin: '2026-05-30 08:15' },
    { id: 2, name: 'Joy Muthoni', username: 'joy.m', role: 'branch_manager', status: 'active', lastLogin: '2026-05-30 07:45' },
    { id: 3, name: 'David Omondi', username: 'david.o', role: 'accountant', status: 'active', lastLogin: '2026-05-29 16:30' },
    { id: 4, name: 'Faith Wanjiku', username: 'faith.w', role: 'auditor', status: 'inactive', lastLogin: '2026-05-25 09:00' },
  ];

  const roleColors: Record<string, string> = {
    super_admin: 'badge-danger',
    branch_manager: 'badge-info',
    accountant: 'badge-success',
    auditor: 'badge-warning',
  };

  const roleLabels: Record<string, string> = {
    super_admin: 'Super Admin',
    branch_manager: 'Branch Manager',
    accountant: 'Accountant',
    auditor: 'Auditor',
  };

  return (
    <div className="min-h-screen">
      <Header title="User Activity" subtitle="Monitor user access and actions" />

      <div className="p-6 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          {[
            { label: 'Total Users', value: '4', icon: Users, color: '#6366f1', bg: 'rgba(99,102,241,0.15)' },
            { label: 'Active Users', value: '3', icon: Activity, color: '#10b981', bg: 'rgba(16,185,129,0.15)' },
            { label: 'Roles Defined', value: '4', icon: Shield, color: '#f59e0b', bg: 'rgba(245,158,11,0.15)' },
            { label: 'Logins Today', value: '2', icon: Clock, color: '#06b6d4', bg: 'rgba(6,182,212,0.15)' },
          ].map((stat, i) => (
            <div key={i} className="glass-card p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: stat.bg }}>
                <stat.icon size={20} style={{ color: stat.color }} />
              </div>
              <div>
                <p className="text-xs text-surface-500 dark:text-surface-400">{stat.label}</p>
                <p className="text-lg font-bold text-surface-900 dark:text-white">{stat.value}</p>
              </div>
            </div>
          ))}
        </div>

        {/* User Management Table */}
        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="chart-title">Dashboard Users</h3>
            <button className="btn-primary text-xs">+ Add User</button>
          </div>
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Username</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Last Login</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="font-medium text-surface-800 dark:text-surface-200">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-white text-xs font-bold">
                          {user.name.charAt(0)}
                        </div>
                        {user.name}
                      </div>
                    </td>
                    <td className="text-surface-500 dark:text-surface-400">{user.username}</td>
                    <td><span className={roleColors[user.role]}>{roleLabels[user.role]}</span></td>
                    <td>
                      <span className={user.status === 'active' ? 'badge-success' : 'badge-danger'}>
                        {user.status}
                      </span>
                    </td>
                    <td className="text-surface-500 dark:text-surface-400 text-xs">{user.lastLogin}</td>
                    <td>
                      <button className="btn-ghost text-xs">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Audit Trail Placeholder */}
        <div className="glass-card p-5">
          <h3 className="chart-title mb-4">Audit Trail</h3>
          <div className="space-y-3">
            {[
              { action: 'Login', user: 'admin', time: '08:15 AM', detail: 'Successful login from 192.168.1.10' },
              { action: 'Export', user: 'admin', time: '08:20 AM', detail: 'Exported dashboard PDF report' },
              { action: 'Login', user: 'joy.m', time: '07:45 AM', detail: 'Successful login from 192.168.1.15' },
              { action: 'View', user: 'joy.m', time: '07:50 AM', detail: 'Viewed Branch Analytics page' },
            ].map((log, i) => (
              <div key={i} className="flex items-center gap-4 p-3 rounded-xl bg-surface-50 dark:bg-surface-800/30">
                <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                  log.action === 'Login' ? 'bg-emerald-500' :
                  log.action === 'Export' ? 'bg-brand-500' : 'bg-cyan-500'
                }`} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-surface-800 dark:text-surface-200">{log.detail}</p>
                  <p className="text-xs text-surface-500 dark:text-surface-400">{log.user} · {log.time}</p>
                </div>
                <span className="badge-info text-[10px]">{log.action}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
