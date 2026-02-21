# Vercel Deployment Troubleshooting

## 500 Internal Server Error - FUNCTION_INVOCATION_FAILED

When you see this error on Vercel, it usually means one of the following:

### 1. Check Debug Endpoint First
Access: `https://your-vercel-domain.vercel.app/api/debug/`

This will show you:
- All environment variables being read
- Which variables are missing
- Database configuration status

### 2. Common Issues and Solutions

#### Missing Environment Variables
**Symptoms:** Debug endpoint shows "Not set" values, warnings about missing credentials

**Solution:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add ALL required variables:
   - `PGDATABASE`
   - `PGHOST`  
   - `PGUSER`
   - `PGPASSWORD`
   - `PGPORT` (usually 5432)
   - `PGSSLMODE` (usually require)
   - `DJANGO_SECRET_KEY`
3. Redeploy your project

#### Database Connection Failed
**Symptoms:** Deployment succeeds but API returns 500 when accessing database-dependent endpoints

**Solution:**
1. Verify all database credentials are correct
2. Check that your database allows connections from Vercel
3. For Neon postgres, add Vercel IP to whitelist (or use connection pooling)
4. Test connection locally with same credentials

#### Django Import Errors
**Symptoms:** Error message about missing modules or import failures

**Solution:**
1. Check that all files in `employees/` and `attendance/` directories are present
2. Verify `__init__.py` files exist in all directories
3. Check `requirements.txt` has all dependencies
4. Run locally: `python manage.py runserver` to verify

### 3. Vercel Logs

To see detailed logs:

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Deployments"
   - Click on a deployment
   - Scroll down to "Runtime Logs" (for functions) or "Build Logs"

2. **Via CLI:**
```bash
vercel logs https://your-project.vercel.app --tail
```

### 4. Check Build Process

The `build_files.sh` script runs during deployment:
1. Installs dependencies from `requirements.txt`
2. Runs `collectstatic` (may fail safely)
3. Runs `migrate` (may fail if DB not available - that's OK)

If the build fails, check:
- All packages in `requirements.txt` are installable
- Python version is compatible (3.12)
- No syntax errors in Python files

### 5. Local Testing Before Deployment

```bash
# Test locally with same WSGI handler
export DJANGO_SETTINGS_MODULE=api.settings
python -c "from wsgi_handler import app; print('WSGI app loaded successfully')"

# Run the server
python manage.py runserver

# Test endpoints
curl http://127.0.0.1:8000/api/health/
curl http://127.0.0.1:8000/api/debug/
```

### 6. Verify Status

After fixing issues:
1. Redeploy: `vercel --prod` or push to main branch
2. Check Vercel dashboard for deployment status
3. Test endpoints:
   - `https://your-domain.vercel.app/api/health/` (should return 200)
   - `https://your-domain.vercel.app/api/debug/` (should show config)

### 7. Critical Checklist

- [ ] All environment variables set in Vercel project settings
- [ ] Database credentials are correct
- [ ] Database allows connections from Vercel
- [ ] `requirements.txt` contains all dependencies
- [ ] All app directories have `__init__.py` files
- [ ] No Python syntax errors (test locally)
- [ ] `wsgi_handler.py` exists and is correct
- [ ] `vercel.json` is properly configured

### 8. Request Error Responses

If you see errors in the response body:
- Read the error message carefully
- Check Vercel deployment logs
- The `/api/debug/` endpoint will show what's configured
- Look for "Missing environment variables" warnings

## Database Issues Specifically

**If database operations fail but API loads:**
- This is expected if database credentials aren't set up yet
- Non-database endpoints will still work
- Setup database and redeploy

**If database connection times out:**
- Check database firewall/whitelist settings
- Verify hostname is accessible from Vercel
- For Neon: might need connection pooling with PgBouncer
