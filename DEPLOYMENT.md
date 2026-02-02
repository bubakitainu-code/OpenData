# Deployment Guide

## Vercel Deployment

### Quick Deployment

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
cd path/to/OpenData
vercel --prod
```

### Alternative: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository: `satyamrojhax/OpenData`
4. Vercel will auto-detect Python configuration
5. Click "Deploy"

### Environment Variables (Optional)

If you need to configure environment variables:

```bash
vercel env add ENCRYPTION_KEY production
vercel env add BASE_URL production
```

## Railway Deployment

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login and Deploy
```bash
railway login
railway init
railway up
```

### 3. Configure Environment
```bash
railway variables set ENCRYPTION_KEY=maggikhalo
railway variables set PORT=8000
```

## Render Deployment

### 1. Create `render.yaml`
```yaml
services:
  - type: web
    name: video-api-proxy
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ENCRYPTION_KEY
        value: maggikhalo
```

### 2. Deploy via Render Dashboard
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Select "Web Service"
4. Auto-deploy from main branch

## Docker Deployment

### 1. Build Docker Image
```bash
docker build -t video-api-proxy .
```

### 2. Run Container
```bash
docker run -p 8000:8000 video-api-proxy
```

### 3. Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENCRYPTION_KEY=maggikhalo
    restart: unless-stopped
```

## Heroku Deployment

### 1. Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Deploy
```bash
heroku create your-app-name
heroku buildpacks:set heroku/python
git push heroku main
```

### 3. Configure Environment
```bash
heroku config:set ENCRYPTION_KEY=maggikhalo
```

## Testing Deployment

### Test API Endpoints
```bash
# Test root endpoint
curl https://your-domain.vercel.app/

# Test video API
curl "https://your-domain.vercel.app/api/get-video-url?batchId=694e195974706955f00b8672&subjectId=694e914dc0e261270c605514&childId=6960d657ea1a12af73c5b05e"
```

### Monitor Logs
```bash
# Vercel
vercel logs

# Railway
railway logs

# Render
# Check dashboard logs
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Timeout Issues**
   - Increase timeout in HTTP client
   - Check serverless function limits

3. **CORS Issues**
   - Verify CORS middleware is properly configured
   - Check allowed origins

4. **Environment Variables**
   - Ensure all required env vars are set
   - Check variable names match exactly

### Performance Optimization

1. **Enable Caching**
   - Add response caching headers
   - Implement Redis for frequent requests

2. **Rate Limiting**
   - Add rate limiting middleware
   - Implement request quotas

3. **Monitoring**
   - Add health check endpoints
   - Implement error tracking

## Security Considerations

1. **API Keys**
   - Store sensitive keys in environment variables
   - Use secret management services

2. **Rate Limiting**
   - Implement per-IP rate limits
   - Add request validation

3. **HTTPS Only**
   - Force HTTPS in production
   - Use secure headers

## Scaling

### Horizontal Scaling
- Load balancer configuration
- Multiple server instances
- Database connection pooling

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching layers

## Monitoring

### Key Metrics
- Response times
- Error rates
- Request volume
- Resource usage

### Tools
- Vercel Analytics
- Railway Monitoring
- Render Metrics
- Custom monitoring solutions
