"""
SQLite 데이터베이스 파일 모니터링 및 쿼리 추출 스크립트
DeskPro.exe가 실행 중일 때 SQLite 데이터베이스 파일을 모니터링합니다.
"""

import os
import sys
import time
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
import winreg

def find_sqlite_databases():
    """시스템에서 SQLite 데이터베이스 파일을 찾습니다."""
    db_files = []
    
    # 일반적인 위치들
    search_paths = [
        Path.home() / 'AppData' / 'Local',
        Path.home() / 'AppData' / 'Roaming',
        Path('C:\\ProgramData'),
        Path('C:\\Program Files (x86)'),
        Path('.'),
    ]
    
    extensions = ['.db', '.sqlite', '.sqlite3', '.db3']
    
    print("SQLite 데이터베이스 파일 검색 중...")
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        try:
            for ext in extensions:
                for db_file in search_path.rglob(f'*{ext}'):
                    try:
                        # SQLite 파일인지 확인
                        conn = sqlite3.connect(str(db_file))
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
                        cursor.fetchone()
                        conn.close()
                        
                        db_files.append(db_file)
                        print(f"  발견: {db_file}")
                    except:
                        pass
        except PermissionError:
            pass
    
    return db_files

def extract_schema(db_path):
    """데이터베이스 스키마를 추출합니다."""
    schema = []
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 테이블 목록
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            # 테이블 스키마
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = cursor.fetchone()
            if result:
                schema.append(result[0])
            
            # 인덱스 정보
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='{table_name}'")
            indexes = cursor.fetchall()
            for (index_sql,) in indexes:
                if index_sql:
                    schema.append(index_sql)
        
        conn.close()
    except Exception as e:
        print(f"스키마 추출 오류 ({db_path}): {e}")
    
    return schema

def monitor_database_changes(db_path, output_file='monitored_queries.txt'):
    """데이터베이스 변경사항을 모니터링합니다."""
    print(f"\n데이터베이스 모니터링 시작: {db_path}")
    print("프로그램을 실행하고 사용한 후 Ctrl+C로 중지하세요.\n")
    
    # 초기 상태 저장
    initial_state = {}
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            initial_state[table] = cursor.fetchone()[0]
        conn.close()
    except Exception as e:
        print(f"초기 상태 확인 오류: {e}")
        return
    
    try:
        while True:
            time.sleep(2)
            current_state = {}
            
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    current_state[table] = cursor.fetchone()[0]
                
                # 변경사항 확인
                for table in tables:
                    if current_state.get(table, 0) != initial_state.get(table, 0):
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        change = current_state[table] - initial_state.get(table, 0)
                        print(f"[{timestamp}] {table}: {change:+d} 행 변경")
                        
                        # 최근 데이터 확인
                        try:
                            cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 5")
                            rows = cursor.fetchall()
                            with open(output_file, 'a', encoding='utf-8') as f:
                                f.write(f"\n[{timestamp}] {table} 변경 감지\n")
                                f.write(f"변경된 행 수: {change}\n")
                                f.write(f"최근 데이터:\n{rows}\n\n")
                        except:
                            pass
                        
                        initial_state[table] = current_state[table]
                
                conn.close()
            except Exception as e:
                print(f"모니터링 오류: {e}")
    
    except KeyboardInterrupt:
        print("\n모니터링 중지됨.")

def save_database_info(db_files, output_file='database_info.txt'):
    """데이터베이스 정보를 저장합니다."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SQLite 데이터베이스 정보\n")
        f.write("=" * 80 + "\n\n")
        
        for db_path in db_files:
            f.write(f"\n데이터베이스: {db_path}\n")
            f.write("-" * 80 + "\n")
            
            schema = extract_schema(db_path)
            if schema:
                f.write("스키마:\n")
                for sql in schema:
                    f.write(f"  {sql}\n")
            else:
                f.write("스키마를 추출할 수 없습니다.\n")
            
            f.write("\n")
    
    print(f"\n데이터베이스 정보가 {output_file}에 저장되었습니다.")

if __name__ == '__main__':
    print("SQLite 데이터베이스 모니터링 도구\n")
    
    # 데이터베이스 파일 찾기
    db_files = find_sqlite_databases()
    
    if not db_files:
        print("\nSQLite 데이터베이스 파일을 찾을 수 없습니다.")
        print("수동으로 데이터베이스 경로를 입력하세요:")
        db_path = input("경로: ").strip()
        if db_path and Path(db_path).exists():
            db_files = [Path(db_path)]
        else:
            print("유효하지 않은 경로입니다.")
            sys.exit(1)
    
    # 데이터베이스 정보 저장
    save_database_info(db_files)
    
    # 모니터링 옵션
    if len(db_files) > 0:
        print(f"\n발견된 데이터베이스:")
        for i, db in enumerate(db_files, 1):
            print(f"  {i}. {db}")
        
        choice = input("\n모니터링을 시작하시겠습니까? (y/n): ").strip().lower()
        if choice == 'y':
            if len(db_files) == 1:
                monitor_database_changes(db_files[0])
            else:
                idx = int(input(f"모니터링할 데이터베이스 번호 (1-{len(db_files)}): ")) - 1
                if 0 <= idx < len(db_files):
                    monitor_database_changes(db_files[idx])

