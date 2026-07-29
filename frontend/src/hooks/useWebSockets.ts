import { useEffect, useRef, useState } from "react";

export function useWebSockets(url: string) {
  const [messages, setMessages] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!url) return;

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };
    ws.onclose = () => setIsConnected(false);

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = (msg: any) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(msg));
    }
  };

  return { messages, isConnected, sendMessage };
}
