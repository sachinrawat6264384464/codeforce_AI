import { useEffect, useState } from 'react';
import { SyncStatus } from '@/types/database';

export const useSyncWebsocket = (projectId: string, databaseId: string | null) => {
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);

  useEffect(() => {
    if (!databaseId) return;

    // Use a fixed project_id for hackathon demo or dynamic if provided
    const wsUrl = `ws://localhost:8000/api/v1/ws/projects/${projectId}/runs/sync_${databaseId}`;
    
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data: SyncStatus = JSON.parse(event.data);
        setSyncStatus(data);
      } catch (err) {
        console.error("Failed to parse websocket message", err);
      }
    };

    ws.onclose = () => {
      console.log(`WebSocket for sync_${databaseId} closed`);
    };

    return () => {
      ws.close();
    };
  }, [projectId, databaseId]);

  return syncStatus;
};
