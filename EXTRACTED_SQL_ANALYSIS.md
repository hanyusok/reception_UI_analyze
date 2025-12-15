# Extracted SQL Queries Analysis

**File**: `extracted_sql_queries.txt`  
**Total Lines**: 3,765  
**Date**: 2025-01-15

## Overview

This file contains SQL queries extracted from reverse engineering a binary application. The queries were extracted from the application's memory/binary structure and represent the database operations the application performs.

## File Structure

- **Format**: Each query is numbered (쿼리 #1, 쿼리 #2, etc.)
- **Encoding**: Mixed encodings (UTF-16, UTF-8)
- **Quality**: Many queries are incomplete or corrupted with binary data
- **Source**: Extracted from compiled application binary

## Key Findings

### Valid SQL Queries Found

The file contains several valid SQL queries that match the database schema:

1. **INSERT INTO MASTERAUX**
   - `INSERT INTO MASTERAUX (PCODE, VISIDATE) VALUES`
   - Matches the MASTERAUX table structure

2. **INSERT INTO CARD**
   - `INSERT INTO CARD (PCODE, ENDDATE, BEGINDATE, FNAME, FIDNUM, UNIONCODE, CARDNUM, CARETYPE, CHA, OTHERAREA) VALUES`
   - Matches the CARD table structure

3. **INSERT INTO WAIT**
   - `INSERT INTO WAIT (PCODE, VISIDATE, RESID1, RESID2, GOODOC, ROOMCODE, ROOMNM, DEPTCODE, DEPTNM, DOCTRCODE, DOCTRNM) VALUES`
   - Waiting list/queue table

4. **SELECT Statements**
   - Various SELECT queries
   - Firebird system queries (RDB$INDEX_NAME, etc.)

### Data Quality Issues

1. **Binary Data Corruption**
   - Many queries contain binary data mixed with SQL
   - Encoding issues (UTF-16 vs UTF-8)
   - Incomplete query strings

2. **Delphi/InterBase Components**
   - Contains references to TIBSQL, FIB components
   - Firebird/InterBase specific SQL syntax
   - Component property data mixed in

3. **Incomplete Queries**
   - Many queries are fragments
   - Missing VALUES clauses
   - Missing WHERE conditions

## Relevance to Current Project

### ✅ **Useful Information**

1. **Table Names Confirmed**
   - MASTERAUX - Matches current schema
   - CARD - Matches current schema
   - WAIT - Additional table (waiting list)
   - DUO - Additional table

2. **Field Names**
   - Confirms field names used in the original application
   - Matches the schema defined in DATABASE_SETUP.md (before deletion)

3. **Firebird-Specific Queries**
   - Confirms the original application uses Firebird
   - Shows Firebird system table queries (RDB$*)

### ⚠️ **Limitations**

1. **Not Directly Usable**
   - Queries are incomplete/corrupted
   - Cannot be used as-is for API implementation
   - Need to be reconstructed from schema

2. **Outdated for Current Architecture**
   - Current project uses remote REST API
   - These queries are for direct database access
   - Not needed for frontend implementation

3. **Binary Data**
   - Much of the file contains binary/compiled code
   - Not human-readable SQL

## Recommendations

### For Current Project

1. **Not Required for Frontend**
   - Frontend uses remote REST API
   - These queries are handled by the remote API service
   - No need to implement these in the frontend

2. **Useful for Reference**
   - Can help understand original application structure
   - Useful for documenting expected behavior
   - May help with API endpoint design

3. **For Remote API Service**
   - These queries could be useful for the remote API service implementation
   - Help understand what operations the original application performed
   - Can guide API endpoint design

## File Status

- **Purpose**: Reference/documentation of original application
- **Action Required**: None for frontend project
- **Use Case**: Understanding original application behavior
- **Maintenance**: Optional - can be kept for reference or removed

## Summary

The `extracted_sql_queries.txt` file contains SQL queries extracted from reverse engineering the original application. While it provides useful insights into the database structure and operations, it's **not directly relevant** to the current frontend project since:

1. Frontend uses remote REST API (no direct SQL)
2. Many queries are corrupted/incomplete
3. Queries are for reference only, not implementation

The file can be kept for reference or removed if not needed.

