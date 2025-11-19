# TICE Frontend - React Integration

## Quick Start

This frontend has been integrated with the TICE Flask backend.

### Prerequisites
- Node.js (v18 or higher)
- Backend running on port 5000

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```

The app will be available at http://localhost:8080

### API Integration

All API calls are configured to proxy through Vite to the Flask backend:
- `/api/*` → `http://localhost:5000/api/*`

See `src/lib/api.ts` for available API functions.

### Features
- Real-time IP threat analysis
- Multi-source intelligence aggregation
- Interactive threat score visualization
- PDF report generation and download
- Dark/Light theme toggle
- Responsive design

### Key Files
- `src/pages/Index.tsx` - Main dashboard
- `src/lib/api.ts` - API client functions
- `vite.config.ts` - Vite configuration with proxy

### Testing
1. Start backend: `python app.py` (from root directory)
2. Start frontend: `npm run dev` (from this directory)
3. Open http://localhost:8080
4. Enter IP address: `8.8.8.8` or `45.142.212.61`
5. Click "Analyze"
6. Download PDF report

For detailed integration documentation, see `FRONTEND_BACKEND_INTEGRATION_COMPLETE.md` in the root directory.
