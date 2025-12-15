# Database Schema Mapping

**Date**: 2025-01-15  
**Source**: Extracted SQL queries from `extracted_sql_queries.txt`  
**Database**: Firebird 2.5

## Overview

This document provides a comprehensive schema mapping based on SQL queries extracted from the original application. The schema represents the database structure used by the reception system.

## Table Relationships

```
PERSON (환자)
  ├── CARD (보험카드) [1:N via PCODE]
  ├── FAMILY (가족) [N:1 via FCODE]
  ├── MASTERAUX (진료보조정보) [1:N via PCODE, VISIDATE]
  ├── CHECKPERSON (체크인정보) [1:1 via PCODE, VISIDATE]
  ├── FEELOG (수납로그) [1:N via PCODE, VISIDATE]
  ├── DISEREG (질병등록) [1:N via PCODE]
  └── VAX2 (백신) [1:N via PCODE]

WAIT (대기목록) [Standalone]
LAST (시퀀스/마지막값) [System]
COMPUTER (컴퓨터정보) [System]
VIEWCHECK (조회체크) [System]
```

## Table Schemas

### 1. PERSON (환자 정보 테이블)

**Description**: 환자 기본 정보를 저장하는 메인 테이블

**Primary Key**: `PCODE` (추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Primary Key) | INSERT, UPDATE |
| `PNAME` | VARCHAR | 환자 이름 | UPDATE |
| `PBIRTH` | DATE | 생년월일 | UPDATE |
| `PIDNUM` | VARCHAR | 주민등록번호 (앞자리) | UPDATE |
| `PIDNUM2` | VARCHAR | 주민등록번호 (뒷자리) | UPDATE |
| `SEX` | CHAR(1) | 성별 (M/F) | UPDATE |
| `BLOODTYPE` | VARCHAR | 혈액형 | UPDATE |
| `PICTURE` | BLOB | 사진 | UPDATE |
| `PSNIDT` | VARCHAR | 환자 ID 타입 | UPDATE |
| `PSNID` | VARCHAR | 환자 ID | UPDATE |
| `RELATION` | VARCHAR | 관계 | UPDATE |
| `RELATION2` | VARCHAR | 관계2 | UPDATE |
| `CRIPPLED` | BOOLEAN/SMALLINT | 장애 여부 | UPDATE |
| `BOHUN` | BOOLEAN/SMALLINT | 보훈 여부 | UPDATE |
| `AGREE` | BOOLEAN/SMALLINT | 개인정보활용 동의 | UPDATE |
| `PERINFO` | VARCHAR | 개인정보 | UPDATE |
| `DIABETES` | VARCHAR | 당뇨 | UPDATE |
| `SAMEDATE1` | DATE | 동일 날짜1 | UPDATE |
| `SAMEDATE2` | DATE | 동일 날짜2 | UPDATE |
| `JAEHAN` | VARCHAR | 재한 | UPDATE |
| `SEARCHID` | VARCHAR | 검색 ID | UPDATE |
| `LASTCHECK` | DATE/TIMESTAMP | 마지막 체크 | UPDATE |
| `FCODE` | VARCHAR/INTEGER | 가족 코드 (Foreign Key → FAMILY) | UPDATE |

**Key Operations**:
- `UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, ... WHERE ...`
- `UPDATE PERSON SET BLOODTYPE = :BloodType WHERE ...`
- `UPDATE PERSON SET PICTURE = :Picture WHERE ...`
- `DELETE FROM PERSON WHERE ...`

---

### 2. CARD (보험카드 정보 테이블)

**Description**: 보험 카드 정보 저장

**Primary Key**: `PCODE` (추정, Foreign Key → PERSON)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | INSERT, UPDATE |
| `ENDDATE` | DATE | 유효 기간 종료일 | INSERT, UPDATE |
| `BEGINDATE` | DATE | 유효 기간 시작일 | INSERT, UPDATE |
| `FNAME` | VARCHAR | 세대주명 (가족 이름) | INSERT, UPDATE |
| `FIDNUM` | VARCHAR | 가족 주민번호 | INSERT, UPDATE |
| `UNIONCODE` | VARCHAR | 조합 코드 | INSERT, UPDATE |
| `CARDNUM` | VARCHAR | 카드 번호 | INSERT, UPDATE |
| `COMPANY` | VARCHAR | 직장/회사 | UPDATE |
| `CARETYPE` | VARCHAR | 요양 유형 (A/B/C 등) | INSERT, UPDATE |
| `CHA` | VARCHAR | 차 | INSERT, UPDATE |
| `OTHERAREA` | VARCHAR | 기타 지역 | INSERT, UPDATE |

**Key Operations**:
- `INSERT INTO CARD (PCODE, ENDDATE, BEGINDATE, FNAME, FIDNUM, UNIONCODE, CARDNUM, CARETYPE, CHA, OTHERAREA) VALUES ...`
- `UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, FNAME = :Fname, ... WHERE ...`
- `DELETE FROM CARD WHERE ...`

---

### 3. MASTERAUX (마스터 보조 정보 테이블)

**Description**: 진료 관련 보조 정보 (접수, 진단, 수수료 등)

**Primary Key**: `PCODE`, `VISIDATE` (복합키 추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | INSERT, UPDATE |
| `VISIDATE` | DATE | 방문 날짜 | INSERT, UPDATE |
| `ACCEPT` | VARCHAR/BOOLEAN | 접수 여부 | UPDATE |
| `ACCEPTNUM` | VARCHAR/INTEGER | 접수 번호 | UPDATE |
| `ACCEPTNUM2` | VARCHAR/INTEGER | 접수 번호2 | UPDATE |
| `ERRCODE` | VARCHAR | 오류 코드 | UPDATE |
| `SELFEE2` | DECIMAL | 선택 수수료 | UPDATE |
| `REQCAREFEE2` | DECIMAL | 요청 요양비 | UPDATE |
| `REMCAREFEE` | DECIMAL | 제거 요양비 | UPDATE |
| `REQPREGFEE2` | DECIMAL | 요청 예약 수수료 | UPDATE |
| `REMPREGFEE` | DECIMAL | 제거 예약 수수료 | UPDATE |
| `PRESNUM2` | VARCHAR | 처방 번호 | UPDATE |
| `DX2` | VARCHAR | 진단 | UPDATE |
| `DX2SP` | VARCHAR | 진단 특기 | UPDATE |
| `REQFEE2` | DECIMAL | 요청 수수료 | UPDATE |
| `GENFEE2` | DECIMAL | 일반 수수료 | UPDATE |
| `CHK` | VARCHAR/BOOLEAN | 체크 | UPDATE |
| `SPCODE` | VARCHAR | 특수 코드 | UPDATE |
| `BUDAM` | DECIMAL | 부담금 | UPDATE |
| `CAREFEE` | DECIMAL | 요양비 | UPDATE |
| `PREGFEE` | DECIMAL | 예약 수수료 | UPDATE |
| `PIDNUM` | VARCHAR | 주민등록번호 (복사) | UPDATE |
| `PNAME` | VARCHAR | 환자 이름 (복사) | UPDATE |

**Key Operations**:
- `INSERT INTO MASTERAUX (PCODE, VISIDATE) VALUES ...`
- `UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, ... WHERE ...`
- `UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, ... WHERE ...`

---

### 4. CHECKPERSON (체크인 환자 테이블)

**Description**: 접수 시 신체 계측 정보 (Vital Signs)

**Primary Key**: `PCODE`, `VISIDATE` (복합키 추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | UPDATE |
| `VISIDATE` | DATE | 방문 날짜 (Foreign Key → MASTERAUX) | UPDATE |
| `WEIGHT` | DECIMAL | 체중 (kg) | UPDATE |
| `HEIGHT` | DECIMAL | 키 (cm) | UPDATE |
| `TEMPERATUR` | DECIMAL | 체온 (°C) | UPDATE |
| `PULSE` | INTEGER | 맥박 (bpm) | UPDATE |
| `SYSTOLIC` | INTEGER | 수축기 혈압 (mmHg) | UPDATE |
| `DIASTOLIC` | INTEGER | 이완기 혈압 (mmHg) | UPDATE |

**Key Operations**:
- `UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE ...`
- `DELETE FROM CHECKPERSON WHERE ...`

---

### 5. FEELOG (수납 로그 테이블)

**Description**: 수납 관련 로그

**Primary Key**: `PCODE`, `VISIDATE` (복합키 추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `VISIDATE` | DATE | 방문 날짜 | INSERT, UPDATE |
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | INSERT, UPDATE |
| `PNAME` | VARCHAR | 환자 이름 | INSERT, UPDATE |
| `MISU` | DECIMAL | 미수금 | UPDATE |
| `WHANBUL` | DECIMAL | 완불 | UPDATE |
| `WHANSU` | DECIMAL | 완수 | UPDATE |

**Key Operations**:
- `INSERT INTO FEELOG (VISIDATE, PCODE, PNAME) VALUES ...`
- `UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu WHERE ...`

---

### 6. FAMILY (가족 정보 테이블)

**Description**: 가족 단위 정보

**Primary Key**: `FCODE` (추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `FCODE` | VARCHAR/INTEGER | 가족 코드 (Primary Key) | INSERT, UPDATE |
| `ZIPCODE2` | VARCHAR | 우편번호2 | UPDATE |

**Key Operations**:
- `INSERT INTO FAMILY (FCODE) VALUES (:Fcode)`
- `UPDATE FAMILY SET ZIPCODE2 = :ZipCode2, ... WHERE ...`

---

### 7. DISEREG (질병 등록 테이블)

**Description**: 질병 등록 정보

**Primary Key**: `PCODE`, `DR_TYPE`, `SDATE` (복합키 추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | INSERT, UPDATE |
| `DR_TYPE` | VARCHAR | 질병 유형 | INSERT, UPDATE |
| `DR_STR` | VARCHAR | 질병 문자열 | INSERT, UPDATE |
| `SDATE` | DATE | 시작 날짜 | INSERT, UPDATE |
| `BDATE` | DATE | 종료 날짜 | INSERT, UPDATE |

**Key Operations**:
- `INSERT INTO DISEREG (PCODE, DR_TYPE, DR_STR, SDATE, BDATE) VALUES ...`
- `DELETE FROM DISEREG WHERE ...`

---

### 8. WAIT (대기 목록 테이블)

**Description**: 대기 목록 정보

**Primary Key**: `PCODE`, `VISIDATE` (복합키 추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | INSERT |
| `VISIDATE` | DATE | 방문 날짜 | INSERT |
| `RESID1` | VARCHAR | 예약 ID1 | INSERT |
| `RESID2` | VARCHAR | 예약 ID2 | INSERT |
| `GOODOC` | VARCHAR | 좋은 의사 | INSERT |
| `ROOMCODE` | VARCHAR | 방 코드 | INSERT |
| `ROOMNM` | VARCHAR | 방 이름 | INSERT |
| `DEPTCODE` | VARCHAR | 부서 코드 | INSERT |
| `DEPTNM` | VARCHAR | 부서 이름 | INSERT |
| `DOCTRCODE` | VARCHAR | 의사 코드 | INSERT |
| `DOCTRNM` | VARCHAR | 의사 이름 | INSERT |

**Key Operations**:
- `INSERT INTO WAIT (PCODE, VISIDATE, RESID1, RESID2, GOODOC, ROOMCODE, ROOMNM, DEPTCODE, DEPTNM, DOCTRCODE, DOCTRNM) VALUES ...`

---

### 9. VAX2 (백신 테이블)

**Description**: 예방접종 정보

**Primary Key**: `PCODE` (추정)

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `PCODE` | VARCHAR/INTEGER | 환자 코드 (Foreign Key → PERSON) | DELETE |

**Key Operations**:
- `DELETE FROM VAX2 WHERE ...`

---

### 10. LAST (시퀀스/마지막값 테이블)

**Description**: 시퀀스나 마지막 사용된 값 저장

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `FCODE` | VARCHAR/INTEGER | 마지막 가족 코드 | UPDATE |

**Key Operations**:
- `UPDATE LAST SET FCODE = :Fcode`

---

### 11. VIEWCHECK (조회 체크 테이블)

**Description**: 조회 체크 정보

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `VIEWCHECK` | VARCHAR/BOOLEAN | 조회 체크 | UPDATE |
| `VIEWTEXT` | VARCHAR | 조회 텍스트 | UPDATE |

**Key Operations**:
- `UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE ...`

---

### 12. COMPUTER (컴퓨터 정보 테이블)

**Description**: 컴퓨터 정보

| Field Name | Type | Description | Source |
|------------|------|-------------|--------|
| `COMPUTER` | VARCHAR | 컴퓨터 이름/ID | INSERT |

**Key Operations**:
- `INSERT INTO COMPUTER (COMPUTER) VALUES ...`

---

## Field Type Mappings

### Firebird Data Types

Based on the extracted queries and Firebird 2.5 conventions:

| SQL Usage | Firebird Type | Notes |
|-----------|---------------|-------|
| `:Pname`, `:Fname` | `VARCHAR(n)` | String values |
| `:Pbirth`, `:EndDate` | `DATE` | Date values |
| `:Pcode`, `:AcceptNum` | `INTEGER` or `VARCHAR` | Numeric IDs |
| `:Crippled`, `:Bohun`, `:Agree` | `SMALLINT` (0/1) | Boolean flags |
| `:Weight`, `:Height`, `:Misu` | `DECIMAL(10,2)` | Decimal values |
| `:Picture` | `BLOB` | Binary data |

## API Endpoint Mapping

Based on the schema, here are the recommended API endpoints:

### Patient Management
- `GET /api/patients` - List patients (PERSON)
- `GET /api/patients/:id` - Get patient details (PERSON)
- `POST /api/patients` - Create patient (PERSON)
- `PUT /api/patients/:id` - Update patient (PERSON)
- `DELETE /api/patients/:id` - Delete patient (PERSON)

### Card Management
- `GET /api/patients/:id/card` - Get patient card (CARD)
- `POST /api/patients/:id/card` - Create/update card (CARD)
- `PUT /api/patients/:id/card` - Update card (CARD)
- `DELETE /api/patients/:id/card` - Delete card (CARD)

### Visit Management
- `GET /api/visits` - List visits (MASTERAUX)
- `GET /api/visits/:patientId/:visitDate` - Get visit details (MASTERAUX)
- `POST /api/visits` - Create visit (MASTERAUX)
- `PUT /api/visits/:patientId/:visitDate` - Update visit (MASTERAUX)

### Vital Signs
- `GET /api/vitals/:patientId/:visitDate` - Get vital signs (CHECKPERSON)
- `POST /api/vitals/:patientId/:visitDate` - Create vital signs (CHECKPERSON)
- `PUT /api/vitals/:patientId/:visitDate` - Update vital signs (CHECKPERSON)

### Payment
- `GET /api/payments/:patientId` - Get payment history (FEELOG)
- `POST /api/payments` - Create payment record (FEELOG)
- `PUT /api/payments/:patientId/:visitDate` - Update payment (FEELOG)

### Family
- `GET /api/families/:fcode` - Get family (FAMILY)
- `POST /api/families` - Create family (FAMILY)
- `PUT /api/families/:fcode` - Update family (FAMILY)

## Notes

1. **Primary Keys**: Most tables use `PCODE` as part of the primary key. Composite keys are common (e.g., `PCODE` + `VISIDATE`).

2. **Foreign Keys**: 
   - `PCODE` references `PERSON.PCODE`
   - `FCODE` references `FAMILY.FCODE`
   - `VISIDATE` + `PCODE` may reference `MASTERAUX`

3. **Data Types**: Firebird 2.5 uses:
   - `SMALLINT` for boolean values (0/1)
   - `VARCHAR(n)` for strings
   - `DATE` for dates
   - `DECIMAL(p,s)` for monetary/numeric values
   - `BLOB` for binary data

4. **Parameter Binding**: All queries use `:Parameter` syntax (Firebird/InterBase style).

5. **Missing Information**: Some fields may have additional constraints, indexes, or relationships not visible in the extracted queries.

## Validation Schema (Zod)

Based on this schema, here are TypeScript/Zod validation schemas that could be used:

```typescript
// Patient Schema
const patientSchema = z.object({
  pcode: z.string().optional(),
  pname: z.string(),
  pbirth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  pidnum: z.string().optional(),
  pidnum2: z.string().optional(),
  sex: z.enum(['M', 'F']),
  crippled: z.boolean().default(false),
  bohun: z.boolean().default(false),
  agree: z.boolean().default(false),
});

// Card Schema
const cardSchema = z.object({
  pcode: z.string(),
  enddate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  begindate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  fname: z.string(),
  fidnum: z.string().optional(),
  unioncode: z.string().optional(),
  cardnum: z.string().optional(),
  company: z.string().optional(),
  caretype: z.string().optional(),
  cha: z.string().optional(),
  otherarea: z.string().optional(),
});

// Vital Signs Schema
const vitalSchema = z.object({
  pcode: z.string(),
  visidate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  weight: z.number().positive().optional(),
  height: z.number().positive().optional(),
  temperatur: z.number().optional(),
  pulse: z.number().int().positive().optional(),
  systolic: z.number().int().positive().optional(),
  diastolic: z.number().int().positive().optional(),
});

// Payment Schema
const paymentSchema = z.object({
  pcode: z.string(),
  visidate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  misu: z.number().default(0),
  whanbul: z.number().default(0),
  whansu: z.number().default(0),
});
```

---

**Last Updated**: 2025-01-15  
**Source Files**: 
- `extracted_sql_queries.txt`
- `SQL_QUERY_ANALYSIS_SUMMARY.md`
- `UI_SQL_MAPPING_SUMMARY.md`

