import { NextRequest, NextResponse } from 'next/server'

/**
 * Proxy endpoint for patient search
 * Forwards requests to remote API: /api/databases/mtsdb/tables/PERSON/search
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const pname = searchParams.get('pname') || ''

    if (!pname) {
      return NextResponse.json(
        { message: '검색어(pname)가 필요합니다.' },
        { status: 400 }
      )
    }

    // Get remote API base URL from environment
    // If API_BASE_URL is set, use it; otherwise assume remote API is on same server
    const remoteApiUrl = process.env.API_BASE_URL || 'http://localhost:3000'
    
    // Construct the full remote API URL
    // Note: If remote API is on a different server/port, API_BASE_URL should point to that server
    const remoteUrl = `${remoteApiUrl}/api/databases/mtsdb/tables/PERSON/search?pname=${encodeURIComponent(pname)}`
    
    console.log('Proxying search request to:', remoteUrl)
    
    const response = await fetch(remoteUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      // Add cache control to avoid stale results
      cache: 'no-store',
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Remote API error:', response.status, errorText)
      return NextResponse.json(
        { message: `원격 API 오류: ${response.status} ${response.statusText}` },
        { status: response.status }
      )
    }

    const data = await response.json()
    
    return NextResponse.json(data, { status: 200 })
  } catch (error: any) {
    console.error('Patient search proxy error:', error)
    return NextResponse.json(
      { message: error.message || '환자 검색에 실패했습니다' },
      { status: 500 }
    )
  }
}

