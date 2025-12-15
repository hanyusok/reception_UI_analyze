/**
 * Remote REST API Client
 * This module provides functions to call the remote RESTful API service
 * instead of connecting directly to the database.
 * 
 * The remote API service handles all database operations (Firebird 2.5).
 */

// Remote API base URL from environment variable
const API_BASE_URL = process.env.API_BASE_URL || process.env.REMOTE_API_URL || 'http://localhost:3000'

/**
 * Make HTTP request to remote REST API
 */
async function apiRequest<T>(
  endpoint: string,
  method: string = 'GET',
  body?: any,
  params?: Record<string, string>
): Promise<T> {
  let url = `${API_BASE_URL}${endpoint}`
  
  // Add query parameters if provided
  if (params && Object.keys(params).length > 0) {
    const searchParams = new URLSearchParams(params)
    url += `?${searchParams.toString()}`
  }

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  }

  if (body) {
    config.body = JSON.stringify(body)
  }

  try {
    const response = await fetch(url, config)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: `HTTP ${response.status}: ${response.statusText}`,
      }))
      throw new Error(errorData.message || 'API request failed')
    }

    return await response.json()
  } catch (error) {
    console.error('API request error', { url, method, error })
    throw error
  }
}

/**
 * Query function - calls remote API endpoint
 * This maintains compatibility with existing code that expects a database query function
 * 
 * @param text - SQL query (for reference, actual query is handled by remote API)
 * @param params - Query parameters
 */
export async function query(text: string, params?: any[]): Promise<any> {
  // For compatibility, we can map SQL queries to API endpoints
  // This is a simplified version - you may need to adjust based on your remote API structure
  
  console.log('Query called (forwarding to remote API)', { text, params })
  
  // Example: If query is for patients, call /api/patients endpoint
  // You'll need to customize this based on your remote API structure
  if (text.includes('SELECT * FROM PERSON')) {
    const keyword = params?.[0]?.replace(/%/g, '') || ''
    return apiRequest('/api/patients', 'GET', undefined, keyword ? { keyword } : undefined)
  }
  
  // Default: return empty result
  // You should implement proper mapping based on your remote API endpoints
  return { rows: [], rowCount: 0 }
}

/**
 * Transaction function - calls remote API with transaction support
 * Note: Transaction handling depends on your remote API implementation
 */
export async function transaction(callback: (client: any) => Promise<any>) {
  // Create a client-like object that makes API calls
  const client = {
    query: async (text: string, params?: any[]) => {
      // Map SQL queries to API calls
      // This is a placeholder - customize based on your API structure
      return query(text, params)
    }
  }

  try {
    const result = await callback(client)
    return result
  } catch (error) {
    // Transaction rollback would be handled by remote API
    throw error
  }
}

export default {
  query,
  transaction,
  apiRequest,
}
