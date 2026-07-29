export interface DatabaseConnection {
  id: string;
  user_id: string;
  name: string;
  db_type: 'postgresql' | 'mysql' | 'sqlserver' | 'oracle' | 'sqlite' | 'snowflake' | 'bigquery';
  host?: string;
  port?: number;
  db_name?: string;
  username?: string;
  ssl_enabled: boolean;
  cloud_url?: string;
  status: 'connected' | 'syncing' | 'failed';
  last_sync_time?: string;
  created_at: string;
}

export interface DatabaseMetadata {
  schemas: number;
  tables: number;
  columns: number;
  relationships: number;
  views: number;
  owners: number;
  lineage: number;
}

export interface SyncStatus {
  status: 'connecting' | 'reading' | 'building' | 'uploading' | 'finished' | 'error';
  progress: number;
  message: string;
}
