# IMPORTANT: Database Migration Required!

After deploying these changes, you MUST run database migrations to create the `PasswordResetRequest` table.

## Local Development

```bash
python manage.py makemigrations
python manage.py migrate
```

## Render Production

The migrations will run automatically during deployment because of the `build.sh` script.

However, if you need to run them manually:

1. Go to Render Dashboard → Your Service → Shell
2. Run:
```bash
python manage.py migrate
```

## What This Does

Creates a new database table `journal_passwordresetrequest` with fields:
- `id` - Primary key
- `email` - Email address requesting reset
- `requested_at` - Timestamp of request
- `ip_address` - IP address (for security tracking)

This table tracks password reset requests to enforce the once-per-24-hours limit.

## No Migration File?

If `manage.py makemigrations` doesn't create a migration file, it means:
1. The database already has the table, OR
2. Django hasn't detected the model changes

In that case, just run `migrate` and it should work fine.
