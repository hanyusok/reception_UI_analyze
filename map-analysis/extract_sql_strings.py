"""
DeskPro.exe에서 SQL 쿼리 문자열 추출 스크립트
실행 파일에서 SQL 관련 문자열을 추출합니다.
"""

import re
import sys
from pathlib import Path

def extract_sql_strings(file_path):
    """
    실행 파일에서 SQL 쿼리 패턴을 찾아 추출합니다.
    """
    print(f"파일 읽는 중: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return []
    
    # 인코딩 시도 (UTF-8, UTF-16, CP949)
    sql_queries = []
    
    # UTF-8로 디코딩 시도
    try:
        text = content.decode('utf-8', errors='ignore')
        sql_queries.extend(find_sql_patterns(text, 'UTF-8'))
    except:
        pass
    
    # UTF-16으로 디코딩 시도
    try:
        text = content.decode('utf-16', errors='ignore')
        sql_queries.extend(find_sql_patterns(text, 'UTF-16'))
    except:
        pass
    
    # CP949로 디코딩 시도 (한국어)
    try:
        text = content.decode('cp949', errors='ignore')
        sql_queries.extend(find_sql_patterns(text, 'CP949'))
    except:
        pass
    
    # 바이너리에서 직접 패턴 검색 (인코딩 무관)
    sql_queries.extend(find_sql_in_binary(content))
    
    # 중복 제거
    unique_queries = list(set(sql_queries))
    
    return unique_queries

def find_sql_patterns(text, encoding):
    """텍스트에서 SQL 패턴을 찾습니다."""
    queries = []
    
    # SQL 키워드 패턴
    sql_patterns = [
        r'(?i)(SELECT\s+.*?(?:FROM|WHERE|ORDER|GROUP|LIMIT|UNION))',
        r'(?i)(INSERT\s+INTO\s+.*?(?:VALUES|SELECT))',
        r'(?i)(UPDATE\s+.*?SET\s+.*?(?:WHERE|$))',
        r'(?i)(DELETE\s+FROM\s+.*?(?:WHERE|$))',
        r'(?i)(CREATE\s+TABLE\s+.*?(?:\(|$))',
        r'(?i)(ALTER\s+TABLE\s+.*?)',
        r'(?i)(DROP\s+TABLE\s+.*?)',
        r'(?i)(CREATE\s+INDEX\s+.*?)',
        r'(?i)(PRAGMA\s+.*?)',
    ]
    
    for pattern in sql_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
        for match in matches:
            query = match.group(1).strip()
            # 최소 길이 필터 (너무 짧은 것은 제외)
            if len(query) > 10:
                queries.append((query, encoding))
    
    return queries

def find_sql_in_binary(content):
    """바이너리에서 SQL 키워드를 포함한 문자열을 찾습니다."""
    queries = []
    
    # SQL 키워드 (바이트로)
    keywords = [
        b'SELECT',
        b'INSERT',
        b'UPDATE',
        b'DELETE',
        b'CREATE TABLE',
        b'ALTER TABLE',
        b'DROP TABLE',
        b'FROM',
        b'WHERE',
        b'PRAGMA',
    ]
    
    for keyword in keywords:
        idx = 0
        while True:
            idx = content.find(keyword, idx)
            if idx == -1:
                break
            
            # 키워드 주변 문자열 추출 (최대 500바이트)
            start = max(0, idx - 50)
            end = min(len(content), idx + 500)
            snippet = content[start:end]
            
            # 인쇄 가능한 문자만 추출
            try:
                text = ''.join(chr(b) if 32 <= b < 127 or b in [9, 10, 13] else ' ' for b in snippet)
                # SQL 패턴 확인
                if re.search(r'(?i)(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|PRAGMA)', text):
                    # 문장 끝까지 추출
                    match = re.search(r'(?i)(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|PRAGMA).*?[;]', text)
                    if match:
                        queries.append((match.group(0).strip(), 'BINARY'))
            except:
                pass
            
            idx += 1
    
    return queries

def save_results(queries, output_file='extracted_sql_queries.txt'):
    """추출된 쿼리를 파일로 저장합니다."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("추출된 SQL 쿼리 목록\n")
        f.write("=" * 80 + "\n\n")
        
        if not queries:
            f.write("SQL 쿼리를 찾을 수 없습니다.\n")
            return
        
        for i, (query, encoding) in enumerate(queries, 1):
            f.write(f"\n[쿼리 #{i}] (인코딩: {encoding})\n")
            f.write("-" * 80 + "\n")
            f.write(query + "\n")
            f.write("-" * 80 + "\n")
    
    print(f"\n결과가 {output_file}에 저장되었습니다.")
    print(f"총 {len(queries)}개의 SQL 쿼리가 추출되었습니다.")

if __name__ == '__main__':
    exe_path = Path('DeskPro.exe')
    
    if not exe_path.exists():
        print(f"오류: {exe_path} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("SQL 쿼리 추출 시작...")
    queries = extract_sql_strings(exe_path)
    
    if queries:
        print(f"\n추출된 쿼리 수: {len(queries)}")
        print("\n처음 5개 미리보기:")
        for i, (query, encoding) in enumerate(queries[:5], 1):
            print(f"\n[{i}] ({encoding})")
            print(query[:200] + ("..." if len(query) > 200 else ""))
    
    save_results(queries)

