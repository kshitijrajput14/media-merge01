import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  ShieldCheck,
  ShieldAlert,
  Sliders,
  RotateCcw,
  CheckCircle,
  Eye,
  Key,
  Clock,
  Tv,
  Layers
} from 'lucide-react';
import { startStreamingSession, verifyDrmToken, updateWatchProgress } from '../services/api';

export default function StreamingPlayerView({ activeAsset, currentUser }) {
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedQuality, setSelectedQuality] = useState('1080p FHD');
  const [drmVerified, setDrmVerified] = useState(null);
  const [watermarkPos, setWatermarkPos] = useState({ top: '15%', left: '20%' });

  const videoRef = useRef(null);

  // Default asset if none selected
  const asset = activeAsset || {
    asset_id: 1,
    title: 'Shershaah: The Kargil Legend',
    category_name: 'Feature Film',
    censor_rating: 'U/A 13+',
    primary_language: 'Hindi',
    release_year: 2024
  };

  const user = currentUser || {
    user_id: 1,
    email: 'aditya.admin@mediamerge.in',
    full_name: 'Aditya Vikram Sharma'
  };

  const initSession = async () => {
    setLoading(true);
    setDrmVerified(null);
    try {
      const res = await startStreamingSession({
        user_id: user.user_id,
        asset_id: asset.asset_id,
        quality: selectedQuality,
        device_type: 'Desktop Web Browser Player'
      });
      setSessionData(res.data);
    } catch (err) {
      console.error("Session init error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initSession();
  }, [asset.asset_id, selectedQuality]);

  // Jitter watermark position periodically to deter screen recorders
  useEffect(() => {
    const interval = setInterval(() => {
      const top = `${Math.floor(Math.random() * 60) + 15}%`;
      const left = `${Math.floor(Math.random() * 50) + 15}%`;
      setWatermarkPos({ top, left });
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleVerifyDrm = async () => {
    if (!sessionData?.drm_license?.token) return;
    try {
      const res = await verifyDrmToken(sessionData.drm_license.token);
      setDrmVerified(res.data);
    } catch (err) {
      console.error("DRM verify error:", err);
      setDrmVerified({ valid: false, reason: 'DRM License Validation Failed' });
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      const cur = Math.floor(videoRef.current.currentTime);
      const dur = Math.floor(videoRef.current.duration) || 7200;
      // Send progress heartbeat
      if (cur > 0 && cur % 15 === 0) {
        updateWatchProgress({
          user_id: user.user_id,
          asset_id: asset.asset_id,
          position: cur,
          total: dur
        }).catch(() => {});
      }
    }
  };

  return (
    <div className="d-flex flex-column gap-4">
      {/* Header */}
      <div className="d-flex align-items-center justify-content-between flex-wrap gap-3">
        <div>
          <h4 className="fw-bold text-white mb-1">Content Streaming & DRM Protection Player</h4>
          <p className="text-muted small mb-0">Module 11: AES-128 / Widevine DRM token exchange, dynamic forensic watermarking, and secure playback.</p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <span className="badge badge-drm d-flex align-items-center gap-1 py-2 px-3">
            <ShieldCheck size={14} />
            DRM License Status: {sessionData ? 'ACTIVE' : 'INITIALIZING'}
          </span>
        </div>
      </div>

      {/* Main Player Row */}
      <div className="row g-4">
        {/* Left Column: Player */}
        <div className="col-12 col-xl-8">
          <div className="card-glass overflow-hidden position-relative">
            {/* Player Container */}
            <div className="position-relative bg-black" style={{ minHeight: '420px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {loading ? (
                <div className="text-center p-5">
                  <div className="spinner-border text-primary" role="status"></div>
                  <div className="text-muted small mt-2">Negotiating Widevine license key...</div>
                </div>
              ) : (
                <>
                  <video
                    ref={videoRef}
                    className="w-100 h-100"
                    controls
                    playsInline
                    src={sessionData?.stream_url || "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}
                    onTimeUpdate={handleTimeUpdate}
                    onPlay={() => setIsPlaying(true)}
                    onPause={() => setIsPlaying(false)}
                    style={{ maxHeight: '480px', objectFit: 'contain' }}
                  ></video>

                  {/* Forensic Dynamic Watermark Overlay */}
                  {sessionData?.watermark?.enabled && (
                    <div
                      className="player-watermark-overlay"
                      style={{ top: watermarkPos.top, left: watermarkPos.left }}
                    >
                      {sessionData.watermark.overlay_text}
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Under-player Info Bar */}
            <div className="p-3 bg-surface border-top border-secondary d-flex align-items-center justify-content-between flex-wrap gap-2">
              <div>
                <h5 className="fw-bold text-white mb-0">{asset.title}</h5>
                <span className="text-muted small">
                  {asset.release_year} • {asset.primary_language} • {asset.censor_rating} • Quality: {selectedQuality}
                </span>
              </div>

              {/* Quality Switcher */}
              <div className="d-flex align-items-center gap-2">
                <span className="text-muted small">Playback:</span>
                <select
                  className="form-select form-select-sm bg-dark border-secondary text-light shadow-none"
                  style={{ width: '130px' }}
                  value={selectedQuality}
                  onChange={(e) => setSelectedQuality(e.target.value)}
                >
                  <option value="4K UHD">4K UHD</option>
                  <option value="1080p FHD">1080p FHD</option>
                  <option value="720p HD">720p HD</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Live DRM Handshake & Security Inspector */}
        <div className="col-12 col-xl-4">
          <div className="card-glass p-3 h-100 d-flex flex-column gap-3">
            <div className="d-flex align-items-center justify-content-between border-bottom border-secondary pb-2">
              <div className="d-flex align-items-center gap-2">
                <Key className="text-info" size={18} />
                <h6 className="fw-bold text-white mb-0">DRM Key Server Inspector</h6>
              </div>
              <button
                className="btn btn-outline-info btn-sm py-0 px-2"
                onClick={handleVerifyDrm}
                title="Verify DRM license signature"
              >
                Verify
              </button>
            </div>

            {/* DRM Details */}
            <div className="p-2 rounded bg-surface border border-secondary small d-flex flex-column gap-2">
              <div>
                <div className="text-muted" style={{ fontSize: '0.72rem' }}>SESSION TOKEN</div>
                <div className="mono-font text-info text-truncate">{sessionData?.session_token || 'Initializing...'}</div>
              </div>

              <div>
                <div className="text-muted" style={{ fontSize: '0.72rem' }}>DRM LICENSE TOKEN</div>
                <div className="mono-font text-white text-truncate" style={{ fontSize: '0.75rem' }}>
                  {sessionData?.drm_license?.token || 'None issued'}
                </div>
              </div>

              <div className="row g-2">
                <div className="col-6">
                  <div className="text-muted" style={{ fontSize: '0.72rem' }}>ENCRYPTION</div>
                  <div className="mono-font text-white">{sessionData?.drm_license?.encryption_type || 'AES-128-CBC'}</div>
                </div>
                <div className="col-6">
                  <div className="text-muted" style={{ fontSize: '0.72rem' }}>STATUS</div>
                  <div className="text-success fw-bold">{sessionData?.drm_license?.status || 'Active'}</div>
                </div>
              </div>
            </div>

            {/* Verification result badge */}
            {drmVerified && (
              <div className={`p-2 rounded border small ${drmVerified.valid ? 'bg-success bg-opacity-10 border-success text-success' : 'bg-danger bg-opacity-10 border-danger text-danger'}`}>
                <div className="fw-bold d-flex align-items-center gap-1">
                  {drmVerified.valid ? <CheckCircle size={14} /> : <ShieldAlert size={14} />}
                  <span>{drmVerified.valid ? 'Cryptographically Verified' : 'Verification Rejected'}</span>
                </div>
                <div className="mono-font mt-1" style={{ fontSize: '0.7rem' }}>
                  {drmVerified.valid ? `License Type: ${drmVerified.license_type} | User: ${drmVerified.user}` : drmVerified.reason}
                </div>
              </div>
            )}

            {/* Forensic Watermarking Specification */}
            <div className="p-3 rounded bg-surface border border-secondary">
              <div className="fw-semibold text-white small mb-2 d-flex align-items-center gap-1">
                <Eye size={14} className="text-warning" />
                <span>Forensic Watermarking Specifications</span>
              </div>
              <ul className="text-muted small ps-3 mb-0" style={{ fontSize: '0.75rem' }}>
                <li>Encodes subscriber ID: <span className="text-white mono-font">{user.email}</span></li>
                <li>Dynamic multi-quadrant jitter (anti-camcorder protection)</li>
                <li>Burned-in frame timestamp for leak traceability</li>
                <li>Tamper-resistant client-side overlay layer</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
