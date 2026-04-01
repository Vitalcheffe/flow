import { useState, useEffect, useCallback } from 'react';

interface Simulation {
  id: string;
  name: string;
  solver: string;
  status: string;
  created_at: string;
  duration_seconds: number | null;
  result_summary: Record<string, unknown>;
}

interface UseSimulationsResult {
  simulations: Simulation[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
  create: (data: { name: string; solver: string; description?: string }) => Promise<Simulation | null>;
  run: (id: string) => Promise<boolean>;
  remove: (id: string) => Promise<boolean>;
}

export function useSimulations(): UseSimulationsResult {
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSimulations = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/v1/simulations/');
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      setSimulations(data.simulations || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSimulations();
  }, [fetchSimulations]);

  const create = async (data: { name: string; solver: string; description?: string }) => {
    try {
      const res = await fetch('/api/v1/simulations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Failed to create');
      const sim = await res.json();
      setSimulations((prev) => [sim, ...prev]);
      return sim;
    } catch {
      return null;
    }
  };

  const run = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/simulations/${id}/run`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to run');
      const updated = await res.json();
      setSimulations((prev) => prev.map((s) => (s.id === id ? updated : s)));
      return true;
    } catch {
      return false;
    }
  };

  const remove = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/simulations/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete');
      setSimulations((prev) => prev.filter((s) => s.id !== id));
      return true;
    } catch {
      return false;
    }
  };

  return {
    simulations,
    loading,
    error,
    refetch: fetchSimulations,
    create,
    run,
    remove,
  };
}
