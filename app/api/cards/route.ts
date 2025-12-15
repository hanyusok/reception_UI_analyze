/**
 * 가족/보험카드 정보 API 라우트
 * POST: 카드 정보 저장
 */

import { NextRequest, NextResponse } from 'next/server'
import { query, transaction } from '@/lib/db'
import { cardSchema } from '@/lib/validations'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validatedData = cardSchema.parse(body)
    
    // 트랜잭션으로 처리
    // INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
    // UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, ...
    const result = await transaction(async (client) => {
      // 가족 정보 생성 (FCODE가 있는 경우)
      if (validatedData.fcode) {
        const familyQuery = `
          INSERT INTO FAMILY (FCODE) 
          VALUES ($1)
          ON CONFLICT (FCODE) DO NOTHING
          RETURNING *
        `
        await client.query(familyQuery, [validatedData.fcode])
      }
      
      // 카드 정보 업데이트 또는 삽입
      const cardQuery = `
        INSERT INTO CARD (
          FCODE, FNAME, FIDNUM, BEGINDATE, ENDDATE, 
          CARETYPE, CARDNUM, COMPANY
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (FCODE) DO UPDATE SET
          FNAME = EXCLUDED.FNAME,
          FIDNUM = EXCLUDED.FIDNUM,
          BEGINDATE = EXCLUDED.BEGINDATE,
          ENDDATE = EXCLUDED.ENDDATE,
          CARETYPE = EXCLUDED.CARETYPE,
          CARDNUM = EXCLUDED.CARDNUM,
          COMPANY = EXCLUDED.COMPANY
        RETURNING *
      `
      
      const cardResult = await client.query(cardQuery, [
        validatedData.fcode || null,
        validatedData.fname || null,
        validatedData.fidnum || null,
        validatedData.begindate || null,
        validatedData.enddate || null,
        validatedData.caretype || null,
        validatedData.cardnum || null,
        validatedData.company || null,
      ])
      
      return { card: cardResult.rows[0] }
    })
    
    return NextResponse.json(result, { status: 200 })
  } catch (error: any) {
    console.error('Card save error:', error)
    
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { message: '입력값 검증 실패', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: '카드 정보 저장에 실패했습니다' },
      { status: 500 }
    )
  }
}

