'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { cardSchema, type CardFormData } from '@/lib/validations'
import { cardApi, ApiError } from '@/lib/api-client'

export default function CardForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CardFormData>({
    resolver: zodResolver(cardSchema),
  })

  const onSubmit = async (data: CardFormData) => {
    setIsLoading(true)
    setError(null)
    setSuccess(false)

    try {
      await cardApi.save(data)
      setSuccess(true)
      reset()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('카드 정보 저장에 실패했습니다')
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
          카드 정보가 저장되었습니다
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            세대주명
          </label>
          <input
            type="text"
            {...register('fname')}
            className="input-field"
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            가족번호
          </label>
          <input
            type="text"
            {...register('fcode')}
            className="input-field"
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            주민번호
          </label>
          <input
            type="text"
            {...register('fidnum')}
            className="input-field"
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            구분
          </label>
          <select
            {...register('caretype')}
            className="input-field"
            disabled={isLoading}
          >
            <option value="">선택하세요</option>
            <option value="1">건강보험</option>
            <option value="2">의료급여</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            적용기간 시작
          </label>
          <input
            type="date"
            {...register('begindate')}
            className="input-field"
            disabled={isLoading}
          />
          {errors.begindate && (
            <p className="mt-1 text-sm text-red-600">{errors.begindate.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            적용기간 종료
          </label>
          <input
            type="date"
            {...register('enddate')}
            className="input-field"
            disabled={isLoading}
          />
          {errors.enddate && (
            <p className="mt-1 text-sm text-red-600">{errors.enddate.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            증번호
          </label>
          <input
            type="text"
            {...register('cardnum')}
            className="input-field"
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            직장
          </label>
          <input
            type="text"
            {...register('company')}
            className="input-field"
            disabled={isLoading}
          />
        </div>
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
