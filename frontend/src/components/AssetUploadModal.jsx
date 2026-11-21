import React, { useState, useEffect } from 'react';
import { X, Upload, CheckCircle } from 'lucide-react';
import { getCategories, getFormats, getRightsHolders, getDrmPolicies, createAsset } from '../services/api';

export default function AssetUploadModal({ onClose, onSuccess }) {
  const [categories, setCategories] = useState([]);
  const [formats, setFormats] = useState([]);
  const [holders, setHolders] = useState([]);
  const [drmPolicies, setDrmPolicies] = useState([]);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 1,
    format: 2,
    drm_policy: 1,
    rights_holder: 1,
    duration_seconds: 7200,
    file_size_mb: 4200.0,
    storage_path: '/storage/vault/2024/new_master.mp4',
    censor_rating: 'U/A 13+',
    release_year: 2024,
    primary_language: 'Hindi',
    status: 'Published',
    created_by: 1
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [resCat, resFmt, resHold, resDrm] = await Promise.all([
          getCategories(),
          getFormats(),
          getRightsHolders(),
          getDrmPolicies()
        ]);
        setCategories(resCat.data.results || resCat.data || []);
        setFormats(resFmt.data.results || resFmt.data || []);
        setHolders(resHold.data.results || resHold.data || []);
        setDrmPolicies(resDrm.data.results || resDrm.data || []);
      } catch (err) {
        console.error("Error loading dropdown options:", err);
      }
    };
    fetchOptions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: (name === 'category' || name === 'format' || name === 'drm_policy' || name === 'rights_holder' || name === 'duration_seconds' || name === 'release_year') ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await createAsset(formData);
      if (onSuccess) onSuccess();
      onClose();
    } catch (err) {
      console.error("Asset creation error:", err);
      setError(err.response?.data?.message || 'Failed to ingest media asset');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.85)', zIndex: 1060 }} tabIndex="-1">
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content card-glass border-secondary text-light">
          <div className="modal-header border-secondary py-3">
            <div className="d-flex align-items-center gap-2">
              <Upload className="text-primary" size={20} />
              <h5 className="modal-title fw-bold text-white mb-0">Ingest New Media Asset</h5>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="modal-body p-4">
              {error && <div className="alert alert-danger py-2 small">{error}</div>}

              <div className="row g-3">
                <div className="col-12 col-md-8">
                  <label className="form-label small text-muted">Asset Title *</label>
                  <input
                    type="text"
                    name="title"
                    required
                    className="form-control form-control-sm bg-surface border-secondary text-light shadow-none"
                    placeholder="e.g. Fighter: Sky Warriors"
                    value={formData.title}
                    onChange={handleChange}
                  />
                </div>

                <div className="col-12 col-md-4">
                  <label className="form-label small text-muted">Primary Language</label>
                  <select
                    name="primary_language"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.primary_language}
                    onChange={handleChange}
                  >
                    <option value="Hindi">Hindi</option>
                    <option value="Tamil">Tamil</option>
                    <option value="Telugu">Telugu</option>
                    <option value="Kannada">Kannada</option>
                    <option value="Malayalam">Malayalam</option>
                    <option value="Bengali">Bengali</option>
                    <option value="English">English</option>
                  </select>
                </div>

                <div className="col-12">
                  <label className="form-label small text-muted">Synopsis / Description</label>
                  <textarea
                    name="description"
                    rows="2"
                    className="form-control form-control-sm bg-surface border-secondary text-light shadow-none"
                    placeholder="Brief storyline or release summary..."
                    value={formData.description}
                    onChange={handleChange}
                  ></textarea>
                </div>

                <div className="col-12 col-md-4">
                  <label className="form-label small text-muted">Category *</label>
                  <select
                    name="category"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.category}
                    onChange={handleChange}
                  >
                    {categories.map(c => (
                      <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
                    ))}
                  </select>
                </div>

                <div className="col-12 col-md-4">
                  <label className="form-label small text-muted">Encoding Format *</label>
                  <select
                    name="format"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.format}
                    onChange={handleChange}
                  >
                    {formats.map(f => (
                      <option key={f.format_id} value={f.format_id}>{f.format_name}</option>
                    ))}
                  </select>
                </div>

                <div className="col-12 col-md-4">
                  <label className="form-label small text-muted">DRM Security Policy *</label>
                  <select
                    name="drm_policy"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.drm_policy}
                    onChange={handleChange}
                  >
                    {drmPolicies.map(d => (
                      <option key={d.policy_id} value={d.policy_id}>{d.policy_name}</option>
                    ))}
                  </select>
                </div>

                <div className="col-12 col-md-6">
                  <label className="form-label small text-muted">Rights Holder Studio *</label>
                  <select
                    name="rights_holder"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.rights_holder}
                    onChange={handleChange}
                  >
                    {holders.map(h => (
                      <option key={h.rights_holder_id} value={h.rights_holder_id}>{h.legal_name}</option>
                    ))}
                  </select>
                </div>

                <div className="col-6 col-md-3">
                  <label className="form-label small text-muted">Censor Rating</label>
                  <select
                    name="censor_rating"
                    className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.censor_rating}
                    onChange={handleChange}
                  >
                    <option value="U">U</option>
                    <option value="U/A 13+">U/A 13+</option>
                    <option value="U/A 16+">U/A 16+</option>
                    <option value="A">A</option>
                  </select>
                </div>

                <div className="col-6 col-md-3">
                  <label className="form-label small text-muted">Release Year</label>
                  <input
                    type="number"
                    name="release_year"
                    className="form-control form-control-sm bg-surface border-secondary text-light shadow-none"
                    value={formData.release_year}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            <div className="modal-footer border-secondary py-2">
              <button type="button" className="btn btn-secondary btn-sm" onClick={onClose}>Cancel</button>
              <button type="submit" className="btn btn-primary btn-sm px-4" disabled={submitting}>
                {submitting ? 'Ingesting...' : 'Confirm Ingestion'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
