/**
 * 환자 정보 API 라우트
 * POST: 환자 생성/수정
 * GET: 환자 목록 조회
 * 
 * This route forwards requests to the remote REST API service
 */

import { NextRequest, NextResponse } from 'next/server'
import { remotePatientApi } from '@/lib/remote-api'
import { patientSchema } from '@/lib/validations'

// 환자 생성/수정
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // 데이터 검증
    const validatedData = patientSchema.parse(body)
    
    // Forward to remote API
    if (validatedData.pcode) {
      // Update existing patient
      const result = await remotePatientApi.update(validatedData.pcode.toString(), validatedData)
      return NextResponse.json({ patient: result.patient, isNew: false }, { status: 200 })
    } else {
      // Create new patient
      const result = await remotePatientApi.create(validatedData)
      return NextResponse.json({ patient: result.patient, isNew: true, id: result.id }, { status: 200 })
    }
  } catch (error: any) {
    console.error('Patient save error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: error.message || '환자 정보 저장에 실패했습니다' },
      { status: 500 }
    )
  }
}

// 환자 목록 조회
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const keyword = searchParams.get('keyword') || ''
    
    // Forward to remote API
    const result = await remotePatientApi.search(keyword)
    
    return NextResponse.json(result, { status: 200 })
  } catch (error: any) {
    console.error('Patient search error:', error)
    return NextResponse.json(
      { message: error.message || '환자 검색에 실패했습니다' },
      { status: 500 }
    )
  }
}

