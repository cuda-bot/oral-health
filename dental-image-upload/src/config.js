// Configuration for API endpoints
const config = {
    // Use environment variable for API URL, fallback to localhost for development
    API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8080',
};

export default config; 