import React, { useEffect, useState } from 'react';
import {
  X,
  Layers,
  GitBranch,
  Shield,
  FileText,
  RotateCcw,
  Plus,
  CheckCircle,
  HardDrive
} from 'lucide-react';
import {
  getAssetDetail,
  addAssetVersion,
  rollbackVersion,
  grantAssetPermission,
  addAssetMetadata
} from '../services/api';

export default function AssetDetailModal({ assetId, onClose, onRefresh }) {
  const [asset, setAsset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('metadata'); // 'metadata', 'versions', 'permissions', 'drm'

  // New Version Form State
  const [newVersionNum, setNewVersionNum] = useState('');
  const [newSummary, setNewSummary] = useState('');
  const [versionMsg, setVersionMsg] = useState('');

  // New Metadata Form State
  const [metaKey, setMetaKey] = useState('');
  const [metaVal, setMetaVal] = useState('');

  const fetchDetail = async () => {
    if (!assetId) return;
    setLoading(true);
    try {
      const res = await getAssetDetail(assetId);
      setAsset(res.data);
    } catch (err) {
      console.error("Error loading asset detail:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [assetId]);

  const handleAddVersion = async (e) => {
    e.preventDefault();
    if (!newVersionNum) return;
    try {
      await addAssetVersion(assetId, {
        version_number: newVersionNum,
        change_summary: newSummary,
        file_path: `${asset.storage_path}_${newVersionNum}`,
        file_size_mb: asset.file_size_mb,
        is_active: false
      });
      setVersionMsg(`Version ${newVersionNum} registered successfully!`);
      setNewVersionNum('');
      setNewSummary('');
      fetchDetail();
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error("Add version error:", err);
    }
  };

  const handleRollback = async (versionId, versionNumber) => {
    if (!window.confirm(`Are you sure you want to rollback active master to ${versionNumber}?`)) return;
    try {
      await rollbackVersion(assetId, versionId);
      setVersionMsg(`Asset rolled back to ${versionNumber}!`);
      fetchDetail();
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error("Rollback error:", err);
    }
  };

  const handleAddMeta = async (e) => {
    e.preventDefault();
    if (!metaKey || !metaVal) return;
    try {
      await addAssetMetadata(assetId, { meta_key: metaKey, meta_value: metaVal, data_type: 'string' });
      setMetaKey('');
      setMetaVal('');
      fetchDetail();
    } catch (err) {
      console.error("Add metadata error:", err);
    }
  };

  if (!assetId) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.8)', zIndex: 1050 }} tabIndex="-1">
      <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div className="modal-content card-glass border-secondary text-light">
          {/* Modal Header */}
          <div className="modal-header border-secondary py-3">
            <div className="d-flex align-items-center gap-2">
              <Layers className="text-primary" size={20} />
              <div>
                <h5 className="modal-title fw-bold text-white mb-0">{asset?.title || 'Asset Metadata & Controls'}</h5>
                <span className="text-muted small" style={{ fontSize: '0.75rem' }}>Asset ID: #{assetId} • {asset?.rights_holder_name}</span>
              </div>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>

          {/* Navigation Tabs */}
          <div className="border-bottom border-secondary px-3 pt-2 bg-surface">
            <ul className="nav nav-tabs border-0 gap-2">
              <li className="nav-item">
                <button
                  className={`nav-link text-light py-2 px-3 border-0 rounded-top ${activeTab === 'metadata' ? 'active bg-dark text-primary fw-bold' : ''}`}
                  onClick={() => setActiveTab('metadata')}
                >
                  Technical Metadata
                </button>
              </li>
              <li className="nav-item">
                <button
                  className={`nav-link text-light py-2 px-3 border-0 rounded-top ${activeTab === 'versions' ? 'active bg-dark text-info fw-bold' : ''}`}
                  onClick={() => setActiveTab('versions')}
                >
                  Versions & History ({asset?.versions?.length || 0})
                </button>
              </li>
              <li className="nav-item">
                <button
                  className={`nav-link text-light py-2 px-3 border-0 rounded-top ${activeTab === 'permissions' ? 'active bg-dark text-warning fw-bold' : ''}`}
                  onClick={() => setActiveTab('permissions')}
                >
                  Access Permissions ({asset?.permissions?.length || 0})
                </button>
              </li>
            </ul>
          </div>

          {/* Modal Body */}
          <div className="modal-body p-4">
            {loading ? (
              <div className="text-center p-4">
                <div className="spinner-border text-primary" role="status"></div>
                <div className="text-muted mt-2 small">Loading asset specifications...</div>
              </div>
            ) : (
              <>
                {versionMsg && (
                  <div className="alert alert-success d-flex align-items-center gap-2 py-2 mb-3" role="alert">
                    <CheckCircle size={16} />
                    <span className="small">{versionMsg}</span>
                  </div>
                )}

                {/* TAB 1: METADATA */}
                {activeTab === 'metadata' && (
                  <div className="d-flex flex-column gap-3">
                    <div className="row g-3">
                      <div className="col-md-6">
                        <div className="p-3 rounded bg-surface border border-secondary">
                          <div className="text-muted small">Category & Format</div>
                          <div className="fw-semibold text-white">{asset?.category_details?.category_name}</div>
                          <div className="text-info mono-font small">{asset?.format_details?.format_name}</div>
                        </div>
                      </div>
                      <div className="col-md-6">
                        <div className="p-3 rounded bg-surface border border-secondary">
                          <div className="text-muted small">Encoding Specs</div>
                          <div className="small text-white">Video Codec: <span className="mono-font text-info">{asset?.format_details?.video_codec}</span></div>
                          <div className="small text-white">Audio Codec: <span className="mono-font text-info">{asset?.format_details?.audio_codec}</span></div>
                        </div>
                      </div>
                    </div>

                    <h6 className="fw-bold text-white mt-2 mb-1">Extended Technical Metadata (EAV)</h6>
                    <div className="table-responsive border border-secondary rounded">
                      <table className="table table-dark-custom mb-0 small">
                        <thead>
                          <tr>
                            <th>Parameter</th>
                            <th>Value</th>
                            <th>Data Type</th>
                          </tr>
                        </thead>
                        <tbody>
                          {(asset?.metadata_entries || []).map((m, i) => (
                            <tr key={i}>
                              <td className="fw-bold text-info mono-font">{m.meta_key}</td>
                              <td className="text-white">{m.meta_value}</td>
                              <td><span className="badge bg-secondary">{m.data_type}</span></td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {/* Add Custom Metadata */}
                    <form onSubmit={handleAddMeta} className="p-3 rounded bg-surface border border-secondary">
                      <div className="fw-semibold small text-white mb-2">Add Technical Parameter</div>
                      <div className="row g-2">
                        <div className="col-5">
                          <input
                            type="text"
                            className="form-control form-control-sm bg-dark border-secondary text-light shadow-none"
                            placeholder="e.g. dolby_vision_profile"
                            value={metaKey}
                            onChange={(e) => setMetaKey(e.target.value)}
                          />
                        </div>
                        <div className="col-5">
                          <input
                            type="text"
                            className="form-control form-control-sm bg-dark border-secondary text-light shadow-none"
                            placeholder="e.g. Profile 8.1 Mel"
                            value={metaVal}
                            onChange={(e) => setMetaVal(e.target.value)}
                          />
                        </div>
                        <div className="col-2">
                          <button type="submit" className="btn btn-primary btn-sm w-100">Add</button>
                        </div>
                      </div>
                    </form>
                  </div>
                )}

                {/* TAB 2: VERSIONS & HISTORY (Module 4) */}
                {activeTab === 'versions' && (
                  <div className="d-flex flex-column gap-3">
                    <div className="d-flex justify-content-between align-items-center">
                      <h6 className="fw-bold text-white mb-0">Version Revisions & Rollback History</h6>
                      <span className="badge bg-info">{asset?.versions?.length || 0} Revisions</span>
                    </div>

                    <div className="table-responsive border border-secondary rounded">
                      <table className="table table-dark-custom mb-0 align-middle small">
                        <thead>
                          <tr>
                            <th>Version</th>
                            <th>Checksum (SHA256)</th>
                            <th>Size</th>
                            <th>Summary of Changes</th>
                            <th>Active Status</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {(asset?.versions || []).map((v) => (
                            <tr key={v.version_id}>
                              <td className="fw-bold text-white mono-font">{v.version_number}</td>
                              <td className="mono-font text-muted small" title={v.checksum_sha256}>
                                {v.checksum_sha256.substring(0, 12)}...
                              </td>
                              <td className="mono-font">{v.file_size_mb} MB</td>
                              <td className="text-light">{v.change_summary || 'Initial Ingestion'}</td>
                              <td>
                                {v.is_active ? (
                                  <span className="badge bg-success">ACTIVE MASTER</span>
                                ) : (
                                  <span className="badge bg-secondary">Archived</span>
                                )}
                              </td>
                              <td>
                                {!v.is_active && (
                                  <button
                                    className="btn btn-outline-warning btn-sm py-0 px-2 d-flex align-items-center gap-1"
                                    onClick={() => handleRollback(v.version_id, v.version_number)}
                                    title="Rollback master asset to this revision"
                                  >
                                    <RotateCcw size={12} />
                                    <span>Rollback</span>
                                  </button>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {/* New Version Ingestion Form */}
                    <form onSubmit={handleAddVersion} className="p-3 rounded bg-surface border border-secondary">
                      <div className="fw-semibold small text-white mb-2">Ingest New Asset Revision</div>
                      <div className="row g-2">
                        <div className="col-4">
                          <input
                            type="text"
                            className="form-control form-control-sm bg-dark border-secondary text-light shadow-none"
                            placeholder="Version e.g. v1.2.0"
                            value={newVersionNum}
                            onChange={(e) => setNewVersionNum(e.target.value)}
                          />
                        </div>
                        <div className="col-6">
                          <input
                            type="text"
                            className="form-control form-control-sm bg-dark border-secondary text-light shadow-none"
                            placeholder="Change description e.g. Dialogue audio mix boost"
                            value={newSummary}
                            onChange={(e) => setNewSummary(e.target.value)}
                          />
                        </div>
                        <div className="col-2">
                          <button type="submit" className="btn btn-info btn-sm w-100">Commit</button>
                        </div>
                      </div>
                    </form>
                  </div>
                )}

                {/* TAB 3: ACCESS CONTROL & PERMISSIONS (Module 3) */}
                {activeTab === 'permissions' && (
                  <div className="d-flex flex-column gap-3">
                    <h6 className="fw-bold text-white mb-0">Granular Access Permissions</h6>
                    <p className="text-muted small mb-1">Control view, edit, download, and publish privileges by user or role.</p>

                    <div className="table-responsive border border-secondary rounded">
                      <table className="table table-dark-custom mb-0 small">
                        <thead>
                          <tr>
                            <th>Granted To</th>
                            <th>Permission Type</th>
                            <th>Authorized By</th>
                            <th>Granted At</th>
                          </tr>
                        </thead>
                        <tbody>
                          {(asset?.permissions || []).map((p, idx) => (
                            <tr key={idx}>
                              <td className="fw-semibold text-white">
                                {p.user_name ? `${p.user_name} (User)` : `Role: ${p.role_name}`}
                              </td>
                              <td>
                                <span className={`badge ${
                                  p.permission_type === 'publish' ? 'bg-danger' :
                                  p.permission_type === 'edit' ? 'bg-warning text-dark' : 'bg-primary'
                                }`}>
                                  {p.permission_type.toUpperCase()}
                                </span>
                              </td>
                              <td className="text-muted">{p.granter_name || 'Admin'}</td>
                              <td className="text-muted mono-font">{p.granted_at ? p.granted_at.substring(0, 10) : '2024-02-01'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          <div className="modal-footer border-secondary py-2">
            <button type="button" className="btn btn-secondary btn-sm" onClick={onClose}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
}
