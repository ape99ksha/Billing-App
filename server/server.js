const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cors = require('cors');
const dbRoutes = require('./routes/db');

// Middleware
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.DATABASE, {
    dbName: 'BillingApp',
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => console.log('✅ MongoDB Connected'))
.catch((err) => {
    console.error('❌ MongoDB Error:', err);
    process.exit(1); // Exit if DB connection fails
});

// Test route
app.get('/', (req, res) => {
    res.send('🚀 Server is running!');
});

// API routes
app.use('/api', dbRoutes);

// Start server
const PORT = process.env.PORT || 6000;
app.listen(PORT, () => {
    console.log(`✅ Server is running on port ${PORT}`);
});
