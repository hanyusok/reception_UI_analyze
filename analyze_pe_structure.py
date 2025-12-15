"""
DeskPro.exe PE 파일 구조 분석 스크립트
실행 파일의 구조를 분석하여 함수, 임포트, 리소스 등을 추출합니다.
"""

import struct
import sys
from pathlib import Path
from collections import defaultdict

class PEAnalyzer:
    """PE 파일 분석기"""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = None
        self.dos_header = None
        self.pe_header_offset = None
        self.pe_signature = None
        self.coff_header = None
        self.optional_header = None
        self.sections = []
        self.imports = []
        self.exports = []
        self.strings = []
        
    def read_file(self):
        """파일 읽기"""
        try:
            with open(self.file_path, 'rb') as f:
                self.data = f.read()
            return True
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return False
    
    def parse_dos_header(self):
        """DOS 헤더 파싱"""
        if len(self.data) < 64:
            return False
        
        # DOS 헤더 확인 (MZ 시그니처)
        if self.data[0:2] != b'MZ':
            print("유효한 PE 파일이 아닙니다 (MZ 시그니처 없음)")
            return False
        
        # PE 헤더 오프셋 (0x3C 위치)
        self.pe_header_offset = struct.unpack('<I', self.data[60:64])[0]
        return True
    
    def parse_pe_header(self):
        """PE 헤더 파싱"""
        if self.pe_header_offset is None or len(self.data) < self.pe_header_offset + 24:
            return False
        
        # PE 시그니처 확인 (PE\0\0)
        if self.data[self.pe_header_offset:self.pe_header_offset+4] != b'PE\x00\x00':
            print("유효한 PE 파일이 아닙니다 (PE 시그니처 없음)")
            return False
        
        self.pe_signature = self.pe_header_offset
        
        # COFF 헤더
        coff_offset = self.pe_header_offset + 4
        self.coff_header = {
            'Machine': struct.unpack('<H', self.data[coff_offset:coff_offset+2])[0],
            'NumberOfSections': struct.unpack('<H', self.data[coff_offset+2:coff_offset+4])[0],
            'TimeDateStamp': struct.unpack('<I', self.data[coff_offset+4:coff_offset+8])[0],
            'PointerToSymbolTable': struct.unpack('<I', self.data[coff_offset+8:coff_offset+12])[0],
            'NumberOfSymbols': struct.unpack('<I', self.data[coff_offset+12:coff_offset+16])[0],
            'SizeOfOptionalHeader': struct.unpack('<H', self.data[coff_offset+16:coff_offset+18])[0],
            'Characteristics': struct.unpack('<H', self.data[coff_offset+18:coff_offset+20])[0],
        }
        
        return True
    
    def parse_sections(self):
        """섹션 헤더 파싱"""
        if not self.coff_header:
            return False
        
        optional_header_offset = self.pe_header_offset + 24
        sections_offset = optional_header_offset + self.coff_header['SizeOfOptionalHeader']
        
        num_sections = self.coff_header['NumberOfSections']
        
        for i in range(num_sections):
            section_offset = sections_offset + (i * 40)
            if len(self.data) < section_offset + 40:
                break
            
            section = {
                'Name': self.data[section_offset:section_offset+8].rstrip(b'\x00').decode('utf-8', errors='ignore'),
                'VirtualSize': struct.unpack('<I', self.data[section_offset+8:section_offset+12])[0],
                'VirtualAddress': struct.unpack('<I', self.data[section_offset+12:section_offset+16])[0],
                'SizeOfRawData': struct.unpack('<I', self.data[section_offset+16:section_offset+20])[0],
                'PointerToRawData': struct.unpack('<I', self.data[section_offset+20:section_offset+24])[0],
                'Characteristics': struct.unpack('<I', self.data[section_offset+36:section_offset+40])[0],
            }
            self.sections.append(section)
        
        return True
    
    def extract_strings_from_section(self, section_name='.rdata'):
        """특정 섹션에서 문자열 추출"""
        strings = []
        
        for section in self.sections:
            if section_name.lower() in section['Name'].lower():
                start = section['PointerToRawData']
                end = min(start + section['SizeOfRawData'], len(self.data))
                
                current_string = b''
                for i in range(start, end):
                    byte = self.data[i]
                    if 32 <= byte < 127:  # 인쇄 가능한 ASCII
                        current_string += bytes([byte])
                    else:
                        if len(current_string) >= 4:  # 최소 4바이트 이상
                            try:
                                strings.append(current_string.decode('utf-8', errors='ignore'))
                            except:
                                pass
                        current_string = b''
        
        return strings
    
    def find_sqlite_functions(self):
        """SQLite 관련 함수 찾기"""
        sqlite_functions = []
        sqlite_keywords = [
            b'sqlite3_',
            b'SQLITE_',
            b'sqlite_',
        ]
        
        for keyword in sqlite_keywords:
            idx = 0
            while True:
                idx = self.data.find(keyword, idx)
                if idx == -1:
                    break
                
                # 함수명 추출 (키워드부터 공백/널까지)
                start = idx
                end = start + 100
                snippet = self.data[start:end]
                
                # 인쇄 가능한 문자만 추출
                func_name = b''
                for b in snippet:
                    if 32 <= b < 127 or b == 0:
                        if b == 0:
                            break
                        func_name += bytes([b])
                    else:
                        break
                
                if len(func_name) > len(keyword):
                    sqlite_functions.append(func_name.decode('utf-8', errors='ignore'))
                
                idx += 1
        
        return list(set(sqlite_functions))
    
    def find_dll_imports(self):
        """임포트된 DLL 및 함수 찾기"""
        imports = defaultdict(list)
        
        # .idata 섹션 찾기
        idata_section = None
        for section in self.sections:
            if '.idata' in section['Name'].lower() or '.rdata' in section['Name'].lower():
                idata_section = section
                break
        
        if not idata_section:
            return imports
        
        # 간단한 DLL 이름 검색
        dll_names = [b'sqlite3.dll', b'kernel32.dll', b'user32.dll', b'msvcrt.dll']
        
        for dll_name in dll_names:
            idx = 0
            while True:
                idx = self.data.find(dll_name, idx)
                if idx == -1:
                    break
                
                # DLL 이름 주변에서 함수명 찾기 시도
                imports[dll_name.decode('utf-8', errors='ignore')].append(f"참조 위치: 0x{idx:X}")
                idx += 1
        
        return imports
    
    def analyze(self):
        """전체 분석 수행"""
        if not self.read_file():
            return False
        
        if not self.parse_dos_header():
            return False
        
        if not self.parse_pe_header():
            return False
        
        if not self.parse_sections():
            return False
        
        return True
    
    def generate_report(self, output_file='pe_analysis_report.txt'):
        """분석 보고서 생성"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("DeskPro.exe PE 파일 구조 분석 보고서\n")
            f.write("=" * 80 + "\n\n")
            
            # 기본 정보
            f.write("## 기본 정보\n")
            f.write(f"파일: {self.file_path}\n")
            f.write(f"파일 크기: {len(self.data):,} bytes\n")
            if self.coff_header:
                f.write(f"머신 타입: 0x{self.coff_header['Machine']:04X}\n")
                f.write(f"섹션 수: {self.coff_header['NumberOfSections']}\n")
                f.write(f"빌드 시간: {self.coff_header['TimeDateStamp']}\n")
            f.write("\n")
            
            # 섹션 정보
            f.write("## 섹션 정보\n")
            for section in self.sections:
                f.write(f"\n섹션: {section['Name']}\n")
                f.write(f"  가상 크기: {section['VirtualSize']:,} bytes\n")
                f.write(f"  실제 크기: {section['SizeOfRawData']:,} bytes\n")
                f.write(f"  가상 주소: 0x{section['VirtualAddress']:08X}\n")
                f.write(f"  원시 데이터 오프셋: 0x{section['PointerToRawData']:08X}\n")
            f.write("\n")
            
            # SQLite 함수
            f.write("## SQLite 관련 함수\n")
            sqlite_funcs = self.find_sqlite_functions()
            if sqlite_funcs:
                for func in sorted(set(sqlite_funcs)):
                    f.write(f"  - {func}\n")
            else:
                f.write("  SQLite 함수를 찾을 수 없습니다.\n")
            f.write("\n")
            
            # DLL 임포트
            f.write("## 임포트된 DLL\n")
            imports = self.find_dll_imports()
            for dll, refs in imports.items():
                f.write(f"\n{dll}:\n")
                for ref in refs[:10]:  # 처음 10개만
                    f.write(f"  {ref}\n")
            f.write("\n")
            
            # .rdata 섹션에서 문자열 추출
            f.write("## .rdata 섹션에서 추출된 문자열 (SQL 관련)\n")
            strings = self.extract_strings_from_section('.rdata')
            sql_strings = [s for s in strings if any(kw in s.upper() for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'TABLE'])]
            for sql_str in sql_strings[:50]:  # 처음 50개만
                if len(sql_str) > 10:
                    f.write(f"  {sql_str[:200]}\n")
        
        print(f"\n분석 보고서가 {output_file}에 저장되었습니다.")

if __name__ == '__main__':
    exe_path = Path('DeskPro.exe')
    
    if not exe_path.exists():
        print(f"오류: {exe_path} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("PE 파일 구조 분석 시작...")
    analyzer = PEAnalyzer(exe_path)
    
    if analyzer.analyze():
        print("분석 완료!")
        analyzer.generate_report()
    else:
        print("분석 실패!")

