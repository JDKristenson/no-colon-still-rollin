# Deployment Guide

## Overview
No Colon, Still Rollin' is deployed using:
- **Local Development**: SQLite database (automatic setup)
- **Replit**: SQLite database (works with Replit's filesystem)
- **Vercel**: Requires external PostgreSQL database (Vercel has read-only filesystem)

## Local Development (Mac/Linux)

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt

   cd ../frontend
   npm install
   ```

2. **Start both servers:**
   ```bash
   ./start.sh
   ```
   - Backend runs on http://localhost:8000
   - Frontend runs on http://localhost:5173
   - Database auto-initializes on first run at `data/cancer_foods.db`

## Replit Deployment

1. **Import from GitHub:**
   - Go to Replit.com
   - Click "Create Repl" > "Import from GitHub"
   - Enter repository URL

2. **Configure .replit file:**
   ```toml
   run = "bash start.sh"

   [deployment]
   run = ["bash", "start.sh"]
   deploymentTarget = "cloudrun"
   ```

3. **Set environment variables:**
   - `NCBI_EMAIL`: Your email for PubMed API
   - `NCBI_API_KEY`: (optional) PubMed API key for higher rate limits

4. **Deploy:**
   - Click "Run" to test locally
   - Click "Deploy" for production
   - SQLite database persists in Replit's filesystem

## Vercel Deployment

⚠️ **Important**: Vercel has a read-only filesystem, so SQLite won't persist data. You need an external PostgreSQL database.

### Option 1: Vercel Postgres (Recommended)

1. **Create Vercel Postgres database:**
   ```bash
   vercel
   vercel postgres create no-colon-db
   ```

2. **Link to your project:**
   ```bash
   vercel env pull .env.local
   ```
   This creates `.env.local` with `POSTGRES_URL` automatically set.

3. **Set environment variables in Vercel dashboard:**
   - Go to your project settings
   - Add environment variable:
     - `DATABASE_URL`: (auto-set by Vercel Postgres)
     - `NCBI_EMAIL`: Your email
     - `NCBI_API_KEY`: (optional) Your PubMed API key

4. **Deploy:**
   ```bash
   vercel --prod
   ```

### Option 2: External PostgreSQL (Supabase, Railway, etc.)

1. **Create a PostgreSQL database** on your provider of choice:
   - [Supabase](https://supabase.com) - Free tier with 500MB
   - [Railway](https://railway.app) - Free tier with 512MB
   - [Neon](https://neon.tech) - Free tier with 3GB
   - [PlanetScale](https://planetscale.com) - MySQL alternative

2. **Get connection string** (format: `postgresql://user:password@host:port/database`)

3. **Set in Vercel environment variables:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `NCBI_EMAIL`: Your email
   - `NCBI_API_KEY`: (optional) Your PubMed API key

4. **Deploy:**
   ```bash
   vercel --prod
   ```

### Option 3: Demo Mode (No Persistence)

For testing only - database resets on each deployment:

1. **Deploy without DATABASE_URL:**
   ```bash
   vercel --prod
   ```

2. **Note:**
   - SQLite file is created but stored in `/tmp/`
   - All data is lost when the serverless function shuts down
   - Only useful for demos or development previews

## Database Migration (SQLite → PostgreSQL)

When moving from local SQLite to production PostgreSQL:

1. **Export data from SQLite:**
   ```bash
   sqlite3 data/cancer_foods.db .dump > backup.sql
   ```

2. **Connect to PostgreSQL:**
   ```bash
   psql $DATABASE_URL
   ```

3. **Run the schema creation** (happens automatically on first backend startup)

4. **Import data** (if needed):
   - Use a tool like `pgloader` or manually insert data
   - Or let the app re-seed on first startup

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Vercel | SQLite local file | PostgreSQL connection string for production |
| `DATABASE_PATH` | No | `data/cancer_foods.db` | SQLite file path (local/Replit only) |
| `NCBI_EMAIL` | Recommended | None | Email for NCBI/PubMed API (required for research features) |
| `NCBI_API_KEY` | No | None | NCBI API key for higher rate limits |
| `CORS_ORIGINS` | No | `http://localhost:5173` | Comma-separated list of allowed origins |
| `DEFAULT_USER` | No | `jesse` | Default username |
| `DEFAULT_WEIGHT_LBS` | No | `179` | Default weight in pounds |

## Troubleshooting

### Database not persisting on Vercel
- **Cause**: Using SQLite on Vercel's read-only filesystem
- **Solution**: Set up external PostgreSQL database (see above)

### PubMed research features not working
- **Cause**: Missing NCBI_EMAIL environment variable
- **Solution**: Add your email to environment variables

### CORS errors in frontend
- **Cause**: Frontend origin not in CORS_ORIGINS
- **Solution**: Add your deployment URL to CORS_ORIGINS environment variable

### Database seeding fails
- **Cause**: Database permissions or connection issues
- **Solution**: Check DATABASE_URL and ensure database is accessible
- The app will continue to run even if seeding fails (tables are still created)

## Health Check

After deployment, verify the app is running:

```bash
# Check backend health
curl https://your-domain.vercel.app/health

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "message": "No Colon, Still Rollin'"
}
```

## Next Steps for PostgreSQL Migration

Currently, the backend uses `sqlite3` directly. For full PostgreSQL support:

1. **Refactor to use SQLAlchemy ORM** throughout the codebase
2. **Create database adapters** for SQLite and PostgreSQL
3. **Update all raw SQL queries** to use parameterized queries
4. **Add connection pooling** for better performance
5. **Implement migrations** using Alembic

This is planned for Phase 3 after genetic profiling features are implemented.
