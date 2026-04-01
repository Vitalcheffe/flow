/**
 * FLOW API Client
 */

const BASE_URL = '/api/v1';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // Health
  health: () => request<{ status: string; version: string }>('/health'),

  // Simulations
  listSimulations: (params?: { page?: number; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.page) query.set('page', String(params.page));
    if (params?.status) query.set('status', params.status);
    return request<any>(`/simulations/?${query}`);
  },

  getSimulation: (id: string) => request<any>(`/simulations/${id}`),

  createSimulation: (data: { name: string; solver: string; description?: string }) =>
    request<any>('/simulations/', { method: 'POST', body: JSON.stringify(data) }),

  updateSimulation: (id: string, data: Partial<{ name: string; description: string }>) =>
    request<any>(`/simulations/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),

  deleteSimulation: (id: string) =>
    request<void>(`/simulations/${id}`, { method: 'DELETE' }),

  uploadGeometry: async (id: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${BASE_URL}/simulations/${id}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  runSimulation: (id: string, overrides?: { solver?: string }) =>
    request<any>(`/simulations/${id}/run`, {
      method: 'POST',
      body: JSON.stringify({ solver_override: overrides?.solver }),
    }),

  cancelSimulation: (id: string) =>
    request<any>(`/simulations/${id}/cancel`, { method: 'POST' }),

  // Solvers
  listSolvers: () => request<any[]>('/solvers/'),
  getSolver: (type: string) => request<any>(`/solvers/${type}`),

  // Results
  getResults: (id: string) => request<any>(`/results/${id}`),
  getResultFields: (id: string) => request<any>(`/results/${id}/fields`),
};
