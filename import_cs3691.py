import sqlite3
from pathlib import Path

db = Path('question_bank.db')
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

bank = cur.execute('SELECT id FROM question_banks ORDER BY id LIMIT 1').fetchone()
if not bank:
    raise SystemExit('No question bank found. Run database_schema.py first.')
bank_id = bank['id']

unit = cur.execute('SELECT id FROM units WHERE question_bank_id = ? AND unit_number = 1', (bank_id,)).fetchone()
if not unit:
    unit = cur.execute('SELECT id FROM units WHERE question_bank_id = ? ORDER BY unit_number LIMIT 1', (bank_id,)).fetchone()
if not unit:
    raise SystemExit('No units found for active question bank.')
unit_id = unit['id']

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
    'Verify schedulability using Rate Monotonic Scheduling (RMS) policy. Compute schedule for an interval equal to the least-common multiple periods. Compare RMS with EDF in terms of CPU utilization for T1(C=3,T=20), T2(C=2,T=5), T3(C=2,T=10).',
    'Explain the importance of Memory and I/O Devices Interfacing.',
    'With a neat sketch explain the functional components of typical IoT.',
    'Program the 8051 software timer/counter for time-of-day clock. Use three ports to output Hours, Minutes and Seconds in BCD. Draw the flowchart depicting operation.'
]

inserted = 0
skipped = 0


def add_question(text, marks, co, bt):
    global inserted, skipped
    exists = cur.execute(
        'SELECT 1 FROM questions WHERE question_bank_id = ? AND question_text = ? LIMIT 1',
        (bank_id, text)
    ).fetchone()
    if exists:
        skipped += 1
        return
    cur.execute('''
        INSERT INTO questions (question_bank_id, unit_id, marks, question_text, co_mapping, bt_level, difficulty, status, choice_group, created_by)
        VALUES (?, ?, ?, ?, ?, ?, 'medium', 'approved', '', 1)
    ''', (bank_id, unit_id, marks, text, co, bt))
    inserted += 1

for q in part_a:
    add_question(q, 2, 'CO1', 'L1')
for q in priority_1:
    add_question(q, 13, 'CO2', 'L3')
for q in priority_2:
    add_question(q, 16, 'CO3', 'L4')

conn.commit()

totals = cur.execute('''
    SELECT marks, COUNT(*) as cnt FROM questions
    WHERE question_bank_id = ?
    GROUP BY marks ORDER BY marks
''', (bank_id,)).fetchall()

print(f'Inserted: {inserted}, Skipped duplicates: {skipped}')
print('Counts by marks:')
for row in totals:
    print(f"  {row['marks']} -> {row['cnt']}")

conn.close()
