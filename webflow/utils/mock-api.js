export const mockCheckAvailability = async (checkIn, checkOut) => ({
    data: [
        {
            listingId: "villa_1",
            available: true,
            price: { amount: 450, currency: "USD" },
            image: "mock-villa1.jpg"
        },
        {
            listingId: "villa_2", 
            available: true,
            price: { amount: 650, currency: "USD" },
            image: "mock-villa2.jpg"
        }
    ]
});
