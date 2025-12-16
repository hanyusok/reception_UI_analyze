"""
고급 코드 분석 스크립트
PE 파일을 더 깊이 분석하여 함수 호출, API 사용, SQL 쿼리 패턴을 추출합니다.
"""

import struct
import re
import sys
from pathlib import Path
from collections import defaultdict

def analyze_pe_file(file_path):
    """PE 파일 고급 분석"""
    print(f"파일 분석 중: {file_path}")
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    results = {
        'sql_queries': [],
        'api_calls': [],
        'function_patterns': [],
        'data_structures': [],
    }
    
    # 1. SQL 쿼리 패턴 분석 (더 정교한 방법)
    results['sql_queries'] = extract_sql_queries_advanced(data)
    
    # 2. Windows API 호출 패턴
    results['api_calls'] = extract_api_calls(data)
    
    # 3. 함수 호출 패턴
    results['function_patterns'] = extract_function_patterns(data)
    
    # 4. 데이터 구조 패턴
    results['data_structures'] = extract_data_structures(data)
    
    return results

def extract_sql_queries_advanced(data):
    """고급 SQL 쿼리 추출"""
    queries = []
    
    # SQLite 함수 호출 패턴
    sqlite_functions = [
        b'sqlite3_prepare',
        b'sqlite3_exec',
        b'sqlite3_step',
        b'sqlite3_bind',
    ]
    
    for func in sqlite_functions:
        idx = 0
        while True:
            idx = data.find(func, idx)
            if idx == -1:
                break
            
            # 함수 호출 주변 분석
            # 일반적으로 함수 호출 후 문자열 인자가 올 수 있음
            context_start = max(0, idx - 200)
            context_end = min(len(data), idx + 1000)
            context = data[context_start:context_end]
            
            # SQL 쿼리 패턴 찾기
            sql_patterns = [
                rb'SELECT\s+.*?FROM',
                rb'INSERT\s+INTO\s+.*?VALUES',
                rb'UPDATE\s+.*?SET',
                rb'DELETE\s+FROM\s+.*?WHERE',
            ]
            
            for pattern in sql_patterns:
                matches = re.finditer(pattern, context, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    query = match.group(0).decode('utf-8', errors='ignore').strip()
                    if len(query) > 10:
                        queries.append({
                            'query': query,
                            'function': func.decode('utf-8', errors='ignore'),
                            'offset': hex(idx),
                        })
            
            idx += 1
    
    # 문자열 섹션에서 직접 검색
    queries.extend(extract_sql_from_strings(data))
    
    return queries

def extract_sql_from_strings(data):
    """문자열에서 SQL 추출 (개선된 버전)"""
    queries = []
    
    # 연속된 인쇄 가능한 문자 찾기 (문자열 후보)
    current_string = b''
    string_start = 0
    
    for i in range(len(data)):
        byte = data[i]
        
        if 32 <= byte < 127:  # 인쇄 가능한 ASCII
            if not current_string:
                string_start = i
            current_string += bytes([byte])
        else:
            if len(current_string) >= 20:  # 최소 길이
                # SQL 패턴 확인
                text = current_string.decode('utf-8', errors='ignore')
                
                sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
                if any(keyword in text.upper() for keyword in sql_keywords):
                    # SQL 문장 추출
                    match = re.search(
                        r'(?i)(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP).*?(?:;|$)',
                        text,
                        re.DOTALL
                    )
                    if match:
                        query = match.group(0).strip()
                        if len(query) > 15:
                            queries.append({
                                'query': query,
                                'function': 'STRING_SECTION',
                                'offset': hex(string_start),
                            })
            
            current_string = b''
    
    return queries

def extract_api_calls(data):
    """Windows API 호출 추출"""
    api_calls = []
    
    # 일반적인 Windows API 패턴
    api_patterns = [
        (b'CreateFile', 'FILE_OPERATION'),
        (b'ReadFile', 'FILE_OPERATION'),
        (b'WriteFile', 'FILE_OPERATION'),
        (b'RegOpenKey', 'REGISTRY'),
        (b'RegQueryValue', 'REGISTRY'),
        (b'InternetOpen', 'NETWORK'),
        (b'HttpSendRequest', 'NETWORK'),
        (b'LoadLibrary', 'DLL_LOAD'),
        (b'GetProcAddress', 'DLL_LOAD'),
    ]
    
    for pattern, category in api_patterns:
        idx = 0
        count = 0
        while idx < len(data) and count < 100:  # 최대 100개
            idx = data.find(pattern, idx)
            if idx == -1:
                break
            
            api_calls.append({
                'api': pattern.decode('utf-8', errors='ignore'),
                'category': category,
                'offset': hex(idx),
            })
            
            idx += 1
            count += 1
    
    return api_calls

def extract_function_patterns(data):
    """함수 호출 패턴 추출"""
    patterns = []
    
    # x86 호출 패턴 (E8 = CALL rel32)
    call_pattern = b'\xE8'
    idx = 0
    count = 0
    
    while idx < len(data) - 5 and count < 1000:
        idx = data.find(call_pattern, idx)
        if idx == -1:
            break
        
        # 상대 주소 읽기
        try:
            rel_addr = struct.unpack('<i', data[idx+1:idx+5])[0]
            target_addr = idx + 5 + rel_addr
            
            if 0 <= target_addr < len(data):
                # 대상 주소 주변에서 함수명 시도
                context = data[max(0, target_addr-50):min(len(data), target_addr+50)]
                # 인쇄 가능한 문자열 찾기
                text = ''.join(chr(b) if 32 <= b < 127 else ' ' for b in context)
                if any(keyword in text.upper() for keyword in ['SQL', 'QUERY', 'SELECT', 'INSERT']):
                    patterns.append({
                        'type': 'CALL',
                        'from': hex(idx),
                        'to': hex(target_addr),
                        'context': text[:100],
                    })
        except:
            pass
        
        idx += 1
        count += 1
    
    return patterns

def extract_data_structures(data):
    """데이터 구조 패턴 추출"""
    structures = []
    
    # 테이블 이름 패턴 (일반적인 명명 규칙)
    table_patterns = [
        rb'\b(user|member|customer|client|order|product|item|data|info|log|history)\w*\b',
        rb'\b(tbl|table|tb_|_table)\w+\b',
    ]
    
    for pattern in table_patterns:
        matches = re.finditer(pattern, data, re.IGNORECASE)
        for match in matches:
            text = match.group(0).decode('utf-8', errors='ignore')
            if len(text) > 2:
                structures.append({
                    'type': 'TABLE_NAME_CANDIDATE',
                    'name': text,
                    'offset': hex(match.start()),
                })
    
    return structures

def generate_advanced_report(results, output_file='advanced_analysis_report.txt'):
    """고급 분석 보고서 생성"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DeskPro.exe 고급 코드 분석 보고서\n")
        f.write("=" * 80 + "\n\n")
        
        # SQL 쿼리
        f.write("## 추출된 SQL 쿼리\n")
        f.write(f"총 {len(results['sql_queries'])}개 발견\n\n")
        for i, query_info in enumerate(results['sql_queries'][:100], 1):  # 최대 100개
            f.write(f"\n[쿼리 #{i}]\n")
            f.write(f"위치: {query_info['offset']}\n")
            f.write(f"관련 함수: {query_info['function']}\n")
            f.write(f"쿼리:\n{query_info['query']}\n")
            f.write("-" * 80 + "\n")
        
        # API 호출
        f.write("\n\n## Windows API 호출\n")
        api_by_category = defaultdict(list)
        for api in results['api_calls']:
            api_by_category[api['category']].append(api)
        
        for category, apis in api_by_category.items():
            f.write(f"\n### {category}\n")
            for api in apis[:20]:  # 카테고리별 최대 20개
                f.write(f"  - {api['api']} (위치: {api['offset']})\n")
        
        # 함수 패턴
        f.write("\n\n## SQL 관련 함수 호출 패턴\n")
        for i, pattern in enumerate(results['function_patterns'][:50], 1):
            f.write(f"\n[패턴 #{i}]\n")
            f.write(f"  호출 위치: {pattern['from']} -> {pattern['to']}\n")
            f.write(f"  컨텍스트: {pattern['context']}\n")
        
        # 데이터 구조
        f.write("\n\n## 추정 테이블 이름\n")
        unique_tables = {}
        for struct_info in results['data_structures']:
            name = struct_info['name'].upper()
            if name not in unique_tables:
                unique_tables[name] = struct_info['offset']
        
        for name, offset in sorted(unique_tables.items())[:50]:
            f.write(f"  - {name} (위치: {offset})\n")
    
    print(f"\n고급 분석 보고서가 {output_file}에 저장되었습니다.")

if __name__ == '__main__':
    exe_path = Path('DeskPro.exe')
    
    if not exe_path.exists():
        print(f"오류: {exe_path} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("고급 코드 분석 시작...")
    print("이 작업은 시간이 걸릴 수 있습니다...\n")
    
    results = analyze_pe_file(exe_path)
    
    print("\n분석 완료!")
    print(f"  - SQL 쿼리: {len(results['sql_queries'])}개")
    print(f"  - API 호출: {len(results['api_calls'])}개")
    print(f"  - 함수 패턴: {len(results['function_patterns'])}개")
    print(f"  - 데이터 구조: {len(results['data_structures'])}개")
    
    generate_advanced_report(results)

