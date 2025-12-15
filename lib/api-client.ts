/**
 * API 클라이언트 유틸리티
 */

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: any
  headers?: Record<string, string>
}

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = 'GET', body, headers = {} } = options

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  }

  if (body) {
    config.body = JSON.stringify(body)
  }

  try {
    const response = await fetch(`/api${endpoint}`, config)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        errorData.message || '요청에 실패했습니다',
        response.status,
        errorData
      )
    }

    return await response.json()
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError('네트워크 오류가 발생했습니다', 0, error)
  }
}

// 환자 관련 API
export const patientApi = {
  // 환자 검색
  search: (keyword: string) =>
    apiRequest<{ patients: any[] }>('/patients/search', {
      method: 'GET',
      headers: { keyword },
    }),

  // 환자 조회
  get: (id: string) =>
    apiRequest<{ patient: any }>(`/patients/${id}`),

  // 환자 생성/수정
  save: (data: any) =>
    apiRequest<{ patient: any; id: string }>('/patients', {
      method: 'POST',
      body: data,
    }),

  // 환자 수정
  update: (id: string, data: any) =>
    apiRequest<{ patient: any }>(`/patients/${id}`, {
      method: 'PUT',
      body: data,
    }),

  // 환자 삭제
  delete: (id: string) =>
    apiRequest(`/patients/${id}`, {
      method: 'DELETE',
    }),
}

// 가족/카드 관련 API
export const cardApi = {
  // 카드 정보 저장
  save: (data: any) =>
    apiRequest<{ card: any }>('/cards', {
      method: 'POST',
      body: data,
    }),

  // 카드 정보 수정
  update: (id: string, data: any) =>
    apiRequest<{ card: any }>(`/cards/${id}`, {
      method: 'PUT',
      body: data,
    }),
}

// 신체계측 관련 API
export const vitalApi = {
  // 신체계측 정보 저장
  save: (patientId: string, data: any) =>
    apiRequest<{ vital: any }>(`/vitals/${patientId}`, {
      method: 'POST',
      body: data,
    }),

  // 신체계측 정보 수정
  update: (patientId: string, data: any) =>
    apiRequest<{ vital: any }>(`/vitals/${patientId}`, {
      method: 'PUT',
      body: data,
    }),
}

// 수납 관련 API
export const paymentApi = {
  // 수납 정보 저장
  save: (data: any) =>
    apiRequest<{ payment: any }>('/payments', {
      method: 'POST',
      body: data,
    }),

  // 수납 내역 조회
  getHistory: (patientId: string) =>
    apiRequest<{ payments: any[] }>(`/payments/history/${patientId}`),
}

export { ApiError }

