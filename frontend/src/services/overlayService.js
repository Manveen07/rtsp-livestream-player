// src/services/overlayService.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
});

export const overlayService = {
  // Get all overlays
  getAll: async () => {
    const { data } = await API.get('/overlays');
    return data;
  },

  // Get single overlay
  getById: async (id) => {
    const { data } = await API.get(`/overlays/${id}`);
    return data;
  },

  // Create overlay
  create: async (overlayData) => {
    const { data } = await API.post('/overlays', overlayData);
    return data;
  },

  // Update overlay
  update: async (id, overlayData) => {
    const { data } = await API.put(`/overlays/${id}`, overlayData);
    return data;
  },

  // Delete overlay
  delete: async (id) => {
    const { data } = await API.delete(`/overlays/${id}`);
    return data;
  },

  // Get overlays for specific stream
  getByStream: async (streamId) => {
    const { data } = await API.get(`/overlays/stream/${streamId}`);
    return data;
  }
};

