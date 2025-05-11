// server.js
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors({ 
    origin: 'http://localhost:3000', // Allow only your React frontend
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // Allowed methods
    allowedHeaders: ['Content-Type'], // Allowed headers
    credentials: true // Allow cookies or authentication headers if needed
}));

app.use(express.json({ limit: '20mb' }));

// Ensure Uploads Directory Exists
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
    console.log('Uploads directory created.');
}

// Upload Endpoint
app.post('/upload', (req, res) => {
    const { image } = req.body;

    if (!image) {
        return res.status(400).json({ error: 'No image provided' });
    }

    const match = image.match(/^data:image\/(jpeg|png|jpg);base64,(.+)$/);
    if (!match) {
        return res.status(400).json({ error: 'Invalid image format' });
    }

    const fileExtension = match[1];
    const base64Data = match[2];
    const filePath = path.join(uploadDir, `image_${Date.now()}.${fileExtension}`);

    fs.writeFile(filePath, base64Data, 'base64', (err) => {
        if (err) {
            console.error('File Save Error:', err.message);
            return res.status(500).json({ error: 'Failed to save image' });
        }

        console.log('Image saved at:', filePath);
        res.status(200).json({ message: 'Image uploaded successfully', path: `http://localhost:5000/uploads/${path.basename(filePath)}` });
    });
});

// Serve Uploaded Images
app.use('/uploads', express.static(uploadDir));

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
