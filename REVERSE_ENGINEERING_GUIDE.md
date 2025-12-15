# DeskPro.exe 리버스 엔지니어링 가이드

이 가이드는 DeskPro.exe 실행 파일에서 SQL 쿼리를 추출하여 프론트엔드 UI 개발을 위한 기초 자료를 만드는 방법을 설명합니다.

## 📋 목차

1. [개요](#개요)
2. [필요한 도구](#필요한-도구)
3. [추출 방법](#추출-방법)
4. [스크립트 사용법](#스크립트-사용법)
5. [고급 방법](#고급-방법)

## 개요

DeskPro.exe는 SQLite 데이터베이스를 사용하는 것으로 보입니다 (`sqlite3.dll` 존재). SQL 쿼리를 추출하는 방법은 여러 가지가 있습니다:

1. **정적 분석**: 실행 파일에서 문자열 추출
2. **동적 분석**: 실행 중 메모리/네트워크 모니터링
3. **데이터베이스 분석**: SQLite 파일 직접 분석

## 필요한 도구

### 필수 도구
- Python 3.7+
- 필요한 Python 패키지:
  ```bash
  pip install psutil
  ```

### 선택적 도구 (고급 분석)
- **IDA Pro** 또는 **Ghidra**: 디스어셈블러
- **x64dbg**: 디버거
- **Process Monitor**: 파일/레지스트리 모니터링
- **Wireshark**: 네트워크 트래픽 분석
- **Strings.exe**: 문자열 추출 도구

## 추출 방법

### 방법 0: PE 파일 구조 분석 (코드 분석)

**사용 스크립트**: `analyze_pe_structure.py`

```bash
python analyze_pe_structure.py
```

이 스크립트는:
- PE 파일 구조를 파싱하여 섹션 정보 추출
- SQLite 함수 호출 패턴 분석
- DLL 임포트 정보 추출
- 섹션별 문자열 분석
- 결과를 `pe_analysis_report.txt`에 저장

**장점**: 실제 코드 구조를 이해할 수 있음
**단점**: PE 파일 구조 지식 필요

### 방법 0-1: 고급 코드 분석

**사용 스크립트**: `advanced_code_analysis.py`

```bash
python advanced_code_analysis.py
```

이 스크립트는:
- SQLite 함수 호출 주변 컨텍스트 분석
- Windows API 호출 패턴 추출
- 함수 호출 패턴 분석
- 데이터 구조 및 테이블 이름 추정
- 결과를 `advanced_analysis_report.txt`에 저장

**장점**: 더 깊은 코드 분석, 함수 호출 관계 파악
**단점**: 시간이 오래 걸림

### 방법 1: 문자열 추출 (가장 간단)

**사용 스크립트**: `extract_sql_strings.py`

```bash
python extract_sql_strings.py
```

이 스크립트는:
- 실행 파일에서 SQL 키워드(SELECT, INSERT, UPDATE 등)를 포함한 문자열을 추출
- 여러 인코딩(UTF-8, UTF-16, CP949)으로 시도
- 결과를 `extracted_sql_queries.txt`에 저장

**장점**: 빠르고 간단
**단점**: 완전한 쿼리를 찾지 못할 수 있음

### 방법 2: 데이터베이스 모니터링

**사용 스크립트**: `monitor_sqlite.py`

```bash
python monitor_sqlite.py
```

이 스크립트는:
- 시스템에서 SQLite 데이터베이스 파일을 자동으로 찾음
- 데이터베이스 스키마를 추출
- 실행 중 변경사항을 모니터링하여 사용되는 쿼리를 추론

**사용 순서**:
1. 스크립트 실행하여 데이터베이스 파일 위치 확인
2. DeskPro.exe 실행
3. 프로그램의 각 기능을 사용
4. 스크립트가 변경사항을 기록

**장점**: 실제 사용되는 쿼리 패턴 파악 가능
**단점**: 간접적인 방법, 모든 쿼리를 캡처하지 못할 수 있음

### 방법 3: 메모리 덤프 분석

**사용 스크립트**: `extract_from_memory.py`

```bash
# DeskPro.exe를 먼저 실행한 후
python extract_from_memory.py
```

이 스크립트는:
- 실행 중인 프로세스의 메모리를 스캔
- 메모리에서 SQL 쿼리 문자열을 추출

**주의**: 관리자 권한이 필요할 수 있습니다.

**장점**: 실행 중 실제 사용되는 쿼리 추출 가능
**단점**: 시간이 오래 걸리고, 일부 쿼리는 찾지 못할 수 있음

## 스크립트 사용법

### 1단계: 환경 설정

```bash
# Python 패키지 설치
pip install psutil
```

### 2단계: 기본 추출 시도

```bash
# 방법 1: 문자열 추출
python extract_sql_strings.py

# 방법 2: 데이터베이스 찾기 및 스키마 추출
python monitor_sqlite.py
```

### 3단계: 동적 분석 (선택)

```bash
# DeskPro.exe 실행
# 다른 터미널에서
python extract_from_memory.py
```

### 4단계: 결과 분석

생성된 파일들:
- `extracted_sql_queries.txt`: 문자열 추출 결과
- `database_info.txt`: 데이터베이스 스키마
- `monitored_queries.txt`: 모니터링 결과
- `extracted_memory_queries.txt`: 메모리 추출 결과

## 고급 방법

### 방법 4: 디버거 사용 (고급)

1. **x64dbg** 다운로드 및 설치
2. DeskPro.exe를 x64dbg로 열기
3. SQLite 함수에 브레이크포인트 설정:
   - `sqlite3_prepare_v2`
   - `sqlite3_exec`
4. 실행하여 SQL 쿼리 문자열 확인

### 방법 5: Process Monitor 사용

1. **Process Monitor** 실행
2. DeskPro.exe 프로세스 필터링
3. 파일 시스템 활동 모니터링
4. `.db`, `.sqlite` 파일 접근 확인
5. 해당 파일을 직접 분석

### 방법 6: SQLite 로깅 활성화

SQLite는 쿼리 로깅을 지원합니다. `sqlite3.dll`을 교체하거나 후킹하여 쿼리를 로깅할 수 있습니다.

**주의**: 이 방법은 복잡하고 DLL 수정이 필요합니다.

### 방법 7: 네트워크 트래픽 분석

웹서비스를 사용하는 경우 (`webService.dll` 존재):
1. **Wireshark** 실행
2. 로컬호스트 트래픽 캡처
3. HTTP 요청/응답에서 SQL 쿼리 확인

## 결과 활용

추출된 SQL 쿼리를 바탕으로:

1. **데이터베이스 스키마 재구성**
   - 테이블 구조 파악
   - 관계(Relationship) 파악

2. **API 엔드포인트 설계**
   - 각 쿼리가 어떤 기능에 사용되는지 매핑
   - RESTful API 설계

3. **프론트엔드 컴포넌트 설계**
   - 데이터 모델 기반 UI 컴포넌트 설계
   - 폼 필드 및 검색 조건 파악

## 주의사항

⚠️ **법적 고려사항**:
- 리버스 엔지니어링은 소프트웨어 라이선스에 따라 제한될 수 있습니다
- 개인 사용 또는 교육 목적으로만 사용하세요
- 상업적 사용 전에 법적 검토를 받으세요

⚠️ **기술적 제한사항**:
- 일부 쿼리는 동적으로 생성되어 추출이 어려울 수 있습니다
- 암호화된 쿼리는 추가 분석이 필요합니다
- 최적화된 바이너리는 문자열이 최소화되어 있을 수 있습니다

## 문제 해결

### "프로세스를 찾을 수 없습니다"
- DeskPro.exe가 실행 중인지 확인
- 관리자 권한으로 실행 시도

### "SQL 쿼리를 찾을 수 없습니다"
- 여러 방법을 조합하여 시도
- 디버거나 전문 도구 사용 고려

### "데이터베이스 파일을 찾을 수 없습니다"
- Process Monitor로 파일 접근 추적
- 레지스트리에서 경로 확인

## 다음 단계

1. 추출된 쿼리를 분석하여 데이터 모델 설계
2. API 스펙 문서 작성
3. 프론트엔드 UI 컴포넌트 설계
4. 데이터베이스 마이그레이션 스크립트 작성

## 참고 자료

- [SQLite 공식 문서](https://www.sqlite.org/docs.html)
- [IDA Pro 사용법](https://www.hex-rays.com/products/ida/support/)
- [x64dbg 문서](https://x64dbg.com/docs/)

---

**작성일**: 2025-12-12
**목적**: DeskPro.exe 리버스 엔지니어링을 통한 SQL 쿼리 추출

