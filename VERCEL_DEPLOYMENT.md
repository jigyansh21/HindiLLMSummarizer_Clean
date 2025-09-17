# Vercel Deployment Guide for MultiLanguage AI Text Summarizer

This guide will help you deploy the MultiLanguage AI Text Summarizer on Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Vercel CLI** (optional): Install with `npm i -g vercel`

## Files Created for Vercel Deployment

### 1. `vercel.json`
- Configuration file for Vercel deployment
- Specifies Python runtime and routing
- Sets environment variables and function timeout

### 2. `api/index.py`
- WSGI entry point for Vercel
- Imports and exports the FastAPI app

### 3. `requirements.txt` (Updated)
- Optimized dependencies for Vercel deployment
- Lighter versions of ML libraries to fit Vercel's constraints

### 4. `.vercelignore`
- Excludes unnecessary files from deployment
- Reduces deployment size and improves performance

## Deployment Steps

### Method 1: Using Vercel Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Project**:
   - Framework Preset: Other
   - Root Directory: `./` (root)
   - Build Command: Leave empty
   - Output Directory: Leave empty

3. **Environment Variables**:
   - Add `PYTORCH_JIT=0` in the Environment Variables section

4. **Deploy**:
   - Click "Deploy"
   - Wait for the build to complete

### Method 2: Using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set up project settings
   - Deploy

## Important Notes

### Vercel Limitations
- **Function Timeout**: 30 seconds (configurable in vercel.json)
- **Memory**: 1024MB maximum
- **File Size**: 50MB maximum for serverless functions
- **Cold Starts**: First request may be slower due to model loading

### Optimizations Made
1. **Lighter Dependencies**: Used smaller versions of ML libraries
2. **Excluded Files**: Font files and unnecessary assets excluded
3. **Environment Variables**: Set `PYTORCH_JIT=0` for better compatibility
4. **Function Timeout**: Set to 30 seconds for ML processing

### Potential Issues and Solutions

1. **Memory Issues**:
   - The app uses T5 model which can be memory-intensive
   - Consider using smaller models or extractive summarization only

2. **Cold Start Delays**:
   - First request may take 10-30 seconds to load the model
   - Subsequent requests will be faster

3. **File Upload Limits**:
   - PDF files are limited to 15 pages
   - Large files may cause timeout issues

## Testing the Deployment

After deployment, test these endpoints:

1. **Health Check**: `https://your-app.vercel.app/health`
2. **Language Selection**: `https://your-app.vercel.app/`
3. **API Documentation**: `https://your-app.vercel.app/docs`

## Monitoring and Debugging

1. **Vercel Dashboard**: Monitor function logs and performance
2. **Function Logs**: Check for errors in the Vercel dashboard
3. **Environment Variables**: Ensure all required variables are set

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS settings as instructed

## Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Check that all dependencies are in requirements.txt
   - Ensure Python path is correctly set in api/index.py

2. **Memory Errors**:
   - Reduce model size or use extractive summarization only
   - Check Vercel function logs for memory usage

3. **Timeout Errors**:
   - Increase function timeout in vercel.json
   - Optimize model loading

4. **Static File Issues**:
   - Ensure templates and static files are in correct directories
   - Check file paths in the FastAPI app

## Performance Tips

1. **Model Loading**: Consider lazy loading of ML models
2. **Caching**: Implement caching for frequently used summaries
3. **Error Handling**: Add comprehensive error handling for production
4. **Monitoring**: Set up monitoring for function performance

## Support

For issues specific to this deployment:
- Check Vercel function logs
- Verify all files are correctly configured
- Test locally first with `python main.py`

---

**Created by Jigyansh ECE Undergraduate, Thapar Institute of Engineering Technology, Patiala**
