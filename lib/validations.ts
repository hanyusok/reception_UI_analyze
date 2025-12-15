/**
 * 폼 입력값 검증 스키마 (Zod 사용)
 */

import { z } from 'zod'

// 환자 정보 검증 스키마
export const patientSchema = z.object({
  pname: z.string().min(1, '수진자명을 입력하세요'),
  pbirth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, '올바른 날짜 형식이 아닙니다'),
  pidnum: z.string().regex(/^\d{6}$/, '주민번호 앞자리는 6자리 숫자입니다').optional(),
  pidnum2: z.string().regex(/^\d{7}$/, '주민번호 뒷자리는 7자리 숫자입니다').optional(),
  sex: z.enum(['M', 'F'], { required_error: '성별을 선택하세요' }),
  relation: z.string().optional(),
  crippled: z.boolean().default(false),
  bohun: z.boolean().default(false),
  agree: z.boolean().default(false),
  pcode: z.string().optional(),
})

// 가족/카드 정보 검증 스키마
export const cardSchema = z.object({
  fname: z.string().optional(),
  fcode: z.string().optional(),
  fidnum: z.string().optional(),
  begindate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, '올바른 날짜 형식이 아닙니다').optional(),
  enddate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, '올바른 날짜 형식이 아닙니다').optional(),
  caretype: z.string().optional(),
  cardnum: z.string().optional(),
  company: z.string().optional(),
})

// 신체계측 정보 검증 스키마
export const vitalSchema = z.object({
  weight: z.string().regex(/^\d+(\.\d+)?$/, '올바른 숫자 형식이 아닙니다').optional(),
  height: z.string().regex(/^\d+(\.\d+)?$/, '올바른 숫자 형식이 아닙니다').optional(),
  temperatur: z.string().regex(/^\d+(\.\d+)?$/, '올바른 숫자 형식이 아닙니다').optional(),
  pulse: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
  systolic: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
  diastolic: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
})

// 수납 정보 검증 스키마
export const paymentSchema = z.object({
  misu: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
  whanbul: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
  whansu: z.string().regex(/^\d+$/, '올바른 숫자 형식이 아닙니다').optional(),
})

export type PatientFormData = z.infer<typeof patientSchema>
export type CardFormData = z.infer<typeof cardSchema>
export type VitalFormData = z.infer<typeof vitalSchema>
export type PaymentFormData = z.infer<typeof paymentSchema>

