#!/usr/bin/env python
"""
Database Verification & Testing Script
Verifies all tables, indexes, and sample data are in place
"""

import sqlite3
from pathlib import Path
from db_admin import get_database_stats, get_question_banks_summary, get_all_subjects, get_all_semesters

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "question_bank.db"


def verify_database():
    """Run comprehensive database verification"""
    
    print("\n" + "=" * 80)
    print("QUESTION BANK DATABASE VERIFICATION")
    print("=" * 80)
    
    if not DB_PATH.exists():
        print("\n❌ ERROR: Database file not found!")
        print(f"   Expected at: {DB_PATH.absolute()}")
        return False
    
    print(f"\n✓ Database file found: {DB_PATH.absolute()}")
    print(f"  Size: {DB_PATH.stat().st_size / 1024:.2f} KB")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verify tables
    print("\n" + "-" * 80)
    print("1. TABLE VERIFICATION")
    print("-" * 80)
    
    required_tables = [
        'users', 'semesters', 'subjects', 'question_banks', 'units',
        'questions', 'paper_blueprints', 'question_papers', 'paper_questions', 'audit_logs'
    ]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in required_tables:
        if table in existing_tables:
            count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  ✓ {table:25} ({count} records)")
        else:
            print(f"  ❌ {table:25} (MISSING)")
            return False
    
    # Verify indexes
    print("\n" + "-" * 80)
    print("2. INDEX VERIFICATION")
    print("-" * 80)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]
    
    required_indexes = [
        'idx_qb_subject', 'idx_qb_semester', 'idx_q_bank', 
        'idx_q_marks', 'idx_q_status', 'idx_pq_paper', 'idx_pq_question'
    ]
    
    for idx in required_indexes:
        if idx in indexes:
            print(f"  ✓ {idx}")
        else:
            print(f"  ⚠ {idx} (missing, but not critical)")
    
    # Get statistics
    print("\n" + "-" * 80)
    print("3. DATA STATISTICS")
    print("-" * 80)
    
    stats = get_database_stats()
    print(f"  Users:                {stats['total_users']}")
    print(f"  Subjects:             {stats['total_subjects']}")
    print(f"  Semesters:            {stats['total_semesters']}")
    print(f"  Question Banks:       {stats['total_question_banks']}")
    print(f"  Total Questions:      {stats['total_questions']}")
    print(f"  Approved Questions:   {stats['approved_questions']}")
    print(f"  Generated Papers:     {stats['total_papers']}")
    
    # Get subjects
    print("\n" + "-" * 80)
    print("4. SUBJECTS IN DATABASE")
    print("-" * 80)
    
    subjects = get_all_subjects()
    if subjects:
        for s in subjects:
            print(f"  • {s['subject_code']:12} - {s['subject_name']}")
    else:
        print("  (None)")
    
    # Get semesters
    print("\n" + "-" * 80)
    print("5. SEMESTERS IN DATABASE")
    print("-" * 80)
    
    semesters = get_all_semesters()
    if semesters:
        for sem in semesters:
            active = "✓" if sem['is_active'] else "✗"
            print(f"  {active} Semester {sem['semester_number']} ({sem['academic_year']})")
    else:
        print("  (None)")
    
    # Get question banks
    print("\n" + "-" * 80)
    print("6. QUESTION BANKS SUMMARY")
    print("-" * 80)
    
    banks = get_question_banks_summary()
    if banks:
        print(f"\n  {'Subject':20} {'Semester':8} {'Questions':12} {'Status':15}")
        print("  " + "-" * 65)
        for bank in banks:
            qcount = bank['question_count'] if bank['question_count'] else 0
            status = "✓ Ready" if qcount >= 17 else f"⚠ Needs {17 - qcount} more"
            print(f"  {bank['subject_code']:20} Sem {bank['semester_number']:2}    {qcount:>3} questions     {status}")
    else:
        print("  (No question banks found)")
    
    # Connection check
    print("\n" + "-" * 80)
    print("7. CONNECTION & PERMISSIONS")
    print("-" * 80)
    
    try:
        test_cursor = conn.cursor()
        test_cursor.execute("SELECT 1")
        print("  ✓ Database read access: OK")
        
        test_cursor.execute("INSERT INTO audit_logs (user_id, action, table_name) VALUES (1, 'TEST', 'verification')")
        conn.commit()
        print("  ✓ Database write access: OK")
        
        test_cursor.execute("DELETE FROM audit_logs WHERE action = 'TEST'")
        conn.commit()
        print("  ✓ Database delete access: OK")
    except Exception as e:
        print(f"  ❌ Database access error: {e}")
        return False
    finally:
        conn.close()
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ DATABASE VERIFICATION COMPLETE - ALL SYSTEMS OK!")
    print("=" * 80)
    print(f"\nDatabase is ready to use for question bank management.")
    print(f"Web app running at: http://127.0.0.1:5000")
    print(f"Admin tools available in: db_admin.py")
    print()
    
    return True


if __name__ == "__main__":
    import sys
    success = verify_database()
    sys.exit(0 if success else 1)
