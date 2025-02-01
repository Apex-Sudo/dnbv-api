import { mockCheckAvailability } from './mock-api.js';

const isProduction = process.env.NODE_ENV === 'production';

export const api = {
    checkAvailability: async (checkIn, checkOut) => {
        if (isProduction) {
            const response = await fetch('/api/v1/availability', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ checkIn, checkOut })
            });
            return response.json();
        }
        return mockCheckAvailability(checkIn, checkOut);
    }
};
