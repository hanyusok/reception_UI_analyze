'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import PatientForm from '@/components/PatientForm'
import ReceptionPanel from '@/components/ReceptionPanel'
import PaymentPanel from '@/components/PaymentPanel'
import VitalPanel from '@/components/VitalPanel'

type TabType = 'reception' | 'patient' | 'payment' | 'vital'

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabType>('reception')

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        {/* 탭 네비게이션 */}
        <div className="mb-6">
          <div className="flex space-x-2 border-b border-gray-200">
            {[
              { id: 'reception', label: '접수업무' },
              { id: 'patient', label: '인적조회' },
              { id: 'payment', label: '수납' },
              { id: 'vital', label: '신체계측' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                className={`px-6 py-3 font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* 탭 컨텐츠 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 왼쪽 패널 */}
          <div className="lg:col-span-2">
            {activeTab === 'reception' && <ReceptionPanel />}
            {activeTab === 'patient' && <PatientForm />}
            {activeTab === 'payment' && <PaymentPanel />}
            {activeTab === 'vital' && <VitalPanel />}
          </div>

          {/* 오른쪽 패널 - 대기 목록 */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">대기 목록</h2>
              <div className="space-y-2">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium">홍길동</div>
                  <div className="text-sm text-gray-600">2024-01-15 14:30</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

