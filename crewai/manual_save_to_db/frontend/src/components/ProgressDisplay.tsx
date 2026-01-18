import type { ProgressEvent } from '../types/trip';

interface ProgressDisplayProps {
  events: ProgressEvent[];
  isConnected: boolean;
}

// Parse and format raw agent messages into readable text
function formatStatusMessage(message: string): { type: string; text: string } | null {
  // Parse AgentAction messages
  const agentActionMatch = message.match(/AgentAction\(thought='([^']*)'(?:.*tool='([^']*)')?/);
  if (agentActionMatch) {
    const thought = agentActionMatch[1];
    const tool = agentActionMatch[2];
    // Extract the meaningful part of the thought (after "Thought: ")
    const cleanThought = thought.replace(/^Thought:\s*/i, '').trim();
    if (tool) {
      return { type: 'action', text: `🔍 Using ${tool}: ${cleanThought.slice(0, 150)}${cleanThought.length > 150 ? '...' : ''}` };
    }
    return { type: 'thinking', text: `💭 ${cleanThought.slice(0, 150)}${cleanThought.length > 150 ? '...' : ''}` };
  }

  // Parse ToolResult messages
  const toolResultMatch = message.match(/ToolResult\(result='(.{0,100})/);
  if (toolResultMatch) {
    // Check if it's a search result
    if (message.includes('searchParameters')) {
      const queryMatch = message.match(/'q':\s*'([^']+)'/);
      if (queryMatch) {
        return { type: 'result', text: `📋 Search completed: "${queryMatch[1]}"` };
      }
      return { type: 'result', text: '📋 Search results received' };
    }
    return { type: 'result', text: '📋 Tool result received' };
  }

  // Parse task completion messages
  if (message.toLowerCase().includes('task complete') || message.toLowerCase().includes('completed')) {
    return { type: 'complete', text: `✅ ${message.slice(0, 100)}` };
  }

  // Parse error messages
  if (message.toLowerCase().includes('error')) {
    return { type: 'error', text: `❌ ${message.slice(0, 150)}` };
  }

  // Default: clean up and return the message
  const cleanMessage = message.slice(0, 150) + (message.length > 150 ? '...' : '');
  return { type: 'info', text: cleanMessage };
}

export function ProgressDisplay({ events, isConnected }: ProgressDisplayProps) {
  // Get the latest meaningful progress
  const completedTasks = events.filter(e => e.event_type === 'task_complete');
  const latestTask = completedTasks[completedTasks.length - 1];
  const progress = latestTask?.progress_percent ?? (events.length > 0 ? 5 : 0);

  // Get the last 6 status messages and format them
  const recentEvents = events.slice(-6).reverse();
  const formattedStatuses = recentEvents.length > 0
    ? recentEvents.map(e => formatStatusMessage(e.message)).filter(Boolean) as { type: string; text: string }[]
    : [{ type: 'info', text: 'Initializing...' }];

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

      {/* Current status - showing last 6 formatted messages */}
      <div className="current-status">
        <strong>Agent Activity:</strong>
        <div className="status-messages">
          {formattedStatuses.map((status, idx) => (
            <div key={idx} className={`status-line status-${status.type} ${idx === 0 ? 'latest' : 'older'}`}>
              {status.text}
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
