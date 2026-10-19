#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> [1/2] Building React frontend production bundle..."
cd frontend
npm ci || npm install
npm run build
cd ..

echo "==> [2/2] Installing Python backend dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Build completed successfully! Ready for uvicorn."

