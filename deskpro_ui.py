import sys
import sqlite3
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTabWidget, QTableWidget, 
    QTableWidgetItem, QGroupBox, QGridLayout, QRadioButton, 
    QCheckBox, QComboBox, QDateEdit, QFrame, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QDate

class DatabaseManager:
    def __init__(self, db_path="deskpro.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # PERSON 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PERSON (
                PCODE INTEGER PRIMARY KEY AUTOINCREMENT,
                PNAME TEXT NOT NULL,
                PBIRTH TEXT,
                PIDNUM TEXT,
                PIDNUM2 TEXT,
                SEX TEXT,
                RELATION TEXT,
                CRIPPLED INTEGER DEFAULT 0,
                BOHUN INTEGER DEFAULT 0,
                AGREE INTEGER DEFAULT 0,
                FCODE INTEGER
            )
        ''')
        
        # CARD 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CARD (
                PCODE INTEGER,
                FNAME TEXT,
                BEGINDATE TEXT,
                ENDDATE TEXT,
                CARETYPE TEXT,
                CARDNUM TEXT,
                FOREIGN KEY (PCODE) REFERENCES PERSON(PCODE)
            )
        ''')
        
        # MASTERAUX 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MASTERAUX (
                PCODE INTEGER,
                VISIDATE TEXT,
                ACCEPTNUM TEXT,
                DX2 TEXT,
                FOREIGN KEY (PCODE) REFERENCES PERSON(PCODE)
            )
        ''')
        
        # 샘플 데이터 추가 (데이터가 없을 경우)
        cursor.execute("SELECT COUNT(*) FROM PERSON")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO PERSON (PNAME, PBIRTH, PIDNUM, SEX) VALUES (?, ?, ?, ?)", 
                           ("홍길동", "1990-01-01", "900101-1234567", "M"))
            cursor.execute("INSERT INTO PERSON (PNAME, PBIRTH, PIDNUM, SEX) VALUES (?, ?, ?, ?)", 
                           ("김철수", "1985-05-20", "850520-1234567", "M"))
        
        conn.commit()
        conn.close()

    def search_patients(self, keyword):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM PERSON WHERE PNAME LIKE ?"
        cursor.execute(query, (f"%{keyword}%",))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def save_patient(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if 'PCODE' in data and data['PCODE']:
            # 수정 (UPDATE)
            query = '''
                UPDATE PERSON SET 
                PNAME = :PNAME, PBIRTH = :PBIRTH, PIDNUM = :PIDNUM, 
                SEX = :SEX, RELATION = :RELATION, AGREE = :AGREE 
                WHERE PCODE = :PCODE
            '''
            cursor.execute(query, data)
        else:
            # 신규 (INSERT)
            fields = ['PNAME', 'PBIRTH', 'PIDNUM', 'SEX', 'RELATION', 'AGREE']
            placeholders = [f":{f}" for f in fields]
            query = f"INSERT INTO PERSON ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(query, data)
            
        conn.commit()
        conn.close()

class DeskProUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_patient_pcode = None
        
        self.setWindowTitle("DeskPro - 접수 및 진료 관리 시스템 (SQL 연동)")
        self.setGeometry(100, 100, 1200, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # 헤더
        header_layout = QHBoxLayout()
        for btn_text in ["종료", "설정", "인적사항", "검사입력", "계산서", "접수일자", "메일", "진료실", "신체계측", "수납", "영상", "원격접속"]:
            btn = QPushButton(btn_text)
            header_layout.addWidget(btn)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        
        # 왼쪽 패널
        left_panel = QVBoxLayout()
        self.left_tabs = QTabWidget()
        self.reception_tab = QWidget()
        self.setup_reception_tab(self.reception_tab)
        self.left_tabs.addTab(self.reception_tab, "접수업무")
        left_panel.addWidget(self.left_tabs)
        content_layout.addLayout(left_panel, 2)
        
        # 오른쪽 패널
        right_panel = QVBoxLayout()
        self.right_tabs = QTabWidget()
        self.right_tabs.addTab(self.create_waiting_list(), "대기")
        right_panel.addWidget(self.right_tabs)
        content_layout.addLayout(right_panel, 3)
        
        main_layout.addLayout(content_layout)

    def setup_reception_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("수진자 검색:"))
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("조회")
        search_btn.clicked.connect(self.on_search)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)
        
        # 인적사항 폼
        self.form_fields = {}
        info_group = QGroupBox("인적사항")
        grid = QGridLayout()
        
        grid.addWidget(QLabel("수진자명"), 0, 0)
        self.form_fields['PNAME'] = QLineEdit()
        grid.addWidget(self.form_fields['PNAME'], 0, 1)
        
        grid.addWidget(QLabel("주민번호"), 1, 0)
        self.form_fields['PIDNUM'] = QLineEdit()
        grid.addWidget(self.form_fields['PIDNUM'], 1, 1, 1, 3)
        
        grid.addWidget(QLabel("생년월일"), 2, 0)
        self.form_fields['PBIRTH'] = QDateEdit(calendarPopup=True)
        self.form_fields['PBIRTH'].setDisplayFormat("yyyy-mm-dd")
        grid.addWidget(self.form_fields['PBIRTH'], 2, 1)
        
        grid.addWidget(QLabel("성별"), 3, 0)
        self.gender_m = QRadioButton("남")
        self.gender_f = QRadioButton("여")
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.gender_m)
        gender_layout.addWidget(self.gender_f)
        grid.addLayout(gender_layout, 3, 1)
        
        self.form_fields['AGREE'] = QCheckBox("개인정보활용 동의")
        grid.addWidget(self.form_fields['AGREE'], 4, 1)
        
        info_group.setLayout(grid)
        layout.addWidget(info_group)
        
        # 액션 버튼
        act_layout = QHBoxLayout()
        self.btn_save = QPushButton("접수/저장")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_new = QPushButton("신규")
        self.btn_new.clicked.connect(self.clear_form)
        act_layout.addWidget(self.btn_save)
        act_layout.addWidget(self.btn_new)
        layout.addLayout(act_layout)

        # 검색 결과 테이블
        self.result_table = QTableWidget(0, 4)
        self.result_table.setHorizontalHeaderLabels(["개인번호", "성명", "생년월일", "주민번호"])
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.itemDoubleClicked.connect(self.load_patient_details)
        layout.addWidget(self.result_table)

    def create_waiting_list(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.wait_table = QTableWidget(5, 4)
        self.wait_table.setHorizontalHeaderLabels(["순번", "성명", "상태", "시간"])
        layout.addWidget(self.wait_table)
        return widget

    def on_search(self):
        keyword = self.search_input.text()
        results = self.db.search_patients(keyword)
        
        self.result_table.setRowCount(0)
        for row_data in results:
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(str(row_data['PCODE'])))
            self.result_table.setItem(row, 1, QTableWidgetItem(row_data['PNAME']))
            self.result_table.setItem(row, 2, QTableWidgetItem(row_data['PBIRTH']))
            self.result_table.setItem(row, 3, QTableWidgetItem(row_data['PIDNUM']))

    def load_patient_details(self, item):
        row = item.row()
        pcode = self.result_table.item(row, 0).text()
        
        # 테이블에서 직접 로드 (실제로는 DB 재조회 권장)
        self.current_patient_pcode = int(pcode)
        self.form_fields['PNAME'].setText(self.result_table.item(row, 1).text())
        self.form_fields['PIDNUM'].setText(self.result_table.item(row, 3).text())
        
        birth_str = self.result_table.item(row, 2).text()
        if birth_str:
            self.form_fields['PBIRTH'].setDate(QDate.fromString(birth_str, "yyyy-MM-dd"))
            
        # 성별/동의 등은 검색결과에 없으므로 여기선 생략 또는 DB 재조회 로직 추가

    def on_save(self):
        data = {
            'PNAME': self.form_fields['PNAME'].text(),
            'PBIRTH': self.form_fields['PBIRTH'].date().toString("yyyy-MM-dd"),
            'PIDNUM': self.form_fields['PIDNUM'].text(),
            'SEX': 'M' if self.gender_m.isChecked() else 'F',
            'AGREE': 1 if self.form_fields['AGREE'].isChecked() else 0,
            'RELATION': '본인'
        }
        
        if self.current_patient_pcode:
            data['PCODE'] = self.current_patient_pcode
            
        try:
            self.db.save_patient(data)
            QMessageBox.information(self, "성공", "환자 정보가 저장되었습니다.")
            self.on_search()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {str(e)}")

    def clear_form(self):
        self.current_patient_pcode = None
        self.form_fields['PNAME'].clear()
        self.form_fields['PIDNUM'].clear()
        self.form_fields['PBIRTH'].setDate(QDate.currentDate())
        self.form_fields['AGREE'].setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeskProUI()
    window.show()
    sys.exit(app.exec())
