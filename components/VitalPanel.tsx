'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { vitalSchema, type VitalFormData } from '@/lib/validations'
import { vitalApi, ApiError } from '@/lib/api-client'

export default function VitalPanel() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [patientId, setPatientId] = useState<string>('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<VitalFormData>({
    resolver: zodResolver(vitalSchema),
  })

  const onSubmit = async (data: VitalFormData) => {
    if (!patientId) {
      setError('환자 ID를 입력하세요')
      return
    }

    setIsLoading(true)
    setError(null)
    setSuccess(false)

    try {
      await vitalApi.save(patientId, data)
      setSuccess(true)
      reset()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('신체계측 정보 저장에 실패했습니다')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-6">신체계측</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              체중 (kg)
            </label>
            <input
              type="number"
              step="0.1"
              {...register('weight')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.weight && (
              <p className="mt-1 text-sm text-red-600">{errors.weight.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              키 (cm)
            </label>
            <input
              type="number"
              step="0.1"
              {...register('height')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.height && (
              <p className="mt-1 text-sm text-red-600">{errors.height.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              체온 (°C)
            </label>
            <input
              type="number"
              step="0.1"
              {...register('temperatur')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.temperatur && (
              <p className="mt-1 text-sm text-red-600">{errors.temperatur.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              맥박 (bpm)
            </label>
            <input
              type="number"
              {...register('pulse')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.pulse && (
              <p className="mt-1 text-sm text-red-600">{errors.pulse.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              수축기 혈압 (mmHg)
            </label>
            <input
              type="number"
              {...register('systolic')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.systolic && (
              <p className="mt-1 text-sm text-red-600">{errors.systolic.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              이완기 혈압 (mmHg)
            </label>
            <input
              type="number"
              {...register('diastolic')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.diastolic && (
              <p className="mt-1 text-sm text-red-600">{errors.diastolic.message}</p>
            )}
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-4 border-t">
          <button
            type="button"
            onClick={() => reset()}
            className="btn-secondary"
            disabled={isLoading}
          >
            초기화
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
    </div>
  )
}

