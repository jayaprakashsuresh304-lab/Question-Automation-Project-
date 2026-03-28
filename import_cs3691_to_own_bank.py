import sqlite3
from pathlib import Path

db = Path('question_bank.db')
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Ensure semester exists (Sem 5, 2025-2026)
sem = cur.execute("SELECT id FROM semesters WHERE semester_number = 5 AND academic_year = '2025-2026' LIMIT 1").fetchone()
if sem:
    sem_id = sem['id']
else:
    cur.execute("INSERT INTO semesters (semester_number, academic_year, is_active) VALUES (5, '2025-2026', 1)")
    sem_id = cur.lastrowid

# Ensure subject exists
sub = cur.execute("SELECT id FROM subjects WHERE subject_code = 'CS3691' LIMIT 1").fetchone()
if sub:
    subject_id = sub['id']
else:
    cur.execute("INSERT INTO subjects (subject_code, subject_name, department, total_marks, created_by) VALUES ('CS3691', 'EMBEDDED SYSTEM AND IOT', 'CSE', 100, 1)")
    subject_id = cur.lastrowid

# Ensure question bank exists for subject + semester
qb = cur.execute("SELECT id FROM question_banks WHERE subject_id = ? AND semester_id = ? LIMIT 1", (subject_id, sem_id)).fetchone()
if qb:
    bank_id = qb['id']
else:
    cur.execute("INSERT INTO question_banks (subject_id, semester_id, created_by) VALUES (?, ?, 1)", (subject_id, sem_id))
    bank_id = cur.lastrowid

# Ensure units 1..5 exist
for i in range(1, 6):
    ex = cur.execute("SELECT 1 FROM units WHERE question_bank_id = ? AND unit_number = ?", (bank_id, i)).fetchone()
    if not ex:
        cur.execute("INSERT INTO units (question_bank_id, unit_number, unit_name) VALUES (?, ?, ?)", (bank_id, i, f'Unit {i}'))

unit1 = cur.execute("SELECT id FROM units WHERE question_bank_id = ? AND unit_number = 1", (bank_id,)).fetchone()['id']

part_a = [
    'State the difference between RET and RET1 instruction in 8051.',
    'What is a microcontroller and give example.',
    'Differentiate ROM and RAM.',
    'How is the register bank selected in 8051 microcontrollers.',
    'What is the difference between compiler and cross compiler.',
    'Define RTOS.',
    'What are the applications of an embedded system.',
    'What is context switching.',
    'Differentiate between active sensor and passive sensors.',
    'Compare IoT devices and Computers.',
    'Sketch the TMOD register table of 8051 for timer operation.',
    'Explain bitwise operations in Embedded C language.',
    'Write an Embedded C program for the 8051 to toggle P1.0.',
    'Mention the role of scheduling in multitasking environment.',
    'What is the use of queue?'
]

priority_1 = [
    'Explain programming techniques for delay generation using timer.',
    'Write program to demonstrate stack operation in 8051 microcontrollers.',
    'Explain the concept of scheduling policies. Discuss the concept of context switching.',
    'Discuss the various states of a task in Real-Time Operating systems.',
    'Explain the features of Arduino. Discuss types of Arduino boards, sketch structure with pin structures.',
    'Illustrate in detail about timer/counter operations of 8051 microcontroller.'
]

priority_2 = [
    'Explain the architecture of the 8051 microcontrollers with suitable diagrams.',
    'Explain the instruction set and addressing modes of the 8051 microcontrollers with examples.',
    'Verify the schedulable using Rate Monotonic Scheduling (RMS) policy. Compute the schedule for an interval equal to the least-common multiple periods of the process. Compare RMS with EDF and analyse in terms of CPU utilization.',
    'Explain the importance of Memory and I/O Devices Interfacing.',
    'With a neat sketch explain the functional components of typical IoT.',
    'Program the 8051 software timer/counter for time-of-day clock. Use three ports to output Hours, Minutes and Seconds in BCD. Draw the flowchart that depicts the operation.'
]

ins = 0
skip = 0

def addq(text, marks, co, bt):
    global ins, skip
    ex = cur.execute("SELECT 1 FROM questions WHERE question_bank_id = ? AND question_text = ? LIMIT 1", (bank_id, text)).fetchone()
    if ex:
        skip += 1
        return
    cur.execute("""
        INSERT INTO questions (question_bank_id, unit_id, marks, question_text, co_mapping, bt_level, difficulty, status, choice_group, created_by)
        VALUES (?, ?, ?, ?, ?, ?, 'medium', 'approved', '', 1)
    """, (bank_id, unit1, marks, text, co, bt))
    ins += 1

for q in part_a:
    addq(q, 2, 'CO1', 'L1')
for q in priority_1:
    addq(q, 13, 'CO2', 'L3')
for q in priority_2:
    addq(q, 16, 'CO3', 'L4')

conn.commit()

tot = cur.execute("SELECT marks, COUNT(*) cnt FROM questions WHERE question_bank_id = ? GROUP BY marks ORDER BY marks", (bank_id,)).fetchall()
print('Bank ID:', bank_id)
print('Inserted:', ins, 'Skipped:', skip)
for r in tot:
    print(f"  {r['marks']} -> {r['cnt']}")

conn.close()
