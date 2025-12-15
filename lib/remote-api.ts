/**
 * Remote REST API Client
 * 
 * This module provides a clean interface to call the remote RESTful API service.
 * The remote API service handles all database operations with Firebird 2.5.
 */

const API_BASE_URL = process.env.API_BASE_URL || process.env.REMOTE_API_URL || 'http://localhost:3000'

class RemoteApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message)
    this.name = 'RemoteApiError'
  }
}

async function remoteApiRequest<T>(
  endpoint: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
    body?: any
    params?: Record<string, string>
    headers?: Record<string, string>
  } = {}
): Promise<T> {
  const { method = 'GET', body, params, headers = {} } = options

  let url = `${API_BASE_URL}${endpoint}`
  
  // Add query parameters
  if (params && Object.keys(params).length > 0) {
    const searchParams = new URLSearchParams(params)
    url += `?${searchParams.toString()}`
  }

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...headers,
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
      throw new RemoteApiError(
        errorData.message || 'API request failed',
        response.status,
        errorData
      )
    }

    return await response.json()
  } catch (error) {
    if (error instanceof RemoteApiError) {
      throw error
    }
    console.error('Remote API request error', { url, method, error })
    throw new RemoteApiError('Network error occurred', 0, error)
  }
}

// Patient API
export const remotePatientApi = {
  search: (keyword: string) =>
    remoteApiRequest<{ patients: any[] }>('/api/patients', {
      method: 'GET',
      params: keyword ? { keyword } : undefined,
    }),

  get: (id: string) =>
    remoteApiRequest<{ patient: any }>(`/api/patients/${id}`),

  create: (data: any) =>
    remoteApiRequest<{ patient: any; id: string }>('/api/patients', {
      method: 'POST',
      body: data,
    }),

  update: (id: string, data: any) =>
    remoteApiRequest<{ patient: any }>(`/api/patients/${id}`, {
      method: 'PUT',
      body: data,
    }),

  delete: (id: string) =>
    remoteApiRequest(`/api/patients/${id}`, {
      method: 'DELETE',
    }),
}

// Card API
export const remoteCardApi = {
  save: (data: any) =>
    remoteApiRequest<{ card: any }>('/api/cards', {
      method: 'POST',
      body: data,
    }),

  update: (id: string, data: any) =>
    remoteApiRequest<{ card: any }>(`/api/cards/${id}`, {
      method: 'PUT',
      body: data,
    }),
}

// Vital API
export const remoteVitalApi = {
  save: (patientId: string, data: any) =>
    remoteApiRequest<{ vital: any }>(`/api/vitals/${patientId}`, {
      method: 'POST',
      body: data,
    }),

  update: (patientId: string, data: any) =>
    remoteApiRequest<{ vital: any }>(`/api/vitals/${patientId}`, {
      method: 'PUT',
      body: data,
    }),
}

// Payment API
export const remotePaymentApi = {
  save: (data: any) =>
    remoteApiRequest<{ payment: any }>('/api/payments', {
      method: 'POST',
      body: data,
    }),

  getHistory: (patientId: string) =>
    remoteApiRequest<{ payments: any[] }>(`/api/payments/history/${patientId}`),
}

export { RemoteApiError, remoteApiRequest }

