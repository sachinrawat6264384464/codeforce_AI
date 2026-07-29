import React from 'react';
import { Database, Plus, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { DatabaseConnection } from '@/types/database';

interface DatabaseListProps {
  databases: DatabaseConnection[];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}

export const DatabaseList: React.FC<DatabaseListProps> = ({ databases, selectedId, onSelect }) => {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-800 h-full flex flex-col">
      <div className="p-4 border-b border-gray-800 flex justify-between items-center">
        <h2 className="text-sm font-semibold text-gray-200">Data Sources</h2>
        <button 
          onClick={() => onSelect(null)}
          className="p-1 hover:bg-gray-800 rounded-md text-gray-400 hover:text-white transition-colors"
          title="New Connection"
        >
          <Plus size={16} />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {databases.length === 0 ? (
          <div className="p-4 text-xs text-gray-500 text-center">
            No databases connected yet.
          </div>
        ) : (
          <ul className="py-2">
            {databases.map((db) => (
              <li key={db.id}>
                <button
                  onClick={() => onSelect(db.id)}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-colors ${
                    selectedId === db.id ? 'bg-indigo-900/40 border-l-2 border-indigo-500' : 'hover:bg-gray-800 border-l-2 border-transparent'
                  }`}
                >
                  <Database size={16} className={selectedId === db.id ? 'text-indigo-400' : 'text-gray-500'} />
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm truncate ${selectedId === db.id ? 'text-indigo-100 font-medium' : 'text-gray-300'}`}>
                      {db.name}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">{db.db_type}</p>
                  </div>
                  {db.status === 'connected' && <CheckCircle size={14} className="text-emerald-500" />}
                  {db.status === 'syncing' && <RefreshCw size={14} className="text-blue-400 animate-spin" />}
                  {db.status === 'failed' && <XCircle size={14} className="text-red-500" />}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
