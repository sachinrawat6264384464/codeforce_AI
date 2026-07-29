'use client';

import React, { useState } from 'react';
import { DatabaseList } from '@/features/data-sources/components/DatabaseList';
import { ConnectionForm } from '@/features/data-sources/components/ConnectionForm';
import { MetadataDashboard } from '@/features/data-sources/components/MetadataDashboard';
import { useGetDatabases } from '@/features/data-sources/api/useDatabaseApi';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';

const queryClient = new QueryClient();

const DataSourcesContent = () => {
  const { data: databases, isLoading } = useGetDatabases();
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const selectedDatabase = databases?.find(db => db.id === selectedId);

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden text-gray-200">
      <DatabaseList 
        databases={databases || []} 
        selectedId={selectedId} 
        onSelect={setSelectedId} 
      />
      
      <main className="flex-1 flex flex-col relative">
        {isLoading ? (
          <div className="flex-1 flex items-center justify-center">
            <Loader2 size={32} className="animate-spin text-indigo-500" />
          </div>
        ) : selectedDatabase ? (
          <MetadataDashboard 
            database={selectedDatabase} 
            onDeleted={() => setSelectedId(null)} 
          />
        ) : (
          <div className="flex-1 flex items-center justify-center p-8 overflow-y-auto">
            <ConnectionForm />
          </div>
        )}
      </main>
    </div>
  );
};

export default function DataSourcesPage() {
  return (
    <QueryClientProvider client={queryClient}>
      <DataSourcesContent />
    </QueryClientProvider>
  );
}
