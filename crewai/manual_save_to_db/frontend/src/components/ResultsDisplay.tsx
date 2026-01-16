import ReactMarkdown from 'react-markdown';
import type { ScheduledActivity } from '../types/trip';

interface ResultsDisplayProps {
  result: string | null;
  schedule: ScheduledActivity[];
  onNewPlan: () => void;
}

export function ResultsDisplay({ result, schedule, onNewPlan }: ResultsDisplayProps) {
  // Group activities by date
  const scheduleByDate = schedule.reduce((acc, activity) => {
    if (!acc[activity.date]) {
      acc[activity.date] = [];
    }
    acc[activity.date].push(activity);
    return acc;
  }, {} as Record<string, ScheduledActivity[]>);

  // Sort dates
  const sortedDates = Object.keys(scheduleByDate).sort();

  // Extract summary sections from result markdown, removing daily schedule tables
  // Keeps intro (before daily schedules) and ending summary (costs, tips, etc.)
  const extractSummary = (markdown: string): string => {
    let introSection = '';
    let endingSection = '';

    // Find where the daily schedule starts (## Day 1, ## Day X, etc.)
    const dayPattern = /\n## Day \d+/i;
    const dayMatch = markdown.match(dayPattern);

    // Alternative: look for date-based headers like "## 2026-01-20"
    const dateHeaderPattern = /\n## \d{4}-\d{2}-\d{2}/;
    const dateMatch = markdown.match(dateHeaderPattern);

    const scheduleStartIndex = dayMatch?.index ?? dateMatch?.index;

    if (scheduleStartIndex !== undefined) {
      // Get intro section (before daily schedules)
      introSection = markdown.substring(0, scheduleStartIndex).trim();

      // Find where the daily schedule ends and ending summary begins
      // Look for headers that typically come after daily schedules
      const endingSectionPatterns = [
        /\n## (?:Trip |Estimated |Total |Budget|Cost|Expense|Summary|Highlight|Tip|Note|Important|Recommendation)/i,
        /\n## (?:Additional|Final|Closing|Overall)/i,
        /\n\*\*(?:Total|Estimated|Budget|Cost)/i,
      ];

      // Find all "## Day X" headers to determine where they end
      const allDayHeaders = [...markdown.matchAll(/\n## Day \d+[^\n]*/gi)];
      const allDateHeaders = [...markdown.matchAll(/\n## \d{4}-\d{2}-\d{2}[^\n]*/g)];
      const allScheduleHeaders = [...allDayHeaders, ...allDateHeaders];

      if (allScheduleHeaders.length > 0) {
        // Find the last schedule header
        let lastHeaderEnd = 0;
        for (const match of allScheduleHeaders) {
          if (match.index !== undefined) {
            const headerEnd = match.index + match[0].length;
            if (headerEnd > lastHeaderEnd) {
              lastHeaderEnd = headerEnd;
            }
          }
        }

        // Look for the next non-day header after the last day header
        const remainingContent = markdown.substring(lastHeaderEnd);
        const nextSectionMatch = remainingContent.match(/\n## (?!Day \d)/i);

        if (nextSectionMatch?.index !== undefined) {
          endingSection = remainingContent.substring(nextSectionMatch.index).trim();
        }
      }

      // Combine intro and ending sections
      if (endingSection) {
        return introSection + '\n\n---\n\n' + endingSection;
      }
      return introSection;
    }

    // If no daily schedule found, return the full content
    return markdown;
  };

  const summaryMarkdown = result ? extractSummary(result) : null;

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Your Vacation Plan</h2>
        <button onClick={onNewPlan} className="new-plan-btn">
          Plan Another Trip
        </button>
      </div>

      {/* Summary section from result markdown (daily schedule tables removed) */}
      {summaryMarkdown && (
        <div className="result-markdown">
          <ReactMarkdown>{summaryMarkdown}</ReactMarkdown>
        </div>
      )}

      {/* Structured schedule view */}
      {sortedDates.length > 0 && (
        <div className="schedule-view">
          <h3>Daily Schedule</h3>
          {sortedDates.map((date) => (
            <div key={date} className="day-schedule">
              <h4>
                {new Date(date + 'T12:00:00').toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </h4>
              <table>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Activity</th>
                    <th>Location</th>
                    <th>Duration</th>
                    <th>Transportation</th>
                  </tr>
                </thead>
                <tbody>
                  {scheduleByDate[date].map((activity, idx) => (
                    <tr key={idx}>
                      <td className="time-cell">{activity.time_slot}</td>
                      <td className="activity-cell">
                        <strong>{activity.activity_name}</strong>
                        <p className="activity-desc">{activity.activity_description}</p>
                        {activity.notes && (
                          <p className="activity-notes"><em>Note: {activity.notes}</em></p>
                        )}
                      </td>
                      <td>{activity.location}</td>
                      <td>{activity.duration}</td>
                      <td>{activity.transportation || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!summaryMarkdown && sortedDates.length === 0 && (
        <div className="empty-state">
          <p>No schedule data available. The planning may have encountered an issue.</p>
        </div>
      )}

      <div className="results-footer">
        <button onClick={onNewPlan} className="new-plan-btn">
          Plan Another Trip
        </button>
      </div>
    </div>
  );
}
