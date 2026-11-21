import React from 'react';
import {
  LayoutDashboard,
  Film,
  Search,
  GitBranch,
  ShieldAlert,
  FileSignature,
  DollarSign,
  TrendingUp,
  CreditCard,
  PlaySquare,
  Sparkles,
  Users
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard & KPIs', icon: LayoutDashboard, module: 'Mod 8' },
    { id: 'catalog', label: 'Media Asset Catalog', icon: Film, module: 'Mod 1' },
    { id: 'search', label: 'Advanced Search', icon: Search, module: 'Mod 2' },
    { id: 'versions', label: 'Versioning & Revisions', icon: GitBranch, module: 'Mod 4' },
    { id: 'contracts', label: 'Contracts & Rights', icon: FileSignature, module: 'Mod 5' },
    { id: 'royalties', label: 'Royalty & Sales Engine', icon: DollarSign, module: 'Mod 6, 7' },
    { id: 'streaming', label: 'DRM Streaming Player', icon: PlaySquare, module: 'Mod 11' },
    { id: 'subscriptions', label: 'Plans & GST Billing', icon: CreditCard, module: 'Mod 10' },
    { id: 'recommendations', label: 'AI Recommendations', icon: Sparkles, module: 'Mod 12' },
    { id: 'access', label: 'Permissions & Roles', icon: ShieldAlert, module: 'Mod 3, 9' },
  ];

  return (
    <aside className="d-flex flex-column gap-2 p-3 card-glass" style={{ minWidth: '260px' }}>
      <div className="text-uppercase text-muted px-3 pb-2 small fw-bold tracking-wider" style={{ fontSize: '0.72rem' }}>
        Platform Modules
      </div>
      {menuItems.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <div
            key={item.id}
            className={`sidebar-link ${isActive ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <Icon size={18} className={isActive ? 'text-primary' : 'text-muted'} />
            <span className="flex-grow-1">{item.label}</span>
            <span className="badge bg-dark border border-secondary text-muted" style={{ fontSize: '0.65rem' }}>
              {item.module}
            </span>
          </div>
        );
      })}

      <div className="mt-auto pt-3 border-top border-secondary text-muted small text-center">
        <div>MediaMerge v1.0.0</div>
        <div style={{ fontSize: '0.7rem' }}>MCA 2nd Year Project P11</div>
      </div>
    </aside>
  );
}
