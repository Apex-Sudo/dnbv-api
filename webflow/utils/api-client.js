class DnbvAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async checkAvailability(checkIn, checkOut) {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/availability`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ checkIn, checkOut })
            });
            if (!response.ok) throw new Error('Availability check failed');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
}

export const api = new DnbvAPI();
