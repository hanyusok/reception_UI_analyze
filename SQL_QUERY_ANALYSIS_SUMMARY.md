# SQL 쿼리 분석 요약 보고서

## 📊 전체 통계

- **전체 추출된 쿼리**: 168개
- **유효한 쿼리**: 30개 (17.9%)
- **깨진 쿼리**: 122개 (72.6%)
- **유효하지 않은 내용**: 16개 (9.5%)

## ✅ 유효한 쿼리 분석

### 카테고리별 분포

| 카테고리 | 개수 | 비율 |
|---------|------|------|
| UPDATE | 21개 | 70% |
| DELETE | 7개 | 23.3% |
| CREATE_TABLE | 1개 | 3.3% |
| INSERT | 1개 | 3.3% |

### 발견된 주요 테이블

#### 1. **PERSON** (환자 정보 테이블)
- 환자 기본 정보를 저장하는 메인 테이블
- 주요 필드:
  - `PNAME`: 환자 이름
  - `PBIRTH`: 생년월일
  - `PIDNUM`, `PIDNUM2`: 주민등록번호
  - `SEX`: 성별
  - `BLOODTYPE`: 혈액형
  - `PICTURE`: 사진
  - `PSNIDT`, `PSNID`: 환자 ID
  - `RELATION`, `RELATION2`: 관계
  - `CRIPPLED`: 장애 여부
  - `BOHUN`: 보훈 여부
  - `AGREE`: 동의 여부
  - `PERINFO`: 개인정보
  - `DIABETES`: 당뇨
  - `SAMEDATE1`, `SAMEDATE2`: 동일 날짜
  - `JAEHAN`: 재한
  - `SEARCHID`: 검색 ID
  - `LASTCHECK`: 마지막 체크

**주요 쿼리**:
```sql
UPDATE PERSON SET BLOODTYPE = :BloodType WHERE ...
UPDATE PERSON SET PICTURE = :Picture WHERE ...
UPDATE PERSON SET PSNIDT = :PsnIdT WHERE ...
UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE ...
UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, ... WHERE ...
UPDATE PERSON SET LASTCHECK = :LastCheck WHERE ...
DELETE FROM PERSON WHERE ...
```

#### 2. **MASTERAUX** (마스터 보조 정보 테이블)
- 진료 관련 보조 정보
- 주요 필드:
  - `PCODE`: 환자 코드
  - `VISIDATE`: 방문 날짜
  - `ACCEPT`, `ACCEPTNUM`, `ACCEPTNUM2`: 접수 관련
  - `ERRCODE`: 오류 코드
  - `SELFEE2`: 선택 수수료
  - `REQCAREFEE2`, `REMCAREFEE`: 요양비 관련
  - `REQPREGFEE2`, `REMPREGFEE`: 예약 수수료 관련
  - `PRESNUM2`: 처방 번호
  - `DX2`, `DX2SP`: 진단 관련
  - `REQFEE2`: 요청 수수료
  - `GENFEE2`: 일반 수수료
  - `CHK`: 체크
  - `SPCODE`: 특수 코드
  - `BUDAM`: 부담금
  - `CAREFEE`: 요양비
  - `PREGFEE`: 예약 수수료

**주요 쿼리**:
```sql
UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, ... WHERE ...
UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, ... WHERE ...
UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, ... WHERE ...
UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, ... WHERE ...
```

#### 3. **CARD** (카드 정보 테이블)
- 보험 카드 정보
- 주요 필드:
  - `PCODE`: 환자 코드
  - `ENDDATE`, `BEGINDATE`: 유효 기간
  - `FNAME`: 가족 이름
  - `FIDNUM`: 가족 주민번호
  - `UNIONCODE`: 조합 코드
  - `CARDNUM`: 카드 번호
  - `COMPANY`: 회사
  - `CARETYPE`: 요양 유형
  - `CHA`: 차
  - `OTHERAREA`: 기타 지역

**주요 쿼리**:
```sql
UPDATE CARD SET ENDDATE = :EDate1 WHERE ...
UPDATE CARD SET FNAME = :Fname WHERE ...
UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, FNAME = :Fname, ... WHERE ...
DELETE FROM CARD WHERE ...
```

#### 4. **CHECKPERSON** (체크인 환자 테이블)
- 접수 시 체크인 정보
- 주요 필드:
  - `WEIGHT`: 체중
  - `HEIGHT`: 키
  - `TEMPERATUR`: 체온
  - `PULSE`: 맥박
  - `SYSTOLIC`: 수축기 혈압
  - `DIASTOLIC`: 이완기 혈압

**주요 쿼리**:
```sql
UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, 
       PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE ...
DELETE FROM CHECKPERSON WHERE ...
```

#### 5. **FEELOG** (수납 로그 테이블)
- 수납 관련 로그
- 주요 필드:
  - `MISU`: 미수
  - `WHANBUL`: 완불
  - `WHANSU`: 완수

**주요 쿼리**:
```sql
UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu WHERE ...
```

#### 6. **기타 테이블**
- **DISEREG**: 질병 등록 테이블
  ```sql
  CREATE TABLE DISEREG (...)
  DELETE FROM DISEREG WHERE ...
  ```

- **VAX2**: 백신 관련 테이블
  ```sql
  DELETE FROM VAX2 WHERE ...
  ```

- **DUO**: 기타 테이블
  ```sql
  DELETE FROM DUO WHERE ...
  ```

- **VIEWCHECK**: 조회 체크 테이블
  ```sql
  UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE ...
  ```

- **FAMILY**: 가족 정보 테이블
  ```sql
  INSERT INTO FAMILY (FCODE) VALUES (:Fcode)
  ```

- **LAST**: 마지막 정보 테이블
  ```sql
  UPDATE LAST SET FCODE = :Fcode
  ```

## ⚠️ 문제점 분석

### 1. 깨진 쿼리 (122개, 72.6%)

**원인**:
- 인코딩 문제 (UTF-16 변환 오류)
- 불완전한 쿼리 (WHERE 절 누락, VALUES 절 누락 등)
- 바이너리 데이터 혼입
- 제어 문자 포함

**예시**:
```sql
INSERT INTO DUO? ?? VALUES  -- 불완전한 쿼리
INSERT INTO WAIT? ?? (PCODE, VISIDATE, ...) VALUES  -- 인코딩 오류로 특수문자 포함
```

### 2. 유효하지 않은 내용 (16개, 9.5%)

**원인**:
- Delphi 컴포넌트 코드 (TStringGrid, TComponent 등)
- 에러 메시지 텍스트
- 바이너리 데이터

**예시**:
```
delete from dataset. (No delete query)&Cannot refresh row...
TStringGrid grdRegInfo Left Top Width Height...
```

## 📋 프론트엔드 UI 개발을 위한 권장사항

### 1. 데이터 모델 설계

다음과 같은 주요 엔티티를 식별했습니다:

```
Person (환자)
  ├── Card (보험카드)
  ├── Family (가족)
  ├── MasterAux (진료보조정보)
  ├── CheckPerson (체크인정보)
  ├── Feelog (수납로그)
  ├── Disereg (질병등록)
  └── Vax2 (백신)
```

### 2. 주요 화면 구성 제안

#### 환자 관리 화면
- 환자 기본 정보 (PERSON 테이블)
- 보험 카드 정보 (CARD 테이블)
- 가족 정보 (FAMILY 테이블)

#### 접수/진료 화면
- 접수 정보 (MASTERAUX 테이블)
- 체크인 정보 (CHECKPERSON 테이블)
- 진단 정보 (MASTERAUX.DX2, DX2SP)

#### 수납 화면
- 수납 로그 (FEELOG 테이블)
- 수수료 정보 (MASTERAUX의 각종 FEE 필드)

### 3. API 엔드포인트 설계 제안

```
GET    /api/persons              # 환자 목록 조회
GET    /api/persons/:id          # 환자 상세 조회
PUT    /api/persons/:id          # 환자 정보 수정
DELETE /api/persons/:id          # 환자 삭제

GET    /api/persons/:id/card     # 보험카드 조회
PUT    /api/persons/:id/card     # 보험카드 수정

GET    /api/visits               # 방문 목록
GET    /api/visits/:id           # 방문 상세 (MASTERAUX)
PUT    /api/visits/:id           # 방문 정보 수정

GET    /api/checkperson/:id      # 체크인 정보 조회
PUT    /api/checkperson/:id      # 체크인 정보 수정

GET    /api/feelog               # 수납 로그 조회
PUT    /api/feelog/:id           # 수납 로그 수정
```

### 4. 주의사항

1. **파라미터 바인딩**: 모든 쿼리가 `:Parameter` 형식의 바인딩을 사용하므로, SQL Injection 방지를 위해 반드시 파라미터화된 쿼리를 사용해야 합니다.

2. **WHERE 절**: 대부분의 쿼리에서 WHERE 절이 생략되어 있으므로, 실제 사용 시 적절한 조건을 추가해야 합니다.

3. **NULL 처리**: MASTERAUX 테이블의 UPDATE 쿼리에서 NULL 값 설정이 많으므로, 프론트엔드에서 NULL 처리 로직이 필요합니다.

4. **트랜잭션**: 일부 쿼리가 트랜잭션으로 묶여 있을 수 있으므로 (예: LAST, FAMILY, PERSON 업데이트), 관련 작업은 트랜잭션으로 처리해야 합니다.

## 📁 생성된 파일

1. **sql_query_review_report.txt**: 전체 검토 보고서
2. **valid_sql_queries.txt**: 유효한 쿼리만 정리된 파일
3. **SQL_QUERY_ANALYSIS_SUMMARY.md**: 이 요약 문서

## 🔍 다음 단계

1. 실제 데이터베이스 파일을 찾아 스키마를 직접 확인
2. SELECT 쿼리를 더 많이 추출 (현재는 UPDATE/DELETE 위주)
3. 테이블 간 관계(Relationship) 파악
4. 인덱스 및 제약조건 확인

---

**분석 일시**: 2025-12-12
**분석 도구**: review_sql_queries.py

