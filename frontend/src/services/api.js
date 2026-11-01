/**
 * API service for HarvestSense backend communication
 */

const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch API health');
  return res.json();
}

export async function fetchCrops() {
  const res = await fetch(`${API_BASE}/crops`);
  if (!res.ok) throw new Error('Failed to fetch crops');
  return res.json();
}

export async function fetchCropDetail(cropId) {
  const res = await fetch(`${API_BASE}/crops/${cropId}`);
  if (!res.ok) throw new Error(`Failed to fetch crop detail for ${cropId}`);
  return res.json();
}

export async function fetchMarkets() {
  const res = await fetch(`${API_BASE}/markets`);
  if (!res.ok) throw new Error('Failed to fetch markets');
  return res.json();
}

export async function fetchVehicles() {
  const res = await fetch(`${API_BASE}/vehicles`);
  if (!res.ok) throw new Error('Failed to fetch vehicles');
  return res.json();
}

export async function fetchScenarios() {
  const res = await fetch(`${API_BASE}/scenarios`);
  if (!res.ok) throw new Error('Failed to fetch scenarios');
  return res.json();
}

export async function fetchFaostatSummary() {
  const res = await fetch(`${API_BASE}/faostat/summary`);
  if (!res.ok) throw new Error('Failed to fetch FAOSTAT summary');
  return res.json();
}

export async function runOptimization(payload) {
  const res = await fetch(`${API_BASE}/optimize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Optimization failed');
  }
  return res.json();
}

export async function runSimulation(payload) {
  const res = await fetch(`${API_BASE}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Simulation failed');
  }
  return res.json();
}

