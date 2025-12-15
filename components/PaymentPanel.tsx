'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { paymentSchema, type PaymentFormData } from '@/lib/validations'
import { paymentApi, ApiError } from '@/lib/api-client'

export default function PaymentPanel() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [patientId, setPatientId] = useState<string>('')
  const [paymentHistory, setPaymentHistory] = useState<any[]>([])
  const [loadingHistory, setLoadingHistory] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PaymentFormData>({
    resolver: zodResolver(paymentSchema),
  })

  const onSubmit = async (data: PaymentFormData) => {
    if (!patientId) {
      setError('환자 ID를 입력하세요')
      return
    }

    setIsLoading(true)
    setError(null)
    setSuccess(false)

    try {
      await paymentApi.save({ ...data, pcode: patientId })
      setSuccess(true)
      reset()
      loadPaymentHistory()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('수납 정보 저장에 실패했습니다')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const loadPaymentHistory = async () => {
    if (!patientId) return

    setLoadingHistory(true)
    try {
      const result = await paymentApi.getHistory(patientId)
      setPaymentHistory(result.payments)
    } catch (err) {
      console.error('수납 내역 조회 실패:', err)
    } finally {
      setLoadingHistory(false)
    }
  }

  useEffect(() => {
    if (patientId) {
      loadPaymentHistory()
    }
  }, [patientId])

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold mb-6">수납 정보</h2>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                미수금 (원)
              </label>
            <input
              type="number"
              {...register('misu')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.misu && (
              <p className="mt-1 text-sm text-red-600">{errors.misu.message}</p>
            )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                완불 (원)
              </label>
            <input
              type="number"
              {...register('whanbul')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.whanbul && (
              <p className="mt-1 text-sm text-red-600">{errors.whanbul.message}</p>
            )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                완수 (원)
              </label>
            <input
              type="number"
              {...register('whansu')}
              className="input-field"
              disabled={isLoading}
            />
            {errors.whansu && (
              <p className="mt-1 text-sm text-red-600">{errors.whansu.message}</p>
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
      </div>

      {/* 수납 내역 목록 */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">수납 내역</h2>
          {patientId && (
            <button
              onClick={loadPaymentHistory}
              className="btn-secondary text-sm"
              disabled={loadingHistory}
            >
              {loadingHistory ? '로딩 중...' : '새로고침'}
            </button>
          )}
        </div>
        
        {loadingHistory ? (
          <div className="text-center py-8 text-gray-500">로딩 중...</div>
        ) : paymentHistory.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            {patientId ? '수납 내역이 없습니다' : '환자 ID를 입력하면 수납 내역을 조회할 수 있습니다'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    내원일자
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    미수금
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    완불
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    완수
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    총액
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paymentHistory.map((payment, index) => (
                  <tr key={index}>
                    <td className="px-4 py-3 text-sm">{payment.visidate}</td>
                    <td className="px-4 py-3 text-sm">{payment.misu?.toLocaleString() || 0}</td>
                    <td className="px-4 py-3 text-sm">{payment.whanbul?.toLocaleString() || 0}</td>
                    <td className="px-4 py-3 text-sm">{payment.whansu?.toLocaleString() || 0}</td>
                    <td className="px-4 py-3 text-sm font-medium">
                      {payment.total?.toLocaleString() || 0}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

