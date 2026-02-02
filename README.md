# Video API Proxy

A Python FastAPI proxy server that fetches and decrypts video data from deltastudy.site API endpoints.

## Features

- **Video Data Fetching**: Fetches encrypted video data from the original API
- **DRM Key Extraction**: Extracts KID from MPD URLs and retrieves DRM keys
- **AES-256-GCM Decryption**: Decrypts video data using the provided encryption key
- **Unified Endpoint**: Single endpoint to get complete video information including DRM keys
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Cross-origin resource sharing enabled
- **Production Ready**: Clean, optimized code with proper structure

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns server information and available endpoints.

**Response:**
```json
{
  "message": "Video API Proxy Server",
  "version": "1.0.0",
  "endpoints": {
    "/api/video": "GET - Fetch encrypted video data",
    "/api/kid": "POST - Extract KID from MPD URL", 
    "/api/otp": "GET - Get DRM key using KID",
    "/api/get-video-url": "GET - Unified endpoint for complete video info"
  }
}
```

### 2. Get Video Data
```
GET /api/video?batchId={batchId}&subjectId={subjectId}&childId={childId}
```
Fetches encrypted video data from the original API.

**Parameters:**
- `batchId` (string, required): Batch identifier
- `subjectId` (string, required): Subject identifier  
- `childId` (string, required): Video/content identifier

**Response:**
```json
{
  "data": "iv:encrypted_data_hex_string"
}
```

### 3. Extract KID
```
POST /api/kid
Content-Type: application/json

{
  "mpdUrl": "https://example.com/video.mpd"
}
```
Extracts KID (Key ID) from MPD URL for DRM decryption.

**Response:**
```json
{
  "kid": "0b078188e99a72fa65951d4721416d07",
  "success": true
}
```

### 4. Get DRM Key
```
GET /api/otp?kid={kid}
```
Retrieves DRM decryption key using KID.

**Parameters:**
- `kid` (string, required): Key identifier from MPD

**Response:**
```json
{
  "success": true,
  "keyid": "0b078188e99a72fa65951d4721416d07",
  "key": "0f3f172305754bf09546c045bfbe70aa"
}
```

### 5. Unified Video Info Endpoint ⭐
```
GET /api/get-video-url?batchId={batchId}&subjectId={subjectId}&childId={childId}
```
**Complete endpoint that handles the entire workflow:**
1. Fetches encrypted video data from `/api/video`
2. Decrypts the data using AES-256-GCM
3. Extracts KID from MPD URL via `/api/kid`
4. Gets DRM key via `/api/otp`
5. Returns complete video information ready for playback

**Response:**
```json
{
  "success": true,
  "data": {
    "url": "https://sec-prod-mediacdn.pw.live/fb130d20-2dcf-44ac-a706-733ac9bb709a/master.mpd",
    "signedUrl": "?URLPrefix=aHR0cHM6Ly9zZWMtcHJvZC1tZWRpYWNkbi5wdy5saXZlL2ZiMTMwZDIwLTJkY2YtNDRhYy1hNzA2LTczM2FjOWJiNzA5YQ&Expires=1770077881&KeyName=pw-prod-key&Signature=W2bJBex5Lin-dIO57GmAwUnJBF4eM_nYClve9YAtckKGODLvY1NhTKMvFyzNIAWiO6uUUAAFEdHAeLV4HomNDA",
    "urlType": "penpencilvdo",
    "scheduleInfo": {
      "startTime": "2026-01-22T03:30:00.000Z",
      "endTime": "2026-01-22T05:13:18.401Z"
    },
    "videoContainer": "DASH",
    "isCmaf": false,
    "serverTime": 1770063449601,
    "cdnType": "Gcp"
  },
  "stream_url": "https://sec-prod-mediacdn.pw.live/fb130d20-2dcf-44ac-a706-733ac9bb709a/master.mpd?URLPrefix=aHR0cHM6Ly9zZWMtcHJvZC1tZWRpYWNkbi5wdy5saXZlL2ZiMTMwZDIwLTJkY2YtNDRhYy1hNzA2LTczM2FjOWJiNzA5YQ&Expires=1770077881&KeyName=pw-prod-key&Signature=W2bJBex5Lin-dIO57GmAwUnJBF4eM_nYClve9YAtckKGODLvY1NhTKMvFyzNIAWiO6uUUAAFEdHAeLV4HomNDA",
  "url_type": "penpencilvdo",
  "drm": {
    "kid": "0b078188e99a72fa65951d4721416d07",
    "key": "0f3f172305754bf09546c045bfbe70aa"
  }
}
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to project directory:**
```bash
cd path/to/OpenData
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python -c "import fastapi, uvicorn, httpx, cryptography; print('All dependencies installed successfully')"
```

## Usage

### Quick Start

1. **Start the server:**
```bash
python app.py
```

2. **Server will start on:** `http://localhost:8000`

3. **Test the API:**
```bash
# Test root endpoint
curl http://localhost:8000/

# Test complete video info (recommended)
curl "http://localhost:8000/api/get-video-url?batchId=694e195974706955f00b8672&subjectId=694e914dc0e261270c605514&childId=6960d657ea1a12af73c5b05e"
```

### Example Usage

**Python Example:**
```python
import requests

# Get complete video information
params = {
    "batchId": "694e195974706955f00b8672",
    "subjectId": "694e914dc0e261270c605514", 
    "childId": "6960d657ea1a12af73c5b05e"
}

response = requests.get("http://localhost:8000/api/get-video-url", params=params)
data = response.json()

if data["success"]:
    print(f"Stream URL: {data['stream_url']}")
    print(f"DRM KID: {data['drm']['kid']}")
    print(f"DRM Key: {data['drm']['key']}")
```

**JavaScript Example:**
```javascript
const params = new URLSearchParams({
    batchId: "694e195974706955f00b8672",
    subjectId: "694e914dc0e261270c605514",
    childId: "6960d657ea1a12af73c5b05e"
});

fetch(`http://localhost:8000/api/get-video-url?${params}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Stream URL:", data.stream_url);
            console.log("DRM Info:", data.drm);
        }
    });
```

## Configuration

### Environment Variables
Currently, the encryption key is hardcoded as `"maggikhalo"` to match the JavaScript implementation. For production use, you can modify the `ENCRYPTION_KEY` constant in `app.py`.

### Server Configuration
- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8000` (default)
- **Timeout**: 30 seconds for HTTP requests

### Customization
To change server settings, modify the last line in `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **FastAPI** | `0.104.1` | Modern, fast web framework for building APIs |
| **Uvicorn** | `0.24.0` | ASGI server for running FastAPI applications |
| **httpx** | `0.25.2` | Async HTTP client for making requests to upstream APIs |
| **cryptography** | `>=41.0.0` | Cryptographic library for AES-GCM decryption |
| **python-multipart** | `0.0.6` | Support for form data parsing |

## Technical Details

### Decryption Process
The proxy implements AES-256-GCM decryption identical to the JavaScript implementation:

1. **Key Derivation**: Uses "maggikhalo" padded to 32 bytes
2. **IV Extraction**: First 12 bytes from the encrypted payload
3. **Tag Separation**: Last 16 bytes are the GCM authentication tag
4. **Decryption**: AES-256-GCM with derived key, IV, and tag

### Request Headers
The proxy mimics browser behavior with proper headers:
- User-Agent: Chrome Mobile
- Accept headers for media content
- Security headers (sec-ch-ua, etc.)
- CORS-compliant headers

## Security Notes

- **CORS**: Enabled for all origins (configure for production)
- **Logging**: All requests are logged for debugging
- **Error Handling**: Sensitive information is not exposed in error messages
- **Rate Limiting**: Consider implementing for production use
- **Authentication**: No authentication required (add as needed)

## Error Handling

The API includes comprehensive error handling for:

- **HTTP Errors**: Upstream API failures (4xx, 5xx)
- **Decryption Failures**: Invalid encrypted data or wrong keys
- **Missing Parameters**: Required query parameters not provided
- **Network Timeouts**: Connection issues with upstream APIs
- **Invalid Formats**: Malformed responses or data

**Error Response Format:**
```json
{
  "detail": "Descriptive error message"
}
```

## Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 8000

CMD ["python", "app.py"]
```

### Systemd Service
```ini
[Unit]
Description=Video API Proxy
After=network.target

[Service]
Type=simple
User=apiuser
WorkingDirectory=/path/to/OpenData
ExecStart=/usr/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   netstat -tulpn | grep :8000
   # Kill process or change port in app.py
   ```

2. **Decryption Failures**
   - Verify the encryption key matches the JavaScript implementation
   - Check if the encrypted data format is correct (iv:encrypted_data)

3. **Network Issues**
   - Ensure internet connectivity for upstream API calls
   - Check firewall settings for outbound connections

### Debug Mode
Enable debug logging by modifying the logging level in `app.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is provided as-is for educational and development purposes. Please respect the terms of service of the upstream APIs.
