# Question Bank Database Documentation

## Database Overview
Comprehensive multi-subject, multi-user question bank system with semester tracking and paper history.

## Tables

### 1. **USERS** - Teacher/Admin Accounts
```
id (PK)          - Unique user ID
username         - Login username (UNIQUE)
password_hash    - Encrypted password
full_name        - Teacher/Admin name
email            - Email address (UNIQUE)
role             - 'admin' or 'teacher'
is_active        - Account status (1/0)
created_at       - Account creation timestamp
updated_at       - Last update timestamp
```

### 2. **SEMESTERS** - Academic Terms
```
id (PK)          - Unique semester ID
semester_number  - Semester order (1-8)
academic_year    - Year range "2025-2026"
start_date       - Semester start date
end_date         - Semester end date
is_active        - Current status
created_at       - Record creation timestamp
```

### 3. **SUBJECTS** - Courses/Modules
```
id (PK)          - Unique subject ID
subject_code     - Code like "CCW332" (UNIQUE)
subject_name     - Full name (e.g., "Digital Marketing")
department       - Department name
credits          - Course credits
description      - Course description
total_marks      - Max marks for subject
created_by (FK)  - User who created it
is_active        - Status
created_at       - Creation timestamp
updated_at       - Last update timestamp
```

### 4. **QUESTION_BANKS** - Bank Organization
```
id (PK)          - Unique bank ID
subject_id (FK)  - Link to subject
semester_id (FK) - Link to semester
created_by (FK)  - Teacher who created it
total_questions  - Count of questions
last_updated     - Last modification
is_locked        - Prevent edits (1/0)
created_at       - Creation timestamp
updated_at       - Last update timestamp
UNIQUE(subject_id, semester_id) - One bank per subject per semester
```

### 5. **UNITS** - Chapters/Topics
```
id (PK)          - Unique unit ID
question_bank_id (FK) - Parent bank
unit_number      - Unit 1, 2, 3, etc.
unit_name        - Unit title
description      - Unit details
question_count   - Total questions in unit
created_at       - Creation timestamp
```

### 6. **QUESTIONS** - Individual Questions
```
id (PK)          - Unique question ID
question_bank_id (FK) - Parent bank
unit_id (FK)     - Parent unit
question_text    - Full question text
marks            - 2, 13, or 15
co_mapping       - CO1, CO2, etc.
bt_level         - Bloom's Taxonomy (K1-K6, L1-L6)
difficulty       - 'easy', 'medium', 'hard'
question_type    - 'essay', 'short', 'mcq'
image_path       - Path to diagram/image
choice_group     - For pairing (e.g., "C1", "B12")
status           - 'draft', 'approved', 'rejected'
created_by (FK)  - Author
approved_by (FK) - Approver
created_at       - Creation timestamp
updated_at       - Last change timestamp
```

### 7. **PAPER_BLUEPRINTS** - Question Paper Rules
```
id (PK)          - Blueprint ID
subject_id (FK)  - For subject
blueprint_name   - "Standard 100-mark pattern"
description      - Details about structure
total_marks      - 100
is_default       - Default blueprint (1/0)
blueprint_config - JSON with part structure:
                   {
                     "parts": [
                       {"id": "A", "marks": 2, "count": 10},
                       {"id": "B", "marks": 13, "count": 5},
                       {"id": "C", "marks": 15, "count": 1, "hasChoice": true}
                     ]
                   }
created_by (FK)  - Created by user
created_at       - Creation timestamp
updated_at       - Last update timestamp
```

### 8. **QUESTION_PAPERS** - Generated Papers
```
id (PK)          - Paper ID
subject_id (FK)  - Subject reference
semester_id (FK) - Semester reference
paper_title      - "Model Exam - Sem 5"
exam_type        - "Model", "University", "CIA"
exam_date        - Exam date
exam_time        - Time slot
created_by (FK)  - Paper creator
blueprint_id (FK) - Blueprint used
status           - 'draft', 'published'
is_published     - Published status
total_marks      - Sum of question marks
created_at       - Creation timestamp
updated_at       - Last update timestamp
```

### 9. **PAPER_QUESTIONS** - Paper Composition
```
id (PK)          - Link ID
paper_id (FK)    - Parent paper
question_id (FK) - Selected question
part             - 'A', 'B', 'C'
question_number  - Display order (1, 2, 3...)
has_choice       - Has OR option (1/0)
choice_question_id (FK) - Other choice option
created_at       - When added to paper
```

### 10. **AUDIT_LOGS** - Change History
```
id (PK)          - Log ID
user_id (FK)     - Who made change
action           - 'INSERT', 'UPDATE', 'DELETE'
table_name       - Affected table
record_id        - Affected record
old_value        - Before change
new_value        - After change
timestamp        - When changed
```

## Relationships

```
1 USER → N SUBJECT (teacher creates multiple subjects)
1 USER → N QUESTION_BANK
1 USER → N QUESTION_PAPER
1 USER → N QUESTION

1 SUBJECT → N QUESTION_BANK (one bank per semester per subject)
1 SEMESTER → N QUESTION_BANK

1 QUESTION_BANK → N UNIT
1 QUESTION_BANK → N QUESTION
1 QUESTION_BANK → N PAPER_BLUEPRINT

1 UNIT → N QUESTION

1 SUBJECT → N PAPER_BLUEPRINT
1 SUBJECT → N QUESTION_PAPER

1 PAPER_BLUEPRINT → N QUESTION_PAPER

1 QUESTION_PAPER → N PAPER_QUESTIONS
1 QUESTION → N PAPER_QUESTIONS (one question can be used in many papers)
```

## Sample Queries

### Get all subjects created by a teacher:
```sql
SELECT * FROM subjects WHERE created_by = 1;
```

### Get all questions for a specific semester and subject:
```sql
SELECT q.* 
FROM questions q
JOIN question_banks qb ON q.question_bank_id = qb.id
WHERE qb.subject_id = 1 AND qb.semester_id = 1
ORDER BY q.marks, q.unit_id;
```

### Get questions by marks (for paper generation):
```sql
SELECT q.* 
FROM questions q
WHERE q.question_bank_id = 1 AND q.marks = 2 AND q.status = 'approved'
ORDER BY q.unit_id;
```

### Get all papers generated for a subject:
```sql
SELECT qp.*, s.subject_name 
FROM question_papers qp
JOIN subjects s ON qp.subject_id = s.id
WHERE qp.subject_id = 1
ORDER BY qp.created_at DESC;
```

### Get questions used in a specific paper:
```sql
SELECT pq.*, q.question_text, q.marks, q.co_mapping, q.bt_level
FROM paper_questions pq
JOIN questions q ON pq.question_id = q.id
WHERE pq.paper_id = 5
ORDER BY pq.part, pq.question_number;
```

## Indexes
- `idx_qb_subject` - Quick lookup of banks by subject
- `idx_qb_semester` - Quick lookup of banks by semester
- `idx_q_bank` - Quick lookup of questions by bank
- `idx_q_marks` - Quick filter questions by marks
- `idx_q_status` - Quick filter approved questions
- `idx_pq_paper` - Quick lookup paper composition
- `idx_pq_question` - Quick lookup where question is used

## Backup Strategy
- Old database auto-backed up when schema is updated
- Backup filename: `question_bank_backup_YYYYMMDD_HHMMSS.db`
- Store backups in separate directory

## Future Enhancements
- Add users table with authentication
- Add role-based access control (RBAC)
- Add question bulk import from Excel
- Add paper PDF generation and storage
- Add question difficulty tracking (adjust based on student performance)
- Add question reuse analytics
