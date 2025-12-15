# UI 요소와 SQL 쿼리 매핑 보고서

이 문서는 DeskPro.exe의 UI 화면 요소와 SQL 쿼리를 매칭한 결과입니다.

## 목차
1. [버튼과 SQL 쿼리 매핑](#버튼과-sql-쿼리-매핑)
2. [입력 필드와 SQL 쿼리 매핑](#입력-필드와-sql-쿼리-매핑)
3. [탭과 SQL 쿼리 매핑](#탭과-sql-쿼리-매핑)
4. [테이블별 UI 요소 정리](#테이블별-ui-요소-정리)

## 버튼과 SQL 쿼리 매핑

### 신체계측
- **카테고리**: header
- **액션**: body_measurement
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET BLOODTYPE = :BloodType WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = :Picture WHERE...
    ```
  - [UPDATE] FEELOG
    ```sql
    UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu Ұ ￿￿+ WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EDate1 WHERE...
    ```
  - [UPDATE] CHECKPERSON
    ```sql
    UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET FNAME = :Fname WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, Ұ ￿￿N PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, RELATION2 = :Relation2, Ұ ￿￿J CRIPPLED = :Crippled, BOHUN = :Bohun, AG...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, Ұ ￿￿: FNAME = :Fname, FIDNUM = :Fidnum, UNIONCODE = :UnionCode, Ұ ￿￿> CARDNUM = :CardNum, COMPANY = :Company, CARETYPE = :CareType, Ұ ￿￿P CH...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET LASTCHECK = :LastCheck WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] VIEWCHECK
    ```sql
    UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```
  - [UPDATE] FAMILY
    ```sql
    UPDATE FAMILY SET Ұ ￿￿ ZIPCODE2 = :ZipCode2, N2 = :N2, Ұ ￿￿, HOUSENUM = :HouseNum, ZIPCODE3 = :ZipCode3, Ұ ￿￿@ ZONE3 = :Zone3, HOUSENUM3 = :HouseNum3, LOCALCODE = :LocalCode, Ұ ￿￿8 PHONENUM = :PhoneNu...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = NULL WHERE...
    ```
  - [UPDATE] MASTERNUM
    ```sql
    UPDATE MASTERNUM SET N = :N WHERE...
    ```

### 수납
- **카테고리**: header
- **액션**: payment
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET BLOODTYPE = :BloodType WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = :Picture WHERE...
    ```
  - [UPDATE] FEELOG
    ```sql
    UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu Ұ ￿￿+ WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EDate1 WHERE...
    ```
  - [UPDATE] CHECKPERSON
    ```sql
    UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET FNAME = :Fname WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, Ұ ￿￿N PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, RELATION2 = :Relation2, Ұ ￿￿J CRIPPLED = :Crippled, BOHUN = :Bohun, AG...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, Ұ ￿￿: FNAME = :Fname, FIDNUM = :Fidnum, UNIONCODE = :UnionCode, Ұ ￿￿> CARDNUM = :CardNum, COMPANY = :Company, CARETYPE = :CareType, Ұ ￿￿P CH...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET LASTCHECK = :LastCheck WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] VIEWCHECK
    ```sql
    UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```
  - [UPDATE] FAMILY
    ```sql
    UPDATE FAMILY SET Ұ ￿￿ ZIPCODE2 = :ZipCode2, N2 = :N2, Ұ ￿￿, HOUSENUM = :HouseNum, ZIPCODE3 = :ZipCode3, Ұ ￿￿@ ZONE3 = :Zone3, HOUSENUM3 = :HouseNum3, LOCALCODE = :LocalCode, Ұ ￿￿8 PHONENUM = :PhoneNu...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = NULL WHERE...
    ```
  - [UPDATE] MASTERNUM
    ```sql
    UPDATE MASTERNUM SET N = :N WHERE...
    ```

### 접수
- **카테고리**: reception_buttons
- **액션**: register_patient
- **관련 SQL 쿼리**:
  - [INSERT] LAST, FAMILY
    ```sql
    UPDATE LAST SET FCODE = :Fcode Ұ ￿￿* INSERT INTO FAMILY (FCODE) VALUES (:Fcode) Ұ ￿￿5 UPDATE PERSON SET FCODE = :Fcode WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET BLOODTYPE = :BloodType WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = :Picture WHERE...
    ```
  - [UPDATE] FEELOG
    ```sql
    UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu Ұ ￿￿+ WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EDate1 WHERE...
    ```
  - [UPDATE] CHECKPERSON
    ```sql
    UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET FNAME = :Fname WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, Ұ ￿￿N PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, RELATION2 = :Relation2, Ұ ￿￿J CRIPPLED = :Crippled, BOHUN = :Bohun, AG...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, Ұ ￿￿: FNAME = :Fname, FIDNUM = :Fidnum, UNIONCODE = :UnionCode, Ұ ￿￿> CARDNUM = :CardNum, COMPANY = :Company, CARETYPE = :CareType, Ұ ￿￿P CH...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET LASTCHECK = :LastCheck WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] VIEWCHECK
    ```sql
    UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```
  - [UPDATE] FAMILY
    ```sql
    UPDATE FAMILY SET Ұ ￿￿ ZIPCODE2 = :ZipCode2, N2 = :N2, Ұ ￿￿, HOUSENUM = :HouseNum, ZIPCODE3 = :ZipCode3, Ұ ￿￿@ ZONE3 = :Zone3, HOUSENUM3 = :HouseNum3, LOCALCODE = :LocalCode, Ұ ￿￿8 PHONENUM = :PhoneNu...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = NULL WHERE...
    ```
  - [UPDATE] MASTERNUM
    ```sql
    UPDATE MASTERNUM SET N = :N WHERE...
    ```

### 접종
- **카테고리**: reception_buttons
- **액션**: vaccination
- **관련 SQL 쿼리**:
  - [DELETE] dataset
    ```sql
    delete from dataset. (No delete query)&Cannot refresh row. (No refresh query) Buffer not set!Circular references not permitted SQL Parse Error:...
    ```
  - [DELETE] PERSON
    ```sql
    DELETE FROM PERSON WHERE...
    ```
  - [DELETE] CARD
    ```sql
    DELETE FROM CARD WHERE...
    ```
  - [DELETE] VAX2
    ```sql
    DELETE FROM VAX2 WHERE...
    ```
  - [DELETE] DISEREG
    ```sql
    DELETE FROM DISEREG WHERE...
    ```
  - [DELETE] CHECKPERSON
    ```sql
    DELETE FROM CHECKPERSON WHERE...
    ```
  - [DELETE] DUO
    ```sql
    DELETE FROM DUO 䴆䥁䑎XҰ ￿￿) WHERE...
    ```

### 새가족
- **카테고리**: reception_buttons
- **액션**: new_family
- **관련 SQL 쿼리**:
  - [INSERT] LAST, FAMILY
    ```sql
    UPDATE LAST SET FCODE = :Fcode Ұ ￿￿* INSERT INTO FAMILY (FCODE) VALUES (:Fcode) Ұ ￿￿5 UPDATE PERSON SET FCODE = :Fcode WHERE...
    ```

### 수정
- **카테고리**: reception_buttons
- **액션**: modify_patient
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET BLOODTYPE = :BloodType WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = :Picture WHERE...
    ```
  - [UPDATE] FEELOG
    ```sql
    UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu Ұ ￿￿+ WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EDate1 WHERE...
    ```
  - [UPDATE] CHECKPERSON
    ```sql
    UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET FNAME = :Fname WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, Ұ ￿￿N PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, RELATION2 = :Relation2, Ұ ￿￿J CRIPPLED = :Crippled, BOHUN = :Bohun, AG...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, Ұ ￿￿: FNAME = :Fname, FIDNUM = :Fidnum, UNIONCODE = :UnionCode, Ұ ￿￿> CARDNUM = :CardNum, COMPANY = :Company, CARETYPE = :CareType, Ұ ￿￿P CH...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET LASTCHECK = :LastCheck WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] VIEWCHECK
    ```sql
    UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```
  - [UPDATE] FAMILY
    ```sql
    UPDATE FAMILY SET Ұ ￿￿ ZIPCODE2 = :ZipCode2, N2 = :N2, Ұ ￿￿, HOUSENUM = :HouseNum, ZIPCODE3 = :ZipCode3, Ұ ￿￿@ ZONE3 = :Zone3, HOUSENUM3 = :HouseNum3, LOCALCODE = :LocalCode, Ұ ￿￿8 PHONENUM = :PhoneNu...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = NULL WHERE...
    ```
  - [UPDATE] MASTERNUM
    ```sql
    UPDATE MASTERNUM SET N = :N WHERE...
    ```

### 기록
- **카테고리**: reception_buttons
- **액션**: record_visit
- **관련 SQL 쿼리**:
  - [INSERT] LAST, FAMILY
    ```sql
    UPDATE LAST SET FCODE = :Fcode Ұ ￿￿* INSERT INTO FAMILY (FCODE) VALUES (:Fcode) Ұ ￿￿5 UPDATE PERSON SET FCODE = :Fcode WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET BLOODTYPE = :BloodType WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = :Picture WHERE...
    ```
  - [UPDATE] FEELOG
    ```sql
    UPDATE FEELOG SET MISU = :Misu, WHANBUL = :Whanbul, WHANSU = :Whansu Ұ ￿￿+ WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PSNIDT = :PsnIdT, PSNID = :PsnId WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EDate1 WHERE...
    ```
  - [UPDATE] CHECKPERSON
    ```sql
    UPDATE CHECKPERSON SET WEIGHT = :WEIGHT, HEIGHT = :HEIGHT, TEMPERATUR = :TEMPERATUR, PULSE = :PULSE, SYSTOLIC = :SYSTOLIC, DIASTOLIC = :DIASTOLIC WHERE...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET FNAME = :Fname WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PNAME = :Pname, PBIRTH = :Pbirth, PIDNUM = :Pidnum, Ұ ￿￿N PIDNUM2 = :Pidnum2, SEX = :Sex, RELATION = :Relation, RELATION2 = :Relation2, Ұ ￿￿J CRIPPLED = :Crippled, BOHUN = :Bohun, AG...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate, BEGINDATE = :BeginDate, Ұ ￿￿: FNAME = :Fname, FIDNUM = :Fidnum, UNIONCODE = :UnionCode, Ұ ￿￿> CARDNUM = :CardNum, COMPANY = :Company, CARETYPE = :CareType, Ұ ￿￿P CH...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET LASTCHECK = :LastCheck WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] VIEWCHECK
    ```sql
    UPDATE VIEWCHECK SET VIEWCHECK = :ViewCheck, VIEWTEXT = :Vw WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```
  - [UPDATE] FAMILY
    ```sql
    UPDATE FAMILY SET Ұ ￿￿ ZIPCODE2 = :ZipCode2, N2 = :N2, Ұ ￿￿, HOUSENUM = :HouseNum, ZIPCODE3 = :ZipCode3, Ұ ￿￿@ ZONE3 = :Zone3, HOUSENUM3 = :HouseNum3, LOCALCODE = :LocalCode, Ұ ￿￿8 PHONENUM = :PhoneNu...
    ```
  - [UPDATE] CARD
    ```sql
    UPDATE CARD SET ENDDATE = :EndDate WHERE...
    ```
  - [UPDATE] PERSON
    ```sql
    UPDATE PERSON SET PICTURE = NULL WHERE...
    ```
  - [UPDATE] MASTERNUM
    ```sql
    UPDATE MASTERNUM SET N = :N WHERE...
    ```

### 접수
- **카테고리**: treatment_fields
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET Ұ ￿￿ 수진자 진료확인번호 내려받기 실패... 다시 시도해주세요. Ұ ￿￿@ UPDATE MASTERAUX SET ACCEPT = :Accept, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿( ERRCODE = :ErrCode, SELFEE2 = :SelFee2, Ұ ￿￿...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET ACCEPT = NULL, ACCEPTNUM = NULL, Ұ ￿￿# ACCEPTNUM2 = NULL, SELFEE2 = NULL, Ұ ￿￿' REQCAREFEE2 = NULL, REMCAREFEE = NULL, Ұ ￿￿( REQPREGFEE2 := NULL, REMPREGFEE = NULL, Ұ ￿￿< PRESNUM2...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET PIDNUM = :Pidnum, Pname = :Pname, CHK = :Chk, Ұ ￿￿6 SPCODE = :Spcode, BUDAM = :Budam, CAREFEE = :CareFee, Ұ ￿￿> PREGFEE = :PregFee WHERE...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK := :Chk, SPCODE = :Spcode, Ұ ￿￿D ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, ACCEPTNUM2 = :AcceptNum2, Ұ ￿￿ SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :R...
    ```
  - [UPDATE] MASTERAUX
    ```sql
    UPDATE MASTERAUX SET CHK = :Chk, SPCODE = :Spcode, Ұ ￿￿> ACCEPT = :Accept, ACCEPTNUM = :AcceptNum, SELFEE2 = :SelFee2, Ұ ￿￿6 REQCAREFEE2 = :ReqCareFee2, REMCAREFEE = :RemCareFee, Ұ ￿￿6 REQPREGFEE2 = :...
    ```

## 입력 필드와 SQL 쿼리 매핑

### personal_info_fields

#### 수진자명
- **필드**: PNAME
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 관계
- **필드**: RELATION
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 개인번호
- **필드**: PCODE
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 주민번호
- **필드**: PIDNUM
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] MASTERAUX
    - 필드 'PIDNUM' 사용됨
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 생년월일
- **필드**: PBIRTH
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 성별_남
- **필드**: SEX
- **테이블**: PERSON
- **타입**: radio
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 성별_여
- **필드**: SEX
- **테이블**: PERSON
- **타입**: radio
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 장애인
- **필드**: CRIPPLED
- **테이블**: PERSON
- **타입**: checkbox
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 급여제한자
- **필드**: BOHUN
- **테이블**: PERSON
- **타입**: checkbox
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 개인정보활용_동의
- **필드**: AGREE
- **테이블**: PERSON
- **타입**: checkbox
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

### family_info_fields

#### 세대주명
- **필드**: FNAME
- **테이블**: CARD
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 가족번호
- **필드**: FCODE
- **테이블**: FAMILY
- **타입**: input
- **관련 SQL 쿼리**:
  - [INSERT] LAST, FAMILY
    - 필드 'FCODE' 사용됨
  - [UPDATE] FAMILY

#### 주민번호
- **필드**: FIDNUM
- **테이블**: CARD
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 적용기간_시작
- **필드**: BEGINDATE
- **테이블**: CARD
- **타입**: date
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 적용기간_종료
- **필드**: ENDDATE
- **테이블**: CARD
- **타입**: date
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 구분
- **필드**: CARETYPE
- **테이블**: CARD
- **타입**: dropdown
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 증번호
- **필드**: CARDNUM
- **테이블**: CARD
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

#### 직장
- **필드**: COMPANY
- **테이블**: CARD
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [UPDATE] CARD
  - [DELETE] CARD

### address_fields

#### 우편번호
- **필드**: POSTAL_CODE
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 주소
- **필드**: ADDRESS
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 전화번호
- **필드**: PHONE
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

#### 휴대전화
- **필드**: MOBILE
- **테이블**: PERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [UPDATE] PERSON
  - [DELETE] PERSON

### vital_fields

#### 체중
- **필드**: WEIGHT
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

#### 키
- **필드**: HEIGHT
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

#### 체온
- **필드**: TEMPERATUR
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

#### 맥박
- **필드**: PULSE
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

#### 수축기혈압
- **필드**: SYSTOLIC
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

#### 이완기혈압
- **필드**: DIASTOLIC
- **테이블**: CHECKPERSON
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] CHECKPERSON
  - [DELETE] CHECKPERSON

### payment_fields

#### 미수금
- **필드**: MISU
- **테이블**: FEELOG
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] FEELOG
    - 필드 'MISU' 사용됨

#### 완불
- **필드**: WHANBUL
- **테이블**: FEELOG
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] FEELOG

#### 완수
- **필드**: WHANSU
- **테이블**: FEELOG
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] FEELOG

### treatment_fields

#### 접수번호
- **필드**: ACCEPTNUM
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 접수번호2
- **필드**: ACCEPTNUM2
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 진단
- **필드**: DX2
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 진단특기
- **필드**: DX2SP
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 처방번호
- **필드**: PRESNUM2
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 요양비
- **필드**: CAREFEE
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

#### 예약수수료
- **필드**: PREGFEE
- **테이블**: MASTERAUX
- **타입**: input
- **관련 SQL 쿼리**:
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX
  - [UPDATE] MASTERAUX

## 탭과 SQL 쿼리 매핑

## 테이블별 UI 요소 정리

### CARD 테이블

**관련 UI 요소**:
- 세대주명 (input)
  - 필드: FNAME
- 주민번호 (input)
  - 필드: FIDNUM
- 적용기간_시작 (date)
  - 필드: BEGINDATE
- 적용기간_종료 (date)
  - 필드: ENDDATE
- 구분 (dropdown)
  - 필드: CARETYPE
- 증번호 (input)
  - 필드: CARDNUM
- 직장 (input)
  - 필드: COMPANY

**사용되는 SQL 쿼리**:
- [UPDATE] 쿼리 #7
- [UPDATE] 쿼리 #9
- [UPDATE] 쿼리 #11
- [UPDATE] 쿼리 #19
- [DELETE] 쿼리 #3

### CHECKPERSON 테이블

**관련 UI 요소**:
- 체중 (input)
  - 필드: WEIGHT
- 키 (input)
  - 필드: HEIGHT
- 체온 (input)
  - 필드: TEMPERATUR
- 맥박 (input)
  - 필드: PULSE
- 수축기혈압 (input)
  - 필드: SYSTOLIC
- 이완기혈압 (input)
  - 필드: DIASTOLIC

**사용되는 SQL 쿼리**:
- [UPDATE] 쿼리 #8
- [DELETE] 쿼리 #6

### FAMILY 테이블

**관련 UI 요소**:
- 가족번호 (input)
  - 필드: FCODE

**사용되는 SQL 쿼리**:
- [INSERT] 쿼리 #1
- [UPDATE] 쿼리 #18

### FEELOG 테이블

**관련 UI 요소**:
- 미수금 (input)
  - 필드: MISU
- 완불 (input)
  - 필드: WHANBUL
- 완수 (input)
  - 필드: WHANSU

**사용되는 SQL 쿼리**:
- [UPDATE] 쿼리 #4

### MASTERAUX 테이블

**관련 UI 요소**:
- 접수 (button)
  - 필드: ACCEPT
- 접수번호 (input)
  - 필드: ACCEPTNUM
- 접수번호2 (input)
  - 필드: ACCEPTNUM2
- 진단 (input)
  - 필드: DX2
- 진단특기 (input)
  - 필드: DX2SP
- 처방번호 (input)
  - 필드: PRESNUM2
- 요양비 (input)
  - 필드: CAREFEE
- 예약수수료 (input)
  - 필드: PREGFEE

**사용되는 SQL 쿼리**:
- [UPDATE] 쿼리 #2
- [UPDATE] 쿼리 #12
- [UPDATE] 쿼리 #14
- [UPDATE] 쿼리 #16
- [UPDATE] 쿼리 #17

### PERSON 테이블

**관련 UI 요소**:
- 수진자명 (input)
  - 필드: PNAME
- 관계 (input)
  - 필드: RELATION
- 개인번호 (input)
  - 필드: PCODE
- 주민번호 (input)
  - 필드: PIDNUM
- 생년월일 (input)
  - 필드: PBIRTH
- 성별_남 (radio)
  - 필드: SEX
- 성별_여 (radio)
  - 필드: SEX
- 장애인 (checkbox)
  - 필드: CRIPPLED
- 급여제한자 (checkbox)
  - 필드: BOHUN
- 개인정보활용_동의 (checkbox)
  - 필드: AGREE
- 우편번호 (input)
  - 필드: POSTAL_CODE
- 주소 (input)
  - 필드: ADDRESS
- 전화번호 (input)
  - 필드: PHONE
- 휴대전화 (input)
  - 필드: MOBILE

**사용되는 SQL 쿼리**:
- [UPDATE] 쿼리 #1
- [UPDATE] 쿼리 #3
- [UPDATE] 쿼리 #5
- [UPDATE] 쿼리 #6
- [UPDATE] 쿼리 #10
- [UPDATE] 쿼리 #13
- [UPDATE] 쿼리 #20
- [DELETE] 쿼리 #2

