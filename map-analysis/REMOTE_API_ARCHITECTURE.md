# Remote REST API Architecture

**Date**: 2025-01-15  
**Architecture**: Frontend → Next.js API Routes → Remote REST API → Firebird Database

## Architecture Overview

This project uses a **remote REST API service** architecture instead of direct database connections:

```
┌─────────────┐      ┌──────────────────┐      ┌──────────────────┐      ┌──────────────┐
│   Frontend  │─────▶│  Next.js API      │─────▶│  Remote REST API │─────▶│   Firebird   │
│  (React)    │      │  Routes (Proxy)   │      │  Service         │      │  Database    │
└─────────────┘      └──────────────────┘      └──────────────────┘      └──────────────┘
```

### Component Responsibilities

1. **Frontend (React Components)**
   - User interface and interactions
   - Calls Next.js API routes via `lib/api-client.ts`
   - Handles form validation and error display

2. **Next.js API Routes** (`app/api/*`)
   - Proxy layer that forwards requests to remote REST API
   - Validates request data
   - Handles errors and responses
   - Uses `lib/remote-api.ts` to call remote service

3. **Remote REST API Service**
   - Handles all database operations
   - Connects to Firebird 2.5 database
   - Provides RESTful endpoints
   - Manages transactions and business logic

4. **Firebird 2.5 Database**
   - Stores all application data
   - Managed by remote REST API service

## Configuration

### Environment Variables

Create `.env.local` file:

```env
# Remote REST API service URL
API_BASE_URL=http://localhost:3000
# Or use alternative name
REMOTE_API_URL=http://your-api-server:port
```

### Default Configuration

- **Default API URL**: `http://localhost:3000`
- If remote API is on different host/port, update `API_BASE_URL` accordingly

## Code Structure

### `lib/remote-api.ts`
- Clean interface to call remote REST API
- Provides typed API methods:
  - `remotePatientApi` - Patient operations
  - `remoteCardApi` - Card/Family operations
  - `remoteVitalApi` - Vital signs operations
  - `remotePaymentApi` - Payment operations

### `lib/db.ts`
- Legacy compatibility layer
- Forwards database-style queries to remote API
- Maintains compatibility with existing code

### `app/api/*/route.ts`
- Next.js API routes that proxy to remote API
- Validates requests
- Forwards to `lib/remote-api.ts`

## Benefits

1. **Separation of Concerns**
   - Frontend doesn't need database drivers
   - Database logic isolated in remote service
   - Easier to scale and maintain

2. **Security**
   - Database credentials not exposed to frontend
   - Centralized authentication/authorization
   - Better access control

3. **Flexibility**
   - Can change database without frontend changes
   - Multiple frontends can use same API
   - Easier to version API

4. **No Database Dependencies**
   - Frontend doesn't need any database drivers (uses remote REST API)
   - Lighter frontend bundle
   - Simpler deployment

## API Endpoints

The remote REST API should provide these endpoints:

### Patients
- `GET /api/patients` - List patients (with optional `?keyword=search`)
- `GET /api/patients/:id` - Get patient by ID
- `POST /api/patients` - Create patient
- `PUT /api/patients/:id` - Update patient
- `DELETE /api/patients/:id` - Delete patient

### Cards
- `POST /api/cards` - Save card information
- `PUT /api/cards/:id` - Update card information

### Vitals
- `POST /api/vitals/:patientId` - Save vital signs
- `PUT /api/vitals/:patientId` - Update vital signs

### Payments
- `POST /api/payments` - Save payment information
- `GET /api/payments/history/:patientId` - Get payment history

## Migration Notes

### Removed
- ❌ All database driver packages (not needed)
- ❌ Direct database connection code
- ❌ Database configuration in frontend

### Added
- ✅ `lib/remote-api.ts` - Remote API client
- ✅ Updated `lib/db.ts` - HTTP client wrapper
- ✅ Updated API routes to proxy to remote API

### Updated
- ✅ `package.json` - Removed database dependencies
- ✅ Environment variables - Now uses `API_BASE_URL`
- ✅ Documentation - Updated architecture docs

## Next Steps

1. **Configure Remote API URL**
   - Set `API_BASE_URL` in `.env.local`
   - Ensure remote API service is running

2. **Test Connection**
   - Verify remote API is accessible
   - Test each endpoint

3. **Update API Routes** (if needed)
   - Customize endpoint mappings in `app/api/*/route.ts`
   - Adjust request/response formats if remote API differs

4. **Error Handling**
   - Ensure proper error handling for network failures
   - Add retry logic if needed
   - Handle authentication if remote API requires it

