'use client'

import { useState } from 'react'
import PatientForm from './PatientForm'
import CardForm from './CardForm'

export default function ReceptionPanel() {
  const [showPatientForm, setShowPatientForm] = useState(false)
  const [showCardForm, setShowCardForm] = useState(false)

  return (
    <div className="space-y-6">
      {/* 검색 및 액션 버튼 */}
      <div className="card">
        <div className="flex space-x-2 mb-4">
          <input
            type="text"
            placeholder="수진자 검색..."
            className="input-field flex-1"
          />
          <button className="btn-primary">검색</button>
        </div>
        
        <div className="flex flex-wrap gap-2">
          <button 
            onClick={() => setShowPatientForm(true)}
            className="btn-primary"
          >
            접수
          </button>
          <button className="btn-secondary">수정</button>
          <button 
            onClick={() => setShowCardForm(true)}
            className="btn-secondary"
          >
            새가족
          </button>
          <button className="btn-secondary">기록</button>
          <button className="btn-secondary">취소</button>
        </div>
      </div>

      {/* 환자 정보 폼 */}
      {showPatientForm && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">인적사항</h2>
            <button
              onClick={() => setShowPatientForm(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <PatientForm />
        </div>
      )}

      {/* 카드 정보 폼 */}
      {showCardForm && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">가족/보험카드 정보</h2>
            <button
              onClick={() => setShowCardForm(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <CardForm />
        </div>
      )}
    </div>
  )
}

