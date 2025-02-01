import { api } from '../utils/api-client.js';

class BookingWidget extends HTMLElement {
    constructor() {
        super();
        this.findVillaButton = document.querySelector('.Submit.Button');
        this.dateInput = document.querySelector('#date-range');

        this.errorDiv = document.createElement('div');
        this.errorDiv.className = 'dnbv-error';
        if (this.dateInput) {
            this.dateInput.parentNode.appendChild(this.errorDiv);
        }
    }

    connectedCallback() {
        if (this.findVillaButton) {
            this.findVillaButton.addEventListener('click', this.handleSubmit.bind(this));
        }
    }

    validateDates(dateRange) {
        if (!dateRange) throw new Error('Please select dates');
        const [checkIn, checkOut] = dateRange.split(' – ');
        if (!checkIn || !checkOut) throw new Error('Please select both check-in and check-out dates');

        const checkInDate = new Date(checkIn);
        const checkOutDate = new Date(checkOut);

        // Only validate max stay as minDate is handled by flatpickr
        if ((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24) > 30) {
            throw new Error('Maximum stay is 30 days');
        }

        return [checkIn, checkOut];
    }

    async handleSubmit(event) {
        event.preventDefault();
        this.errorDiv.textContent = '';

        try {
            const dateRange = this.dateInput.value;
            const [checkIn, checkOut] = this.validateDates(dateRange);

            this.findVillaButton.classList.add('loading');
            const result = await api.checkAvailability(checkIn, checkOut);

            sessionStorage.setItem('checkIn', checkIn);
            sessionStorage.setItem('checkOut', checkOut);

            if (result?.listings?.length) {
                sessionStorage.setItem('availableListings', JSON.stringify(result.listings));
                window.location.href = '/villas';
            } else {
                this.errorDiv.textContent = 'No properties available for these dates';
            }
        } catch (error) {
            this.errorDiv.textContent = error.message;
            console.error('Booking Error:', error);
        } finally {
            this.findVillaButton.classList.remove('loading');
        }
    }
}

customElements.define('dnbv-booking', BookingWidget);
