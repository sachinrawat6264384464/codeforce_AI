import React from 'react';
import { useGetDatabaseMetadata, useSyncDatabase, useDeleteDatabase } from '../api/useDatabaseApi';
import { useSyncWebsocket } from '../hooks/useSyncWebsocket';
import { DatabaseConnection } from '@/types/database';
import { Layers, Table2, Columns, Link2, Users, Network, Trash2, RefreshCw, Loader2 } from 'lucide-react';

interface MetadataDashboardProps {
  database: DatabaseConnection;
  onDeleted: () => void;
}

export const MetadataDashboard: React.FC<MetadataDashboardProps> = ({ database, onDeleted }) => {
  // Pass dynamic project_id if available, using 'default' for prototype
  const syncStatus = useSyncWebsocket('default', database.id);
  const syncDb = useSyncDatabase();
  const deleteDb = useDeleteDatabase();
  
  const { data: metadata, isLoading, refetch } = useGetDatabaseMetadata(database.id);

  const handleSync = async () => {
    try {
      await syncDb.mutateAsync(database.id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (confirm("Are you sure you want to delete this connection?")) {
      await deleteDb.mutateAsync(database.id);
      onDeleted();
    }
  };

  const isSyncing = database.status === 'syncing' || Boolean(syncStatus && syncStatus.status !== 'finished' && syncStatus.status !== 'error');

  const stats = [
    { label: 'Schemas', value: metadata?.schemas || 0, icon: Layers, color: 'text-blue-400' },
    { label: 'Tables', value: metadata?.tables || 0, icon: Table2, color: 'text-indigo-400' },
    { label: 'Columns', value: metadata?.columns || 0, icon: Columns, color: 'text-emerald-400' },
    { label: 'Relationships', value: metadata?.relationships || 0, icon: Link2, color: 'text-purple-400' },
    { label: 'Owners', value: metadata?.owners || 0, icon: Users, color: 'text-orange-400' },
    { label: 'Lineage Hops', value: metadata?.lineage || 0, icon: Network, color: 'text-rose-400' },
  ];

  return (
    <div className="flex-1 overflow-y-auto bg-gray-950 p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex items-center justify-between bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{database.name}</h1>
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span className="capitalize px-2 py-1 bg-gray-800 rounded">{database.db_type}</span>
              <span>{database.host}:{database.port}</span>
              {database.last_sync_time && <span>Last sync: {new Date(database.last_sync_time).toLocaleString()}</span>}
            </div>
          </div>
          
          <div className="flex gap-3">
            <button 
              onClick={handleSync}
              disabled={isSyncing}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              {isSyncing ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
              {isSyncing ? 'Syncing...' : 'Sync to DataHub'}
            </button>
            <button 
              onClick={handleDelete}
              className="p-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg transition-colors"
              title="Delete Connection"
            >
              <Trash2 size={18} />
            </button>
          </div>
        </div>

        {/* Sync Progress */}
        {syncStatus && syncStatus.status !== 'finished' && syncStatus.status !== 'error' && (
          <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-indigo-400 font-medium capitalize">{syncStatus.status}...</span>
              <span className="text-gray-400">{syncStatus.progress}%</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2 mb-2 overflow-hidden">
              <div 
                className="bg-indigo-500 h-2 rounded-full transition-all duration-500 ease-out" 
                style={{ width: `${syncStatus.progress}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500">{syncStatus.message}</p>
          </div>
        )}

        {/* Stats Grid */}
        <div>
          <h2 className="text-xl font-semibold text-white mb-4">Metadata Summary</h2>
          {isLoading ? (
            <div className="flex justify-center p-12">
              <Loader2 size={32} className="animate-spin text-indigo-500" />
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {stats.map((stat, idx) => (
                <div key={idx} className="bg-gray-900 p-6 rounded-2xl border border-gray-800 hover:border-gray-700 transition-colors shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <stat.icon size={24} className={stat.color} />
                    <span className="text-3xl font-bold text-white">{stat.value}</span>
                  </div>
                  <p className="text-gray-400 text-sm font-medium">{stat.label}</p>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Placeholder for actual tables explorer */}
        <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl h-64 flex items-center justify-center text-gray-500">
          Table Explorer visualization goes here
        </div>
      </div>
    </div>
  );
};
