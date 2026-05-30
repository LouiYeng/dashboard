import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { useState } from 'react';

export default function MainLayout() {
  const [sidebarCollapsed] = useState(false);

  return (
    <div className="min-h-screen gradient-mesh">
      <Sidebar />
      <main
        className="transition-all duration-300 ease-in-out"
        style={{ marginLeft: sidebarCollapsed ? '72px' : '256px' }}
      >
        <Outlet />
      </main>
    </div>
  );
}
