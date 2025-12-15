'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { patientSchema, type PatientFormData } from '@/lib/validations'
import { patientApi, ApiError } from '@/lib/api-client'

export default function PatientForm() {
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
