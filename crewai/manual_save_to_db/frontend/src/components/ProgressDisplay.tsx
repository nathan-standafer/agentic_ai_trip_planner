import type { ProgressEvent } from '../types/trip';

interface ProgressDisplayProps {
  events: ProgressEvent[];
  isConnected: boolean;
}

export function ProgressDisplay({ events, isConnected }: ProgressDisplayProps) {
  // Get the latest meaningful progress
  const completedTasks = events.filter(e => e.event_type === 'task_complete');
  const latestTask = completedTasks[completedTasks.length - 1];
  const progress = latestTask?.progress_percent ?? (events.length > 0 ? 5 : 0);

  // Get the last 3 status messages
  const recentEvents = events.slice(-3).reverse();
  const statusMessages = recentEvents.length > 0
    ? recentEvents.map(e => e.message)
    : ['Initializing...'];

  return (
    <div className="progress-display">
      <h2>Planning Your Vacation</h2>

      {/* Progress bar */}
      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{ width: `${Math.max(0, progress)}%` }}
        />
      </div>
      <div className="progress-text">
        {progress >= 0 ? `${progress}% Complete` : 'Working...'}
      </div>

      {/* Connection status */}
      <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
        <span className="status-dot"></span>
        {isConnected ? 'Connected to server' : 'Disconnected'}
      </div>

      {/* Current status - showing last 3 messages */}
      <div className="current-status">
        <strong>Status:</strong>
        <div className="status-messages">
          {statusMessages.map((msg, idx) => (
            <div key={idx} className={`status-line ${idx === 0 ? 'latest' : 'older'}`}>
              {msg}
            </div>
          ))}
        </div>
      </div>

      {/* Task progress checklist */}
      <div className="task-checklist">
        <h3>Progress</h3>
        <ul>
          <li className={progress >= 25 ? 'completed' : progress > 0 ? 'active' : ''}>
            <span className="check-icon">{progress >= 25 ? '✓' : progress > 0 ? '...' : '○'}</span>
            Researching activities
          </li>
          <li className={progress >= 50 ? 'completed' : progress >= 25 ? 'active' : ''}>
            <span className="check-icon">{progress >= 50 ? '✓' : progress >= 25 ? '...' : '○'}</span>
            Saving activities
          </li>
          <li className={progress >= 75 ? 'completed' : progress >= 50 ? 'active' : ''}>
            <span className="check-icon">{progress >= 75 ? '✓' : progress >= 50 ? '...' : '○'}</span>
            Creating daily schedule
          </li>
          <li className={progress >= 95 ? 'completed' : progress >= 75 ? 'active' : ''}>
            <span className="check-icon">{progress >= 95 ? '✓' : progress >= 75 ? '...' : '○'}</span>
            Generating report
          </li>
        </ul>
      </div>

      {/* Event log (collapsible) */}
      <details className="event-log">
        <summary>Activity Log ({events.length} events)</summary>
        <div className="event-list">
          {events.slice().reverse().map((event, index) => (
            <div key={index} className={`event-item event-${event.event_type}`}>
              <span className="event-time">
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
              <span className="event-type">[{event.event_type}]</span>
              <span className="event-message">
                {event.message.slice(0, 100)}
                {event.message.length > 100 ? '...' : ''}
              </span>
            </div>
          ))}
        </div>
      </details>
    </div>
  );
}
