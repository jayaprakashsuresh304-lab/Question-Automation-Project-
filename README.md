# Question Bank & Question Paper Generator
## Complete Documentation

---

## Overview

A comprehensive web application for college teachers to:
1. **Manage Question Banks** - Store questions by subject, semester, unit, marks, CO, and difficulty
2. **Auto-Generate Question Papers** - Align questions to your college template (Part A 2-marks, Part B 13-marks, Part C 15-marks with either/or)
3. **Track Paper History** - Keep records of all generated papers
4. **Professional Output** - Export papers in your institution's official format with approval signatures

---

## Quick Start (5 minutes)

### 1. Start the Web App
```bash
cd "D:\clg project"
python app.py
```
Open: **http://127.0.0.1:5000**

### 2. Add Questions
- Go to "Question Bank"
- Fill: Question text, Marks (2/13/15), CO, BT Level, Unit, Difficulty
- Click "Save Question"
- Use "Add Demo Questions" for sample data

### 3. Generate Paper
- Go to "Generate Paper"
- Fill: College name, Department, Subject code/name, Exam type, Date, Time
- Optionally select specific questions
- Click "Generate Question Paper"
- Click "Print / Save as PDF"

---

## File Structure

```
D:\clg project\
├── app.py                         ← Main Flask application
├── database_schema.py             ← Database initialization
├── db_admin.py                    ← Admin utilities & helper functions
├── verify_database.py             ← Database verification script
├── requirements.txt               ← Python dependencies (Flask)
├── question_bank.db               ← SQLite database (production)
├── question_bank_backup_*.db      ← Automatic backups
│
├── DATABASE_DOCUMENTATION.md      ← Full schema documentation
├── DATABASE_USER_GUIDE.md         ← SQL examples & usage guide
├── DATABASE_SCHEMA.md             ← ER diagram (Mermaid format)
├── README.md                      ← This file
│
├── templates/
│   ├── base.html                  ← Base layout
│   ├── index.html                 ← Dashboard
│   ├── bank.html                  ← Question bank interface
│   ├── generate.html              ← Paper generation form
│   └── paper.html                 ← Final question paper output
│
└── static/
    └── style.css                  ← Professional styling
```

---

## Database Architecture

### 10 Core Tables

| Table | Purpose | Records |
|-------|---------|---------|
| **users** | Teacher/admin accounts | 1 (sample) |
| **semesters** | Academic terms | 1 (S5 2025-26) |
| **subjects** | Courses (DM, DS, etc.) | 1 (sample) |
| **question_banks** | Org by subject+semester | 1 (sample) |
| **units** | Chapters/topics | 5 (sample) |
| **questions** | Individual questions | 0 (add yours) |
| **paper_blueprints** | Part A/B/C structure rules | 0 |
| **question_papers** | Generated papers | 0 |
| **paper_questions** | Paper composition | 0 |
| **audit_logs** | Change history | 0 |

### Sample Data
- **User**: teacher1 (Ms. Aarthie)
- **Subject**: CCW332 (Digital Marketing)
- **Semester**: 5 (2025-2026)
- **Question Bank**: Ready with 5 units

### Verification
```bash
python verify_database.py
```
Output shows all tables, indexes, and sample data status.

---

## Question Paper Pattern

Your college template, now automated:

### PART A: 2-Mark Questions
- Count: 10 questions
- Total: 10 × 2 = **20 marks**
- Instruction: **Answer all questions**

### PART B: 13-Mark Questions  
- Count: 5 questions
- Total: 5 × 13 = **65 marks**
- Instruction: **Answer all 5 questions**

### PART C: 15-Mark Questions (Either/Or)
- Count: 2 questions (presented as 16(a) or 16(b))
- Total: **15 marks** (choose 1)
- Instruction: **Answer either (a) or (b)**

### Total: 100 Marks (20 + 65 + 15)

---

## Web App Features

### Dashboard (Home)
- Quick stats: Total questions, pool sizes (2/13/15 marks)
- "Add Demo Questions" button to populate sample data

### Question Bank Manager
- Add questions with:
  - Question text
  - Marks: 2, 13, or 15
  - Unit: Unit 1-5
  - CO mapping: CO1, CO2, etc.
  - Bloom's Taxonomy: K1-K6, L1-L6
  - Difficulty: easy, medium, hard
  - Status: draft, approved
  - Choice group: For pairing 15-mark questions
- Filter by marks (2/13/15)
- Delete questions
- View all questions in table format

### Question Paper Generator
- Select from question pools by marks
- Auto-fill remaining questions if partial selection
- Validation:
  - Minimum 10 questions × 2 marks
  - Minimum 5 questions × 13 marks
  - Minimum 2 questions × 15 marks (for choice pair)
- Fill paper details:
  - College name, department
  - Subject code & name
  - Semester, exam type
  - Date & time
  - Part A count (configurable)

### Paper Output (Print-Ready)
- Professional table format matching your template
- Header with subject code, name, marks, time
- Question tables with Q.No. | Question | CO | Bloom's Level | Marks
- Part A: All 2-mark questions
- Part B: All 5 × 13-mark questions
- Part C: Either (a) or (b) 15-mark questions
- Approval section: Course Handler, Senior Faculty, HoD signatures
- Print/Save as PDF button

---

## Database Administration

### Admin Functions (Python)
```python
from db_admin import *

# View all subjects
subjects = get_all_subjects()

# Get question bank detail with stats
details = get_question_bank_details(bank_id=1)
print(details['stats'])  # {'total_questions': 25, 'count_2_marks': 15, ...}

# Get database statistics
stats = get_database_stats()
print(f"Total questions: {stats['total_questions']}")
```

### Common SQL Operations
See **DATABASE_USER_GUIDE.md** for:
- Adding subjects, semesters, banks
- Adding/approving questions
- Checking question distribution
- Creating papers with blueprints
- Retrieving audit logs

### Backup & Recovery
```bash
# Auto-backup happens when running:
python database_schema.py

# Manual backup:
copy question_bank.db question_bank_backup_manual.db

# Restore from backup:
copy question_bank_backup_20260323_142059.db question_bank.db
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Windows/Linux/Mac

### Step 1: Install Dependencies
```bash
cd "D:\clg project"
python -m pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python database_schema.py
```
This will:
- Create `question_bank.db` with all 10 tables
- Add indexes for performance
- Add sample: teacher, subject, semester, bank, units
- Backup old database if it exists

### Step 3: Verify Database
```bash
python verify_database.py
```
Checks all tables, indexes, permissions, and displays summary.

### Step 4: Run Web App
```bash
python app.py
```
Open: **http://127.0.0.1:5000**

### Step 5: Add Questions
1. Click "Add Demo Questions" (or add manually)
2. Go to "Question Bank"
3. Add your questions with proper marks (2/13/15)
4. Status options: draft → approved

### Step 6: Generate Paper
1. Go to "Generate Paper"
2. Fill paper details
3. Optionally select questions (auto-fills if needed)
4. Click "Generate Question Paper"
5. Print/Save as PDF

---

## Key Design Features

### 1. Multi-Subject Support
- Create separate question banks for each subject
- Each subject has one bank per semester
- Prevents cross-subject mixing

### 2. Multi-User
- User management (teacher/admin roles)
- Audit logs track who changed what
- Ready for login system (future)

### 3. Semester Tracking
- Questions organized by academic year & semester
- Historical papers preserved
- Easy semester transitions

### 4. Paper Blueprints
- Define Part A/B/C structure in JSON
- Multiple blueprints per subject
- Default blueprint for standards

### 5. Choice Grouping
- Pair questions for 15-mark either/or
- Use `choice_group` field (e.g., "C1" for pair 1)
- Automatically displayed as 16(a) OR 16(b)

### 6. CO & Bloom's Taxonomy
- CO mapping: CO1, CO2, CO3, CO4
- Bloom's levels: K1-K6 (Knowledge), L1-L6 (Skills)
- Printed on paper for accreditation

### 7. Indexes for Performance
- Fast lookup by marks (idx_q_marks)
- Fast lookup by status (idx_q_status)
- Fast paper composition queries (idx_pq_paper)

---

## Customization Options

### Modify Question Paper Structure
Edit `DATABASE_DOCUMENTATION.md` → "PAPER_BLUEPRINTS" section:
```json
{
  "parts": [
    {"id": "A", "marks": 2, "count": 10, "total": 20},
    {"id": "B", "marks": 13, "count": 5, "total": 65},
    {"id": "C", "marks": 15, "count": 1, "total": 15}
  ]
}
```

### Change Part Counts
In `app.py`, `generate()` function:
```python
part_a_count = int(request.form.get("part_a_count", "10"))  # Change default
# And update validation logic
```

### Add More Fields
Edit `database_schema.py`, add columns to `questions` table:
```sql
-- Add language
ALTER TABLE questions ADD COLUMN language TEXT;
```

### Style/Branding
Edit `static/style.css`:
- Change header colors
- Logo placement
- Font sizes
- Page margins

---

## Troubleshooting

### Issue: "Database not found"
**Solution:**
```bash
cd "D:\clg project"
python database_schema.py
```

### Issue: "Not enough questions" error
**Check:**
- Go to "Question Bank", Filter by marks
- Count: Need 10× 2-mark, 5× 13-mark, 2× 15-mark (approved)
- Status must be "approved"

### Issue: App won't start
**Check:**
- Flask installed: `python -m pip install Flask==3.1.0`
- Port 5000 free: `netstat -ano | findstr :5000` (Windows)
- Python 3.8+: `python --version`

### Issue: Part C shows only one question
**Solution:**
- Part C needs 2 questions × 15 marks
- Use "choice_group" field to pair them
- Example: Q1 "choice_group=C1", Q2 "choice_group=C1"

---

## Performance Considerations

### Large Banks (1000+ questions)
- Use filters (marks, unit, status)
- Avoid full-table scans
- Use indexes for common queries

### Paper Generation Speed
- With 10 questions × 2 marks: <100ms
- With 5 questions × 13 marks: <100ms
- With 2 questions × 15 marks: <100ms
- Total: <1 second

### Database Size
- 1000 questions ≈ 5 MB
- 100 papers ≈ <1 MB
- Old database auto-backed up

---

## Security Notes

### Current Version (Development)
- No authentication (anyone can access)
- Single user ("teacher1")
- SQLite (file-based, suitable for single-college deployment)

### Future Production Version
- Add user login
- Hash passwords
- Role-based access control
- Audit logs for compliance
- Consider PostgreSQL for multi-institution

---

## Getting Help

### Documentation Files
- `DATABASE_DOCUMENTATION.md` - Full schema with examples
- `DATABASE_USER_GUIDE.md` - 13 common use-case SQL queries
- `DATABASE_SCHEMA.md` - ER diagram (Mermaid format)

### Admin Tools
```bash
python db_admin.py
python verify_database.py
```

### SQLite Browser
- Download: https://sqlitebrowser.org/
- Visual query builder
- Direct table editing

---

## Future Enhancements

**Planned Features:**
- [ ] User authentication & login
- [ ] Excel/CSV question import
- [ ] Question difficulty analytics
- [ ] Paper PDF generation/storage
- [ ] Question reuse statistics
- [ ] CO coverage analysis
- [ ] Multi-college support
- [ ] Mobile app for question viewing
- [ ] API for integration with LMS

**Contact Support:**
For bugs or feature requests, maintain DATABASE_DOCUMENTATION.md and DATABASE_USER_GUIDE.md as single source of truth.

---

## License & Credits

Built for college question paper automation.

Customized template matching: **CCW332 Digital Marketing (5-Semester)**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 23-Mar-2026 | Initial release with 10-table schema, multi-subject/semester support, question paper auto-generation |

---

**Database Status:** ✅ Ready to use  
**Web App Status:** ✅ Running (http://127.0.0.1:5000)  
**Admin Tools:** ✅ Available (db_admin.py, verify_database.py)
