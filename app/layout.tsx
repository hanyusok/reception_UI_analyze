import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '접수 시스템',
  description: '간결한 접수 관리 시스템',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}

