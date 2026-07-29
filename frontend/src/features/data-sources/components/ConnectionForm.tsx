import React, { useState } from 'react';
import { useTestConnection, useConnectDatabase } from '../api/useDatabaseApi';
import { DatabaseConnection } from '@/types/database';
import { Loader2 } from 'lucide-react';

export const ConnectionForm: React.FC = () => {
  const testConn = useTestConnection();
  const connectDb = useConnectDatabase();
  
  const [formData, setFormData] = useState<Partial<DatabaseConnection> & { password?: string }>({
    name: '',
    db_type: 'postgresql',
    host: 'localhost',
    port: 5432,
    db_name: '',
    username: '',
    password: '',
    ssl_enabled: false
  });

  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : (type === 'number' ? Number(value) : value)
    }));
  };

  const handleTest = async () => {
    setMessage(null);
    try {
      const res = await testConn.mutateAsync(formData);
      setMessage({ text: 'Connection successful!', type: 'success' });
    } catch (err: any) {
      setMessage({ text: err.response?.data?.detail || 'Connection failed', type: 'error' });
    }
  };

  const handleConnect = async () => {
    setMessage(null);
    try {
      await connectDb.mutateAsync(formData);
      setMessage({ text: 'Database connected and saved!', type: 'success' });
      // Reset form or handle state
    } catch (err: any) {
      setMessage({ text: err.response?.data?.detail || 'Failed to save connection', type: 'error' });
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-gray-900 rounded-xl border border-gray-800 shadow-2xl">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">Connect Database</h2>
        <p className="text-gray-400 text-sm">Add a new data source to sync metadata into DataHub for AI context.</p>
      </div>

      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-400 mb-1">Connection Name</label>
            <input name="name" value={formData.name} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" placeholder="e.g. Production DB" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-400 mb-1">Database Type</label>
            <select name="db_type" value={formData.db_type} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none">
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="sqlserver">SQL Server</option>
              <option value="sqlite">SQLite</option>
              <option value="snowflake">Snowflake</option>
              <option value="bigquery">BigQuery</option>
            </select>
          </div>
        </div>

        {formData.db_type !== 'sqlite' && (
          <div className="grid grid-cols-3 gap-4">
            <div className="col-span-2">
              <label className="block text-xs font-medium text-gray-400 mb-1">Host</label>
              <input name="host" value={formData.host} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Port</label>
              <input name="port" type="number" value={formData.port} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" />
            </div>
          </div>
        )}

        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1">Database Name</label>
          <input name="db_name" value={formData.db_name} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" placeholder={formData.db_type === 'sqlite' ? '/path/to/db.sqlite' : 'db_name'} />
        </div>

        {formData.db_type !== 'sqlite' && (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Username</label>
              <input name="username" value={formData.username} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1">Password</label>
              <input name="password" type="password" value={formData.password} onChange={handleChange} className="w-full bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-white text-sm focus:ring-1 focus:ring-indigo-500 outline-none" />
            </div>
          </div>
        )}

        <div className="flex items-center gap-2">
          <input type="checkbox" name="ssl_enabled" checked={formData.ssl_enabled} onChange={handleChange} id="ssl" className="rounded bg-gray-950 border-gray-800 text-indigo-500 focus:ring-indigo-500" />
          <label htmlFor="ssl" className="text-sm text-gray-400 cursor-pointer">Enable SSL/TLS</label>
        </div>

        {message && (
          <div className={`p-3 rounded-lg text-sm ${message.type === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
            {message.text}
          </div>
        )}

        <div className="flex items-center gap-4 pt-4 border-t border-gray-800">
          <button 
            onClick={handleTest}
            disabled={testConn.isPending || connectDb.isPending}
            className="px-4 py-2 text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors flex items-center gap-2"
          >
            {testConn.isPending && <Loader2 size={16} className="animate-spin" />}
            Test Connection
          </button>
          
          <button 
            onClick={handleConnect}
            disabled={testConn.isPending || connectDb.isPending || !formData.name}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            {connectDb.isPending && <Loader2 size={16} className="animate-spin" />}
            Connect & Save
          </button>
        </div>
      </div>
    </div>
  );
};
