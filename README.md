🎥 Live RTSP Player with Overlay ManagementA full-stack application for broadcasting RTSP video streams directly in the browser, complete with a real-time, drag-and-drop editor for adding custom text and image overlays. Built with a robust Flask and FFmpeg backend and a dynamic React frontend.✨ Tech Stack🚀 FeaturesSeamless Livestreaming: Ingests any RTSP stream and converts it to HLS for smooth, low-latency playback on the web.Dynamic Overlay Editor: A fully interactive, drag-and-drop interface to manage overlays directly on the video player.Text & Image Overlays: Add custom text labels or upload logos and images to brand your stream.Real-Time CRUD Operations: Create, read, update, and delete overlays on the fly. All changes are saved to a MongoDB database and reflected instantly.Persistent State: Overlay positions, sizes, and content are saved and reloaded automatically.Responsive UI: A clean and modern interface that works great on all screen sizes.Simple Controls: Includes standard video player controls like play, pause, and volume adjustment.📖 User Documentation: Getting StartedFollow these instructions to set up and run the application on your local machine.PrerequisitesEnsure you have the following software installed on your system:Python 3.8+: Download PythonNode.js 16+: Download Node.jsMongoDB: Download MongoDB Community Server or use a cloud service like MongoDB Atlas.FFmpeg: Download FFmpeg and ensure it's added to your system's PATH.1. Clone the Repositorygit clone [https://github.com/Manveen07/rtsp-livestream-player.git](https://github.com/Manveen07/rtsp-livestream-player.git)
cd rtsp-livestream-player
2. Backend SetupFirst, set up and run the Flask backend server.# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Create a .env file for custom configuration
# cp .env.example .env

# Run the backend server
python app.py
The backend will now be running at http://localhost:5000.3. Frontend SetupOpen a new terminal window and set up the React frontend.# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Run the frontend development server
npm run dev
The frontend will now be running at http://localhost:5173.4. Running the ApplicationStart MongoDB: Ensure your MongoDB server is running in the background.Open the App: Open your web browser and navigate to http://localhost:5173.Enter RTSP URL: In the input field, enter an RTSP stream URL. You can use a sample one for testing: rtsp://demo:demo@rtsp.stream/patternStart Stream: Click the "Start Stream" button. The video player will load and begin playing the HLS stream.How to Use the Overlay EditorAdd Overlays: Click the + Text or + Logo buttons to add new overlays to the video.Move & Resize: Click and drag an overlay to move it. Drag the handles on the corners and sides to resize it.Edit Properties: Select an overlay by clicking on it. The properties panel on the right will allow you to change its name, content (text or image URL), and stacking order (Z-index).Save Changes: All changes to position, size, and properties are saved automatically.Delete Overlays: Select an overlay and click the "Delete" button in the properties panel.📚 API DocumentationThe backend provides a RESTful API for managing streams and overlays.Base URL: http://localhost:5000Stream EndpointsStart a StreamEndpoint: POST /api/stream/startDescription: Starts the RTSP to HLS conversion process for a given URL.Request Body:{
  "rtsp_url": "rtsp://your-stream-url"
}
Success Response (200 OK):{
  "success": true,
  "stream_id": "stream_1665841337_abc123",
  "hls_url": "/static/hls/stream_1665841337_abc123/stream.m3u8"
}
Stop a StreamEndpoint: POST /api/stream/stopDescription: Stops the FFmpeg process for the currently active stream.Request Body:{
  "stream_id": "stream_1665841337_abc123"
}
Success Response (200 OK):{
  "success": true,
  "message": "Stream stopped successfully"
}
Overlay EndpointsGet All OverlaysEndpoint: GET /api/overlaysDescription: Retrieves a list of all saved overlays from the database.Success Response (200 OK):[
  {
    "_id": "6349d6f1a1b2c3d4e5f6a7b8",
    "name": "Main Logo",
    "type": "image",
    "content": "[https://via.placeholder.com/150](https://via.placeholder.com/150)",
    "xPercent": 75,
    "yPercent": 5,
    "widthPercent": 20,
    "heightPercent": 15,
    "zIndex": 10,
    "visible": true
  }
]
Create a New OverlayEndpoint: POST /api/overlaysDescription: Creates and saves a new overlay.Request Body:{
  "name": "Live Text",
  "type": "text",
  "content": "LIVE",
  "xPercent": 10,
  "yPercent": 10,
  "widthPercent": 15,
  "heightPercent": 8,
  "zIndex": 5,
  "visible": true
}
Success Response (201 Created): Returns the newly created overlay object with its _id.Update an OverlayEndpoint: PUT /api/overlays/<overlay_id>Description: Updates one or more properties of an existing overlay.Request Body: (Include only the fields you want to change){
  "content": "Stream Starting Soon",
  "xPercent": 12
}
Success Response (200 OK): Returns the complete, updated overlay object.Delete an OverlayEndpoint: DELETE /api/overlays/<overlay_id>Description: Deletes a saved overlay from the database.Success Response (200 OK):{
  "success": true,
  "message": "Overlay deleted"
}
