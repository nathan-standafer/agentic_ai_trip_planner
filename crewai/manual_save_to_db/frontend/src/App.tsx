import { useState, useCallback, useEffect } from 'react';
import { TripForm } from './components/TripForm';
import { ProgressDisplay } from './components/ProgressDisplay';
import { ResultsDisplay } from './components/ResultsDisplay';
import { useSSE } from './hooks/useSSE';
import { startTripPlanning, getTripResult } from './services/api';
import type { TripFormData, ScheduledActivity } from './types/trip';
import './styles/index.css';

type AppState = 'form' | 'planning' | 'results';

export default function App() {
  const [state, setState] = useState<AppState>('form');
  const [tripId, setTripId] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [schedule, setSchedule] = useState<ScheduledActivity[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { events, isConnected, isComplete, error: sseError, reset: resetSSE } = useSSE(tripId);

  // Handle form submission
  const handleSubmit = useCallback(async (data: TripFormData) => {
    try {
      setError(null);
      setIsSubmitting(true);
      const response = await startTripPlanning(data);
      setTripId(response.trip_id);
      setState('planning');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start planning');
    } finally {
      setIsSubmitting(false);
    }
  }, []);

  // Fetch results when SSE completes
  const fetchResults = useCallback(async () => {
    if (!tripId) return;

    try {
      const resultData = await getTripResult(tripId);
      setResult(resultData.result || null);
      setSchedule(resultData.schedule || []);
      setState('results');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get results');
      setState('results');
    }
  }, [tripId]);

  // Check if planning complete
  useEffect(() => {
    if (state === 'planning' && isComplete) {
      fetchResults();
    }
  }, [state, isComplete, fetchResults]);

  // Handle SSE error
  useEffect(() => {
    if (sseError && state === 'planning') {
      // Wait a bit then try to fetch results anyway
      const timeout = setTimeout(fetchResults, 2000);
      return () => clearTimeout(timeout);
    }
  }, [sseError, state, fetchResults]);

  // Start new plan
  const handleNewPlan = useCallback(() => {
    setTripId(null);
    setResult(null);
    setSchedule([]);
    setError(null);
    resetSSE();
    setState('form');
  }, [resetSSE]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Vacation Planner</h1>
        <p className="tagline">Powered by CrewAI Agents</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={() => setError(null)} className="dismiss-btn">
              Dismiss
            </button>
          </div>
        )}

        {sseError && state === 'planning' && (
          <div className="warning-banner">
            Connection issue: {sseError}. Attempting to retrieve results...
          </div>
        )}

        {state === 'form' && (
          <TripForm onSubmit={handleSubmit} isLoading={isSubmitting} />
        )}

        {state === 'planning' && (
          <ProgressDisplay events={events} isConnected={isConnected} />
        )}

        {state === 'results' && (
          <ResultsDisplay
            result={result}
            schedule={schedule}
            onNewPlan={handleNewPlan}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Built with CrewAI, FastAPI, and React</p>
      </footer>
    </div>
  );
}
