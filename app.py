from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import base64
import json
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video API Proxy", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://deltastudy.site"
ENCRYPTION_KEY = "maggikhalo"

class VideoProxy:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        await self.client.aclose()

proxy = VideoProxy()

def hex_to_bytes(hex_string):
    """Convert hex string to bytes"""
    return bytes.fromhex(hex_string)

def derive_key(key_string):
    """Derive 256-bit key from string"""
    # Convert string to bytes and pad/truncate to 32 bytes
    key_bytes = key_string.encode('utf-8')
    if len(key_bytes) < 32:
        key_bytes += b'\x00' * (32 - len(key_bytes))
    elif len(key_bytes) > 32:
        key_bytes = key_bytes[:32]
    return key_bytes

async def decrypt_data(encrypted_data):
    """Decrypt AES-256-GCM encrypted data"""
    try:
        # Split the encrypted data (format: iv:encrypted_data)
        parts = encrypted_data.split(':')
        if len(parts) != 2:
            raise ValueError("Invalid encrypted payload format")
        
        iv_hex, encrypted_hex = parts
        
        # Convert hex to bytes
        iv = hex_to_bytes(iv_hex)
        encrypted_data = hex_to_bytes(encrypted_hex)
        
        # Derive the key using "maggikhalo"
        key = derive_key(ENCRYPTION_KEY)
        
        # For GCM, the last 16 bytes are the authentication tag
        if len(encrypted_data) < 16:
            raise ValueError("Encrypted data too short for GCM tag")
        
        ciphertext = encrypted_data[:-16]
        tag = encrypted_data[-16:]
        
        # Create cipher with tag
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt the data
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Parse JSON
        result = json.loads(decrypted_data.decode('utf-8'))
        return result
    
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        logger.error(f"Encrypted data length: {len(encrypted_data) if encrypted_data else 0}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"success": False, "error": f"Decryption failed: {str(e)}"}

@app.get("/api/video")
async def get_video_data(
    batchId: str = Query(...),
    subjectId: str = Query(...),
    childId: str = Query(...)
):
    """Fetch encrypted video data from the original API"""
    try:
        url = f"{BASE_URL}/api/video"
        params = {
            "batchId": batchId,
            "subjectId": subjectId,
            "childId": childId
        }
        
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36"
        }
        
        response = await proxy.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching video data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch video data: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching video data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/kid")
async def get_kid(mpdUrl: dict):
    """Extract KID from MPD URL"""
    try:
        url = f"{BASE_URL}/api/kid"
        
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36"
        }
        
        response = await proxy.client.post(url, json=mpdUrl, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching KID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch KID: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching KID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/otp")
async def get_drm_key(kid: str = Query(...)):
    """Get DRM key using KID"""
    try:
        url = f"{BASE_URL}/api/otp"
        params = {"kid": kid}
        
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36"
        }
        
        response = await proxy.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching DRM key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch DRM key: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching DRM key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/get-video-url")
async def get_complete_video_info(
    batchId: str = Query(...),
    subjectId: str = Query(...),
    childId: str = Query(...)
):
    """Unified endpoint to get complete video information including DRM keys"""
    try:
        # Step 1: Get encrypted video data
        logger.info(f"Fetching video data for batchId={batchId}, subjectId={subjectId}, childId={childId}")
        video_response = await get_video_data(batchId, subjectId, childId)
        
        if not video_response.get("data"):
            raise HTTPException(status_code=404, detail="No video data found")
        
        # Step 2: Decrypt the video data
        logger.info("Decrypting video data")
        decrypted_data = await decrypt_data(video_response["data"])
        
        # Check if decryption was successful
        if not decrypted_data.get("success") and not decrypted_data.get("data"):
            logger.error(f"Decryption failed: {decrypted_data}")
            raise HTTPException(status_code=500, detail="Failed to decrypt video data")
        
        # Extract video info from the nested structure
        video_info = decrypted_data.get("data", {})
        video_url = video_info.get("url")
        if not video_url:
            raise HTTPException(status_code=404, detail="No video URL found in decrypted data")
        
        # Construct full URL if signedUrl is provided
        full_url = video_url
        if video_info.get("signedUrl"):
            full_url = video_url + video_info["signedUrl"]
        
        # Step 3: Extract KID from MPD URL
        logger.info(f"Extracting KID from MPD URL: {full_url}")
        kid_response = await get_kid({"mpdUrl": full_url})
        
        if not kid_response.get("success"):
            raise HTTPException(status_code=500, detail="Failed to extract KID")
        
        kid = kid_response.get("kid")
        if not kid:
            raise HTTPException(status_code=404, detail="No KID found")
        
        # Step 4: Get DRM key using KID
        logger.info(f"Getting DRM key for KID: {kid}")
        drm_response = await get_drm_key(kid)
        
        if not drm_response.get("success"):
            raise HTTPException(status_code=500, detail="Failed to get DRM key")
        
        # Step 5: Construct complete response
        result = {
            "success": True,
            "data": {
                "url": video_url,
                "signedUrl": video_info.get("signedUrl", ""),
                "urlType": video_info.get("urlType", "penpencilvdo"),
                "scheduleInfo": video_info.get("scheduleInfo", {}),
                "videoContainer": video_info.get("videoContainer", "DASH"),
                "isCmaf": video_info.get("isCmaf", False),
                "serverTime": video_info.get("serverTime", 0),
                "cdnType": video_info.get("cdnType", "Gcp")
            },
            "stream_url": full_url,
            "url_type": video_info.get("urlType", "penpencilvdo"),
            "drm": {
                "kid": drm_response.get("keyid", kid),
                "key": drm_response.get("key", "")
            }
        }
        
        logger.info("Successfully retrieved complete video information")
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_complete_video_info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Video API Proxy Server",
        "version": "1.0.0",
        "endpoints": {
            "/api/video": "GET - Fetch encrypted video data",
            "/api/kid": "POST - Extract KID from MPD URL",
            "/api/otp": "GET - Get DRM key using KID",
            "/api/get-video-url": "GET - Unified endpoint for complete video info"
        }
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await proxy.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
