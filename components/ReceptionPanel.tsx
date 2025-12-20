'use client'

import { useState } from 'react'
import { format } from 'date-fns'
import PatientForm from './PatientForm'
import CardForm from './CardForm'

interface Patient {
  PCODE?: string
  PNAME?: string
  PBIRTH?: string | Date | any
  PIDNUM?: string
  SEX?: string
  [key: string]: any
}

// 날짜 포맷팅 헬퍼 함수
function formatDate(dateValue: any): string {
  if (!dateValue) return ''
  
  try {
    // 문자열인 경우
    if (typeof dateValue === 'string') {
      // 이미 포맷된 문자열인지 확인 (YYYY-MM-DD 형식)
      if (/^\d{4}-\d{2}-\d{2}/.test(dateValue)) {
        return dateValue
      }
      // Date 객체로 파싱 시도
      const date = new Date(dateValue)
      if (!isNaN(date.getTime())) {
        return format(date, 'yyyy-MM-dd')
      }
      return dateValue
    }
    
    // Date 객체인 경우
    if (dateValue instanceof Date) {
      return format(dateValue, 'yyyy-MM-dd')
    }
    
    // 객체인 경우 (Firebird Date 객체 등)
    if (typeof dateValue === 'object') {
      // ISO 문자열이 있는지 확인
      if (dateValue.toISOString) {
        return format(new Date(dateValue.toISOString()), 'yyyy-MM-dd')
      }
      // Firebird/Interbase 등에서 흔히 사용하는 year, month, day 구조 확인
      if (dateValue.year !== undefined && dateValue.month !== undefined && dateValue.day !== undefined) {
        const year = dateValue.year
        const month = String(dateValue.month).padStart(2, '0')
        const day = String(dateValue.day).padStart(2, '0')
        return `${year}-${month}-${day}`
      }
      // 다른 속성들 확인
      if (dateValue.value || dateValue.date) {
        return formatDate(dateValue.value || dateValue.date)
      }
      // 만약 객체가 JSON 문자열화 가능하다면 시도 (단, [object Object] 방지)
      try {
        const jsonStr = JSON.stringify(dateValue)
        if (jsonStr !== '{}' && !jsonStr.includes('[object')) {
          return jsonStr
        }
      } catch (e) {}
    }
    
    const strValue = String(dateValue)
    return strValue === '[object Object]' ? '날짜 형식 오류' : strValue
  } catch (error) {
    console.warn('Date formatting error:', error, dateValue)
    return '날짜 오류'
  }
}

export default function ReceptionPanel() {
  const [showPatientForm, setShowPatientForm] = useState(false)
  const [showCardForm, setShowCardForm] = useState(false)
  const [searchKeyword, setSearchKeyword] = useState('')
  const [searchResults, setSearchResults] = useState<Patient[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null)

  const handleSearch = async () => {
    if (!searchKeyword.trim()) {
      setSearchError('검색어를 입력해주세요.')
      return
    }

    setIsSearching(true)
    setSearchError(null)
    setSearchResults([])

    try {
      // Call Next.js API route which proxies to remote API
      const encodedName = encodeURIComponent(searchKeyword.trim())
      const response = await fetch(
        `/api/databases/mtsdb/tables/PERSON/search?pname=${encodedName}`
      )

      if (!response.ok) {
        throw new Error(`검색 실패: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      
      // Handle different response formats
      let results: Patient[] = []
      if (Array.isArray(data)) {
        results = data
      } else if (data.data && Array.isArray(data.data)) {
        results = data.data
      } else if (data.patients && Array.isArray(data.patients)) {
        results = data.patients
      } else if (data.results && Array.isArray(data.results)) {
        results = data.results
      }

      setSearchResults(results)

      if (results.length === 0) {
        setSearchError('검색 결과가 없습니다.')
      }
    } catch (error: any) {
      console.error('Search error:', error)
      setSearchError(error.message || '검색 중 오류가 발생했습니다.')
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const handleSelectPatient = (patient: Patient) => {
    setSelectedPatient(patient)
    setShowPatientForm(true)
    // 검색 결과 영역 스크롤을 맨 위로
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="space-y-6">
      {/* 검색 및 액션 버튼 */}
      <div className="card">
        <div className="flex space-x-2 mb-4">
          <input
            type="text"
            placeholder="수진자 검색..."
            className="input-field flex-1"
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button 
            className="btn-primary"
            onClick={handleSearch}
            disabled={isSearching}
          >
            {isSearching ? '검색 중...' : '검색'}
          </button>
        </div>

        {/* 검색 결과 */}
        {searchError && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {searchError}
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="mb-4">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              검색 결과 ({searchResults.length}건)
            </h3>
            <div className="space-y-2 max-h-96 overflow-y-auto border border-gray-200 rounded-lg p-2 bg-white">
              {searchResults.map((patient, index) => {
                const formattedBirth = formatDate(patient.PBIRTH)
                const displayPidnum = patient.PIDNUM && patient.PIDNUM.length > 20 
                  ? `${patient.PIDNUM.substring(0, 12)}...` 
                  : patient.PIDNUM
                
                return (
                  <div
                    key={patient.PCODE || index}
                    onClick={() => handleSelectPatient(patient)}
                    className="p-3 bg-gray-50 hover:bg-blue-50 hover:border-blue-200 border border-transparent rounded-lg cursor-pointer transition-all duration-200"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900 mb-1">
                          {patient.PNAME || '이름 없음'}
                        </div>
                        <div className="text-sm text-gray-600 space-y-1">
                          {formattedBirth && (
                            <div className="flex items-center">
                              <span className="text-gray-500 w-20">생년월일:</span>
                              <span className="font-medium">{formattedBirth}</span>
                            </div>
                          )}
                          {displayPidnum && (
                            <div className="flex items-center hidden">
                              <span className="text-gray-500 w-20">주민번호:</span>
                              <span className="font-mono text-xs">{displayPidnum}</span>
                            </div>
                          )}
                          {patient.PCODE && (
                            <div className="flex items-center hidden">
                              <span className="text-gray-500 w-20">코드:</span>
                              <span className="font-medium text-primary-600">{patient.PCODE}</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="ml-3 flex items-center">
                        <svg 
                          className="w-5 h-5 text-gray-400" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M9 5l7 7-7 7" 
                          />
                        </svg>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}
        
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

      {/* 선택된 환자 정보 표시 */}
      {selectedPatient && (
        <div className="card mb-4">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <div className="font-semibold text-gray-900 mb-1">
                {selectedPatient.PNAME || '이름 없음'}
              </div>
              <div className="text-sm text-gray-600 space-y-1">
                {formatDate(selectedPatient.PBIRTH) && (
                  <div className="flex items-center">
                    <span className="text-gray-500 w-20">생년월일:</span>
                    <span className="font-medium">{formatDate(selectedPatient.PBIRTH)}</span>
                  </div>
                )}
                {selectedPatient.PIDNUM && (
                  <div className="flex items-center">
                    <span className="text-gray-500 w-20">주민번호:</span>
                    <span className="font-mono text-xs">
                      {selectedPatient.PIDNUM.length > 20 
                        ? `${selectedPatient.PIDNUM.substring(0, 12)}...` 
                        : selectedPatient.PIDNUM}
                    </span>
                  </div>
                )}
                {selectedPatient.PCODE && (
                  <div className="flex items-center">
                    <span className="text-gray-500 w-20">코드:</span>
                    <span className="font-medium text-primary-600">{selectedPatient.PCODE}</span>
                  </div>
                )}
              </div>
            </div>
            <button
              onClick={() => setSelectedPatient(null)}
              className="ml-3 text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* 환자 정보 폼 */}
      {showPatientForm && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">인적사항</h2>
            <button
              onClick={() => {
                setShowPatientForm(false)
                setSelectedPatient(null)
              }}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <PatientForm patient={selectedPatient} />
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

