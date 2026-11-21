import React, { useState, useEffect, useMemo } from 'react';
import {
  Search,
  Filter,
  Play,
  Eye,
  Sliders,
  Sparkles,
  RefreshCw,
  Layers,
  Film,
  Tag as TagIcon,
  X,
  CheckCircle2
} from 'lucide-react';
import { searchAssets } from '../services/api';
import { MASTER_CATALOG } from '../services/masterCatalog';

export default function SearchRetrievalView({ onSelectAssetForPlay, onInspectAsset }) {
  const [query, setQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCensor, setSelectedCensor] = useState('');
  const [selectedSort, setSelectedSort] = useState('-asset_id');
  const [results, setResults] = useState(MASTER_CATALOG);
  const [loading, setLoading] = useState(false);
  const [isLiveSearch, setIsLiveSearch] = useState(true);

  // Debounce input typing by 200ms for fast live search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  // Execute Search whenever query or filters change
  const executeSearch = async (searchTerm = debouncedQuery) => {
    setLoading(true);
    try {
      const params = {};
      if (searchTerm && searchTerm.trim()) params.q = searchTerm.trim();
      if (selectedLanguage) params.language = selectedLanguage;
      if (selectedCategory) params.category = selectedCategory;
      if (selectedCensor) params.censor = selectedCensor;
      if (selectedSort) params.sort_by = selectedSort;

      const res = await searchAssets(params);
      const apiResults = res.data.results;

      if (Array.isArray(apiResults) && apiResults.length > 0) {
        setResults(apiResults);
        setIsLiveSearch(true);
        setLoading(false);
        return;
      }
    } catch (err) {
      console.warn("Backend search endpoint unavailable, executing client-side index query:", err);
      setIsLiveSearch(false);
    }

    // High-performance client-side search across all 71 master assets
    let filtered = [...MASTER_CATALOG];
    const q = (searchTerm || '').trim().toLowerCase();

    if (q) {
      filtered = filtered.filter((asset) => {
        const titleMatch = (asset.title || '').toLowerCase().includes(q);
        const descMatch = (asset.description || '').toLowerCase().includes(q);
        const langMatch = (asset.primary_language || '').toLowerCase().includes(q);
        const rightsMatch = (asset.rights_holder_name || '').toLowerCase().includes(q);
        const catMatch = (asset.category_name || '').toLowerCase().includes(q);
        const fmtMatch = (asset.format_name || '').toLowerCase().includes(q);
        const tagsMatch = (asset.tags || []).some((t) => (t.tag_name || '').toLowerCase().includes(q));

        return titleMatch || descMatch || langMatch || rightsMatch || catMatch || fmtMatch || tagsMatch;
      });
    }

    if (selectedLanguage) {
      filtered = filtered.filter(
        (a) => (a.primary_language || '').toLowerCase() === selectedLanguage.toLowerCase()
      );
    }

    if (selectedCategory) {
      filtered = filtered.filter(
        (a) => (a.category_name || '').toLowerCase().includes(selectedCategory.toLowerCase())
      );
    }

    if (selectedCensor) {
      filtered = filtered.filter((a) => a.censor_rating === selectedCensor);
    }

    // Sort
    if (selectedSort === 'title') {
      filtered.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else if (selectedSort === '-title') {
      filtered.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
    } else if (selectedSort === '-release_year') {
      filtered.sort((a, b) => (b.release_year || 0) - (a.release_year || 0));
    } else if (selectedSort === '-duration_seconds') {
      filtered.sort((a, b) => (b.duration_seconds || 0) - (a.duration_seconds || 0));
    } else {
      // Default: newest asset_id first
      filtered.sort((a, b) => (b.asset_id || 0) - (a.asset_id || 0));
    }

    setResults(filtered);
    setLoading(false);
  };

  useEffect(() => {
    executeSearch(debouncedQuery);
  }, [debouncedQuery, selectedLanguage, selectedCategory, selectedCensor, selectedSort]);

  const handleManualSubmit = (e) => {
    e.preventDefault();
    executeSearch(query);
  };

  const handleQuickChip = (term, filterType = 'query') => {
    if (filterType === 'query') {
      setQuery(term);
    } else if (filterType === 'language') {
      setSelectedLanguage(term === selectedLanguage ? '' : term);
    } else if (filterType === 'censor') {
      setSelectedCensor(term === selectedCensor ? '' : term);
    }
  };

  const handleResetFilters = () => {
    setQuery('');
    setDebouncedQuery('');
    setSelectedLanguage('');
    setSelectedCategory('');
    setSelectedCensor('');
    setSelectedSort('-asset_id');
  };

  return (
    <div className="d-flex flex-column gap-4">
      {/* Search Header */}
      <div className="d-flex align-items-center justify-content-between flex-wrap gap-2">
        <div>
          <h4 className="fw-bold text-white mb-1 d-flex align-items-center gap-2">
            <Search className="text-primary" size={24} />
            Advanced Search & Faceted Retrieval
          </h4>
          <p className="text-muted small mb-0">
            Real-time indexed search across titles, synopses, cast, metadata tags, languages, and rights holders.
          </p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <span className="badge bg-dark border border-secondary text-info mono-font py-2 px-3">
            {results.length} Matches Found
          </span>
          <button
            className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1"
            onClick={handleResetFilters}
            title="Reset All Filters"
          >
            <RefreshCw size={13} /> Clear
          </button>
        </div>
      </div>

      {/* Main Search Bar & Quick Filters Card */}
      <div className="card-glass p-4">
        <form onSubmit={handleManualSubmit}>
          <div className="input-group mb-3">
            <span className="input-group-text bg-surface border-secondary text-primary px-3">
              <Search size={18} />
            </span>
            <input
              type="text"
              className="form-control form-control-lg bg-surface border-secondary text-light shadow-none"
              placeholder="Search by title (e.g. Jawan, RRR), actor, director, genre, or keyword..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              autoFocus
            />
            {query && (
              <button
                type="button"
                className="btn btn-outline-secondary border-secondary text-muted"
                onClick={() => setQuery('')}
                title="Clear input"
              >
                <X size={16} />
              </button>
            )}
            <button className="btn btn-primary px-4 fw-semibold" type="submit" disabled={loading}>
              {loading ? 'Searching...' : 'Search Engine'}
            </button>
          </div>

          {/* Quick Search Suggestion Pills */}
          <div className="d-flex align-items-center gap-2 flex-wrap mb-3">
            <span className="text-muted small" style={{ fontSize: '0.75rem' }}>Popular Queries:</span>
            {['Jawan', 'RRR', 'Shershaah', 'Kantara', 'Vikram', 'Ponniyin Selvan', '4K', 'War', 'Action', 'Drama'].map((chip) => (
              <button
                key={chip}
                type="button"
                className={`btn btn-sm py-0 px-2 rounded-pill ${query.toLowerCase() === chip.toLowerCase() ? 'btn-primary' : 'btn-outline-secondary'}`}
                style={{ fontSize: '0.75rem' }}
                onClick={() => handleQuickChip(chip, 'query')}
              >
                {chip}
              </button>
            ))}
          </div>

          {/* Facets & Filter Controls */}
          <div className="row g-2 pt-3 border-top border-secondary align-items-center">
            <div className="col-6 col-md-3">
              <label className="form-label small text-muted mb-1">Language</label>
              <select
                className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
              >
                <option value="">All Indian & Global Languages</option>
                <option value="Hindi">Hindi</option>
                <option value="Tamil">Tamil</option>
                <option value="Telugu">Telugu</option>
                <option value="Kannada">Kannada</option>
                <option value="Bengali">Bengali</option>
                <option value="Malayalam">Malayalam</option>
                <option value="English">English</option>
              </select>
            </div>

            <div className="col-6 col-md-3">
              <label className="form-label small text-muted mb-1">Category</label>
              <select
                className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option value="">All Categories</option>
                <option value="Feature Film">Feature Film</option>
                <option value="Web Series">Web Series</option>
                <option value="Documentary">Documentary</option>
                <option value="Archival Classic">Archival Classic</option>
                <option value="Music Video">Music Video</option>
              </select>
            </div>

            <div className="col-6 col-md-3">
              <label className="form-label small text-muted mb-1">CBFC Certification</label>
              <select
                className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                value={selectedCensor}
                onChange={(e) => setSelectedCensor(e.target.value)}
              >
                <option value="">All Certifications</option>
                <option value="U">U (Universal)</option>
                <option value="U/A 7+">U/A 7+</option>
                <option value="U/A 13+">U/A 13+</option>
                <option value="U/A 16+">U/A 16+</option>
                <option value="A">A (Adults Only)</option>
              </select>
            </div>

            <div className="col-6 col-md-3">
              <label className="form-label small text-muted mb-1">Sort Ordering</label>
              <select
                className="form-select form-select-sm bg-surface border-secondary text-light shadow-none"
                value={selectedSort}
                onChange={(e) => setSelectedSort(e.target.value)}
              >
                <option value="-asset_id">Newest Additions First</option>
                <option value="title">Title (A-Z)</option>
                <option value="-title">Title (Z-A)</option>
                <option value="-release_year">Release Year (Latest)</option>
                <option value="-duration_seconds">Duration (Longest)</option>
              </select>
            </div>
          </div>
        </form>
      </div>

      {/* Results Header */}
      <div className="d-flex align-items-center justify-content-between px-1">
        <span className="text-muted small">
          Showing <span className="text-white fw-bold">{results.length}</span> matching assets
          {query && (
            <span> for keyword <strong className="text-info">"{query}"</strong></span>
          )}
        </span>
        {query || selectedLanguage || selectedCategory || selectedCensor ? (
          <button
            className="btn btn-link text-muted small p-0 text-decoration-none"
            onClick={handleResetFilters}
          >
            Clear active filters
          </button>
        ) : null}
      </div>

      {/* Results List */}
      {loading ? (
        <div className="text-center p-5">
          <div className="spinner-border text-primary" role="status"></div>
          <div className="text-muted mt-2 small">Scanning media repository...</div>
        </div>
      ) : results.length === 0 ? (
        <div className="text-center p-5 card-glass">
          <Search size={44} className="text-muted mb-3 opacity-50" />
          <h5 className="text-white">No Matching Assets Found</h5>
          <p className="text-muted small mb-3" style={{ maxWidth: '420px', margin: '0 auto' }}>
            No media asset matches your search query "{query}". Try checking for spelling or adjusting filters.
          </p>
          <div className="d-flex justify-content-center gap-2">
            <button className="btn btn-primary btn-sm" onClick={handleResetFilters}>
              View All 71 Master Assets
            </button>
            <button className="btn btn-outline-secondary btn-sm" onClick={() => setQuery('Jawan')}>
              Try "Jawan"
            </button>
            <button className="btn btn-outline-secondary btn-sm" onClick={() => setQuery('RRR')}>
              Try "RRR"
            </button>
          </div>
        </div>
      ) : (
        <div className="d-flex flex-column gap-3">
          {results.map((asset) => {
            const censorClass =
              asset.censor_rating === 'U' ? 'badge-censor-u' :
              asset.censor_rating === 'A' ? 'badge-censor-a' : 'badge-censor-ua';
            const durationMin = Math.floor((asset.duration_seconds || 5400) / 60);

            return (
              <div
                key={asset.asset_id}
                className="card-glass p-3 d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 position-relative overflow-hidden"
              >
                <div className="d-flex align-items-center gap-3">
                  {/* Visual Icon / Poster Thumbnail */}
                  <div
                    className="rounded bg-surface d-flex flex-column align-items-center justify-content-center text-primary"
                    style={{
                      width: '74px',
                      height: '74px',
                      minWidth: '74px',
                      background: 'linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%)',
                      border: '1px solid rgba(255,255,255,0.08)'
                    }}
                  >
                    <Film size={26} className="text-primary mb-1 opacity-75" />
                    <span className="text-muted mono-font" style={{ fontSize: '0.62rem' }}>
                      #{asset.asset_id}
                    </span>
                  </div>

                  {/* Asset Information */}
                  <div>
                    <div className="d-flex align-items-center gap-2 flex-wrap mb-1">
                      <h6 className="fw-bold text-white mb-0">{asset.title}</h6>
                      <span className="badge bg-secondary" style={{ fontSize: '0.7rem' }}>
                        {asset.category_name}
                      </span>
                      <span className="badge badge-drm">Widevine L1</span>
                      <span className="badge bg-dark border border-secondary text-info" style={{ fontSize: '0.7rem' }}>
                        {asset.primary_language}
                      </span>
                      <span className={`badge ${censorClass}`} style={{ fontSize: '0.7rem' }}>
                        {asset.censor_rating}
                      </span>
                    </div>

                    <p className="text-muted small mb-1 line-clamp-1" style={{ maxWidth: '680px' }}>
                      {asset.description || 'Verified production asset with digital distribution rights.'}
                    </p>

                    <div className="d-flex align-items-center gap-3 text-muted small flex-wrap" style={{ fontSize: '0.72rem' }}>
                      <span>
                        Rights Holder: <strong className="text-light">{asset.rights_holder_name}</strong>
                      </span>
                      <span>•</span>
                      <span>
                        Year: <strong className="text-light">{asset.release_year}</strong>
                      </span>
                      <span>•</span>
                      <span>
                        Duration: <strong className="text-info mono-font">{durationMin} min</strong>
                      </span>
                      <span>•</span>
                      <span>
                        Size: <strong className="text-warning mono-font">{parseFloat(asset.file_size_mb || 0).toFixed(0)} MB</strong>
                      </span>
                    </div>

                    {/* Tag Pills */}
                    {(asset.tags || []).length > 0 && (
                      <div className="d-flex gap-1 mt-2 flex-wrap">
                        {asset.tags.map((t, idx) => (
                          <span
                            key={idx}
                            className="badge bg-dark border border-secondary text-muted"
                            style={{ fontSize: '0.65rem', cursor: 'pointer' }}
                            onClick={() => setQuery(t.tag_name)}
                            title={`Search by tag: ${t.tag_name}`}
                          >
                            #{t.tag_name}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="d-flex align-items-center gap-2 align-self-end align-self-md-center">
                  <button
                    className="btn btn-outline-light btn-sm d-flex align-items-center gap-1"
                    onClick={() => onInspectAsset(asset.asset_id)}
                  >
                    <Eye size={14} />
                    <span>Inspect</span>
                  </button>
                  <button
                    className="btn btn-primary btn-sm d-flex align-items-center gap-1 shadow-sm px-3"
                    onClick={() => onSelectAssetForPlay(asset)}
                  >
                    <Play size={14} fill="white" />
                    <span>Stream</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
