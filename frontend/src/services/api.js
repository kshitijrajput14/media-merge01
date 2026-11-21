import axios from 'axios';

// Dynamically determine API base URL:
// When served on Vite dev server (port 3000), use '/api' to leverage Vite proxy,
// otherwise default to Django's direct URL 'http://127.0.0.1:8000/api'.
const isBrowser = typeof window !== 'undefined';
const API_BASE = isBrowser && window.location.port === '3000'
  ? '/api'
  : 'http://127.0.0.1:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Core & Auth
export const loginUser = (email, password) => apiClient.post('/auth/login/', { email, password });
export const registerUser = (userData) => apiClient.post('/auth/register/', userData);
export const getRoles = () => apiClient.get('/roles/');
export const getUsers = (params) => apiClient.get('/users/', { params });

// Assets & Metadata
export const getAssets = (params) => apiClient.get('/assets/assets/', { params });
export const getAssetDetail = (id) => apiClient.get(`/assets/assets/${id}/`);
export const createAsset = (data) => apiClient.post('/assets/assets/', data);
export const updateAsset = (id, data) => apiClient.put(`/assets/assets/${id}/`, data);
export const getCategories = () => apiClient.get('/assets/categories/');
export const getFormats = () => apiClient.get('/assets/formats/');
export const getTags = () => apiClient.get('/assets/tags/');
export const searchAssets = (params) => apiClient.get('/assets/search/', { params });

// Asset Versioning & Permissions
export const getAllVersions = (params) => apiClient.get('/assets/versions/', { params });
export const addAssetVersion = (assetId, data) => apiClient.post(`/assets/assets/${assetId}/versions/`, data);
export const rollbackVersion = (assetId, versionId) => apiClient.post(`/assets/assets/${assetId}/rollback/${versionId}/`);
export const grantAssetPermission = (assetId, data) => apiClient.post(`/assets/assets/${assetId}/permissions/`, data);
export const addAssetMetadata = (assetId, data) => apiClient.post(`/assets/assets/${assetId}/metadata/`, data);

// Rights & Royalties
export const getRightsHolders = () => apiClient.get('/rights/holders/');
export const getContracts = (params) => apiClient.get('/rights/contracts/', { params });
export const createContract = (data) => apiClient.post('/rights/contracts/', data);
export const getSalesTransactions = (params) => apiClient.get('/rights/sales/', { params });
export const getSalesSummary = () => apiClient.get('/rights/sales/summary/');
export const getRoyaltyCalculations = (params) => apiClient.get('/rights/calculations/', { params });
export const runRoyaltyCalculation = (data) => apiClient.post('/rights/calculations/run-calculation/', data);
export const getRoyaltyPayouts = () => apiClient.get('/rights/payouts/');
export const createRoyaltyPayout = (data) => apiClient.post('/rights/payouts/', data);

// Streaming & DRM
export const getDrmPolicies = () => apiClient.get('/streaming/policies/');
export const startStreamingSession = (data) => apiClient.post('/streaming/start-session/', data);
export const verifyDrmToken = (token) => apiClient.post('/streaming/verify-drm/', { token });
export const getStreamingSessions = (params) => apiClient.get('/streaming/sessions/', { params });

// Subscriptions & Billing
export const getSubscriptionPlans = () => apiClient.get('/subscriptions/plans/');
export const getUserSubscriptions = (params) => apiClient.get('/subscriptions/user-subscriptions/', { params });
export const subscribeToPlan = (data) => apiClient.post('/subscriptions/subscribe/', data);
export const getBillingInvoices = (params) => apiClient.get('/subscriptions/invoices/', { params });

// Analytics & Recommendations
export const getDashboardAnalytics = () => apiClient.get('/analytics/dashboard/');
export const getWatchHistory = (params) => apiClient.get('/analytics/watch-history/', { params });
export const updateWatchProgress = (data) => apiClient.post('/analytics/watch-history/update-progress/', data);
export const getRatings = (params) => apiClient.get('/analytics/ratings/', { params });
export const submitRating = (data) => apiClient.post('/analytics/ratings/', data);
export const getRecommendations = (params) => apiClient.get('/analytics/recommendations/', { params });
export const generateRecommendations = (userId) => apiClient.post('/analytics/recommendations/generate-for-user/', { user_id: userId });
