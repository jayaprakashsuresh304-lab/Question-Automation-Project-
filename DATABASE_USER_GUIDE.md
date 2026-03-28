# Question Bank Database - User Guide

## Quick Start

### 1. Database Files
```
question_bank.db              - Main production database
question_bank_backup_*.db     - Automatic backups (created before schema updates)
database_schema.py            - Schema definition and initialization
db_admin.py                   - Admin utilities and helper functions
```

### 2. Initialize or Reset Database
```bash
python database_schema.py
```
This will:
- Create all tables if they don't exist
- Backup old database (if exists)
- Add sample data (1 teacher, 1 subject "Digital Marketing", 1 semester, 1 question bank with 5 units)

---

## Database Structure Overview

### User Hierarchy
```
👤 USERS (Teachers/Admins)
  ├── 📚 Creates SUBJECTS (Courses)
  │   ├── 🏦 Each Subject has QUESTION_BANKS (one per semester)
  │   │   ├── ❓ Contains QUESTIONS
  │   │   ├── 📖 Organized in UNITS
  │   │   └── 📋 Defines PAPER_BLUEPRINTS (Part A/B/C structure)
  │   └── 📄 Generates QUESTION_PAPERS
  │       └── 🔗 Links to selected QUESTIONS
  └── 📝 All actions logged in AUDIT_LOGS
```

---

## Common Use Cases & SQL Queries

### Case 1: Add a New Subject
```sql
INSERT INTO subjects (subject_code, subject_name, department, credits, total_marks, created_by)
VALUES ('CCW334', 'Data Science', 'Computer Science', 3, 100, 1);
```

### Case 2: Create Question Bank for Subject in Semester 5
```sql
-- First, find subject_id and semester_id
INSERT INTO question_banks (subject_id, semester_id, created_by)
SELECT s.id, sem.id, 1
FROM subjects s, semesters sem
WHERE s.subject_code = 'CCW332' AND sem.semester_number = 5 AND sem.academic_year = '2025-2026';

-- Then add units to the bank (assuming bank_id = 1)
INSERT INTO units (question_bank_id, unit_number, unit_name)
VALUES (1, 1, 'Digital Marketing Fundamentals');
-- ... repeat for units 2-5
```

### Case 3: Add Question to Bank
```sql
INSERT INTO questions 
(question_bank_id, unit_id, question_text, marks, co_mapping, bt_level, difficulty, status, created_by)
VALUES (
  1,  -- question_bank_id
  1,  -- unit_id
  'Define digital marketing strategy with example.',
  2,  -- marks
  'CO1',
  'K2',
  'easy',
  'draft',
  1   -- created_by (teacher_id)
);
```

### Case 4: Approve Question
```sql
UPDATE questions 
SET status = 'approved', approved_by = 1 
WHERE id = 123;
```

### Case 5: Get All Approved 2-Mark Questions from Bank
```sql
SELECT 
  q.id,
  u.unit_number,
  q.question_text,
  q.co_mapping,
  q.bt_level,
  q.difficulty
FROM questions q
JOIN units u ON q.unit_id = u.id
WHERE q.question_bank_id = 1 AND q.marks = 2 AND q.status = 'approved'
ORDER BY u.unit_number, q.id;
```

### Case 6: Get Question Count by Marks in a Bank
```sql
SELECT marks, COUNT(*) as count
FROM questions
WHERE question_bank_id = 1 AND status = 'approved'
GROUP BY marks
ORDER BY marks;
```
**Expected Output** (for balanced bank):
```
marks | count
------|-------
2     | 15   (10 needed for 20 marks Part A)
13    | 8    (5 needed for 65 marks Part B)
15    | 4    (2 needed for 15 marks Part C)
```

### Case 7: Check If Bank Has Enough Questions
```sql
SELECT 
  SUM(CASE WHEN marks = 2 THEN 1 ELSE 0 END) as count_2,
  SUM(CASE WHEN marks = 13 THEN 1 ELSE 0 END) as count_13,
  SUM(CASE WHEN marks = 15 THEN 1 ELSE 0 END) as count_15
FROM questions
WHERE question_bank_id = 1 AND status = 'approved';
```

### Case 8: View All Question Banks with Statistics
```sql
SELECT 
  s.subject_code,
  s.subject_name,
  sem.semester_number,
  sem.academic_year,
  COUNT(q.id) as total_questions,
  SUM(CASE WHEN q.marks = 2 THEN 1 ELSE 0 END) as mark_2_count,
  SUM(CASE WHEN q.marks = 13 THEN 1 ELSE 0 END) as mark_13_count,
  SUM(CASE WHEN q.marks = 15 THEN 1 ELSE 0 END) as mark_15_count
FROM question_banks qb
JOIN subjects s ON qb.subject_id = s.id
JOIN semesters sem ON qb.semester_id = sem.id
LEFT JOIN questions q ON qb.id = q.question_bank_id AND q.status = 'approved'
GROUP BY qb.id
ORDER BY sem.academic_year DESC, sem.semester_number DESC;
```

### Case 9: Save Paper Blueprint (Part A/B/C Structure)
```sql
INSERT INTO paper_blueprints 
(subject_id, blueprint_name, total_marks, blueprint_config, created_by, is_default)
VALUES (
  1,
  'Standard 100-Mark Pattern',
  100,
  '{
    "parts": [
      {"id": "A", "name": "PART A", "marks": 2, "count": 10, "total": 20, "instruction": "Answer all"},
      {"id": "B", "name": "PART B", "marks": 13, "count": 5, "total": 65, "instruction": "Answer all"},
      {"id": "C", "name": "PART C", "marks": 15, "count": 1, "total": 15, "hasChoice": true, "instruction": "Answer either (a) or (b)"}
    ]
  }',
  1,
  1
);
```

### Case 10: Create a Question Paper (Save Generated Paper)
```sql
INSERT INTO question_papers (subject_id, semester_id, paper_title, exam_type, exam_date, exam_time, created_by, blueprint_id, total_marks)
VALUES (1, 1, 'Model Exam - CCW332', 'Model Examination', '2026-04-15', '1:30 PM - 4:30 PM', 1, 1, 100);
```

### Case 11: Add Questions to Paper (Link them)
```sql
-- For Part A (2-mark questions, numbers 1-10)
INSERT INTO paper_questions (paper_id, question_id, part, question_number)
VALUES (1, 145, 'A', 1);  -- paper_id=1, question_id=145, part='A', number=1

-- For Part C (with choice option)
INSERT INTO paper_questions (paper_id, question_id, part, question_number, has_choice, choice_question_id)
VALUES (1, 234, 'C', 16, 1, 235);  -- question 234 is (a), 235 is (b)
```

### Case 12: Retrieve a Generated Paper
```sql
SELECT 
  pq.question_number,
  pq.part,
  q.question_text,
  q.marks,
  q.co_mapping,
  q.bt_level,
  CASE WHEN pq.has_choice = 1 THEN 'OR' ELSE '' END as separator,
  q2.question_text as choice_b_text
FROM paper_questions pq
JOIN questions q ON pq.question_id = q.id
LEFT JOIN questions q2 ON pq.choice_question_id = q2.id
WHERE pq.paper_id = 1
ORDER BY pq.part, pq.question_number;
```

### Case 13: Get Audit History (Track Changes)
```sql
SELECT 
  u.full_name,
  al.action,
  al.table_name,
  al.record_id,
  al.timestamp
FROM audit_logs al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.table_name = 'questions'
ORDER BY al.timestamp DESC
LIMIT 50;
```

---

## Database Admin Functions (Python)

###Using db_admin.py:
```python
from db_admin import *

# Get summary of all question banks
banks = get_question_banks_summary()
for bank in banks:
    print(f"{bank['subject_code']} Sem {bank['semester_number']}: {bank['question_count']} questions")

# Get detailed info about specific bank
details = get_question_bank_details(1)
print(f"Subject: {details['bank']['subject_name']}")
print(f"Total approved questions: {details['stats']['total_questions']}")
print(f"Units: {len(details['units'])}")

# Get database statistics
stats = get_database_stats()
print(f"Total subjects: {stats['total_subjects']}")
print(f"Total approved questions: {stats['approved_questions']}")
print(f"Total papers generated: {stats['total_papers']}")
```

---

## Backup & Recovery

### Automatic Backups
- When you run `python database_schema.py`, old database is backed up with timestamp
- Backup format: `question_bank_backup_YYYYMMDD_HHMMSS.db`

### Manual Backup
```bash
# Windows
copy question_bank.db question_bank_backup_manual.db

# Linux/Mac
cp question_bank.db question_bank_backup_manual.db
```

### Restore from Backup
```bash
# Windows
copy question_bank_backup_20260323_142059.db question_bank.db

# Linux/Mac
cp question_bank_backup_20260323_142059.db question_bank.db
```

---

## Performance Tips

1. **Use marks filter when querying questions**
   ```sql
   -- ✓ Good: Uses index
   SELECT * FROM questions WHERE question_bank_id = 1 AND marks = 2;
   
   -- ✗ Slow: No index on question_text
   SELECT * FROM questions WHERE question_text LIKE '%digital%';
   ```

2. **Bulk insert questions efficiently**
   ```python
   conn = sqlite3.connect('question_bank.db')
   cursor = conn.cursor()
   
   questions = [(data1), (data2), ...]  # List of tuples
   
   cursor.executemany("""
       INSERT INTO questions (...)
       VALUES (?, ?, ...)
   """, questions)
   
   conn.commit()
   conn.close()
   ```

3. **Lock question bank after questions are finalized**
   ```sql
   UPDATE question_banks SET is_locked = 1 WHERE id = 1;
   ```

---

## Tools & Client Software

### SQLite Browser
- **Download**: https://sqlitebrowser.org/
- Use to visually browse, query, and edit database

### Command Line
```bash
sqlite3 question_bank.db
> .tables
> SELECT COUNT(*) FROM questions;
> .quit
```

### Python Script
```python
import sqlite3

conn = sqlite3.connect('question_bank.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM subjects")
for row in cursor.fetchall():
    print(dict(row))

conn.close()
```

---

## Constraints & Validation

| Constraint | Impact |
|-----------|--------|
| subject.subject_code (UNIQUE) | Can't have two subjects with same code |
| semester.academic_year + semester_number (UNIQUE) | One Sem 5 per year |
| question_bank subject_id + semester_id (UNIQUE) | One bank per subject per semester |
| question.marks ∈ {2, 13, 15} | Only these mark values allowed (enforce in app) |
| question.status ∈ {draft, approved, rejected} | Standardized statuses |

---

## Future Enhancements

- [ ] User authentication & login
- [ ] Role-based permissions (who can create/edit/approve)
- [ ] Question bulk import from Excel
- [ ] Paper PDF generation & storage
- [ ] Question difficulty adjustment based on analytics
- [ ] Question reuse statistics
- [ ] CO/BT coverage analysis
- [ ] Paper analytics (which questions chosen most, which avoided)
