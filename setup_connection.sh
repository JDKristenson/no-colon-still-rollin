#!/bin/bash
# Simple connection string setup

echo "🔗 Supabase Connection String Setup"
echo ""

# Direct link to database settings
echo "👉 OPEN THIS LINK:"
echo "https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/database"
echo ""
echo "Then:"
echo "1. Scroll to 'Connection string' section"
echo "2. Click 'Connection pooling' tab"
echo "3. Select 'Transaction' mode"
echo "4. Copy the URI connection string"
echo ""
read -p "Paste your connection string here: " conn_str

if [ -z "$conn_str" ]; then
    echo "No connection string provided. Exiting."
    exit 1
fi

# Create .env if needed
if [ ! -f "backend/.env" ]; then
    cp .env.example backend/.env 2>/dev/null || echo "DATABASE_URL=" > backend/.env
fi

# Update DATABASE_URL
if grep -q "DATABASE_URL=" backend/.env; then
    sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=$conn_str|" backend/.env
else
    echo "DATABASE_URL=$conn_str" >> backend/.env
fi

echo ""
echo "✅ Connection string saved to backend/.env"
echo ""
echo "Now running full setup..."
./setup.sh
