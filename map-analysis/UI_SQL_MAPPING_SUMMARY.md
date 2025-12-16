# UI 요소와 SQL 쿼리 매핑 요약

## 📊 분석 결과

- **UI 요소**: 67개
- **SQL 쿼리**: 30개
- **매핑된 항목**: 46개

## 🎯 주요 버튼과 SQL 쿼리 매핑

### 1. 접수 버튼 (`접수`)
**기능**: 환자 접수 등록
**관련 SQL**:
```sql
-- 가족 정보 생성
INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
UPDATE LAST SET FCODE = :Fcode
UPDATE PERSON SET FCODE = :Fcode WHERE ...

-- 환자 정보 업데이트
UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, ...
```

### 2. 수정 버튼 (`수정`)
**기능**: 환자 정보 수정
**관련 SQL**:
```sql
UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, 
       PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, ... WHERE ...
```

### 3. 신체계측 버튼 (`신체계측`)
**기능**: 환자 신체 계측 정보 입력
**관련 SQL**:
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

### 4. 수납 버튼 (`수납`)
**기능**: 수납 처리
**관련 SQL**:
```sql
UPDATE FEELOG SET 
    MISU = :Misu,      -- 미수금
    WHANBUL = :Whanbul, -- 완불
    WHANSU = :Whansu    -- 완수
WHERE ...
```

### 5. 접종 버튼 (`접종`)
**기능**: 예방접종 정보 관리
**관련 SQL**:
```sql
DELETE FROM VAX2 WHERE ...
```

### 6. 새가족 버튼 (`새가족`)
**기능**: 새 가족 등록
**관련 SQL**:
```sql
INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
```

## 📝 입력 필드와 SQL 쿼리 매핑

### 인적사항 입력 필드

| UI 필드명 | DB 필드명 | 테이블 | SQL 쿼리 타입 |
|---------|----------|--------|--------------|
| 수진자명 | PNAME | PERSON | UPDATE |
| 관계 | RELATION | PERSON | UPDATE |
| 개인번호 | PCODE | PERSON | UPDATE |
| 주민번호 | PIDNUM, PIDNUM2 | PERSON | UPDATE |
| 생년월일 | PBIRTH | PERSON | UPDATE |
| 성별 (남/여) | SEX | PERSON | UPDATE |
| 장애인 | CRIPPLED | PERSON | UPDATE |
| 급여제한자 | BOHUN | PERSON | UPDATE |
| 개인정보활용 동의 | AGREE | PERSON | UPDATE |

**관련 SQL**:
```sql
UPDATE PERSON SET 
    PNAME = :Pname, 
    PBIRTH = :Pbirth, 
    PIDNUM = :Pidnum, 
    PIDNUM2 = :Pidnum2, 
    SEX = :Sex, 
    RELATION = :Relation, 
    RELATION2 = :Relation2, 
    CRIPPLED = :Crippled, 
    BOHUN = :Bohun, 
    AGREE = :Agree, 
    ...
WHERE ...
```

### 가족 정보 입력 필드

| UI 필드명 | DB 필드명 | 테이블 | SQL 쿼리 타입 |
|---------|----------|--------|--------------|
| 세대주명 | FNAME | CARD | UPDATE |
| 가족번호 | FCODE | FAMILY | INSERT, UPDATE |
| 주민번호 | FIDNUM | CARD | UPDATE |
| 적용기간 시작 | BEGINDATE | CARD | UPDATE |
| 적용기간 종료 | ENDDATE | CARD | UPDATE |
| 구분 | CARETYPE | CARD | UPDATE |
| 증번호 | CARDNUM | CARD | UPDATE |
| 직장 | COMPANY | CARD | UPDATE |

**관련 SQL**:
```sql
-- 가족 정보 생성
INSERT INTO FAMILY (FCODE) VALUES (:Fcode)

-- 카드 정보 업데이트
UPDATE CARD SET 
    ENDDATE = :EndDate, 
    BEGINDATE = :BeginDate, 
    FNAME = :Fname, 
    FIDNUM = :Fidnum, 
    UNIONCODE = :UnionCode, 
    CARDNUM = :CardNum, 
    COMPANY = :Company, 
    CARETYPE = :CareType, 
    ...
WHERE ...
```

### 신체계측 (Vital) 입력 필드

| UI 필드명 | DB 필드명 | 테이블 | SQL 쿼리 타입 |
|---------|----------|--------|--------------|
| 체중 | WEIGHT | CHECKPERSON | UPDATE |
| 키 | HEIGHT | CHECKPERSON | UPDATE |
| 체온 | TEMPERATUR | CHECKPERSON | UPDATE |
| 맥박 | PULSE | CHECKPERSON | UPDATE |
| 수축기혈압 | SYSTOLIC | CHECKPERSON | UPDATE |
| 이완기혈압 | DIASTOLIC | CHECKPERSON | UPDATE |

**관련 SQL**:
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

### 수납 정보 입력 필드

| UI 필드명 | DB 필드명 | 테이블 | SQL 쿼리 타입 |
|---------|----------|--------|--------------|
| 미수금 | MISU | FEELOG | UPDATE |
| 완불 | WHANBUL | FEELOG | UPDATE |
| 완수 | WHANSU | FEELOG | UPDATE |

**관련 SQL**:
```sql
UPDATE FEELOG SET 
    MISU = :Misu, 
    WHANBUL = :Whanbul, 
    WHANSU = :Whansu 
WHERE ...
```

### 진료 정보 입력 필드

| UI 필드명 | DB 필드명 | 테이블 | SQL 쿼리 타입 |
|---------|----------|--------|--------------|
| 접수 | ACCEPT | MASTERAUX | UPDATE |
| 접수번호 | ACCEPTNUM | MASTERAUX | UPDATE |
| 접수번호2 | ACCEPTNUM2 | MASTERAUX | UPDATE |
| 진단 | DX2 | MASTERAUX | UPDATE |
| 진단특기 | DX2SP | MASTERAUX | UPDATE |
| 처방번호 | PRESNUM2 | MASTERAUX | UPDATE |
| 요양비 | CAREFEE | MASTERAUX | UPDATE |
| 예약수수료 | PREGFEE | MASTERAUX | UPDATE |

**관련 SQL**:
```sql
UPDATE MASTERAUX SET 
    ACCEPT = :Accept, 
    ACCEPTNUM = :AcceptNum, 
    ACCEPTNUM2 = :AcceptNum2, 
    DX2 = :Dx2, 
    DX2SP = :Dx2Sp, 
    PRESNUM2 = :PresNum2, 
    CAREFEE = :CareFee, 
    PREGFEE = :PregFee, 
    ...
WHERE ...
```

## 📑 탭과 SQL 쿼리 매핑

### 접수업무 탭
- **관련 테이블**: PERSON, CARD, FAMILY, MASTERAUX
- **주요 기능**: 환자 접수, 정보 수정, 가족 등록

### 인적조회 탭
- **관련 테이블**: PERSON
- **주요 기능**: 환자 정보 조회

### 카드조회 탭
- **관련 테이블**: CARD, FAMILY
- **주요 기능**: 보험카드 정보 조회

### 진료기록 탭
- **관련 테이블**: MASTERAUX, CHECKPERSON, FEELOG
- **주요 기능**: 진료 기록 조회

### 인적사항 서브탭
- **관련 테이블**: PERSON
- **주요 기능**: 환자 기본 정보 관리

### Vital 서브탭
- **관련 테이블**: CHECKPERSON
- **주요 기능**: 신체 계측 정보 관리

### 예방접종 서브탭
- **관련 테이블**: VAX2
- **주요 기능**: 예방접종 정보 관리

### 가족명단 서브탭
- **관련 테이블**: FAMILY, PERSON
- **주요 기능**: 가족 목록 조회

### 보험카드 서브탭
- **관련 테이블**: CARD
- **주요 기능**: 보험카드 정보 관리

## 🗂️ 테이블별 UI 요소 정리

### PERSON 테이블
**관련 UI 요소**:
- 수진자명 (input)
- 관계 (input)
- 개인번호 (input)
- 주민번호 (input)
- 생년월일 (input)
- 성별 (radio)
- 장애인 (checkbox)
- 급여제한자 (checkbox)
- 개인정보활용 동의 (checkbox)

**사용되는 SQL 쿼리**:
- `UPDATE PERSON SET PNAME = :Pname, ... WHERE ...`
- `UPDATE PERSON SET BLOODTYPE = :BloodType WHERE ...`
- `UPDATE PERSON SET PICTURE = :Picture WHERE ...`
- `UPDATE PERSON SET LASTCHECK = :LastCheck WHERE ...`
- `DELETE FROM PERSON WHERE ...`

### CARD 테이블
**관련 UI 요소**:
- 세대주명 (input)
- 주민번호 (input)
- 적용기간 시작/종료 (date)
- 구분 (dropdown)
- 증번호 (input)
- 직장 (input)

**사용되는 SQL 쿼리**:
- `UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, ... WHERE ...`
- `UPDATE CARD SET FNAME = :Fname WHERE ...`
- `DELETE FROM CARD WHERE ...`

### CHECKPERSON 테이블
**관련 UI 요소**:
- 체중 (input)
- 키 (input)
- 체온 (input)
- 맥박 (input)
- 수축기혈압 (input)
- 이완기혈압 (input)

**사용되는 SQL 쿼리**:
- `UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, ... WHERE ...`
- `DELETE FROM CHECKPERSON WHERE ...`

### FEELOG 테이블
**관련 UI 요소**:
- 미수금 (input)
- 완불 (input)
- 완수 (input)

**사용되는 SQL 쿼리**:
- `UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu WHERE ...`

### MASTERAUX 테이블
**관련 UI 요소**:
- 접수 (button)
- 접수번호 (input)
- 진단 (input)
- 요양비 (input)
- 예약수수료 (input)

**사용되는 SQL 쿼리**:
- `UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, ... WHERE ...`
- `UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, ... WHERE ...`
- `UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, ... WHERE ...`

### FAMILY 테이블
**관련 UI 요소**:
- 가족번호 (input)
- 새가족 버튼 (button)

**사용되는 SQL 쿼리**:
- `INSERT INTO FAMILY (FCODE) VALUES (:Fcode)`
- `UPDATE FAMILY SET ZIPCODE2 = :ZipCode2, ... WHERE ...`

### VAX2 테이블
**관련 UI 요소**:
- 접종 버튼 (button)
- 예방접종 탭 (tab)

**사용되는 SQL 쿼리**:
- `DELETE FROM VAX2 WHERE ...`

## 🔄 작업 흐름과 SQL 쿼리

### 환자 접수 흐름
1. **접수 버튼 클릭**
   ```sql
   INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
   UPDATE LAST SET FCODE = :Fcode
   ```

2. **인적사항 입력**
   ```sql
   UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, ... WHERE ...
   ```

3. **보험카드 정보 입력**
   ```sql
   UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, ... WHERE ...
   ```

4. **접수 완료**
   ```sql
   UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ... WHERE ...
   ```

### 신체계측 입력 흐름
1. **Vital 탭 선택**
2. **신체계측 버튼 클릭**
3. **체중, 키, 체온 등 입력**
   ```sql
   UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, ... WHERE ...
   ```

### 수납 처리 흐름
1. **수납 탭 선택**
2. **수납 정보 입력**
   ```sql
   UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu WHERE ...
   ```

## 📋 프론트엔드 개발 가이드

### 컴포넌트 구조 제안

```
ReceptionApp
├── HeaderBar
│   ├── ExitButton
│   ├── SettingsButton
│   ├── PersonalInfoButton
│   ├── BodyMeasurementButton → CHECKPERSON UPDATE
│   └── PaymentButton → FEELOG UPDATE
│
├── LeftPanel
│   ├── ReceptionTab
│   │   ├── PatientSearch
│   │   ├── RegisterButton → FAMILY INSERT, PERSON UPDATE
│   │   ├── ModifyButton → PERSON UPDATE
│   │   └── NewFamilyButton → FAMILY INSERT
│   │
│   ├── PersonalInfoTab
│   │   └── PersonalInfoForm → PERSON UPDATE
│   │       ├── NameInput (PNAME)
│   │       ├── BirthDateInput (PBIRTH)
│   │       ├── IdNumberInput (PIDNUM)
│   │       └── GenderRadio (SEX)
│   │
│   └── CardInquiryTab
│       └── CardInfoForm → CARD UPDATE
│
└── RightPanel
    ├── PaymentLedgerTab → FEELOG
    ├── AppointmentTab → MASTERAUX
    └── MedicalHistoryTab → MASTERAUX
```

### API 엔드포인트 매핑

| UI 액션 | HTTP Method | 엔드포인트 | SQL 쿼리 |
|---------|------------|-----------|---------|
| 접수 버튼 | POST | `/api/reception/register` | `INSERT INTO FAMILY`, `UPDATE PERSON` |
| 수정 버튼 | PUT | `/api/patients/:id` | `UPDATE PERSON SET ...` |
| 신체계측 | PUT | `/api/checkperson/:id` | `UPDATE CHECKPERSON SET ...` |
| 수납 | PUT | `/api/feelog/:id` | `UPDATE FEELOG SET ...` |
| 접종 삭제 | DELETE | `/api/vaccination/:id` | `DELETE FROM VAX2 WHERE ...` |

## 📁 생성된 파일

1. **ui_sql_mapping_report.md**: 전체 매핑 보고서 (마크다운)
2. **ui_sql_detailed_mapping.txt**: 상세 매핑 정보 (텍스트)
3. **UI_SQL_MAPPING_SUMMARY.md**: 이 요약 문서

---

**생성 일시**: 2025-12-12
**분석 도구**: ui_sql_mapping.py

