export default function LoadingSkeleton({ rows = 3, type = 'card' }: { rows?: number; type?: 'card' | 'chart' | 'table' }) {
  if (type === 'card') {
    return (
      <div className="glass-card p-5 animate-pulse">
        <div className="flex items-start justify-between mb-3">
          <div className="skeleton w-11 h-11 rounded-xl" />
          <div className="skeleton w-16 h-4 rounded" />
        </div>
        <div className="skeleton w-24 h-3 rounded mb-2" />
        <div className="skeleton w-32 h-7 rounded mb-3" />
        <div className="skeleton w-full h-8 rounded" />
      </div>
    );
  }

  if (type === 'chart') {
    return (
      <div className="chart-card animate-pulse">
        <div className="skeleton w-40 h-5 rounded mb-2" />
        <div className="skeleton w-24 h-3 rounded mb-4" />
        <div className="skeleton w-full h-64 rounded-lg" />
      </div>
    );
  }

  return (
    <div className="glass-card p-5 animate-pulse">
      <div className="skeleton w-40 h-5 rounded mb-4" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 mb-3">
          <div className="skeleton w-1/4 h-4 rounded" />
          <div className="skeleton w-1/3 h-4 rounded" />
          <div className="skeleton w-1/5 h-4 rounded" />
          <div className="skeleton w-1/6 h-4 rounded" />
        </div>
      ))}
    </div>
  );
}
