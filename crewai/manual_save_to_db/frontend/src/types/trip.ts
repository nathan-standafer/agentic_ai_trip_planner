export interface TripFormData {
  arrivalDate: string;        // Required, YYYY-MM-DD
  departureDate: string;      // Optional
  destinations: string;       // Required
  desiredActivities: string;  // Optional
  otherConsiderations: string; // Optional
  foodConsiderations: string;  // Optional
}

export interface ProgressEvent {
  event_type: 'start' | 'task_start' | 'task_complete' | 'step' | 'complete' | 'error';
  task_name?: string;
  agent_name?: string;
  message: string;
  progress_percent: number;
  timestamp: string;
  trip_id: string;
}

export interface ScheduledActivity {
  date: string;
  time_slot: string;
  activity_name: string;
  activity_description: string;
  location: string;
  duration: string;
  transportation?: string;
  notes?: string;
}

export interface TripResult {
  trip_id: string;
  status: 'pending' | 'completed' | 'error';
  result?: string;
  schedule?: ScheduledActivity[];
  error_message?: string;
}

export interface FormErrors {
  arrivalDate?: string;
  departureDate?: string;
  destinations?: string;
}
