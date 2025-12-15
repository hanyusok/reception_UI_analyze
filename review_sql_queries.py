"""
추출된 SQL 쿼리 검토 및 정리 스크립트
깨진 쿼리를 식별하고 유효한 쿼리를 정리합니다.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

class SQLQueryReviewer:
    """SQL 쿼리 검토기"""
    
    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.queries = []
        self.valid_queries = []
        self.broken_queries = []
        self.invalid_queries = []
        self.statistics = defaultdict(int)
        
    def parse_file(self):
        """파일 파싱"""
        print(f"파일 읽는 중: {self.input_file}")
        
        try:
            # 여러 인코딩 시도
            encodings = ['utf-8', 'utf-16', 'cp949', 'latin-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(self.input_file, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                    print(f"성공적으로 읽음 (인코딩: {encoding})")
                    break
                except:
                    continue
            
            if not content:
                print("파일을 읽을 수 없습니다.")
                return False
            
            # 쿼리 블록 파싱
            self._parse_queries(content)
            return True
            
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return False
    
    def _parse_queries(self, content):
        """쿼리 파싱"""
        # 쿼리 블록 패턴: [쿼리 #N] (인코딩: ...) ... --- ... 쿼리 내용 ... ---
        # 한글 깨짐을 고려하여 더 유연한 패턴 사용
        pattern = r'\[[^\]]*#(\d+)\][^\n]*\([^)]*:\s*([^)]+)\)[^\n]*\n-+\n(.*?)\n-+\n'
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            query_num = match.group(1)
            encoding = match.group(2).strip()
            query_text = match.group(3).strip()
            
            self.queries.append({
                'number': int(query_num),
                'encoding': encoding,
                'text': query_text,
                'original': match.group(0)
            })
        
        # 대체 패턴: 더 단순한 형식
        if len(self.queries) == 0:
            # [쿼리 #N] 형식만 찾기
            pattern2 = r'\[[^\]]*#(\d+)\][^\n]*\n-+\n(.*?)\n-+\n'
            matches2 = re.finditer(pattern2, content, re.DOTALL | re.IGNORECASE)
            
            for match in matches2:
                query_num = match.group(1)
                query_text = match.group(2).strip()
                
                # 인코딩 추정
                encoding = 'UNKNOWN'
                if 'UTF-16' in match.group(0) or 'utf-16' in match.group(0).lower():
                    encoding = 'UTF-16'
                elif 'UTF-8' in match.group(0) or 'utf-8' in match.group(0).lower():
                    encoding = 'UTF-8'
                elif 'BINARY' in match.group(0) or 'binary' in match.group(0).lower():
                    encoding = 'BINARY'
                
                self.queries.append({
                    'number': int(query_num),
                    'encoding': encoding,
                    'text': query_text,
                    'original': match.group(0)
                })
    
    def analyze_queries(self):
        """쿼리 분석"""
        print(f"\n총 {len(self.queries)}개의 쿼리 분석 중...")
        
        for query_info in self.queries:
            query_text = query_info['text']
            
            # 기본 검증
            is_valid = self._is_valid_sql(query_text)
            is_broken = self._is_broken(query_text)
            is_invalid = self._is_invalid_content(query_text)
            
            if is_invalid:
                self.invalid_queries.append(query_info)
                self.statistics['invalid'] += 1
            elif is_broken:
                self.broken_queries.append(query_info)
                self.statistics['broken'] += 1
            elif is_valid:
                self.valid_queries.append(query_info)
                self.statistics['valid'] += 1
            else:
                self.broken_queries.append(query_info)
                self.statistics['broken'] += 1
    
    def _is_valid_sql(self, text):
        """유효한 SQL 쿼리인지 확인"""
        # SQL 키워드 확인
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'PRAGMA']
        has_keyword = any(keyword in text.upper() for keyword in sql_keywords)
        
        if not has_keyword:
            return False
        
        # 너무 짧거나 너무 긴 경우 제외
        if len(text) < 10 or len(text) > 10000:
            return False
        
        # 바이너리 데이터나 제어 문자 과다 포함 제외
        control_chars = sum(1 for c in text if ord(c) < 32 and c not in ['\n', '\r', '\t'])
        if control_chars > len(text) * 0.1:  # 10% 이상 제어 문자
            return False
        
        # 기본 SQL 문법 패턴 확인
        patterns = [
            r'(?i)SELECT\s+.*?\s+FROM',
            r'(?i)INSERT\s+INTO\s+\w+',
            r'(?i)UPDATE\s+\w+\s+SET',
            r'(?i)DELETE\s+FROM\s+\w+',
            r'(?i)CREATE\s+TABLE\s+\w+',
        ]
        
        return any(re.search(pattern, text) for pattern in patterns)
    
    def _is_broken(self, text):
        """깨진 쿼리인지 확인"""
        # 불완전한 쿼리 패턴
        broken_patterns = [
            r'SELECT\s*$',  # SELECT만 있고 끝
            r'INSERT\s+INTO\s+\w+\s*$',  # INSERT INTO만 있고 끝
            r'UPDATE\s+\w+\s*$',  # UPDATE만 있고 끝
            r'VALUES\s*$',  # VALUES만 있고 끝
            r'FROM\s*$',  # FROM만 있고 끝
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in broken_patterns):
            return True
        
        # 특수 문자나 바이너리 데이터 과다
        if re.search(r'[^\x20-\x7E\n\r\t]{10,}', text):  # 10개 이상의 비인쇄 문자
            return True
        
        return False
    
    def _is_invalid_content(self, text):
        """유효하지 않은 내용인지 확인 (SQL이 아닌 것)"""
        # SQL이 아닌 내용 패턴
        invalid_patterns = [
            r'^[^A-Za-z]*$',  # 알파벳이 전혀 없음
            r'^[\x00-\x1F\x7F-\xFF]+$',  # 제어 문자나 바이너리만
            r'TStringGrid|TComponent|Delphi|Object',  # Delphi 컴포넌트 코드
            r'\.exe|\.dll|\.obj',  # 파일명
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in invalid_patterns):
            return True
        
        # SQL 키워드가 전혀 없고 너무 짧음
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
        has_sql = any(keyword in text.upper() for keyword in sql_keywords)
        
        if not has_sql and len(text) < 20:
            return True
        
        return False
    
    def clean_query(self, text):
        """쿼리 정리"""
        # 제어 문자 제거 (탭, 줄바꿈은 유지)
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', text)
        
        # 연속된 공백 정리
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        
        # 줄바꿈 정리
        cleaned = re.sub(r'\r\n', '\n', cleaned)
        cleaned = re.sub(r'\r', '\n', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # 앞뒤 공백 제거
        cleaned = cleaned.strip()
        
        return cleaned
    
    def categorize_queries(self):
        """쿼리 카테고리화"""
        categories = defaultdict(list)
        
        for query_info in self.valid_queries:
            text = query_info['text'].upper()
            
            if 'SELECT' in text:
                categories['SELECT'].append(query_info)
            elif 'INSERT' in text:
                categories['INSERT'].append(query_info)
            elif 'UPDATE' in text:
                categories['UPDATE'].append(query_info)
            elif 'DELETE' in text:
                categories['DELETE'].append(query_info)
            elif 'CREATE TABLE' in text:
                categories['CREATE_TABLE'].append(query_info)
            elif 'ALTER' in text:
                categories['ALTER'].append(query_info)
            elif 'DROP' in text:
                categories['DROP'].append(query_info)
            else:
                categories['OTHER'].append(query_info)
        
        return categories
    
    def generate_report(self, output_file='sql_query_review_report.txt'):
        """검토 보고서 생성"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("SQL 쿼리 검토 보고서\n")
            f.write("=" * 80 + "\n\n")
            
            # 통계
            f.write("## 통계\n")
            f.write(f"전체 쿼리 수: {len(self.queries)}\n")
            f.write(f"유효한 쿼리: {self.statistics['valid']}\n")
            f.write(f"깨진 쿼리: {self.statistics['broken']}\n")
            f.write(f"유효하지 않은 내용: {self.statistics['invalid']}\n")
            f.write("\n")
            
            # 카테고리별 통계
            categories = self.categorize_queries()
            f.write("## 카테고리별 통계\n")
            for cat, queries in sorted(categories.items()):
                f.write(f"  {cat}: {len(queries)}개\n")
            f.write("\n")
            
            # 유효한 쿼리 목록
            f.write("=" * 80 + "\n")
            f.write("## 유효한 쿼리 목록\n")
            f.write("=" * 80 + "\n\n")
            
            for i, query_info in enumerate(self.valid_queries, 1):
                cleaned = self.clean_query(query_info['text'])
                f.write(f"\n[유효 쿼리 #{i}] (원본: 쿼리 #{query_info['number']}, 인코딩: {query_info['encoding']})\n")
                f.write("-" * 80 + "\n")
                f.write(cleaned + "\n")
                f.write("-" * 80 + "\n")
            
            # 깨진 쿼리 샘플
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("## 깨진 쿼리 샘플 (처음 20개)\n")
            f.write("=" * 80 + "\n\n")
            
            for i, query_info in enumerate(self.broken_queries[:20], 1):
                f.write(f"\n[깨진 쿼리 #{i}] (원본: 쿼리 #{query_info['number']})\n")
                f.write("-" * 80 + "\n")
                f.write(query_info['text'][:500] + ("..." if len(query_info['text']) > 500 else "") + "\n")
                f.write("-" * 80 + "\n")
        
        print(f"\n검토 보고서가 {output_file}에 저장되었습니다.")
    
    def export_valid_queries(self, output_file='valid_sql_queries.txt'):
        """유효한 쿼리만 별도 파일로 저장"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("유효한 SQL 쿼리 목록\n")
            f.write("=" * 80 + "\n\n")
            
            categories = self.categorize_queries()
            
            for cat in ['CREATE_TABLE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'ALTER', 'DROP', 'OTHER']:
                if cat not in categories:
                    continue
                
                f.write(f"\n{'=' * 80}\n")
                f.write(f"## {cat} 쿼리 ({len(categories[cat])}개)\n")
                f.write(f"{'=' * 80}\n\n")
                
                for i, query_info in enumerate(categories[cat], 1):
                    cleaned = self.clean_query(query_info['text'])
                    f.write(f"\n[{cat} #{i}]\n")
                    f.write("-" * 80 + "\n")
                    f.write(cleaned + "\n")
                    f.write("-" * 80 + "\n")
        
        print(f"유효한 쿼리가 {output_file}에 저장되었습니다.")
    
    def print_summary(self):
        """요약 출력"""
        print("\n" + "=" * 80)
        print("검토 요약")
        print("=" * 80)
        print(f"전체 쿼리 수: {len(self.queries)}")
        
        if len(self.queries) > 0:
            valid_pct = (self.statistics['valid']/len(self.queries)*100) if len(self.queries) > 0 else 0
            broken_pct = (self.statistics['broken']/len(self.queries)*100) if len(self.queries) > 0 else 0
            invalid_pct = (self.statistics['invalid']/len(self.queries)*100) if len(self.queries) > 0 else 0
            
            print(f"  [OK] 유효한 쿼리: {self.statistics['valid']} ({valid_pct:.1f}%)")
            print(f"  [X] 깨진 쿼리: {self.statistics['broken']} ({broken_pct:.1f}%)")
            print(f"  [X] 유효하지 않은 내용: {self.statistics['invalid']} ({invalid_pct:.1f}%)")
            
            categories = self.categorize_queries()
            if categories:
                print("\n카테고리별 분포:")
                for cat, queries in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
                    print(f"  {cat}: {len(queries)}개")
        else:
            print("파싱된 쿼리가 없습니다.")

if __name__ == '__main__':
    input_file = Path('extracted_sql_queries.txt')
    
    if not input_file.exists():
        print(f"오류: {input_file} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    reviewer = SQLQueryReviewer(input_file)
    
    if reviewer.parse_file():
        reviewer.analyze_queries()
        reviewer.print_summary()
        reviewer.generate_report()
        reviewer.export_valid_queries()
    else:
        print("파일 파싱 실패!")
        sys.exit(1)

