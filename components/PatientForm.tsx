'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { format } from 'date-fns'
import { patientSchema, type PatientFormData } from '@/lib/validations'
import { patientApi, ApiError } from '@/lib/api-client'

interface PatientFormProps {
  patient?: {
    PCODE?: string
    PNAME?: string
    PBIRTH?: string | Date | any
    PIDNUM?: string
    PIDNUM2?: string
    SEX?: string
    RELATION?: string
    CRIPPLED?: boolean | number
    BOHUN?: boolean | number
    AGREE?: boolean | number
    [key: string]: any
  } | null
}

// 날짜 포맷팅 헬퍼 함수
function formatDateForInput(dateValue: any): string {
  if (!dateValue) return ''
  
  try {
    // 문자열인 경우
    if (typeof dateValue === 'string') {
      // 이미 YYYY-MM-DD 형식인지 확인
      if (/^\d{4}-\d{2}-\d{2}/.test(dateValue)) {
        return dateValue
      }
      // Date 객체로 파싱 시도
      const date = new Date(dateValue)
      if (!isNaN(date.getTime())) {
        return format(date, 'yyyy-MM-dd')
      }
      // 다른 형식 시도 (YYYYMMDD 등)
      if (/^\d{8}$/.test(dateValue)) {
        return `${dateValue.substring(0, 4)}-${dateValue.substring(4, 6)}-${dateValue.substring(6, 8)}`
      }
      return dateValue
    }
    
    // Date 객체인 경우
    if (dateValue instanceof Date) {
      return format(dateValue, 'yyyy-MM-dd')
    }
    
    // 객체인 경우
    if (typeof dateValue === 'object') {
      if (dateValue.toISOString) {
        return format(new Date(dateValue.toISOString()), 'yyyy-MM-dd')
      }
      if (dateValue.value || dateValue.date) {
        return formatDateForInput(dateValue.value || dateValue.date)
      }
    }
    
    return String(dateValue)
  } catch (error) {
    console.warn('Date formatting error:', error, dateValue)
    return ''
  }
}

// 주민번호 분리 헬퍼 함수
function splitPidnum(pidnum?: string): { pidnum?: string; pidnum2?: string } {
  if (!pidnum) return {}
  
  // 암호화된 문자열인 경우 (base64 등) 처리하지 않음
  if (pidnum.length > 13 || /[^0-9]/.test(pidnum)) {
    return {}
  }
  
  // 13자리 숫자인 경우 앞 6자리, 뒤 7자리로 분리
  if (pidnum.length === 13) {
    return {
      pidnum: pidnum.substring(0, 6),
      pidnum2: pidnum.substring(6, 13),
    }
  }
  
  // 6자리 이하인 경우 앞자리로만
  if (pidnum.length <= 6) {
    return { pidnum }
  }
  
  return {}
}

export default function PatientForm({ patient }: PatientFormProps = {}) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PatientFormData>({
    resolver: zodResolver(patientSchema),
  })

  // patient prop이 변경되면 폼에 데이터 채우기
  useEffect(() => {
    if (patient) {
      const formattedDate = formatDateForInput(patient.PBIRTH)
      const pidnumSplit = splitPidnum(patient.PIDNUM)
      
      const formData: Partial<PatientFormData> = {
        pname: patient.PNAME || '',
        pbirth: formattedDate,
        pidnum: pidnumSplit.pidnum || patient.PIDNUM?.substring(0, 6) || '',
        pidnum2: pidnumSplit.pidnum2 || patient.PIDNUM2 || patient.PIDNUM?.substring(6, 13) || '',
        sex: (patient.SEX as 'M' | 'F') || 'M',
        relation: patient.RELATION || '',
        crippled: Boolean(patient.CRIPPLED),
        bohun: Boolean(patient.BOHUN),
        agree: Boolean(patient.AGREE),
        pcode: patient.PCODE || '',
      }
      
      reset(formData)
    }
  }, [patient, reset])

  const onSubmit = async (data: PatientFormData) => {
    setIsLoading(true)
    setError(null)
    setSuccess(false)

    try {
      await patientApi.save(data)
      setSuccess(true)
      reset()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('환자 정보 저장에 실패했습니다')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {success && (
        <div className="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
          환자 정보가 저장되었습니다
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            수진자명 *
          </label>
          <input
            type="text"
            {...register('pname')}
            className="input-field"
            disabled={isLoading}
          />
          {errors.pname && (
            <p className="mt-1 text-sm text-red-600">{errors.pname.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            관계
          </label>
          <input
            type="text"
            {...register('relation')}
            className="input-field"
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            생년월일 *
          </label>
          <input
            type="date"
            {...register('pbirth')}
            className="input-field"
            disabled={isLoading}
          />
          {errors.pbirth && (
            <p className="mt-1 text-sm text-red-600">{errors.pbirth.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            주민번호 앞자리
          </label>
          <input
            type="text"
            {...register('pidnum')}
            className="input-field"
            maxLength={6}
            placeholder="123456"
            disabled={isLoading}
          />
          {errors.pidnum && (
            <p className="mt-1 text-sm text-red-600">{errors.pidnum.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            주민번호 뒷자리
          </label>
          <input
            type="text"
            {...register('pidnum2')}
            className="input-field"
            maxLength={7}
            placeholder="1234567"
            disabled={isLoading}
          />
          {errors.pidnum2 && (
            <p className="mt-1 text-sm text-red-600">{errors.pidnum2.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            성별 *
          </label>
          <div className="flex space-x-4 mt-2">
            <label className="flex items-center">
              <input
                type="radio"
                value="M"
                {...register('sex')}
                className="mr-2"
                disabled={isLoading}
              />
              남
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="F"
                {...register('sex')}
                className="mr-2"
                disabled={isLoading}
              />
              여
            </label>
          </div>
          {errors.sex && (
            <p className="mt-1 text-sm text-red-600">{errors.sex.message}</p>
          )}
        </div>
      </div>

      <div className="flex space-x-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            {...register('crippled')}
            className="mr-2"
            disabled={isLoading}
          />
          장애인
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            {...register('bohun')}
            className="mr-2"
            disabled={isLoading}
          />
          급여제한자
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            {...register('agree')}
            className="mr-2"
            disabled={isLoading}
          />
          개인정보활용 동의
        </label>
      </div>

      <div className="flex justify-end space-x-2 pt-4 border-t">
        <button
          type="button"
          onClick={() => reset()}
          className="btn-secondary"
          disabled={isLoading}
        >
          취소
        </button>
        <button
          type="submit"
          className="btn-primary"
          disabled={isLoading}
        >
          {isLoading ? '저장 중...' : '저장'}
        </button>
      </div>
    </form>
  )
}
