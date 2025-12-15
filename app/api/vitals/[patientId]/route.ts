/**
 * 신체계측 정보 API 라우트
 * POST: 신체계측 정보 저장
 * PUT: 신체계측 정보 수정
 */

import { NextRequest, NextResponse } from 'next/server'
import { query } from '@/lib/db'
import { vitalSchema } from '@/lib/validations'

export async function POST(
  request: NextRequest,
  { params }: { params: { patientId: string } }
) {
  try {
    const body = await request.json()
    const validatedData = vitalSchema.parse(body)
    
    // UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, ...
    const insertQuery = `
      INSERT INTO CHECKPERSON (
        PCODE, WEIGHT, HEIGHT, TEMPERATUR, PULSE, SYSTOLIC, DIASTOLIC
      ) VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *
    `
    
    const result = await query(insertQuery, [
      params.patientId,
      validatedData.weight ? parseFloat(validatedData.weight) : null,
      validatedData.height ? parseFloat(validatedData.height) : null,
      validatedData.temperatur ? parseFloat(validatedData.temperatur) : null,
      validatedData.pulse ? parseInt(validatedData.pulse) : null,
      validatedData.systolic ? parseInt(validatedData.systolic) : null,
      validatedData.diastolic ? parseInt(validatedData.diastolic) : null,
    ])
    
    return NextResponse.json({ vital: result.rows[0] }, { status: 200 })
  } catch (error: any) {
    console.error('Vital save error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: '신체계측 정보 저장에 실패했습니다' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { patientId: string } }
) {
  try {
    const body = await request.json()
    const validatedData = vitalSchema.parse(body)
    
    const updateQuery = `
      UPDATE CHECKPERSON SET 
        WEIGHT = $1, 
        HEIGHT = $2, 
        TEMPERATUR = $3, 
        PULSE = $4, 
        SYSTOLIC = $5, 
        DIASTOLIC = $6
      WHERE PCODE = $7
      RETURNING *
    `
    
    const result = await query(updateQuery, [
      validatedData.weight ? parseFloat(validatedData.weight) : null,
      validatedData.height ? parseFloat(validatedData.height) : null,
      validatedData.temperatur ? parseFloat(validatedData.temperatur) : null,
      validatedData.pulse ? parseInt(validatedData.pulse) : null,
      validatedData.systolic ? parseInt(validatedData.systolic) : null,
      validatedData.diastolic ? parseInt(validatedData.diastolic) : null,
      params.patientId,
    ])
    
    if (result.rows.length === 0) {
      return NextResponse.json(
        { message: '신체계측 정보를 찾을 수 없습니다' },
        { status: 404 }
      )
    }
    
    return NextResponse.json({ vital: result.rows[0] }, { status: 200 })
  } catch (error: any) {
    console.error('Vital update error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: '신체계측 정보 수정에 실패했습니다' },
      { status: 500 }
    )
  }
}

