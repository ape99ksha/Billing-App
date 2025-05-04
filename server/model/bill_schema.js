const mongoose = require('mongoose');

// Define product schema (for each product row in the bill)
const productSchema = new mongoose.Schema({
    product: String,
    category: String,
    discount: Number,
    quantity: Number,
    total: Number
});

// Define bill schema
const billSchema = new mongoose.Schema({
    customerName: { type: String, required: true },
    products: [productSchema],
    totalAmount: { type: Number, required: true },
    paymentMethod: { type: String, enum: ['Cash', 'Online'], required: true },
    date: { type: Date, default: Date.now }
});

// Create and export the model
module.exports = mongoose.model('Bill', billSchema);
