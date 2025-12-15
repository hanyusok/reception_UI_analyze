# 접수 시스템 UI

웹 브라우저 기반의 간결하고 핵심적인 접수 관리 시스템입니다.

## 기술 스택

- **Next.js 14** - React 프레임워크
- **TypeScript** - 타입 안정성
- **Tailwind CSS** - 유틸리티 기반 스타일링
- **React Hooks** - 상태 관리

## 주요 기능

### 1. 접수업무
- 환자 검색
- 환자 접수 등록
- 인적사항 입력/수정
- 가족/보험카드 정보 관리

### 2. 인적조회
- 환자 정보 조회 및 수정

### 3. 수납
- 수납 정보 입력 (미수금, 완불, 완수)
- 수납 내역 조회

### 4. 신체계측
- 체중, 키, 체온, 맥박, 혈압 입력

## 설치 및 실행

### 1. 의존성 설치

```bash
npm install
```

### 2. 원격 REST API 서비스 설정

이 프로젝트는 원격 RESTful API 서비스를 통해 데이터를 가져옵니다.
원격 API 서비스가 Firebird 2.5 데이터베이스에 연결되어 있습니다.

### 3. 환경 변수 설정

`.env.local` 파일을 생성하고 다음 내용을 추가하세요:

```env
# 원격 REST API 서비스 URL
API_BASE_URL=http://localhost:3000
# 또는
REMOTE_API_URL=http://your-api-server:port
```

### 4. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

### 3. 프로덕션 빌드

```bash
npm run build
npm start
```

## 프로젝트 구조

```
├── app/
│   ├── layout.tsx          # 루트 레이아웃
│   ├── page.tsx            # 메인 페이지
│   └── globals.css         # 전역 스타일
├── components/
│   ├── Header.tsx          # 헤더 컴포넌트
│   ├── ReceptionPanel.tsx  # 접수 패널
│   ├── PatientForm.tsx    # 환자 정보 폼
│   ├── CardForm.tsx        # 카드 정보 폼
│   ├── VitalPanel.tsx      # 신체계측 패널
│   └── PaymentPanel.tsx   # 수납 패널
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

## SQL 쿼리 매핑

각 UI 컴포넌트는 다음과 같은 SQL 쿼리와 매핑됩니다:

### 환자 정보 (PatientForm)
```sql
UPDATE PERSON SET 
  PNAME = :Pname, 
  PBIRTH = :Pbirth, 
  PIDNUM = :Pidnum, 
  PIDNUM2 = :Pidnum2, 
  SEX = :Sex, 
  RELATION = :Relation, 
  CRIPPLED = :Crippled, 
  BOHUN = :Bohun, 
  AGREE = :Agree 
WHERE ...
```

### 가족/카드 정보 (CardForm)
```sql
INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
UPDATE CARD SET 
  ENDDATE = :EndDate, 
  BEGINDATE = :BeginDate, 
  FNAME = :Fname, 
  FIDNUM = :Fidnum, 
  CARETYPE = :CareType, 
  ...
WHERE ...
```

### 신체계측 (VitalPanel)
```sql
UPDATE CHECKPERSON SET 
  WEIGHT = :WEIGHT, 
  HEIGHT = :HEIGHT, 
  TEMPERATUR = :TEMPERATUR, 
  PULSE = :PULSE, 
  SYSTOLIC = :SYSTOLIC, 
  DIASTOLIC = :DIASTOLIC 
WHERE ...
```

### 수납 (PaymentPanel)
```sql
UPDATE FEELOG SET 
  MISU = :Misu, 
  WHANBUL = :Whanbul, 
  WHANSU = :Whansu 
WHERE ...
```

## 완료된 기능

✅ **API 연동**: Next.js API Routes를 통한 백엔드 연동
✅ **데이터 검증**: Zod를 사용한 폼 입력값 검증
✅ **에러 처리**: 에러 메시지 및 예외 처리
✅ **로딩 상태**: 데이터 로딩 중 상태 표시
✅ **Firebird 연동**: 데이터베이스 연결 설정 (Firebird 2.5)

## 다음 단계

1. **데이터베이스 설정**: `DATABASE_SETUP.md` 참고하여 Firebird 데이터베이스 설정
2. **환경 변수 설정**: `.env.local` 파일 생성 및 데이터베이스 연결 정보 입력
3. **인증/인가**: 사용자 로그인 및 권한 관리
4. **테스트**: 각 기능별 테스트 작성

## 참고 문서

- [Next.js 문서](https://nextjs.org/docs)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [UI_SQL_MAPPING_SUMMARY.md](./UI_SQL_MAPPING_SUMMARY.md) - UI와 SQL 쿼리 매핑 상세 정보

