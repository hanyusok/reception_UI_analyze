"""
UI 요소와 SQL 쿼리 매핑 분석 스크립트
UI 화면의 버튼, 레이블, 입력 필드와 SQL 쿼리를 매칭합니다.
"""

import re
from pathlib import Path
from collections import defaultdict

class UISQLMapper:
    """UI와 SQL 매핑 분석기"""
    
    def __init__(self):
        self.ui_elements = {}
        self.sql_queries = []
        self.mappings = []
        
    def load_ui_structure(self):
        """UI 구조 정의 (이미지 분석 기반)"""
        self.ui_elements = {
            # 상단 헤더 버튼
            'header': {
                '종료': {'action': 'exit', 'type': 'button'},
                '설정': {'action': 'settings', 'type': 'button'},
                '인적사항': {'action': 'personal_info', 'type': 'button'},
                '검사입력': {'action': 'exam_input', 'type': 'button'},
                '계산서': {'action': 'invoice', 'type': 'button'},
                '접수일자': {'action': 'reception_date', 'type': 'button'},
                '메일': {'action': 'mail', 'type': 'button'},
                '진료실': {'action': 'consultation_room', 'type': 'button'},
                '신체계측': {'action': 'body_measurement', 'type': 'button'},
                '수납': {'action': 'payment', 'type': 'button'},
                '영상': {'action': 'image', 'type': 'button'},
                '원격접속': {'action': 'remote_access', 'type': 'button'},
            },
            
            # 접수업무 탭 - 버튼
            'reception_buttons': {
                '접수': {'action': 'register_patient', 'type': 'button'},
                '접종': {'action': 'vaccination', 'type': 'button'},
                '새가족': {'action': 'new_family', 'type': 'button'},
                '수정': {'action': 'modify_patient', 'type': 'button'},
                '기록': {'action': 'record_visit', 'type': 'button'},
                '취소': {'action': 'cancel', 'type': 'button'},
            },
            
            # 인적사항 입력 필드
            'personal_info_fields': {
                '수진자명': {'field': 'PNAME', 'table': 'PERSON', 'type': 'input'},
                '관계': {'field': 'RELATION', 'table': 'PERSON', 'type': 'input'},
                '개인번호': {'field': 'PCODE', 'table': 'PERSON', 'type': 'input'},
                '주민번호': {'field': 'PIDNUM', 'table': 'PERSON', 'type': 'input'},
                '생년월일': {'field': 'PBIRTH', 'table': 'PERSON', 'type': 'input'},
                '성별_남': {'field': 'SEX', 'table': 'PERSON', 'type': 'radio', 'value': 'M'},
                '성별_여': {'field': 'SEX', 'table': 'PERSON', 'type': 'radio', 'value': 'F'},
                '장애인': {'field': 'CRIPPLED', 'table': 'PERSON', 'type': 'checkbox'},
                '급여제한자': {'field': 'BOHUN', 'table': 'PERSON', 'type': 'checkbox'},
                '개인정보활용_동의': {'field': 'AGREE', 'table': 'PERSON', 'type': 'checkbox'},
            },
            
            # 가족 정보 입력 필드
            'family_info_fields': {
                '세대주명': {'field': 'FNAME', 'table': 'CARD', 'type': 'input'},
                '가족번호': {'field': 'FCODE', 'table': 'FAMILY', 'type': 'input'},
                '주민번호': {'field': 'FIDNUM', 'table': 'CARD', 'type': 'input'},
                '적용기간_시작': {'field': 'BEGINDATE', 'table': 'CARD', 'type': 'date'},
                '적용기간_종료': {'field': 'ENDDATE', 'table': 'CARD', 'type': 'date'},
                '구분': {'field': 'CARETYPE', 'table': 'CARD', 'type': 'dropdown'},
                '증번호': {'field': 'CARDNUM', 'table': 'CARD', 'type': 'input'},
                '직장': {'field': 'COMPANY', 'table': 'CARD', 'type': 'input'},
            },
            
            # 주소 정보
            'address_fields': {
                '우편번호': {'field': 'POSTAL_CODE', 'table': 'PERSON', 'type': 'input'},
                '주소': {'field': 'ADDRESS', 'table': 'PERSON', 'type': 'input'},
                '전화번호': {'field': 'PHONE', 'table': 'PERSON', 'type': 'input'},
                '휴대전화': {'field': 'MOBILE', 'table': 'PERSON', 'type': 'input'},
            },
            
            # 체크인 정보 (Vital 탭)
            'vital_fields': {
                '체중': {'field': 'WEIGHT', 'table': 'CHECKPERSON', 'type': 'input'},
                '키': {'field': 'HEIGHT', 'table': 'CHECKPERSON', 'type': 'input'},
                '체온': {'field': 'TEMPERATUR', 'table': 'CHECKPERSON', 'type': 'input'},
                '맥박': {'field': 'PULSE', 'table': 'CHECKPERSON', 'type': 'input'},
                '수축기혈압': {'field': 'SYSTOLIC', 'table': 'CHECKPERSON', 'type': 'input'},
                '이완기혈압': {'field': 'DIASTOLIC', 'table': 'CHECKPERSON', 'type': 'input'},
            },
            
            # 수납 관련
            'payment_fields': {
                '미수금': {'field': 'MISU', 'table': 'FEELOG', 'type': 'input'},
                '완불': {'field': 'WHANBUL', 'table': 'FEELOG', 'type': 'input'},
                '완수': {'field': 'WHANSU', 'table': 'FEELOG', 'type': 'input'},
            },
            
            # 진료 정보 (MASTERAUX)
            'treatment_fields': {
                '접수': {'field': 'ACCEPT', 'table': 'MASTERAUX', 'type': 'button'},
                '접수번호': {'field': 'ACCEPTNUM', 'table': 'MASTERAUX', 'type': 'input'},
                '접수번호2': {'field': 'ACCEPTNUM2', 'table': 'MASTERAUX', 'type': 'input'},
                '진단': {'field': 'DX2', 'table': 'MASTERAUX', 'type': 'input'},
                '진단특기': {'field': 'DX2SP', 'table': 'MASTERAUX', 'type': 'input'},
                '처방번호': {'field': 'PRESNUM2', 'table': 'MASTERAUX', 'type': 'input'},
                '요양비': {'field': 'CAREFEE', 'table': 'MASTERAUX', 'type': 'input'},
                '예약수수료': {'field': 'PREGFEE', 'table': 'MASTERAUX', 'type': 'input'},
            },
            
            # 탭
            'tabs': {
                '접수업무': {'action': 'reception_work', 'type': 'tab'},
                '인적조회': {'action': 'personal_inquiry', 'type': 'tab'},
                '카드조회': {'action': 'card_inquiry', 'type': 'tab'},
                '진료기록': {'action': 'medical_records', 'type': 'tab'},
                '인적사항': {'action': 'personal_info_tab', 'type': 'subtab'},
                'Vital': {'action': 'vital_tab', 'type': 'subtab'},
                '예방접종': {'action': 'vaccination_tab', 'type': 'subtab'},
                '예진': {'action': 'pre_exam_tab', 'type': 'subtab'},
                '가족명단': {'action': 'family_list', 'type': 'subtab'},
                '보험카드': {'action': 'insurance_card', 'type': 'subtab'},
            },
        }
    
    def load_sql_queries(self, sql_file='valid_sql_queries.txt'):
        """SQL 쿼리 로드"""
        sql_path = Path(sql_file)
        if not sql_path.exists():
            print(f"SQL 파일을 찾을 수 없습니다: {sql_file}")
            return False
        
        try:
            with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 쿼리 블록 파싱
            pattern = r'\[([^\]]+)\s+#(\d+)\]\s*-+\s*(.*?)\s*-+'
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                category = match.group(1).strip()
                query_num = match.group(2)
                query_text = match.group(3).strip()
                
                # 쿼리 타입 및 테이블 추출
                query_type = self._extract_query_type(query_text)
                tables = self._extract_tables(query_text)
                fields = self._extract_fields(query_text)
                
                self.sql_queries.append({
                    'category': category,
                    'number': query_num,
                    'text': query_text,
                    'type': query_type,
                    'tables': tables,
                    'fields': fields,
                })
            
            return True
        except Exception as e:
            print(f"SQL 파일 읽기 오류: {e}")
            return False
    
    def _extract_query_type(self, query):
        """쿼리 타입 추출"""
        query_upper = query.upper()
        if 'SELECT' in query_upper:
            return 'SELECT'
        elif 'INSERT' in query_upper:
            return 'INSERT'
        elif 'UPDATE' in query_upper:
            return 'UPDATE'
        elif 'DELETE' in query_upper:
            return 'DELETE'
        elif 'CREATE TABLE' in query_upper:
            return 'CREATE'
        else:
            return 'UNKNOWN'
    
    def _extract_tables(self, query):
        """테이블명 추출"""
        tables = []
        
        # FROM 절
        from_match = re.search(r'(?i)FROM\s+(\w+)', query)
        if from_match:
            tables.append(from_match.group(1))
        
        # UPDATE 절
        update_match = re.search(r'(?i)UPDATE\s+(\w+)', query)
        if update_match:
            tables.append(update_match.group(1))
        
        # INSERT INTO 절
        insert_match = re.search(r'(?i)INSERT\s+INTO\s+(\w+)', query)
        if insert_match:
            tables.append(insert_match.group(1))
        
        # CREATE TABLE 절
        create_match = re.search(r'(?i)CREATE\s+TABLE\s+(\w+)', query)
        if create_match:
            tables.append(create_match.group(1))
        
        return list(set(tables))
    
    def _extract_fields(self, query):
        """필드명 추출"""
        fields = []
        
        # SET 절의 필드들
        set_matches = re.finditer(r'(?i)SET\s+([^WHERE]+)', query)
        for match in set_matches:
            set_clause = match.group(1)
            # 필드명 = 값 패턴
            field_matches = re.finditer(r'(\w+)\s*=', set_clause)
            for fm in field_matches:
                field = fm.group(1).strip()
                if field and field not in fields:
                    fields.append(field)
        
        # INSERT INTO (필드1, 필드2, ...) 패턴
        insert_fields_match = re.search(r'(?i)INSERT\s+INTO\s+\w+\s*\(([^)]+)\)', query)
        if insert_fields_match:
            fields_str = insert_fields_match.group(1)
            field_list = [f.strip() for f in fields_str.split(',')]
            fields.extend([f for f in field_list if f and f not in fields])
        
        return fields
    
    def map_ui_to_sql(self):
        """UI 요소와 SQL 쿼리 매핑"""
        for ui_category, ui_items in self.ui_elements.items():
            for ui_name, ui_info in ui_items.items():
                ui_table = ui_info.get('table')
                ui_field = ui_info.get('field')
                ui_action = ui_info.get('action')
                
                # 관련 SQL 쿼리 찾기
                related_queries = []
                
                for sql_query in self.sql_queries:
                    # 테이블 매칭
                    if ui_table and ui_table in sql_query['tables']:
                        related_queries.append(sql_query)
                    # 필드 매칭
                    elif ui_field and ui_field in sql_query['fields']:
                        related_queries.append(sql_query)
                    # 액션 기반 매칭
                    elif self._action_matches(ui_action, sql_query):
                        related_queries.append(sql_query)
                
                if related_queries:
                    self.mappings.append({
                        'ui_category': ui_category,
                        'ui_name': ui_name,
                        'ui_info': ui_info,
                        'related_queries': related_queries,
                    })
    
    def _action_matches(self, action, sql_query):
        """액션과 SQL 쿼리 매칭"""
        action_map = {
            'register_patient': ['INSERT', 'UPDATE'],
            'modify_patient': ['UPDATE'],
            'new_family': ['INSERT'],
            'vaccination': ['DELETE'],  # VAX2 테이블
            'body_measurement': ['UPDATE'],  # CHECKPERSON 테이블
            'payment': ['UPDATE'],  # FEELOG 테이블
            'record_visit': ['UPDATE', 'INSERT'],  # MASTERAUX 테이블
        }
        
        if action in action_map:
            return sql_query['type'] in action_map[action]
        
        return False
    
    def generate_mapping_report(self, output_file='ui_sql_mapping_report.md'):
        """매핑 보고서 생성"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# UI 요소와 SQL 쿼리 매핑 보고서\n\n")
            f.write("이 문서는 DeskPro.exe의 UI 화면 요소와 SQL 쿼리를 매칭한 결과입니다.\n\n")
            f.write("## 목차\n")
            f.write("1. [버튼과 SQL 쿼리 매핑](#버튼과-sql-쿼리-매핑)\n")
            f.write("2. [입력 필드와 SQL 쿼리 매핑](#입력-필드와-sql-쿼리-매핑)\n")
            f.write("3. [탭과 SQL 쿼리 매핑](#탭과-sql-쿼리-매핑)\n")
            f.write("4. [테이블별 UI 요소 정리](#테이블별-ui-요소-정리)\n\n")
            
            # 버튼 매핑
            f.write("## 버튼과 SQL 쿼리 매핑\n\n")
            button_mappings = [m for m in self.mappings if m['ui_info']['type'] == 'button']
            for mapping in button_mappings:
                f.write(f"### {mapping['ui_name']}\n")
                f.write(f"- **카테고리**: {mapping['ui_category']}\n")
                if 'action' in mapping['ui_info']:
                    f.write(f"- **액션**: {mapping['ui_info']['action']}\n")
                f.write(f"- **관련 SQL 쿼리**:\n")
                for query in mapping['related_queries']:
                    f.write(f"  - [{query['type']}] {', '.join(query['tables']) if query['tables'] else 'N/A'}\n")
                    f.write(f"    ```sql\n")
                    f.write(f"    {query['text'][:200]}...\n")
                    f.write(f"    ```\n")
                f.write("\n")
            
            # 입력 필드 매핑
            f.write("## 입력 필드와 SQL 쿼리 매핑\n\n")
            field_mappings = [m for m in self.mappings if m['ui_info']['type'] in ['input', 'checkbox', 'radio', 'dropdown', 'date']]
            
            # 카테고리별로 그룹화
            by_category = defaultdict(list)
            for mapping in field_mappings:
                by_category[mapping['ui_category']].append(mapping)
            
            for category, mappings in by_category.items():
                f.write(f"### {category}\n\n")
                for mapping in mappings:
                    f.write(f"#### {mapping['ui_name']}\n")
                    f.write(f"- **필드**: {mapping['ui_info'].get('field', 'N/A')}\n")
                    f.write(f"- **테이블**: {mapping['ui_info'].get('table', 'N/A')}\n")
                    f.write(f"- **타입**: {mapping['ui_info']['type']}\n")
                    f.write(f"- **관련 SQL 쿼리**:\n")
                    for query in mapping['related_queries']:
                        f.write(f"  - [{query['type']}] {', '.join(query['tables'])}\n")
                        if mapping['ui_info'].get('field') in query['fields']:
                            f.write(f"    - 필드 '{mapping['ui_info']['field']}' 사용됨\n")
                    f.write("\n")
            
            # 탭 매핑
            f.write("## 탭과 SQL 쿼리 매핑\n\n")
            tab_mappings = [m for m in self.mappings if m['ui_info']['type'] in ['tab', 'subtab']]
            for mapping in tab_mappings:
                f.write(f"### {mapping['ui_name']}\n")
                if 'action' in mapping['ui_info']:
                    f.write(f"- **액션**: {mapping['ui_info']['action']}\n")
                f.write(f"- **관련 테이블**:\n")
                tables = set()
                for query in mapping['related_queries']:
                    if query['tables']:
                        tables.update(query['tables'])
                for table in sorted(tables):
                    f.write(f"  - {table}\n")
                f.write("\n")
            
            # 테이블별 정리
            f.write("## 테이블별 UI 요소 정리\n\n")
            table_ui_map = defaultdict(list)
            for mapping in self.mappings:
                ui_table = mapping['ui_info'].get('table')
                if ui_table:
                    table_ui_map[ui_table].append(mapping)
            
            for table, mappings in sorted(table_ui_map.items()):
                f.write(f"### {table} 테이블\n\n")
                f.write("**관련 UI 요소**:\n")
                for mapping in mappings:
                    f.write(f"- {mapping['ui_name']} ({mapping['ui_info']['type']})\n")
                    f.write(f"  - 필드: {mapping['ui_info'].get('field', 'N/A')}\n")
                f.write("\n**사용되는 SQL 쿼리**:\n")
                table_queries = [q for q in self.sql_queries if table in q['tables']]
                for query in table_queries:
                    f.write(f"- [{query['type']}] 쿼리 #{query['number']}\n")
                f.write("\n")
        
        print(f"\n매핑 보고서가 {output_file}에 저장되었습니다.")
    
    def generate_detailed_mapping(self, output_file='ui_sql_detailed_mapping.txt'):
        """상세 매핑 파일 생성 (구조화된 형식)"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("UI 요소와 SQL 쿼리 상세 매핑\n")
            f.write("=" * 80 + "\n\n")
            
            for mapping in self.mappings:
                f.write(f"\n{'=' * 80}\n")
                f.write(f"UI 요소: {mapping['ui_name']}\n")
                f.write(f"{'=' * 80}\n")
                f.write(f"카테고리: {mapping['ui_category']}\n")
                f.write(f"타입: {mapping['ui_info']['type']}\n")
                if 'field' in mapping['ui_info']:
                    f.write(f"데이터베이스 필드: {mapping['ui_info']['field']}\n")
                if 'table' in mapping['ui_info']:
                    f.write(f"데이터베이스 테이블: {mapping['ui_info']['table']}\n")
                if 'action' in mapping['ui_info']:
                    f.write(f"액션: {mapping['ui_info']['action']}\n")
                
                f.write(f"\n관련 SQL 쿼리 ({len(mapping['related_queries'])}개):\n")
                f.write("-" * 80 + "\n")
                for i, query in enumerate(mapping['related_queries'], 1):
                    f.write(f"\n[쿼리 #{i}]\n")
                    f.write(f"타입: {query['type']}\n")
                    f.write(f"테이블: {', '.join(query['tables'])}\n")
                    f.write(f"필드: {', '.join(query['fields'][:10])}\n")  # 처음 10개만
                    f.write(f"쿼리:\n{query['text'][:300]}...\n")
                    f.write("-" * 80 + "\n")
        
        print(f"상세 매핑 파일이 {output_file}에 저장되었습니다.")

if __name__ == '__main__':
    print("UI와 SQL 매핑 분석 시작...")
    
    mapper = UISQLMapper()
    mapper.load_ui_structure()
    print(f"UI 구조 로드 완료: {sum(len(v) for v in mapper.ui_elements.values())}개 요소")
    
    if mapper.load_sql_queries():
        print(f"SQL 쿼리 로드 완료: {len(mapper.sql_queries)}개")
        
        mapper.map_ui_to_sql()
        print(f"매핑 완료: {len(mapper.mappings)}개 매핑")
        
        mapper.generate_mapping_report()
        mapper.generate_detailed_mapping()
        
        print("\n분석 완료!")
    else:
        print("SQL 쿼리 로드 실패!")

