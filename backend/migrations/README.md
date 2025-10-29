# Database Migrations (Archived)

This folder contains historical database migration scripts that have been superseded by the main database initialization code.

## Archived Scripts

### `add_tracking_features.py`
**Date**: Phase 2 development
**Purpose**: Added medication log, hydration tracking, and health photo tagging features

**Changes Applied**:
- Added `tags` and `archived` columns to `health_photos` table
- Created `medication_log` table with foreign keys to users and medications
- Created `hydration_log` table for tracking 8oz water intake
- Created `hydration_goals` table for customizable daily goals
- Added indexes on user_id and date columns for performance

**Status**: ✅ All changes merged into `backend/app/core/database.py` `_create_tables()` method

### `add_new_foods.py`
**Date**: Phase 2 development
**Purpose**: Added kimchi and liver detox tea to foods database

**Foods Added**:
1. **Kimchi** - Fermented foods with probiotics for gut health and immune support
2. **Liver Detox Tea** - Blend of milk thistle, dandelion, turmeric, artichoke for liver protection

**Status**: ✅ Both foods merged into `backend/app/core/init_database.py` `seed_foods()` function

## Current State

As of Phase 2 completion:
- All tables are created automatically via `database.py` on first run
- All foods are seeded automatically via `init_database.py` on first run
- No manual migration scripts needed for fresh deployments
- Database auto-initializes on application startup

## Future Migrations

For Phase 3 genetic profiling features, new tables will be added directly to `database.py` rather than using separate migration scripts. This ensures:
- Idempotent initialization (`CREATE TABLE IF NOT EXISTS`)
- Clean deployments on Vercel, Replit, and local environments
- Single source of truth for database schema
