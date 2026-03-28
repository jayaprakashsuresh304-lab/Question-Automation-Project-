"""
Question Bank Database Schema
Multi-subject, multi-user with semester tracking and paper history
"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "question_bank.db"


def init_database():
    """Create all tables for comprehensive question bank system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. USERS TABLE (Teachers/Admins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT DEFAULT 'teacher',
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. SEMESTERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS semesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester_number INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(semester_number, academic_year)
        )
    """)

    # 3. SUBJECTS TABLE (Courses like DM, DS, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            department TEXT,
            credits INTEGER,
            description TEXT,
            total_marks INTEGER DEFAULT 100,
            created_by INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(subject_code),
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # 4. QUESTION BANKS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            semester_id INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            total_questions INTEGER DEFAULT 0,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
            is_locked BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(subject_id, semester_id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY(semester_id) REFERENCES semesters(id) ON DELETE CASCADE,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # 5. UNITS/CHAPTERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_bank_id INTEGER NOT NULL,
            unit_number INTEGER NOT NULL,
            unit_name TEXT NOT NULL,
            description TEXT,
            question_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(question_bank_id, unit_number),
            FOREIGN KEY(question_bank_id) REFERENCES question_banks(id) ON DELETE CASCADE
        )
    """)

    # 6. QUESTIONS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_bank_id INTEGER NOT NULL,
            unit_id INTEGER,
            question_text TEXT NOT NULL,
            marks INTEGER NOT NULL,
            co_mapping TEXT,
            bt_level TEXT,
            difficulty TEXT,
            question_type TEXT DEFAULT 'essay',
            image_path TEXT,
            choice_group TEXT,
            status TEXT DEFAULT 'draft',
            created_by INTEGER NOT NULL,
            approved_by INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(question_bank_id) REFERENCES question_banks(id) ON DELETE CASCADE,
            FOREIGN KEY(unit_id) REFERENCES units(id) ON DELETE SET NULL,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY(approved_by) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # 7. PAPER BLUEPRINTS TABLE (Store your Part A/B/C rules)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_blueprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            blueprint_name TEXT NOT NULL,
            description TEXT,
            total_marks INTEGER NOT NULL,
            is_default BOOLEAN DEFAULT 0,
            blueprint_config TEXT,
            created_by INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # Example blueprint config (JSON stored as TEXT):
    # {
    #   "parts": [
    #     {"id": "A", "name": "PART A", "marks": 2, "count": 10, "total": 20, "instruction": "Answer all"},
    #     {"id": "B", "name": "PART B", "marks": 13, "count": 5, "total": 65, "instruction": "Answer all"},
    #     {"id": "C", "name": "PART C", "marks": 15, "count": 1, "hasChoice": true, "total": 15, "instruction": "Answer either (a) or (b)"}
    #   ]
    # }

    # 8. QUESTION PAPERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            semester_id INTEGER NOT NULL,
            paper_title TEXT,
            exam_type TEXT,
            exam_date TEXT,
            exam_time TEXT,
            created_by INTEGER NOT NULL,
            blueprint_id INTEGER,
            status TEXT DEFAULT 'draft',
            is_published BOOLEAN DEFAULT 0,
            total_marks INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY(semester_id) REFERENCES semesters(id) ON DELETE CASCADE,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY(blueprint_id) REFERENCES paper_blueprints(id) ON DELETE SET NULL
        )
    """)

    # 9. PAPER QUESTIONS TABLE (Link generated paper to questions)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            part TEXT,
            question_number INTEGER,
            has_choice BOOLEAN DEFAULT 0,
            choice_question_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(paper_id) REFERENCES question_papers(id) ON DELETE CASCADE,
            FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE,
            FOREIGN KEY(choice_question_id) REFERENCES questions(id) ON DELETE SET NULL
        )
    """)

    # 10. AUDIT LOG TABLE (Track all changes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            table_name TEXT,
            record_id INTEGER,
            old_value TEXT,
            new_value TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # Create indexes for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_qb_subject ON question_banks(subject_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_qb_semester ON question_banks(semester_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_q_bank ON questions(question_bank_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_q_marks ON questions(marks)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_q_status ON questions(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pq_paper ON paper_questions(paper_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pq_question ON paper_questions(question_id)")

    conn.commit()
    conn.close()

    print("✓ Database schema created successfully!")
    print("  Tables: users, semesters, subjects, question_banks, units, questions")
    print("          paper_blueprints, question_papers, paper_questions, audit_logs")


def add_sample_data():
    """Add sample data for testing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add sample user (teacher)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, full_name, email, role)
        VALUES (?, ?, ?, ?, ?)
    """, ("teacher1", "hashed_password", "Ms. Aarthie", "aarthie@college.edu", "teacher"))

    # Add sample semester
    cursor.execute("""
        INSERT OR IGNORE INTO semesters (semester_number, academic_year, is_active)
        VALUES (?, ?, ?)
    """, (5, "2025-2026", 1))

    # Add sample subject
    cursor.execute("""
        INSERT OR IGNORE INTO subjects (subject_code, subject_name, department, total_marks, created_by)
        VALUES (?, ?, ?, ?, ?)
    """, ("CCW332", "Digital Marketing", "Computer Science", 100, 1))

    # Add question bank
    cursor.execute("""
        INSERT OR IGNORE INTO question_banks (subject_id, semester_id, created_by)
        VALUES (?, ?, ?)
    """, (1, 1, 1))

    # Add units
    for i in range(1, 6):
        cursor.execute("""
            INSERT OR IGNORE INTO units (question_bank_id, unit_number, unit_name)
            VALUES (?, ?, ?)
        """, (1, i, f"Unit {i}"))

    conn.commit()
    conn.close()

    print("\n✓ Sample data added successfully!")


if __name__ == "__main__":
    # Check if old database exists
    if DB_PATH.exists():
        import os
        backup_path = DB_PATH.with_name(f"question_bank_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        os.rename(DB_PATH, backup_path)
        print(f"Old database backed up to: {backup_path}")

    init_database()
    add_sample_data()
