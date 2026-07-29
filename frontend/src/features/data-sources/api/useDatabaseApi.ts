import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { DatabaseConnection, DatabaseMetadata } from '@/types/database';

// Assume a configured axios instance or base URL is available. For now, we use a basic one.
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
});

// Configure auth token interceptor if needed (assuming localStorage 'token' for prototype)
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const useGetDatabases = () => {
  return useQuery<DatabaseConnection[]>({
    queryKey: ['databases'],
    queryFn: async () => {
      const { data } = await api.get('/database/list');
      return data;
    },
  });
};

export const useGetDatabaseMetadata = (id: string | null) => {
  return useQuery<DatabaseMetadata>({
    queryKey: ['databases', id, 'metadata'],
    queryFn: async () => {
      if (!id) throw new Error("No ID provided");
      const { data } = await api.get(`/database/${id}/metadata`);
      return data;
    },
    enabled: !!id,
  });
};

export const useTestConnection = () => {
  return useMutation({
    mutationFn: async (dbConfig: Partial<DatabaseConnection> & { password?: string }) => {
      const { data } = await api.post('/database/test', dbConfig);
      return data;
    },
  });
};

export const useConnectDatabase = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (dbConfig: Partial<DatabaseConnection> & { password?: string }) => {
      const { data } = await api.post('/database/connect', dbConfig);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['databases'] });
    },
  });
};

export const useDeleteDatabase = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/database/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['databases'] });
    },
  });
};

export const useSyncDatabase = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await api.post(`/database/${id}/sync`);
      return data;
    },
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['databases', id] });
    },
  });
};
