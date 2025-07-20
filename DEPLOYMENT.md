# Vercel Deployment Guide

This guide will help you deploy your Oral Health AI app on Vercel.

## Prerequisites

1. **GitHub Account**: Make sure your code is pushed to a GitHub repository
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Node.js**: For local testing (optional)

## Deployment Steps

### Step 1: Deploy the Backend API

1. **Go to Vercel Dashboard**
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"

2. **Import Repository**
   - Connect your GitHub account if not already connected
   - Select your repository
   - Set the following configuration:
     - **Framework Preset**: Other
     - **Root Directory**: `api`
     - **Build Command**: Leave empty
     - **Output Directory**: Leave empty
     - **Install Command**: `pip install -r requirements.txt`

3. **Environment Variables** (Optional)
   - Add any environment variables if needed

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note down the API URL (e.g., `https://your-api.vercel.app`)

### Step 2: Deploy the Frontend

1. **Create Another Project**
   - Go back to Vercel Dashboard
   - Click "New Project" again
   - Select the same repository

2. **Configure Frontend**
   - **Framework Preset**: Create React App
   - **Root Directory**: `dental-image-upload`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

3. **Environment Variables**
   - Add the following environment variable:
     - **Name**: `REACT_APP_API_URL`
     - **Value**: Your API URL from Step 1 (e.g., `https://your-api.vercel.app`)

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete

### Step 3: Test Your Deployment

1. **Test the API**
   - Visit your API URL (e.g., `https://your-api.vercel.app`)
   - You should see: `{"status": "healthy", "message": "Oral Health AI API is running"}`

2. **Test the Frontend**
   - Visit your frontend URL
   - Try uploading an image to test the full functionality

## Troubleshooting

### Common Issues

1. **API Not Working**
   - Check if the model files are in the `api/models/` directory
   - Verify the API URL in your frontend environment variables
   - Check Vercel function logs for errors

2. **CORS Issues**
   - The API is configured to accept requests from any origin (`*`)
   - In production, you should restrict this to your frontend domain

3. **Model Loading Issues**
   - Ensure the model files are properly copied to the `api/models/` directory
   - Check the file paths in `app.py`

### Environment Variables

Make sure to set these in your Vercel project settings:

**Frontend:**
- `REACT_APP_API_URL`: Your API URL

**Backend:**
- No specific environment variables needed for basic functionality

## Production Considerations

1. **Security**
   - Restrict CORS origins to your frontend domain
   - Add authentication if needed
   - Consider rate limiting

2. **Performance**
   - The models are loaded on each function call (cold start)
   - Consider using a persistent server for better performance

3. **Storage**
   - Images are returned as base64 in the response
   - For production, consider using cloud storage (AWS S3, Cloudinary, etc.)

## Support

If you encounter issues:
1. Check Vercel function logs
2. Verify all files are in the correct directories
3. Test locally first using `npm start` and `python app.py` 