import { useState, FormEvent } from 'react';
import type { TripFormData, FormErrors } from '../types/trip';

interface TripFormProps {
  onSubmit: (data: TripFormData) => void;
  isLoading: boolean;
}

export function TripForm({ onSubmit, isLoading }: TripFormProps) {
  const [formData, setFormData] = useState<TripFormData>({
    arrivalDate: '',
    departureDate: '',
    destinations: '',
    desiredActivities: '',
    otherConsiderations: '',
    foodConsiderations: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.arrivalDate) {
      newErrors.arrivalDate = 'Arrival date is required';
    } else {
      const today = new Date().toISOString().split('T')[0];
      if (formData.arrivalDate < today) {
        newErrors.arrivalDate = 'Arrival date cannot be in the past';
      }
    }

    if (!formData.destinations.trim()) {
      newErrors.destinations = 'At least one destination is required';
    }

    if (formData.departureDate && formData.arrivalDate) {
      if (formData.departureDate <= formData.arrivalDate) {
        newErrors.departureDate = 'Departure must be after arrival';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: keyof TripFormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  // Get today's date for min attribute
  const today = new Date().toISOString().split('T')[0];

  return (
    <form onSubmit={handleSubmit} className="trip-form">
      <h2>Plan Your Vacation</h2>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="arrivalDate">Arrival Date *</label>
          <input
            type="date"
            id="arrivalDate"
            value={formData.arrivalDate}
            onChange={(e) => handleChange('arrivalDate', e.target.value)}
            min={today}
            required
          />
          {errors.arrivalDate && <span className="error">{errors.arrivalDate}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="departureDate">Departure Date</label>
          <input
            type="date"
            id="departureDate"
            value={formData.departureDate}
            onChange={(e) => handleChange('departureDate', e.target.value)}
            min={formData.arrivalDate || today}
          />
          {errors.departureDate && <span className="error">{errors.departureDate}</span>}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="destinations">Destination(s) *</label>
        <input
          type="text"
          id="destinations"
          value={formData.destinations}
          onChange={(e) => handleChange('destinations', e.target.value)}
          placeholder="e.g., Tokyo, Kyoto, Osaka"
          required
        />
        {errors.destinations && <span className="error">{errors.destinations}</span>}
        <small className="hint">Separate multiple destinations with commas</small>
      </div>

      <div className="form-group">
        <label htmlFor="desiredActivities">Desired Activities</label>
        <textarea
          id="desiredActivities"
          value={formData.desiredActivities}
          onChange={(e) => handleChange('desiredActivities', e.target.value)}
          placeholder="e.g., Visit temples; Try local food; Go shopping; See Mt. Fuji"
          rows={3}
        />
        <small className="hint">Separate activities with semicolons</small>
      </div>

      <div className="form-group">
        <label htmlFor="otherConsiderations">Other Considerations</label>
        <textarea
          id="otherConsiderations"
          value={formData.otherConsiderations}
          onChange={(e) => handleChange('otherConsiderations', e.target.value)}
          placeholder="e.g., Family of 3 with a teenager; Hotel already booked at Shinjuku; Interested in anime"
          rows={3}
        />
        <small className="hint">Include travel party details, constraints, or special interests</small>
      </div>

      <div className="form-group">
        <label htmlFor="foodConsiderations">Food Preferences</label>
        <textarea
          id="foodConsiderations"
          value={formData.foodConsiderations}
          onChange={(e) => handleChange('foodConsiderations', e.target.value)}
          placeholder="e.g., Vegetarian options; Local ramen shops; Themed cafes"
          rows={2}
        />
      </div>

      <button type="submit" disabled={isLoading} className="submit-btn">
        {isLoading ? 'Starting...' : 'Start Planning'}
      </button>
    </form>
  );
}
