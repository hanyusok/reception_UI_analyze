"""
프로세스 메모리에서 SQL 쿼리 추출 스크립트
DeskPro.exe 실행 중 메모리에서 SQL 쿼리를 추출합니다.
"""

import sys
import re
import ctypes
from ctypes import wintypes
import psutil

# Windows API 상수
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

def find_process(process_name):
    """프로세스를 찾습니다."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def read_process_memory(pid):
    """프로세스 메모리를 읽어 SQL 쿼리를 추출합니다."""
    # Windows API 함수
    kernel32 = ctypes.windll.kernel32
    OpenProcess = kernel32.OpenProcess
    VirtualQueryEx = kernel32.VirtualQueryEx
    ReadProcessMemory = kernel32.ReadProcessMemory
    CloseHandle = kernel32.CloseHandle
    
    # 프로세스 핸들 열기
    process_handle = OpenProcess(
        PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
        False,
        pid
    )
    
    if not process_handle:
        print(f"프로세스 열기 실패 (PID: {pid})")
        return []
    
    sql_queries = []
    address = 0
    mbi = MEMORY_BASIC_INFORMATION()
    
    print(f"메모리 스캔 중 (PID: {pid})...")
    
    try:
        while address < 0x7FFFFFFF:  # 사용자 공간만
            if VirtualQueryEx(process_handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
                break
            
            # 커밋된 메모리 영역만 읽기
            if mbi.State == MEM_COMMIT and mbi.Protect in (PAGE_READONLY, PAGE_READWRITE):
                buffer = ctypes.create_string_buffer(mbi.RegionSize)
                bytes_read = ctypes.c_size_t()
                
                if ReadProcessMemory(
                    process_handle,
                    ctypes.c_void_p(address),
                    buffer,
                    mbi.RegionSize,
                    ctypes.byref(bytes_read)
                ):
                    # SQL 패턴 검색
                    data = buffer.raw[:bytes_read.value]
                    queries = find_sql_in_memory(data)
                    sql_queries.extend(queries)
            
            address = mbi.BaseAddress + mbi.RegionSize
    
    finally:
        CloseHandle(process_handle)
    
    return sql_queries

def find_sql_in_memory(data):
    """메모리 데이터에서 SQL 쿼리를 찾습니다."""
    queries = []
    
    # 여러 인코딩으로 시도
    encodings = ['utf-8', 'utf-16', 'cp949', 'latin-1']
    
    for encoding in encodings:
        try:
            text = data.decode(encoding, errors='ignore')
            
            # SQL 패턴
            patterns = [
                r'(?i)SELECT\s+.*?(?:FROM|WHERE|ORDER|GROUP|LIMIT|UNION|;)',
                r'(?i)INSERT\s+INTO\s+.*?(?:VALUES|SELECT|;)',
                r'(?i)UPDATE\s+.*?SET\s+.*?(?:WHERE|;)',
                r'(?i)DELETE\s+FROM\s+.*?(?:WHERE|;)',
                r'(?i)CREATE\s+TABLE\s+.*?;',
                r'(?i)ALTER\s+TABLE\s+.*?;',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.DOTALL)
                for match in matches:
                    query = match.group(0).strip()
                    if len(query) > 10 and query not in queries:
                        queries.append(query)
        except:
            continue
    
    # 바이너리에서 직접 검색
    sql_keywords = [b'SELECT', b'INSERT', b'UPDATE', b'DELETE', b'CREATE TABLE']
    for keyword in sql_keywords:
        idx = 0
        while True:
            idx = data.find(keyword, idx)
            if idx == -1:
                break
            
            # 키워드 주변 추출
            start = max(0, idx - 20)
            end = min(len(data), idx + 500)
            snippet = data[start:end]
            
            try:
                text = snippet.decode('utf-8', errors='ignore')
                match = re.search(r'(?i)(SELECT|INSERT|UPDATE|DELETE|CREATE).*?[;\x00]', text)
                if match:
                    query = match.group(0).rstrip('\x00').strip()
                    if len(query) > 10 and query not in queries:
                        queries.append(query)
            except:
                pass
            
            idx += 1
    
    return queries

def main():
    process_name = 'DeskPro.exe'
    
    print(f"{process_name} 프로세스 검색 중...")
    pid = find_process(process_name)
    
    if not pid:
        print(f"{process_name} 프로세스를 찾을 수 없습니다.")
        print("프로그램을 실행한 후 다시 시도하세요.")
        return
    
    print(f"프로세스 발견 (PID: {pid})")
    print("메모리에서 SQL 쿼리 추출 중... (시간이 걸릴 수 있습니다)")
    
    queries = read_process_memory(pid)
    
    if queries:
        # 중복 제거
        unique_queries = list(set(queries))
        
        print(f"\n추출된 쿼리 수: {len(unique_queries)}")
        
        # 결과 저장
        output_file = 'extracted_memory_queries.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("메모리에서 추출된 SQL 쿼리\n")
            f.write("=" * 80 + "\n\n")
            
            for i, query in enumerate(unique_queries, 1):
                f.write(f"\n[쿼리 #{i}]\n")
                f.write("-" * 80 + "\n")
                f.write(query + "\n")
                f.write("-" * 80 + "\n")
        
        print(f"\n결과가 {output_file}에 저장되었습니다.")
        
        # 미리보기
        print("\n처음 5개 미리보기:")
        for i, query in enumerate(unique_queries[:5], 1):
            print(f"\n[{i}]")
            print(query[:200] + ("..." if len(query) > 200 else ""))
    else:
        print("\nSQL 쿼리를 찾을 수 없습니다.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

