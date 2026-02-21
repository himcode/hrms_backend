# Vercel Deployment Guide

## Environment Variables Required

Set the following environment variables in your Vercel project settings:

### Database Configuration
- `PGDATABASE` - PostgreSQL database name (e.g., `neondb`)
- `PGHOST` - PostgreSQL host (e.g., `db.example.com`)
- `PGUSER` - PostgreSQL username
- `PGPASSWORD` - PostgreSQL password
- `PGPORT` - PostgreSQL port (default: `5432`)
- `PGSSLMODE` - SSL mode (default: `require`)

### Django Configuration
- `DJANGO_SECRET_KEY` - Django secret key (default: `strong_ethara_ai`, CHANGE THIS IN PRODUCTION)
- `DEBUG` - Debug mode (`true` or `false`, default: `false`)
- `CORS_ALLOW_ALL` - Allow all CORS origins (`true` or `false`, default: `false`)

## Deployment Steps

1. **Connect your repository**
   - Go to Vercel Dashboard
   - Click "New Project"
   - Import your repository

2. **Add Environment Variables**
   - Go to project Settings → Environment Variables
   - Add all required variables listed above
   - Make sure to use your actual database credentials

3. **Deploy**
   - Vercel will automatically detect the `build_files.sh` script
   - It will install dependencies and run migrations

4. **Monitor Logs**
   - Check Vercel logs for any environment variable issues
   - The logging system will report:
     - Whether environment variables were loaded
     - Database connection details
     - Any missing required variables
     - Migration status

## Logging Output

When the application starts, you'll see logs like:

```
Loading environment variables...
Environment variables loaded
BASE_DIR: /path/to/project
DEBUG mode: False
Database Engine: django.db.backends.postgresql
Database Name: neondb
Database Host: db.example.com
Database Port: 5432
Database User: postgres
Database Password: Set
Database SSL Mode: require
Django WSGI application initialized successfully
```

## Troubleshooting

### Missing Database Credentials
If you see warnings like "Database Password: NOT SET" or "PGHOST not set", check:
1. Environment variables are properly set in Vercel project settings
2. Variable names are exactly as specified above
3. No extra spaces or typos in variable names

### Connection Failures
- Verify database credentials are correct
- Ensure your database whitelist includes Vercel deployment regions
- Check database SSL certificate requirements

### Migrations Failed
- The build script will warn if migrations fail but won't stop deployment
- Check logs for specific migration errors
- May need to run migrations manually in Vercel CLI or after deployment

## Testing Deployed Application

```bash
# Test health endpoint
curl https://your-vercel-domain.vercel.app/api/health/

# Test employees API
curl https://your-vercel-domain.vercel.app/api/employees/

# Test attendance API
curl https://your-vercel-domain.vercel.app/api/attendance/
```
