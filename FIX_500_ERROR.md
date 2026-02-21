# Quick Diagnosis for Vercel 500 Error

## 🔴 You're getting a 500 error. Follow these steps:

### Step 1: Check the Debug Endpoint
```
https://your-vercel-domain.vercel.app/api/debug/
```

This will immediately tell you:
- ✓ Which environment variables are set
- ✗ Which are missing
- ⚠ Configuration warnings

### Step 2: Fix Based on Debug Output

**If you see "Missing environment variables":**
1. Go to Vercel Dashboard
2. Select your project → Settings → Environment Variables
3. Add the missing variables
4. Click "Save" and redeploy (git push or `vercel --prod`)

**If all variables show "Set":**
1. Check Vercel deployment logs
2. Look for specific error messages
3. See VERCEL_TROUBLESHOOTING.md for solutions

### Step 3: Check Vercel Logs
```bash
# View real-time logs
vercel logs https://your-domain.vercel.app --tail

# Or view in dashboard: 
# Project → Deployments → Click deployment → Runtime Logs
```

### Step 4: Test Health Endpoint
```bash
# In browser or curl:
https://your-vercel-domain.vercel.app/api/health/
```

Should return:
```json
{
  "status": "ok",
  "message": "HRMS Backend API is running",
  "environment": "vercel"
}
```

### Step 5: Verify All Required Variables

**MUST HAVE:**
- `PGDATABASE` ← Database name
- `PGHOST` ← Database host (with port removed!)
- `PGUSER` ← Database username
- `PGPASSWORD` ← Database password
- `PGSSLMODE` ← SSL mode (usually `require`)

**OPTIONAL:**
- `DEBUG` (default: false)
- `DJANGO_SECRET_KEY` (default: strong_ethara_ai, CHANGE THIS!)
- `CORS_ALLOW_ALL` (default: false)

### Step 6: Common Mistakes

❌ Database host includes port: `db.example.com:5432`
✅ Database host without port: `db.example.com`
(Port goes in `PGPORT`, not `PGHOST`)

❌ Too many/conflicting variables
✅ Only set what's needed, clear old ones

❌ Password with special characters not escaped
✅ Works as-is in Vercel env vars (no escaping needed)

### Step 7: Redeploy

After fixing:
```bash
git push  # Auto-deploys if connected to GitHub
# OR
vercel --prod
```

Monitor the deployment in Vercel dashboard until it's "Ready".

## Still Having Issues?

1. Check VERCEL_TROUBLESHOOTING.md for detailed solutions
2. Enable detailed logging by setting `DEBUG=true` (temporarily)
3. Check that migrations can run locally with same DB credentials
4. Verify requirements.txt doesn't have package conflicts
