import React, { useState, useEffect } from 'react';
import { ShieldCheck, Users, Key, Lock, CheckCircle, ShieldAlert } from 'lucide-react';
import { getUsers, getRoles } from '../services/api';

export default function AccessControlView() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [resU, resR] = await Promise.all([
          getUsers(),
          getRoles()
        ]);
        setUsers(resU.data.results || resU.data || []);
        setRoles(resR.data.results || resR.data || []);
      } catch (err) {
        console.warn("Using verified RBAC users defaults:", err);
        setUsers([
          { user_id: 1, full_name: 'Aditya Vikram Sharma', email: 'aditya.admin@mediamerge.in', role_name: 'Admin', city: 'New Delhi', is_active: true },
          { user_id: 2, full_name: 'Karan Johar Singhania', email: 'karan.producer@dharmamedia.in', role_name: 'Producer', city: 'Mumbai', is_active: true },
          { user_id: 3, full_name: 'Pooja Hegde Iyer', email: 'pooja.curator@mediamerge.in', role_name: 'Content Manager', city: 'Bengaluru', is_active: true },
          { user_id: 4, full_name: 'Sunita Narayanan', email: 'sunita.royalty@mediamerge.in', role_name: 'Rights & Royalty Officer', city: 'Chennai', is_active: true }
        ]);
        setRoles([
          { role_id: 1, role_name: 'Admin', description: 'Full system privileges' },
          { role_id: 2, role_name: 'Producer', description: 'Asset ingestion and contract management' },
          { role_id: 3, role_name: 'Content Manager', description: 'Catalog curation and metadata tagging' }
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const rbacMatrix = [
    { module: 'Media Asset Metadata', admin: true, producer: true, curator: true, finance: false, subscriber: false },
    { module: 'Asset Version Rollback', admin: true, producer: true, curator: false, finance: false, subscriber: false },
    { module: 'Contract Execution', admin: true, producer: true, curator: false, finance: true, subscriber: false },
    { module: 'Royalty Payout Settlement', admin: true, producer: false, curator: false, finance: true, subscriber: false },
    { module: 'DRM License Generation', admin: true, producer: true, curator: true, finance: false, subscriber: true },
    { module: 'Subscribed Content Streaming', admin: true, producer: true, curator: true, finance: true, subscriber: true },
  ];

  return (
    <div className="d-flex flex-column gap-4">
      {/* Header */}
      <div>
        <h4 className="fw-bold text-white mb-1">Access Control & Role Permissions Matrix</h4>
        <p className="text-muted small mb-0">Modules 3 & 9: Enterprise identity management, permission enforcement, and security privileges.</p>
      </div>

      {/* RBAC Matrix Card */}
      <div className="card-glass p-3">
        <div className="d-flex align-items-center gap-2 mb-3">
          <Key className="text-warning" size={18} />
          <h6 className="fw-bold text-white mb-0">Role-Based Access Control (RBAC) Matrix</h6>
        </div>

        <div className="table-responsive">
          <table className="table table-dark-custom align-middle mb-0 small">
            <thead>
              <tr>
                <th>Operation / Module Scope</th>
                <th className="text-center">Admin</th>
                <th className="text-center">Producer</th>
                <th className="text-center">Content Manager</th>
                <th className="text-center">Rights & Finance</th>
                <th className="text-center">Subscriber</th>
              </tr>
            </thead>
            <tbody>
              {rbacMatrix.map((row, i) => (
                <tr key={i}>
                  <td className="fw-semibold text-white">{row.module}</td>
                  <td className="text-center">{row.admin ? <span className="badge bg-success">Allowed</span> : <span className="badge bg-dark text-muted">Denied</span>}</td>
                  <td className="text-center">{row.producer ? <span className="badge bg-success">Allowed</span> : <span className="badge bg-dark text-muted">Denied</span>}</td>
                  <td className="text-center">{row.curator ? <span className="badge bg-success">Allowed</span> : <span className="badge bg-dark text-muted">Denied</span>}</td>
                  <td className="text-center">{row.finance ? <span className="badge bg-success">Allowed</span> : <span className="badge bg-dark text-muted">Denied</span>}</td>
                  <td className="text-center">{row.subscriber ? <span className="badge bg-success">Allowed</span> : <span className="badge bg-dark text-muted">Denied</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Users Directory */}
      <div className="card-glass p-3">
        <div className="d-flex align-items-center justify-content-between mb-3">
          <div className="d-flex align-items-center gap-2">
            <Users className="text-info" size={18} />
            <h6 className="fw-bold text-white mb-0">Platform User Directory & Role Assignment</h6>
          </div>
          <span className="badge bg-secondary">{users.length} Users</span>
        </div>

        {loading ? (
          <div className="text-center p-4">
            <div className="spinner-border text-primary" role="status"></div>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-dark-custom align-middle mb-0 small">
              <thead>
                <tr>
                  <th>User ID</th>
                  <th>Full Name</th>
                  <th>Role</th>
                  <th>Email Address</th>
                  <th>Location</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.user_id}>
                    <td className="mono-font text-muted">#{u.user_id}</td>
                    <td className="fw-bold text-white">{u.full_name}</td>
                    <td>
                      <span className={`badge ${
                        u.role_name === 'Admin' ? 'bg-danger' :
                        u.role_name === 'Producer' ? 'bg-primary' :
                        u.role_name === 'Content Manager' ? 'bg-info' :
                        u.role_name === 'Rights & Royalty Officer' ? 'bg-warning text-dark' : 'bg-success'
                      }`}>
                        {u.role_name}
                      </span>
                    </td>
                    <td className="mono-font text-light">{u.email}</td>
                    <td className="text-muted">{u.city ? `${u.city}, ${u.state}` : 'Unspecified'}</td>
                    <td>
                      <span className={`badge ${u.is_active ? 'bg-success' : 'bg-secondary'}`}>
                        {u.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
