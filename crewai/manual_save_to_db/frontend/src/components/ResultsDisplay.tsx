import { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import type { ScheduledActivity } from '../types/trip';

interface ResultsDisplayProps {
  result: string | null;
  schedule: ScheduledActivity[];
  onNewPlan: () => void;
  onUpdatePlan: (suggestions: string) => void;
  isUpdating?: boolean;
}

export function ResultsDisplay({ result, schedule, onNewPlan, onUpdatePlan, isUpdating = false }: ResultsDisplayProps) {
  const [suggestions, setSuggestions] = useState('');
  const [isExporting, setIsExporting] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  const handleSubmitUpdate = () => {
    if (suggestions.trim()) {
      onUpdatePlan(suggestions.trim());
      setSuggestions('');
    }
  };

  const handleExportPDF = async () => {
    if (!printRef.current) return;

    setIsExporting(true);
    try {
      const element = printRef.current;

      // Create canvas from the element
      const canvas = await html2canvas(element, {
        scale: 2, // Higher quality
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
      });

      const imgData = canvas.toDataURL('image/png');

      // Calculate dimensions
      const imgWidth = 210; // A4 width in mm
      const pageHeight = 297; // A4 height in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      const pdf = new jsPDF('p', 'mm', 'a4');
      let heightLeft = imgHeight;
      let position = 0;

      // Add first page
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      // Add more pages if needed
      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      // Generate filename with date
      const today = new Date().toISOString().split('T')[0];
      pdf.save(`vacation-plan-${today}.pdf`);
    } catch (error) {
      console.error('Failed to export PDF:', error);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  // Convert time slot string to 24-hour format for proper sorting
  // e.g., "08:00 AM" -> 800, "02:00 PM" -> 1400
  const parseTimeSlot = (timeSlot: string): number => {
    const match = timeSlot.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
    if (!match) return 0;

    let hours = parseInt(match[1], 10);
    const minutes = parseInt(match[2], 10);
    const isPM = match[3].toUpperCase() === 'PM';

    // Convert to 24-hour format
    if (isPM && hours !== 12) {
      hours += 12;
    } else if (!isPM && hours === 12) {
      hours = 0;
    }

    return hours * 100 + minutes;
  };

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

  // Extract different sections from the result markdown
  // Returns: { summary: string, dailyItinerary: string | null }
  const extractSections = (markdown: string): { summary: string; dailyItinerary: string | null } => {
    let introSection = '';
    let endingSection = '';
    let dailyItinerary: string | null = null;

    // Find the first "## Day X" header (the actual daily schedule content)
    const dayPattern = /\n## Day \d+/i;
    const dayMatch = markdown.match(dayPattern);

    // Alternative: look for date-based headers like "## 2026-01-20"
    const dateHeaderPattern = /\n## \d{4}-\d{2}-\d{2}/;
    const dateMatch = markdown.match(dateHeaderPattern);

    // Determine where the daily schedule content actually starts (first ## Day X)
    const scheduleStartIndex = dayMatch?.index ?? dateMatch?.index;

    if (scheduleStartIndex !== undefined) {
      // Get intro section (everything before the first ## Day X)
      // This includes "## Changes Made" and "## Updated Trip Itinerary" header
      introSection = markdown.substring(0, scheduleStartIndex).trim();

      // Find all "## Day X" headers to determine where they end
      const allDayHeaders = [...markdown.matchAll(/\n## Day \d+[^\n]*/gi)];
      const allDateHeaders = [...markdown.matchAll(/\n## \d{4}-\d{2}-\d{2}[^\n]*/g)];
      const allScheduleHeaders = [...allDayHeaders, ...allDateHeaders];

      if (allScheduleHeaders.length > 0) {
        // Find the last schedule header and estimate where its content ends
        let lastHeaderIndex = 0;
        for (const match of allScheduleHeaders) {
          if (match.index !== undefined && match.index > lastHeaderIndex) {
            lastHeaderIndex = match.index;
          }
        }

        // Look for summary sections that come after daily schedules
        // These patterns indicate the end of daily schedule content
        const summaryPatterns = [
          /\n## (?:Trip |Estimated |Total |Budget|Cost|Expense|Summary|Highlight|Tip|Note|Important|Recommendation|Additional|Final|Closing|Overall)/i,
          /\n\*\*(?:Trip Summary|Total|Estimated|Budget|Cost|Highlight)/i,
        ];

        let endingSectionStart: number | undefined;

        // Search for summary sections after the last day header
        const contentAfterLastDay = markdown.substring(lastHeaderIndex);
        for (const pattern of summaryPatterns) {
          const match = contentAfterLastDay.match(pattern);
          if (match?.index !== undefined) {
            const absoluteIndex = lastHeaderIndex + match.index;
            if (endingSectionStart === undefined || absoluteIndex < endingSectionStart) {
              endingSectionStart = absoluteIndex;
            }
          }
        }

        if (endingSectionStart !== undefined) {
          // Extract the daily itinerary (from first ## Day to before summary)
          dailyItinerary = markdown.substring(scheduleStartIndex, endingSectionStart).trim();
          endingSection = markdown.substring(endingSectionStart).trim();
        } else {
          // No ending section found, everything after scheduleStartIndex is daily itinerary
          dailyItinerary = markdown.substring(scheduleStartIndex).trim();
        }
      }

      // Clean up intro section - remove "## Updated Trip Itinerary" header if it's there
      // since it's just a wrapper and the actual content is in the daily schedule
      introSection = introSection.replace(/\n## Updated Trip Itinerary\s*$/i, '').trim();

      // Combine intro and ending sections for the summary
      const summary = endingSection
        ? introSection + '\n\n---\n\n' + endingSection
        : introSection;

      return { summary, dailyItinerary };
    }

    // If no daily schedule found, return the full content as summary
    return { summary: markdown, dailyItinerary: null };
  };

  const { summary: summaryMarkdown, dailyItinerary: rawDailyItinerary } = result
    ? extractSections(result)
    : { summary: null, dailyItinerary: null };

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Your Vacation Plan</h2>
        <div className="header-buttons">
          <button onClick={handleExportPDF} disabled={isExporting} className="export-btn">
            {isExporting ? 'Exporting...' : 'Export PDF'}
          </button>
          <button onClick={onNewPlan} className="new-plan-btn">
            Plan Another Trip
          </button>
        </div>
      </div>

      {/* Printable content area */}
      <div ref={printRef} className="printable-content">

      {/* Summary section from result markdown (daily schedule tables removed) */}
      {summaryMarkdown && (
        <div className="result-markdown">
          <ReactMarkdown>{summaryMarkdown}</ReactMarkdown>
        </div>
      )}

      {/* Collapsible raw markdown itinerary (hidden by default) */}
      {rawDailyItinerary && (
        <details className="raw-itinerary-details">
          <summary>View Raw Itinerary (Markdown)</summary>
          <div className="raw-itinerary-content">
            <ReactMarkdown>{rawDailyItinerary}</ReactMarkdown>
          </div>
        </details>
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
                  {scheduleByDate[date]
                    .slice()
                    .sort((a, b) => parseTimeSlot(a.time_slot) - parseTimeSlot(b.time_slot))
                    .map((activity, idx) => (
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

      </div>{/* End printable-content */}

      {/* Empty state */}
      {!summaryMarkdown && sortedDates.length === 0 && (
        <div className="empty-state">
          <p>No schedule data available. The planning may have encountered an issue.</p>
        </div>
      )}

      {/* Update suggestions section */}
      <div className="update-section">
        <h3>Update Your Plan</h3>
        <p className="update-hint">
          Want to make changes? Describe what you'd like to add, remove, or modify.
        </p>
        <textarea
          value={suggestions}
          onChange={(e) => setSuggestions(e.target.value)}
          placeholder="Examples:&#10;• Add a visit to the Tsukiji Fish Market on day 2&#10;• Replace the afternoon activity on Jan 18th with shopping in Shibuya&#10;• Remove the temple visit on the last day&#10;• Add more food-related activities"
          className="update-textarea"
          disabled={isUpdating}
          rows={4}
        />
        <button
          onClick={handleSubmitUpdate}
          disabled={!suggestions.trim() || isUpdating}
          className="update-btn"
        >
          {isUpdating ? 'Updating Plan...' : 'Update Plan'}
        </button>
      </div>

      <div className="results-footer">
        <button onClick={onNewPlan} className="new-plan-btn">
          Plan Another Trip
        </button>
      </div>
    </div>
  );
}
