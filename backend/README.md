# RTSP Livestream with Overlay Management

Full-stack application for playing RTSP livestreams with customizable overlays. Built with Flask, MongoDB, React, and FFmpeg.

## Features

- 🎥 RTSP to HLS livestream conversion
- 🎨 Drag-and-drop overlay editor (text & images)
- 💾 CRUD API for overlay management
- 🎮 Video playback controls (play, pause, volume)
- 📱 Responsive React frontend
- 🔄 Real-time overlay positioning with percentage-based coordinates

## Tech Stack

**Backend:**
- Python 3.8+ with Flask
- MongoDB (PyMongo)
- FFmpeg for RTSP-to-HLS conversion
- MediaMTX for RTSP server

**Frontend:**
- React 18+ with Vite
- TailwindCSS
- hls.js for HLS playback
- react-rnd for drag/resize overlays
- Axios for API calls

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **MongoDB**: [Download MongoDB](https://www.mongodb.com/try/download/community) or use MongoDB Atlas
- **FFmpeg**: [Download FFmpeg](https://ffmpeg.org/download.html) and add to PATH
- **MediaMTX**: [Download MediaMTX](https://github.com/bluenviron/mediamtx/releases/latest) for local RTSP server

## Installation & Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd rtsp-livestream-app
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

**Configure Environment:**

```bash
cp .env.example .env
```

Edit `.env` file with your settings (defaults work for local testing):

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
MONGO_URI=mongodb://localhost:27017/rtsp_overlay_app
DEFAULT_RTSP_URL=rtsp://localhost:8554/live
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Step 1: Start MongoDB

**Windows:**
```bash
# MongoDB typically runs as a service automatically
# Verify: Open Services and check "MongoDB Server"
```

**Mac:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

### Step 2: Setup RTSP Stream

**Option A: Using MediaMTX (Recommended for Local Testing)**

1. **Start MediaMTX Server:**
   ```bash
   # Double-click: backend/start_mediamtx.bat
   # OR manually:
   cd C:\mediamtx
   mediamtx.exe
   ```
   
   You should see:
   ```
   INF MediaMTX v1.9.3
   INF [RTSP] listener opened on :8554
   ```

2. **Stream Video to MediaMTX:**
   ```bash
   # Double-click: backend/stream_video.bat
   # OR manually (replace with your video path):
   C:\ffmpeg\bin\ffmpeg.exe -re -stream_loop -1 -i C:\Users\YourName\Desktop\sample.mp4 -c copy -f rtsp rtsp://localhost:8554/live
   ```
   
   Leave this running in the background.

**Option B: Using External RTSP Stream**

Update `.env` with external RTSP URL:
```env
DEFAULT_RTSP_URL=rtsp://rtsp.stream/pattern
```

### Step 3: Start Backend

```bash
cd backend
python app.py
```

Backend runs at: **http://localhost:5000**

You should see:
```
[DEBUG] HLS output directory: ...
Starting default RTSP stream: rtsp://localhost:8554/live
[SUCCESS] FFmpeg running with PID: ...
✓ Stream available at: http://localhost:5000/static/hls/stream1/stream.m3u8
```

### Step 4: Start Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

Frontend runs at: **http://localhost:5173**

### Step 5: Access Application

1. Open browser: `http://localhost:5173`
2. In the HLS URL input field, enter: `/static/hls/stream1/stream.m3u8`
3. Click **Load** button
4. Click **Play** button to start the video

## Using the App

### Playing Livestream

1. Enter RTSP/HLS URL in the input field
2. Click "Load" to initialize the stream
3. Use play/pause, volume controls for playback

### Managing Overlays

**Create Overlay:**
- Click "Add Text" for text overlays
- Click "Add Logo" for image overlays (provide image URL)

**Position & Resize:**
- Drag overlays to reposition
- Drag corner handles to resize
- Changes save automatically to database

**Edit Overlay:**
- Click "Select" on saved overlay
- Edit name, content, z-index in the panel
- Toggle visibility with Hide/Show

**Delete Overlay:**
- Click "Delete" on saved overlay

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "RTSP Overlay API"
}
```

#### List All Overlays
```
GET /api/overlays
```

**Response:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "name": "Welcome Text",
    "type": "text",
    "content": "Hello Viewers!",
    "xPercent": 10,
    "yPercent": 10,
    "widthPercent": 30,
    "heightPercent": 10,
    "zIndex": 5,
    "visible": true,
    "created_at": "2025-10-13T20:00:00Z"
  }
]
```

#### Create Overlay
```
POST /api/overlays
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Welcome Text",
  "type": "text",
  "content": "Hello Viewers!",
  "xPercent": 10,
  "yPercent": 10,
  "widthPercent": 30,
  "heightPercent": 10,
  "zIndex": 5,
  "visible": true
}
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "Welcome Text",
  "type": "text",
  "content": "Hello Viewers!",
  "xPercent": 10,
  "yPercent": 10,
  "widthPercent": 30,
  "heightPercent": 10,
  "zIndex": 5,
  "visible": true,
  "created_at": "2025-10-13T20:00:00Z"
}
```

#### Get Single Overlay
```
GET /api/overlays/{id}
```

**Response:** Same as create overlay response

#### Update Overlay
```
PUT /api/overlays/{id}
Content-Type: application/json
```

**Request Body:** (only include fields to update)
```json
{
  "xPercent": 20,
  "yPercent": 15,
  "visible": false
}
```

**Response:** Updated overlay object

#### Delete Overlay
```
DELETE /api/overlays/{id}
```

**Response:** `204 No Content`

### Example cURL Commands

**Create text overlay:**
```bash
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "name": "Channel Name",
    "content": "My Live Stream",
    "xPercent": 5,
    "yPercent": 5,
    "widthPercent": 25,
    "heightPercent": 8,
    "zIndex": 10,
    "visible": true
  }'
```

**Get all overlays:**
```bash
curl http://localhost:5000/api/overlays
```

**Update overlay:**
```bash
curl -X PUT http://localhost:5000/api/overlays/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated Text"}'
```

**Delete overlay:**
```bash
curl -X DELETE http://localhost:5000/api/overlays/507f1f77bcf86cd799439011
```

## Project Structure

```
rtsp-livestream-app/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   ├── .env.example              # Environment template
│   ├── start_mediamtx.bat        # Start RTSP server
│   ├── stream_video.bat          # Stream video to RTSP
│   ├── routes/
│   │   └── overlays.py           # Overlay CRUD endpoints
│   ├── models/
│   │   └── overlay.py            # Overlay data model
│   ├── scripts/
│   │   └── ffmpeg_wrapper.py     # FFmpeg RTSP-to-HLS converter
│   └── static/
│       └── hls/                  # HLS output directory
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main React component
│   │   └── index.css             # Tailwind styles
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   └── tailwind.config.js        # Tailwind configuration
└── README.md
```

## Troubleshooting

### Video Not Playing

**Issue:** Stream not loading or 404 error

**Solutions:**
1. Verify MediaMTX is running: Check for "MediaMTX Server" window
2. Verify FFmpeg is streaming: Check for FFmpeg process in Task Manager
3. Wait 10-15 seconds after starting backend for HLS segments to generate
4. Check backend console for errors
5. Verify HLS files exist: `backend/static/hls/stream1/` should contain `.m3u8` and `.ts` files

### CORS Errors

**Issue:** Frontend can't access backend API

**Solution:**
1. Check `CORS_ORIGINS` in `.env` includes your frontend URL
2. Restart Flask backend after changing `.env`

### MongoDB Connection Error

**Issue:** Backend fails to start with "Connection refused"

**Solutions:**
1. Verify MongoDB is running: 
   - Windows: Check Services for "MongoDB Server"
   - Mac: `brew services list`
   - Linux: `sudo systemctl status mongod`
2. Check `MONGO_URI` in `.env` is correct
3. For MongoDB Atlas, ensure IP is whitelisted

### FFmpeg Not Found

**Issue:** "ffmpeg not found" or "WinError 2"

**Solutions:**
1. Verify FFmpeg is installed: Run `ffmpeg -version` in terminal
2. Add FFmpeg to system PATH
3. Or update `FFMPEG_PATH` in `.env` with full path

### MediaMTX Connection Failed

**Issue:** "Connection refused" on rtsp://localhost:8554

**Solutions:**
1. Check MediaMTX is running
2. Verify port 8554 is not blocked by firewall
3. Restart MediaMTX server

## Production Deployment

### Backend

1. Use production WSGI server (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. Use production MongoDB (MongoDB Atlas)
3. Set `FLASK_DEBUG=False` in `.env`
4. Use environment variables for secrets
5. Setup reverse proxy (Nginx) for serving HLS files

### Frontend

```bash
cd frontend
npm run build
# Serve dist/ folder with Nginx or hosting platform
```

## License

MIT License

## Support

For issues or questions, please open an issue on the GitHub repository.

***

**Created as part of Full Stack Developer Assessment - October 2025**