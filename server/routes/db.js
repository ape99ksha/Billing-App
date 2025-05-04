const express = require('express');
const router = express.Router();
const Bill = require('../model/bill_schema');

// Create a new bill
// POST: Create a new bill
router.post("/", async (req, res) => {
    try {
        const { customerName, products, totalAmount, paymentMethod } = req.body;

        // Validate required fields
        if (!customerName || !products || !totalAmount || !paymentMethod) {
            return res.status(400).json({ message: "Missing required fields" });
        }

        // Create new bill
        const newBill = new Bill({
            customerName,
            products,
            totalAmount,
            paymentMethod,
        });

        await newBill.save();
        res.status(201).json({ message: "Bill added successfully", bill: newBill });
    } catch (error) {
        res.status(500).json({ message: "Server Error", error: error.message });
    }
});

// GET: Fetch all bills
router.get("/", async (req, res) => {
    try {
        const { billId } = req.query;

        if (billId) {
            const bill = await Bill.findById(billId);
            if (!bill) {
                return res.status(404).json({ message: "Bill not found" });
            }
            return res.status(200).json({ message: "Bill found", bill });
        }

        // If no billId is provided, return all bills
        const bills = await Bill.find().sort({ createdAt: -1 });
        res.json(bills);
    } catch (error) {
        res.status(500).json({ message: "Server Error", error: error.message });
    }
});



module.exports = router;
