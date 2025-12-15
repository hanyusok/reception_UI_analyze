'use client'

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-primary-600">접수 시스템</h1>
            <span className="text-sm text-gray-500">
              {new Date().toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long',
              })}
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            <button className="btn-secondary text-sm">설정</button>
            <button className="btn-secondary text-sm">종료</button>
          </div>
        </div>
      </div>
    </header>
  )
}

