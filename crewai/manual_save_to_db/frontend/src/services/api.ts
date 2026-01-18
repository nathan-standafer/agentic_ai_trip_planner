import type { TripFormData, TripResult } from '../types/trip';

const API_BASE = import.meta.env.VITE_API_URL || '';

export async function startTripPlanning(data: TripFormData): Promise<{ trip_id: string }> {
  const response = await fetch(`${API_BASE}/api/trips/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      arrival_date: data.arrivalDate,
      departure_date: data.departureDate || null,
      destinations: data.destinations,
      desired_activities: data.desiredActivities || null,
      other_considerations: data.otherConsiderations || null,
      food_considerations: data.foodConsiderations || null,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to start planning');
  }

  return response.json();
}

export async function getTripResult(tripId: string): Promise<TripResult> {
  const response = await fetch(`${API_BASE}/api/trips/plan/${tripId}/result`);

  if (!response.ok) {
    throw new Error('Failed to get result');
  }

  return response.json();
}

export function getSSEUrl(tripId: string): string {
  return `${API_BASE}/api/trips/plan/${tripId}/stream`;
}

export async function updateTripPlan(tripId: string, suggestions: string): Promise<{ trip_id: string }> {
  const response = await fetch(`${API_BASE}/api/trips/plan/${tripId}/update`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ suggestions }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update plan');
  }

  return response.json();
}
