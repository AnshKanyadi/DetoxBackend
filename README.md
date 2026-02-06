# Detox API Backend

Privacy-focused OCR service for sensitive information detection.

## 🔒 Security Guarantees

- **Images are NEVER stored** - processed in memory only
- **Images are NEVER logged** - only anonymous processing IDs
- **Immediate deletion** - data cleared right after OCR
- **Rate limiting** - prevents abuse
- **Security headers** - all responses include security headers
- **Open source** - verify the code yourself

## Quick Start (Local Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server runs at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/privacy` | GET | Privacy policy |
| `/analyze` | POST | Analyze image for sensitive info |

### POST /analyze

```json
// Request
{
  "image": "base64_encoded_image"
}

// Response
{
  "success": true,
  "detections": [
    {
      "text": "555-123-4567",
      "type": "PHONE",
      "confidence": 0.98,
      "bbox": { "x": 100, "y": 50, "width": 120, "height": 20 }
    }
  ],
  "scale": 3.81,
  "processing_id": "abc123"
}
```

## 🚀 Production Deployment

### Option 1: Railway (Recommended)

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Railway auto-detects Dockerfile
4. Deploy!

```bash
# Or use Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

### Option 2: Render

1. Create account at [render.com](https://render.com)
2. New → Web Service → Connect repo
3. Settings:
   - Runtime: Docker
   - Health Check Path: `/health`

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Option 4: Docker (Self-hosted)

```bash
# Build
docker build -t detox-api .

# Run
docker run -p 8000:8000 detox-api
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `RATE_LIMIT_REQUESTS` | 30 | Requests per window |
| `RATE_LIMIT_WINDOW` | 60 | Window in seconds |

## After Deployment

1. Get your deployed URL (e.g., `https://detox-api.up.railway.app`)
2. Update `background.js` in the extension:

```javascript
servers: {
  local: 'http://localhost:8000',
  hosted: 'https://YOUR-DEPLOYED-URL.com'  // ← Update this
}
```

3. Reload extension
4. Users can now choose "Hosted" mode!

## Privacy Compliance

This service is designed for privacy:

- ✅ GDPR compliant (no data storage)
- ✅ CCPA compliant (no data sale)
- ✅ Zero data retention
- ✅ No third-party sharing
- ✅ Transparent processing

## License

MIT
