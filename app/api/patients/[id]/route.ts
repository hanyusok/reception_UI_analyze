/**
 * 환자 상세 정보 API 라우트
 * GET: 환자 조회
 * PUT: 환자 수정
 * DELETE: 환자 삭제
 */

import { NextRequest, NextResponse } from 'next/server'
import { query, transaction } from '@/lib/db'
import { patientSchema } from '@/lib/validations'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const result = await query(
      'SELECT * FROM PERSON WHERE PCODE = $1',
      [params.id]
    )
    
    if (result.rows.length === 0) {
      return NextResponse.json(
        { message: '환자를 찾을 수 없습니다' },
        { status: 404 }
      )
    }
    
    return NextResponse.json({ patient: result.rows[0] }, { status: 200 })
  } catch (error: any) {
    console.error('Patient get error:', error)
    return NextResponse.json(
      { message: '환자 조회에 실패했습니다' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json()
    const validatedData = patientSchema.parse(body)
    
    const updateQuery = `
      UPDATE PERSON SET 
        PNAME = $1, 
        PBIRTH = $2, 
        PIDNUM = $3, 
        PIDNUM2 = $4, 
        SEX = $5, 
        RELATION = $6, 
        CRIPPLED = $7, 
        BOHUN = $8, 
        AGREE = $9,
        LASTCHECK = CURRENT_TIMESTAMP
      WHERE PCODE = $10
      RETURNING *
    `
    
    const result = await query(updateQuery, [
      validatedData.pname,
      validatedData.pbirth,
      validatedData.pidnum || null,
      validatedData.pidnum2 || null,
      validatedData.sex,
      validatedData.relation || null,
      validatedData.crippled,
      validatedData.bohun,
      validatedData.agree,
      params.id,
    ])
    
    if (result.rows.length === 0) {
      return NextResponse.json(
        { message: '환자를 찾을 수 없습니다' },
        { status: 404 }
      )
    }
    
    return NextResponse.json({ patient: result.rows[0] }, { status: 200 })
  } catch (error: any) {
    console.error('Patient update error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: '환자 정보 수정에 실패했습니다' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // DELETE FROM PERSON WHERE PCODE = :id
    const result = await query(
      'DELETE FROM PERSON WHERE PCODE = $1 RETURNING *',
      [params.id]
    )
    
    if (result.rows.length === 0) {
      return NextResponse.json(
        { message: '환자를 찾을 수 없습니다' },
        { status: 404 }
      )
    }
    
    return NextResponse.json(
      { message: '환자 정보가 삭제되었습니다' },
      { status: 200 }
    )
  } catch (error: any) {
    console.error('Patient delete error:', error)
    return NextResponse.json(
      { message: '환자 정보 삭제에 실패했습니다' },
      { status: 500 }
    )
  }
}

