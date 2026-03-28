"""
Database Admin Panel - Manage subjects, semesters, question banks
Routes and utilities for database administration
"""

from flask import render_template, request, flash, redirect, url_for
import sqlite3
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "question_bank.db"


def get_all_subjects():
    """Get all subjects from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    subjects = cursor.execute("SELECT * FROM subjects ORDER BY subject_code").fetchall()
    conn.close()
    return list(subjects)


def get_all_semesters():
    """Get all semesters"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    semesters = cursor.execute("SELECT * FROM semesters ORDER BY academic_year DESC, semester_number").fetchall()
    conn.close()
    return list(semesters)


def get_question_banks_summary():
    """Get summary of all question banks with stats"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    banks = cursor.execute("""
        SELECT 
            qb.id,
            s.subject_code,
            s.subject_name,
            sem.semester_number,
            sem.academic_year,
            COUNT(q.id) as question_count,
            qb.created_at
        FROM question_banks qb
        JOIN subjects s ON qb.subject_id = s.id
        JOIN semesters sem ON qb.semester_id = sem.id
        LEFT JOIN questions q ON qb.id = q.question_bank_id
        GROUP BY qb.id
        ORDER BY sem.academic_year DESC, sem.semester_number DESC, s.subject_code
    """).fetchall()
    
    conn.close()
    return list(banks)


def get_questions_by_marks_breakdown(question_bank_id):
    """Get breakdown of questions by marks in a bank"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    breakdown = cursor.execute("""
        SELECT 
            marks,
            COUNT(*) as count
        FROM questions
        WHERE question_bank_id = ? AND status = 'approved'
        GROUP BY marks
        ORDER BY marks
    """, (question_bank_id,)).fetchall()
    
    conn.close()
    return list(breakdown)


def get_question_bank_details(question_bank_id):
    """Get detailed view of a specific question bank"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get bank info
    bank = cursor.execute("""
        SELECT 
            qb.*,
            s.subject_code,
            s.subject_name,
            s.total_marks,
            sem.semester_number,
            sem.academic_year
        FROM question_banks qb
        JOIN subjects s ON qb.subject_id = s.id
        JOIN semesters sem ON qb.semester_id = sem.id
        WHERE qb.id = ?
    """, (question_bank_id,)).fetchone()
    
    # Get units with question count
    units = cursor.execute("""
        SELECT 
            u.id,
            u.unit_number,
            u.unit_name,
            COUNT(q.id) as question_count,
            SUM(CASE WHEN q.marks = 2 THEN 1 ELSE 0 END) as count_2,
            SUM(CASE WHEN q.marks = 13 THEN 1 ELSE 0 END) as count_13,
            SUM(CASE WHEN q.marks = 15 THEN 1 ELSE 0 END) as count_15
        FROM units u
        LEFT JOIN questions q ON u.id = q.unit_id AND q.status = 'approved'
        WHERE u.question_bank_id = ?
        GROUP BY u.id
        ORDER BY u.unit_number
    """, (question_bank_id,)).fetchall()
    
    # Get stats
    stats = cursor.execute("""
        SELECT 
            COUNT(*) as total_questions,
            SUM(CASE WHEN marks = 2 THEN 1 ELSE 0 END) as count_2_marks,
            SUM(CASE WHEN marks = 13 THEN 1 ELSE 0 END) as count_13_marks,
            SUM(CASE WHEN marks = 15 THEN 1 ELSE 0 END) as count_15_marks,
            SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_count,
            SUM(CASE WHEN status = 'draft' THEN 1 ELSE 0 END) as draft_count
        FROM questions
        WHERE question_bank_id = ?
    """, (question_bank_id,)).fetchone()
    
    conn.close()
    
    return {
        'bank': bank,
        'units': list(units),
        'stats': dict(stats) if stats else {}
    }


def add_subject(subject_code, subject_name, department, total_marks, created_by=1):
    """Add a new subject"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO subjects (subject_code, subject_name, department, total_marks, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (subject_code, subject_name, department, total_marks, created_by))
        
        conn.commit()
        subject_id = cursor.lastrowid
        conn.close()
        return subject_id
    except sqlite3.IntegrityError as e:
        conn.close()
        return None


def add_semester(semester_number, academic_year, is_active=1):
    """Add a new semester"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO semesters (semester_number, academic_year, is_active)
            VALUES (?, ?, ?)
        """, (semester_number, academic_year, is_active))
        
        conn.commit()
        semester_id = cursor.lastrowid
        conn.close()
        return semester_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def add_question_bank(subject_id, semester_id, created_by=1):
    """Add a new question bank"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO question_banks (subject_id, semester_id, created_by)
            VALUES (?, ?, ?)
        """, (subject_id, semester_id, created_by))
        
        conn.commit()
        bank_id = cursor.lastrowid
        conn.close()
        return bank_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def add_units_to_bank(question_bank_id, num_units=5):
    """Add default units to a question bank"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for i in range(1, num_units + 1):
        cursor.execute("""
            INSERT OR IGNORE INTO units (question_bank_id, unit_number, unit_name)
            VALUES (?, ?, ?)
        """, (question_bank_id, i, f"Unit {i}"))
    
    conn.commit()
    conn.close()


def save_paper_blueprint(subject_id, blueprint_name, total_marks, blueprint_config, created_by=1):
    """Save a paper blueprint (Part A/B/C structure)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO paper_blueprints (subject_id, blueprint_name, total_marks, blueprint_config, created_by)
        VALUES (?, ?, ?, ?, ?)
    """, (subject_id, blueprint_name, total_marks, json.dumps(blueprint_config), created_by))
    
    conn.commit()
    blueprint_id = cursor.lastrowid
    conn.close()
    return blueprint_id


def get_database_stats():
    """Get overall database statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {
        'total_users': cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        'total_subjects': cursor.execute("SELECT COUNT(*) FROM subjects").fetchone()[0],
        'total_semesters': cursor.execute("SELECT COUNT(*) FROM semesters").fetchone()[0],
        'total_question_banks': cursor.execute("SELECT COUNT(*) FROM question_banks").fetchone()[0],
        'total_questions': cursor.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
        'approved_questions': cursor.execute("SELECT COUNT(*) FROM questions WHERE status = 'approved'").fetchone()[0],
        'total_papers': cursor.execute("SELECT COUNT(*) FROM question_papers").fetchone()[0],
    }
    
    conn.close()
    return stats


if __name__ == "__main__":
    print("Database Admin Module")
    print("Use these functions to manage database:")
    print("- get_all_subjects()")
    print("- get_all_semesters()")
    print("- get_question_banks_summary()")
    print("- get_question_bank_details(bank_id)")
    print("- get_database_stats()")
