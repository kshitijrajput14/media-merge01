import React from 'react';
import { Film, ShieldCheck, UserCheck, Bell, Search, Sparkles } from 'lucide-react';

export default function Navbar({ currentRole, setCurrentRole, onQuickSearch, onOpenPlayerDemo }) {
  const roles = [
    { id: 1, name: 'Admin', badge: 'bg-danger' },
    { id: 2, name: 'Producer', badge: 'bg-primary' },
    { id: 3, name: 'Content Manager', badge: 'bg-info' },
    { id: 4, name: 'Rights & Royalty Officer', badge: 'bg-warning text-dark' },
    { id: 6, name: 'Subscriber', badge: 'bg-success' }
  ];

  return (
    <nav className="navbar navbar-expand-lg navbar-dark card-glass px-4 py-2 mb-4 sticky-top">
      <div className="container-fluid p-0">
        <div className="d-flex align-items-center gap-3">
          <div className="d-flex align-items-center gap-2">
            <div className="bg-primary p-2 rounded-3 text-white d-flex align-items-center justify-content-center shadow">
              <Film size={22} />
            </div>
            <div>
              <span className="fw-bolder fs-5 text-white tracking-wide">MediaMerge</span>
              <span className="badge bg-secondary ms-2" style={{ fontSize: '0.65rem' }}>P11 FSD</span>
            </div>
          </div>
          <span className="badge badge-drm d-none d-md-inline-flex align-items-center gap-1">
            <ShieldCheck size={13} />
            Widevine L1 + AES-128 Active
          </span>
        </div>

        {/* Quick Search */}
        <div className="d-none d-lg-flex align-items-center bg-dark rounded-pill px-3 py-1 border border-secondary" style={{ width: '320px' }}>
          <Search size={16} className="text-muted me-2" />
          <input
            type="text"
            className="form-control form-control-sm bg-transparent border-0 text-light shadow-none"
            placeholder="Quick search assets, tags..."
            onChange={(e) => onQuickSearch && onQuickSearch(e.target.value)}
          />
        </div>

        {/* Role Switcher & User Profile */}
        <div className="d-flex align-items-center gap-3">
          <button
            className="btn btn-outline-info btn-sm rounded-pill d-none d-sm-flex align-items-center gap-2"
            onClick={onOpenPlayerDemo}
            title="Launch live streaming player"
          >
            <Sparkles size={14} />
            <span>Launch Player</span>
          </button>

          <div className="d-flex align-items-center gap-2 bg-surface px-3 py-1 rounded-pill border border-secondary">
            <UserCheck size={16} className="text-info" />
            <span className="text-muted small">Role:</span>
            <select
              className="form-select form-select-sm bg-transparent border-0 text-light fw-bold p-0 pe-4 shadow-none"
              style={{ cursor: 'pointer', width: 'auto' }}
              value={currentRole.id}
              onChange={(e) => {
                const found = roles.find(r => r.id === parseInt(e.target.value));
                if (found) setCurrentRole(found);
              }}
            >
              {roles.map(r => (
                <option key={r.id} value={r.id} className="bg-dark text-light">
                  {r.name}
                </option>
              ))}
            </select>
          </div>

          <div className="position-relative cursor-pointer text-muted hover-light">
            <Bell size={18} />
            <span className="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-dark rounded-circle"></span>
          </div>

          <div className="d-flex align-items-center gap-2">
            <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold" style={{ width: '34px', height: '34px', fontSize: '0.85rem' }}>
              {currentRole.name[0]}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
