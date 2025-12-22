import fdb
import json

def check_pbirth():
    db_path = "/mnt/c/Users/DELL/Documents/db/MTSDB.FDB"
    try:
        conn = fdb.connect(
            database=db_path,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
        )
        cursor = conn.cursor()
        
        # '이주현' 환자의 생년월일 조회
        query = "SELECT PCODE, PNAME, PBIRTH FROM PERSON WHERE PNAME LIKE '이주현%'"
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            # PBIRTH의 타입과 값을 상세히 출력
            pbirth_val = row_dict['PBIRTH']
            results.append({
                'PCODE': row_dict['PCODE'],
                'PNAME': row_dict['PNAME'],
                'PBIRTH_VALUE': str(pbirth_val),
                'PBIRTH_TYPE': str(type(pbirth_val))
            })
            
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_pbirth()


