// src/services/streamService.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 30000,
});

// Export as object for consistency with overlayService
export const streamService = {
  start: async (rtsp_url, mode = 'auto', stream_id = null) => {
    const { data } = await API.post('/streams', { rtsp_url, mode, stream_id });
    return data; // { success, stream_id, hls_url, status, mode, pid }
  },

  getStatus: async (stream_id) => {
    const { data } = await API.get(`/streams/${stream_id}`);
    return data; // status object
  },

  list: async () => {
    const { data } = await API.get('/streams');
    return data; // { streams, count, max_concurrent }
  },

  stop: async (stream_id) => {
    const { data } = await API.delete(`/streams/${stream_id}`);
    return data; // { success, message }
  },

  restart: async (stream_id) => {
    const { data } = await API.post(`/streams/${stream_id}/restart`);
    return data;
  },

  getSamples: async () => {
    const { data } = await API.get('/sample-streams');
    return data; // { samples, count }
  }
};

// Keep backward compatibility - also export individual functions
export const createStream = streamService.start;
export const getStreamStatus = streamService.getStatus;
export const listStreams = streamService.list;
export const stopStream = streamService.stop;
export const restartStream = streamService.restart;
export const getSampleStreams = streamService.getSamples;

