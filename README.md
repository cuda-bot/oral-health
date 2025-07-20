# Oral Health AI - Image Analysis Application

A modern, responsive web application that uses AI to analyze dental images and detect potential oral health conditions. The application features a beautiful, user-friendly interface with drag-and-drop functionality and real-time analysis.

## 🚀 Features

- **AI-Powered Analysis**: Uses machine learning to detect oral health conditions
- **Modern UI/UX**: Beautiful, responsive design with gradient backgrounds and smooth animations
- **Drag & Drop**: Easy image upload with drag-and-drop functionality
- **Real-time Processing**: Instant analysis with loading indicators
- **Mobile Responsive**: Works perfectly on all devices
- **Multiple Formats**: Supports JPG, PNG, and GIF images
- **Professional Results**: Detailed analysis with confidence scores and recommendations

## 🏗️ Architecture

The application consists of two main components:

1. **Flask Backend** (`app.py`): Handles image processing and AI predictions
2. **React Frontend** (`dental-image-upload/`): Modern UI with drag-and-drop functionality

## 📁 Project Structure

```
oral-classification-app/
├── app.py                          # Flask backend server
├── models/                         # Trained ML models
│   ├── trained_dental_model.pkl
│   └── label_encoder.pkl
├── templates/                      # Flask HTML templates
│   ├── index.html                  # Modern upload page
│   └── result.html                 # Modern results page
├── static/                         # Static files and uploads
│   └── uploads/
├── dental-image-upload/            # React frontend
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── App.css                 # Modern styling
│   │   └── ImageUpload.js          # Upload component
│   └── public/
│       └── index.html              # React HTML template
└── requirements.txt                # Python dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm or yarn

### Backend Setup (Flask)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server:**
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:5000`

### Frontend Setup (React)

1. **Navigate to the React directory:**
   ```bash
   cd dental-image-upload
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The React app will start on `http://localhost:3000`

## 🎨 UI/UX Features

### Modern Design Elements
- **Gradient Backgrounds**: Beautiful purple-blue gradients
- **Card-based Layout**: Clean, organized content presentation
- **Smooth Animations**: Hover effects and loading animations
- **Professional Typography**: Inter font family for readability
- **Icon Integration**: Font Awesome icons throughout the interface

### User Experience
- **Drag & Drop Upload**: Intuitive file upload experience
- **Loading States**: Clear feedback during processing
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Accessibility**: Proper contrast ratios and keyboard navigation

### Results Display
- **Condition-specific Icons**: Visual indicators for different conditions
- **Confidence Bars**: Animated confidence scores
- **Detailed Descriptions**: Helpful explanations for each condition
- **Action Buttons**: Easy navigation and report printing

## 🔧 Technical Features

### Backend (Flask)
- **Image Processing**: Automatic resizing and optimization
- **ML Integration**: Pre-trained model for oral health classification
- **File Management**: Secure file upload and storage
- **Error Handling**: Robust error handling and validation

### Frontend (React)
- **State Management**: React hooks for component state
- **File Handling**: Advanced file upload with validation
- **API Integration**: Axios for backend communication
- **Responsive Design**: CSS Grid and Flexbox layouts

## 🎯 Supported Conditions

The AI model can detect various oral health conditions:

- **Healthy/Normal**: Good oral health
- **Dental Caries**: Tooth decay and cavities
- **Gingivitis**: Early-stage gum disease
- **Dental Calculus**: Hardened plaque (tartar)
- **Tooth Discoloration**: Staining and discoloration

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- **Desktop**: Full-featured experience with side-by-side layouts
- **Tablet**: Adapted layouts with touch-friendly interactions
- **Mobile**: Stacked layouts with optimized touch targets

## 🔒 Security & Privacy

- **File Validation**: Strict image file type checking
- **Size Limits**: Configurable file size restrictions
- **Secure Storage**: Proper file handling and cleanup
- **Data Protection**: No permanent storage of sensitive data

## 🚀 Deployment (Production)

### 1. Backend (ML API) on Railway

- Push all code (including `api/`, `models/`, `Procfile`, `requirements.txt`) to GitHub.
- Go to [railway.app](https://railway.app) and log in.
- Click **New Project** → **Deploy from GitHub repo**.
- Select your repo.
- Railway will auto-detect Python and use your `Procfile`:
  ```
  web: python api/app.py
  ```
- Wait for build and deployment to finish.
- **Copy your Railway public API URL** (e.g., `https://your-app-name.up.railway.app`).

### 2. Frontend (React) on Vercel

- Go to [vercel.com/dashboard](https://vercel.com/dashboard).
- Click **New Project** and import your GitHub repo.
- Set **Root Directory**: `dental-image-upload`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Add Environment Variable**:
  - **Key:** `REACT_APP_API_URL`
  - **Value:** Your Railway API URL (e.g., `https://your-app-name.up.railway.app`)
- Deploy!
- After deployment, open your Vercel frontend URL and test image upload.

### 3. Environment Variable Recap

- **Vercel (Frontend):**
  - `REACT_APP_API_URL` = Railway backend URL
- **Railway (Backend):**
  - No special variables needed unless you add secrets/config

### 4. Troubleshooting

- **Image upload fails/405 error:**  
  Make sure `REACT_APP_API_URL` is set in Vercel and points to your Railway backend.
- **Model not found:**  
  Ensure `models/` directory is inside `api/` and files are present in Railway.
- **CORS issues:**  
  Your backend uses Flask-CORS with `origins=['*']`. For production, restrict to your frontend domain.
- **Logs:**  
  Check Railway and Vercel dashboards for build/runtime logs.

---

**Congratulations! Your ML-powered web app is live and ready for users!**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Note**: This application is for educational and informational purposes only. It should not replace professional dental consultation. Always consult with qualified dental professionals for accurate diagnosis and treatment. # selforalexamination
