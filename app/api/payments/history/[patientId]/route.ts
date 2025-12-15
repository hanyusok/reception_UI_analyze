/**
 * 수납 내역 조회 API 라우트
 */

import { NextRequest, NextResponse } from 'next/server'
import { query } from '@/lib/db'

export async function GET(
  request: NextRequest,
  { params }: { params: { patientId: string } }
) {
  try {
    const result = await query(
      `SELECT 
        VISIDATE, 
        MISU, 
        WHANBUL, 
        WHANSU,
        (MISU + WHANBUL + WHANSU) as TOTAL
      FROM FEELOG 
      WHERE PCODE = $1 
      ORDER BY VISIDATE DESC 
      LIMIT 50`,
      [params.patientId]
    )
    
    return NextResponse.json({ payments: result.rows }, { status: 200 })
  } catch (error: any) {
    console.error('Payment history error:', error)
    return NextResponse.json(
      { message: '수납 내역 조회에 실패했습니다' },
      { status: 500 }
    )
  }
}

