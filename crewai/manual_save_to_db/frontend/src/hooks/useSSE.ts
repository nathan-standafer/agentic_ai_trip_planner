import { useState, useEffect, useCallback } from 'react';
import type { ProgressEvent } from '../types/trip';
import { getSSEUrl } from '../services/api';

export function useSSE(tripId: string | null) {
  const [events, setEvents] = useState<ProgressEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reconnectKey, setReconnectKey] = useState(0);

  useEffect(() => {
    if (!tripId) return;

    const eventSource = new EventSource(getSSEUrl(tripId));

    eventSource.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const data: ProgressEvent = JSON.parse(event.data);
        setEvents((prev) => [...prev, data]);

        if (data.event_type === 'complete') {
          setIsComplete(true);
          eventSource.close();
        }

        if (data.event_type === 'error') {
          setError(data.message);
          eventSource.close();
        }
      } catch (e) {
        console.error('Failed to parse SSE event:', e);
      }
    };

    eventSource.onerror = () => {
      setError('Connection lost');
      setIsConnected(false);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [tripId, reconnectKey]);

  const reset = useCallback(() => {
    setEvents([]);
    setIsConnected(false);
    setIsComplete(false);
    setError(null);
    // Increment reconnectKey to force useEffect to re-run and reconnect
    setReconnectKey((prev) => prev + 1);
  }, []);

  return { events, isConnected, isComplete, error, reset };
}
