import React, { useEffect, useState } from 'react';
import {
  Film,
  Search,
  Filter,
  Plus,
  Play,
  Layers,
  Shield,
  Eye,
  SlidersHorizontal,
  GitBranch,
  RefreshCw,
  Sparkles,
  Wifi,
  WifiOff
} from 'lucide-react';
import { getAssets, getCategories, getFormats } from '../services/api';
import { MASTER_CATALOG } from '../services/masterCatalog';

const FALLBACK_ASSETS = MASTER_CATALOG;

export default function AssetCatalogView({ onSelectAssetForPlay, onInspectAsset, onOpenUploadModal }) {
  const [assets, setAssets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [formats, setFormats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isBackendLive, setIsBackendLive] = useState(true);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('');
  const [selectedCensor, setSelectedCensor] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'

  const fetchAssetsList = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (selectedFormat) params.format = selectedFormat;
      if (selectedCensor) params.censor = selectedCensor;
      if (searchQuery) params.search = searchQuery;

      const [resAssets, resCats, resFmt] = await Promise.all([
        getAssets(params),
        getCategories(),
        getFormats()
      ]);

      const assetList = resAssets.data.results || resAssets.data || [];
      const catList = resCats.data.results || resCats.data || [];
      const fmtList = resFmt.data.results || resFmt.data || [];

      if (assetList.length > 0) {
        setAssets(assetList);
        setIsBackendLive(true);
      } else {
        // Fallback filter
        let filtered = FALLBACK_ASSETS;
        if (selectedCensor) filtered = filtered.filter(a => a.censor_rating === selectedCensor);
        if (searchQuery) {
          const q = searchQuery.toLowerCase();
          filtered = filtered.filter(a => a.title.toLowerCase().includes(q) || a.primary_language.toLowerCase().includes(q));
        }
        setAssets(filtered);
      }

      setCategories(catList.length > 0 ? catList : [
        { category_id: 1, category_name: 'Feature Film' },
        { category_id: 2, category_name: 'Web Series' },
        { category_id: 3, category_name: 'Documentary' },
        { category_id: 4, category_name: '4K Archival Classic' }
      ]);

      setFormats(fmtList.length > 0 ? fmtList : [
        { format_id: 1, format_name: '4K Ultra HD MP4' },
        { format_id: 2, format_name: 'Full HD 1080p MP4' },
        { format_id: 3, format_name: 'ProRes 422 Master' }
      ]);
    } catch (err) {
      console.warn("Backend not reached, loading reliable master catalog:", err);
      setIsBackendLive(false);
      let filtered = FALLBACK_ASSETS;
      if (selectedCensor) filtered = filtered.filter(a => a.censor_rating === selectedCensor);
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        filtered = filtered.filter(a => a.title.toLowerCase().includes(q) || a.primary_language.toLowerCase().includes(q));
      }
      setAssets(filtered);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssetsList();
  }, [selectedCategory, selectedFormat, selectedCensor]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchAssetsList();
  };

  return (
    <div className="d-flex flex-column gap-4">
      {/* Catalog Header */}
      <div className="d-flex align-items-center justify-content-between flex-wrap gap-3">
        <div>
          <h4 className="fw-bold text-white mb-1 d-flex align-items-center gap-2">
            <Film className="text-primary" size={24} />
            Centralized Media Asset Catalog
          </h4>
          <p className="text-muted small mb-0">Browse, organize, stream, and manage technical metadata across master assets.</p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <button
            className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1"
            onClick={fetchAssetsList}
            title="Refresh Catalog"
          >
            <RefreshCw size={14} /> Refresh
          </button>
          <button
            className="btn btn-primary btn-sm d-flex align-items-center gap-2 shadow"
            onClick={onOpenUploadModal}
          >
            <Plus size={16} />
            <span>Ingest Media Asset</span>
          </button>
          <div className="btn-group btn-group-sm">
            <button
              className={`btn ${viewMode === 'grid' ? 'btn-secondary' : 'btn-outline-secondary'}`}
              onClick={() => setViewMode('grid')}
            >
              Grid
            </button>
            <button
              className={`btn ${viewMode === 'table' ? 'btn-secondary' : 'btn-outline-secondary'}`}
              onClick={() => setViewMode('table')}
            >
              Table
            </button>
          </div>
        </div>
      </div>

      {/* Filters Toolbar */}
      <div className="card-glass p-3">
        <form onSubmit={handleSearchSubmit} className="row g-2 align-items-center">
          <div className="col-12 col-md-4">
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-surface border-secondary text-muted">
                <Search size={14} />
              </span>
              <input
                type="text"
                className="form-control bg-surface border-secondary text-light shadow-none"
                placeholder="Search title, rights holder, tags, language..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="col-6 col-md-2">
            <select
              className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
              ))}
            </select>
          </div>

          <div className="col-6 col-md-2">
            <select
              className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
              value={selectedFormat}
              onChange={(e) => setSelectedFormat(e.target.value)}
            >
              <option value="">All Formats</option>
              {formats.map((f) => (
                <option key={f.format_id} value={f.format_id}>{f.format_name}</option>
              ))}
            </select>
          </div>

          <div className="col-6 col-md-2">
            <select
              className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
              value={selectedCensor}
              onChange={(e) => setSelectedCensor(e.target.value)}
            >
              <option value="">All Censor Ratings</option>
              <option value="U">U (Universal)</option>
              <option value="U/A 13+">U/A 13+</option>
              <option value="U/A 16+">U/A 16+</option>
              <option value="A">A (Adults Only)</option>
            </select>
          </div>

          <div className="col-6 col-md-2 d-flex gap-2">
            <button type="submit" className="btn btn-outline-info btn-sm flex-grow-1">
              Filter
            </button>
            <button
              type="button"
              className="btn btn-outline-secondary btn-sm"
              onClick={() => {
                setSelectedCategory('');
                setSelectedFormat('');
                setSelectedCensor('');
                setSearchQuery('');
                fetchAssetsList();
              }}
              title="Reset Filters"
            >
              <RefreshCw size={13} />
            </button>
          </div>
        </form>
      </div>

      {/* Catalog Counter & Stats */}
      <div className="d-flex align-items-center justify-content-between px-1">
        <span className="text-muted small">
          Showing <span className="text-white fw-bold">{assets.length}</span> verified master media assets
        </span>
        <div className="d-flex align-items-center gap-2">
          {isBackendLive ? (
            <span className="badge bg-success bg-opacity-25 text-success border border-success d-flex align-items-center gap-1" style={{ fontSize: '0.7rem' }}>
              <Wifi size={11} /> Database Live
            </span>
          ) : (
            <span className="badge bg-warning bg-opacity-25 text-warning border border-warning d-flex align-items-center gap-1" style={{ fontSize: '0.7rem' }}>
              <WifiOff size={11} /> Cached Catalog
            </span>
          )}
        </div>
      </div>

      {/* Content Rendering: Grid or Table */}
      {loading ? (
        <div className="text-center p-5">
          <div className="spinner-border text-primary" role="status"></div>
          <div className="text-muted mt-2 small">Loading asset repository...</div>
        </div>
      ) : assets.length === 0 ? (
        <div className="text-center p-5 card-glass">
          <Film size={40} className="text-muted mb-3" />
          <h5 className="text-white">No Assets Found</h5>
          <p className="text-muted small">Try adjusting your filters or search keywords.</p>
          <button className="btn btn-outline-primary btn-sm mt-2" onClick={() => { setSearchQuery(''); setSelectedCategory(''); setSelectedCensor(''); fetchAssetsList(); }}>
            Reset Filters
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="row g-3">
          {assets.map((asset) => {
            const censorClass =
              asset.censor_rating === 'U' ? 'badge-censor-u' :
              asset.censor_rating === 'A' ? 'badge-censor-a' : 'badge-censor-ua';

            const durationMinutes = Math.floor((asset.duration_seconds || 5400) / 60);

            return (
              <div key={asset.asset_id} className="col-12 col-sm-6 col-md-4 col-xl-3">
                <div className="card-glass h-100 d-flex flex-column overflow-hidden position-relative">
                  {/* Thumbnail / Mock Poster */}
                  <div
                    className="position-relative bg-surface d-flex align-items-center justify-content-center text-muted"
                    style={{
                      height: '170px',
                      background: 'linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #030712 100%)'
                    }}
                  >
                    <Film size={48} className="opacity-25 text-primary" />
                    <span className={`position-absolute top-0 start-0 m-2 badge ${censorClass}`}>
                      {asset.censor_rating || 'U/A'}
                    </span>
                    <span className="position-absolute top-0 end-0 m-2 badge badge-drm">
                      Widevine L1
                    </span>
                    <div className="position-absolute bottom-0 start-0 end-0 p-2 bg-gradient bg-dark bg-opacity-75 d-flex justify-content-between align-items-center small">
                      <span className="text-white small fw-semibold text-truncate" style={{ maxWidth: '140px' }}>
                        {asset.category_name || 'Feature'}
                      </span>
                      <span className="text-info mono-font">{durationMinutes}m</span>
                    </div>
                  </div>

                  {/* Body Content */}
                  <div className="p-3 d-flex flex-column flex-grow-1">
                    <h6 className="fw-bold text-white mb-1 text-truncate" title={asset.title}>
                      {asset.title}
                    </h6>
                    <div className="text-muted small mb-2 text-truncate" style={{ fontSize: '0.75rem' }}>
                      {asset.rights_holder_name || 'Studio Master'} • {asset.release_year || '2024'}
                    </div>

                    <p className="text-muted small flex-grow-1 line-clamp-2" style={{ fontSize: '0.8rem', minHeight: '38px' }}>
                      {asset.description || 'Verified production asset with digital distribution rights.'}
                    </p>

                    {/* Metadata tags */}
                    <div className="d-flex flex-wrap gap-1 mb-3">
                      {(asset.tags || []).slice(0, 2).map((t, idx) => (
                        <span key={idx} className="badge bg-dark border border-secondary text-muted" style={{ fontSize: '0.65rem' }}>
                          #{t.tag_name}
                        </span>
                      ))}
                      <span className="badge bg-dark border border-secondary text-info mono-font" style={{ fontSize: '0.65rem' }}>
                        {asset.primary_language}
                      </span>
                      <span className="badge bg-dark border border-secondary text-warning mono-font" style={{ fontSize: '0.65rem' }}>
                        {parseFloat(asset.file_size_mb || 4000).toFixed(0)} MB
                      </span>
                    </div>

                    {/* Actions */}
                    <div className="d-flex gap-2 pt-2 border-top border-secondary">
                      <button
                        className="btn btn-outline-light btn-sm flex-grow-1 d-flex align-items-center justify-content-center gap-1"
                        onClick={() => onInspectAsset(asset.asset_id)}
                      >
                        <Eye size={14} />
                        <span>Inspect</span>
                      </button>
                      <button
                        className="btn btn-primary btn-sm flex-grow-1 d-flex align-items-center justify-content-center gap-1 shadow-sm"
                        onClick={() => onSelectAssetForPlay(asset)}
                      >
                        <Play size={14} fill="white" />
                        <span>Stream</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Table View */
        <div className="card-glass overflow-hidden">
          <div className="table-responsive">
            <table className="table table-dark table-hover mb-0 align-middle">
              <thead className="bg-surface text-muted text-uppercase small" style={{ fontSize: '0.72rem' }}>
                <tr>
                  <th className="py-3 px-3">Asset Title</th>
                  <th className="py-3">Category</th>
                  <th className="py-3">Format</th>
                  <th className="py-3">Duration</th>
                  <th className="py-3">Language</th>
                  <th className="py-3">Censor</th>
                  <th className="py-3">Size</th>
                  <th className="py-3 text-end px-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.asset_id}>
                    <td className="px-3">
                      <div className="fw-semibold text-white">{asset.title}</div>
                      <div className="text-muted small" style={{ fontSize: '0.72rem' }}>
                        {asset.rights_holder_name} • {asset.release_year}
                      </div>
                    </td>
                    <td><span className="badge bg-secondary">{asset.category_name}</span></td>
                    <td className="small text-muted">{asset.format_name}</td>
                    <td className="mono-font small text-info">{Math.floor((asset.duration_seconds || 5400) / 60)} min</td>
                    <td><span className="badge bg-dark border border-secondary text-light">{asset.primary_language}</span></td>
                    <td>
                      <span className={`badge ${asset.censor_rating === 'U' ? 'badge-censor-u' : asset.censor_rating === 'A' ? 'badge-censor-a' : 'badge-censor-ua'}`}>
                        {asset.censor_rating}
                      </span>
                    </td>
                    <td className="mono-font small text-muted">{parseFloat(asset.file_size_mb || 0).toFixed(1)} MB</td>
                    <td className="text-end px-3">
                      <div className="d-flex justify-content-end gap-1">
                        <button
                          className="btn btn-outline-light btn-sm"
                          onClick={() => onInspectAsset(asset.asset_id)}
                          title="Inspect Metadata & Versions"
                        >
                          <Eye size={13} />
                        </button>
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => onSelectAssetForPlay(asset)}
                          title="Stream with DRM"
                        >
                          <Play size={13} fill="white" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
