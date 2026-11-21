import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DashboardView from './components/DashboardView';
import AssetCatalogView from './components/AssetCatalogView';
import SearchRetrievalView from './components/SearchRetrievalView';
import VersioningHistoryView from './components/VersioningHistoryView';
import ContractsRightsView from './components/ContractsRightsView';
import RoyaltyCalculatorView from './components/RoyaltyCalculatorView';
import StreamingPlayerView from './components/StreamingPlayerView';
import SubscriptionsView from './components/SubscriptionsView';
import RecommendationsView from './components/RecommendationsView';
import AccessControlView from './components/AccessControlView';
import AssetDetailModal from './components/AssetDetailModal';
import AssetUploadModal from './components/AssetUploadModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentRole, setCurrentRole] = useState({ id: 1, name: 'Admin', badge: 'bg-danger' });
  const [currentUser, setCurrentUser] = useState({
    user_id: 1,
    full_name: 'Aditya Vikram Sharma',
    email: 'aditya.admin@mediamerge.in',
    role: 1,
    role_name: 'Admin'
  });

  // Modals & Selected Assets
  const [inspectAssetId, setInspectAssetId] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [activeStreamAsset, setActiveStreamAsset] = useState(null);

  const handleSelectAssetForPlay = (asset) => {
    setActiveStreamAsset(asset);
    setActiveTab('streaming');
  };

  const handleInspectAsset = (assetId) => {
    setInspectAssetId(assetId);
  };

  const handleRoleChange = (role) => {
    setCurrentRole(role);
    // Simulate user context change based on role
    if (role.name === 'Producer') {
      setCurrentUser({
        user_id: 2,
        full_name: 'Karan Johar Singhania',
        email: 'karan.producer@dharmamedia.in',
        role: 2,
        role_name: 'Producer'
      });
    } else if (role.name === 'Content Manager') {
      setCurrentUser({
        user_id: 4,
        full_name: 'Pooja Hegde Iyer',
        email: 'pooja.curator@mediamerge.in',
        role: 3,
        role_name: 'Content Manager'
      });
    } else if (role.name === 'Rights & Royalty Officer') {
      setCurrentUser({
        user_id: 6,
        full_name: 'Sunita Narayanan',
        email: 'sunita.royalty@mediamerge.in',
        role: 4,
        role_name: 'Rights & Royalty Officer'
      });
    } else if (role.name === 'Subscriber') {
      setCurrentUser({
        user_id: 9,
        full_name: 'Aarav Gupta',
        email: 'aarav.gupta99@gmail.com',
        role: 6,
        role_name: 'Subscriber'
      });
    } else {
      setCurrentUser({
        user_id: 1,
        full_name: 'Aditya Vikram Sharma',
        email: 'aditya.admin@mediamerge.in',
        role: 1,
        role_name: 'Admin'
      });
    }
  };

  return (
    <div className="min-vh-100 d-flex flex-column" style={{ backgroundColor: 'var(--bg-dark)' }}>
      {/* Top Navbar */}
      <Navbar
        currentRole={currentRole}
        setCurrentRole={handleRoleChange}
        onQuickSearch={() => setActiveTab('search')}
        onOpenPlayerDemo={() => setActiveTab('streaming')}
      />

      {/* Main Workspace */}
      <div className="container-fluid px-4 pb-5 flex-grow-1">
        <div className="row g-4">
          {/* Left Navigation Sidebar */}
          <div className="col-12 col-lg-3 col-xl-2">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
          </div>

          {/* Right Main Content Area */}
          <div className="col-12 col-lg-9 col-xl-10">
            {activeTab === 'dashboard' && (
              <DashboardView onSelectAssetForPlay={handleSelectAssetForPlay} />
            )}

            {activeTab === 'catalog' && (
              <AssetCatalogView
                onSelectAssetForPlay={handleSelectAssetForPlay}
                onInspectAsset={handleInspectAsset}
                onOpenUploadModal={() => setShowUploadModal(true)}
              />
            )}

            {activeTab === 'search' && (
              <SearchRetrievalView
                onSelectAssetForPlay={handleSelectAssetForPlay}
                onInspectAsset={handleInspectAsset}
              />
            )}

            {activeTab === 'versions' && (
              <VersioningHistoryView
                onSelectAssetForPlay={handleSelectAssetForPlay}
                onInspectAsset={handleInspectAsset}
              />
            )}

            {activeTab === 'contracts' && (
              <ContractsRightsView />
            )}

            {activeTab === 'royalties' && (
              <RoyaltyCalculatorView />
            )}

            {activeTab === 'streaming' && (
              <StreamingPlayerView
                activeAsset={activeStreamAsset}
                currentUser={currentUser}
              />
            )}

            {activeTab === 'subscriptions' && (
              <SubscriptionsView currentUser={currentUser} />
            )}

            {activeTab === 'recommendations' && (
              <RecommendationsView
                onSelectAssetForPlay={handleSelectAssetForPlay}
                currentUser={currentUser}
              />
            )}

            {activeTab === 'access' && (
              <AccessControlView />
            )}
          </div>
        </div>
      </div>

      {/* Inspect / Versioning Modal */}
      {inspectAssetId && (
        <AssetDetailModal
          assetId={inspectAssetId}
          onClose={() => setInspectAssetId(null)}
          onRefresh={() => {}}
        />
      )}

      {/* Ingest Asset Modal */}
      {showUploadModal && (
        <AssetUploadModal
          onClose={() => setShowUploadModal(false)}
          onSuccess={() => setActiveTab('catalog')}
        />
      )}
    </div>
  );
}
