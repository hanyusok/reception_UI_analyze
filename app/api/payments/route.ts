/**
 * 수납 정보 API 라우트
 * POST: 수납 정보 저장
 */

import { NextRequest, NextResponse } from 'next/server'
import { query } from '@/lib/db'
import { paymentSchema } from '@/lib/validations'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validatedData = paymentSchema.parse(body)
    
    // UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu
    const insertQuery = `
      INSERT INTO FEELOG (
        PCODE, VISIDATE, MISU, WHANBUL, WHANSU
      ) VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `
    
    const result = await query(insertQuery, [
      body.pcode,
      new Date().toISOString().split('T')[0],
      validatedData.misu ? parseInt(validatedData.misu) : 0,
      validatedData.whanbul ? parseInt(validatedData.whanbul) : 0,
      validatedData.whansu ? parseInt(validatedData.whansu) : 0,
    ])
    
    return NextResponse.json({ payment: result.rows[0] }, { status: 200 })
  } catch (error: any) {
    console.error('Payment save error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: '수납 정보 저장에 실패했습니다' },
      { status: 500 }
    )
  }
}

