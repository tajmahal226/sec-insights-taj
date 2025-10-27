# Deployment Guide

This guide covers deploying the SEC Insights application to production. The architecture uses:
- **Frontend**: Vercel (Next.js)
- **Backend**: Render.com (FastAPI)

## Prerequisites

Before deploying, ensure you have:
1. A Vercel account ([sign up here](https://vercel.com/signup))
2. A Render account ([sign up here](https://render.com/))
3. GitHub repository connected to both platforms
4. Required API keys (OpenAI, AWS, Polygon.io)

## Backend Deployment (Render.com)

The backend is already configured to deploy to Render using the `render.yaml` file in the repository root.

### Steps:

1. **Connect Your Repository**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Blueprint"
   - Connect your GitHub repository
   - Render will detect the `render.yaml` configuration

2. **Configure Environment Variables**

   Set the following environment variable groups in Render:

   **General Settings:**
   - `IS_PREVIEW_ENV`: `false` (production), `true` (preview)
   - `LOG_LEVEL`: `INFO` (production), `DEBUG` (preview)
   - `BACKEND_CORS_ORIGINS`: Include your Vercel frontend URL
   - `S3_BUCKET_NAME`: Your S3 bucket for storage
   - `S3_ASSET_BUCKET_NAME`: Your S3 bucket for assets
   - `CDN_BASE_URL`: Your CloudFront distribution URL
   - `SENTRY_DSN`: (optional) Your Sentry DSN

   **Production Secrets:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `AWS_KEY`: Your AWS access key
   - `AWS_SECRET`: Your AWS secret key
   - `POLYGON_IO_API_KEY`: Your Polygon.io API key

3. **Deploy**
   - Click "Apply" to create the services
   - Render will automatically build and deploy your backend
   - Note your backend URL (e.g., `https://your-app.onrender.com`)

## Frontend Deployment (Vercel)

The repository includes a `vercel.json` configuration file that automatically sets the root directory to `frontend` and configures the build settings. This ensures Vercel can properly detect the Next.js application.

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Import Your Repository**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository

2. **Configure Project Settings**

   The following settings are automatically configured via `vercel.json`, but you can verify them in the Vercel dashboard:
   - **Root Directory**: `frontend` (configured in vercel.json)
   - **Framework Preset**: Next.js (should auto-detect)
   - **Build Command**: `npm run build` (configured in vercel.json)
   - **Output Directory**: `.next` (configured in vercel.json)
   - **Install Command**: `npm install` (configured in vercel.json)

3. **Configure Environment Variables**

   Add the following environment variables in Vercel:

   | Variable | Value | Description |
   |----------|-------|-------------|
   | `NEXT_PUBLIC_BACKEND_URL` | `https://your-app.onrender.com` | Your Render backend URL. Used to proxy `/api/*` calls through Next.js so browser requests stay same-origin for SSE streams. |
   | `NODE_ENV` | `production` | Node environment |

   Optional (for Sentry):
   | Variable | Value | Description |
   |----------|-------|-------------|
   | `NEXT_PUBLIC_SENTRY_DSN` | Your Sentry DSN | Error tracking |

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - Your app will be available at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Root Directory**
   ```bash
   # Production deployment
   vercel --prod

   # Preview deployment
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add NEXT_PUBLIC_BACKEND_URL production
   # Enter your backend URL when prompted
   ```

## Post-Deployment Configuration

### 1. Update CORS Settings

After deploying the frontend, update your backend's `BACKEND_CORS_ORIGINS` environment variable in Render to include your Vercel URL:

```json
["https://your-project.vercel.app", "https://your-custom-domain.com"]
```

### 2. Configure Custom Domain (Optional)

#### Vercel:
1. Go to your project settings → "Domains"
2. Add your custom domain
3. Follow Vercel's DNS configuration instructions

#### Render:
1. Go to your service settings → "Custom Domain"
2. Add your custom domain
3. Update DNS records as instructed

### 3. Configure Preview Deployments

Both Vercel and Render support automatic preview deployments:

- **Vercel**: Automatically creates preview deployments for each pull request
- **Render**: Configure preview environments using the `render.yaml` settings

## Environment Variables Reference

### Frontend (Vercel)

Required:
- `NEXT_PUBLIC_BACKEND_URL`: Backend API URL (e.g., `https://your-app.onrender.com`)

Optional:
- `NEXT_PUBLIC_SENTRY_DSN`: Sentry error tracking
- `CODESPACES`: GitHub Codespaces flag (auto-set)
- `CODESPACE_NAME`: Codespace name (auto-set)

### Backend (Render)

See `render.yaml` for complete configuration. Key variables:
- `DATABASE_URL`: PostgreSQL connection string (auto-set from Render database)
- `OPENAI_API_KEY`: OpenAI API key
- `AWS_KEY` / `AWS_SECRET`: AWS credentials for S3
- `POLYGON_IO_API_KEY`: Polygon.io API key
- `S3_BUCKET_NAME`: S3 bucket for LlamaIndex storage
- `S3_ASSET_BUCKET_NAME`: S3 bucket for document PDFs
- `CDN_BASE_URL`: CloudFront distribution URL

## Continuous Deployment

Both platforms support automatic deployments:

1. **Production**: Deploys automatically when you push to `main` branch
2. **Preview**: Creates preview deployments for pull requests

To enable:
- Ensure your GitHub repository is connected to both Vercel and Render
- Configure branch protection rules as needed
- Merge pull requests to trigger production deployments

## Monitoring and Logging

### Vercel
- View deployment logs in the Vercel dashboard
- Real-time function logs available under "Functions" tab
- Analytics available in project settings

### Render
- View service logs in the Render dashboard
- Configure log drains for external logging services
- Monitor service health and performance metrics

### Sentry (Optional)
- Both frontend and backend are configured for Sentry
- Set `SENTRY_DSN` environment variables to enable
- View errors and performance metrics in Sentry dashboard

## Troubleshooting

### Build Failures

**Frontend (Vercel)**:
- Check that `NEXT_PUBLIC_BACKEND_URL` is set
- Verify Node.js version compatibility (check `package.json` engines)
- Review build logs in Vercel dashboard

**Backend (Render)**:
- Verify all required environment variables are set
- Check Docker build logs
- Ensure database is properly connected

### Runtime Errors

**CORS Issues**:
- Verify `BACKEND_CORS_ORIGINS` includes your frontend URL
- Check that the backend URL in frontend matches actual backend URL

**Database Connection**:
- Verify `DATABASE_URL` is set correctly
- Check database is running and accessible
- Review connection pool settings

**API Key Issues**:
- Verify all API keys are valid and have necessary permissions
- Check rate limits for external APIs (OpenAI, Polygon.io)

### Performance Issues

**Frontend**:
- Enable Vercel Analytics
- Review bundle size and optimize imports
- Use Vercel Edge Functions if needed

**Backend**:
- Monitor Render service metrics
- Adjust scaling settings in `render.yaml`
- Review database query performance

## Local Development

To test the production build locally:

### Frontend
```bash
cd frontend
npm install
npm run build
npm start
```

### Backend
```bash
cd backend
docker-compose up
```

Set environment variables in `.env.local` (frontend) or `.env` (backend) for local testing.

## Rollback Procedures

### Vercel
- Go to Deployments tab
- Find the last working deployment
- Click "..." → "Promote to Production"

### Render
- Go to service dashboard
- Click "Manual Deploy" → "Deploy Previous Version"
- Select the commit/version to deploy

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [SEC Insights GitHub](https://github.com/run-llama/sec-insights)

## Support

For issues specific to this project:
- Review the [FAQ](./FAQ.md)
- Check [GitHub Issues](https://github.com/run-llama/sec-insights/issues)
- Join the [Discord #sec-insights channel](https://discord.com/channels/1059199217496772688/1150942525968879636)

For platform-specific issues:
- [Vercel Support](https://vercel.com/support)
- [Render Support](https://render.com/docs/support)
