graph TD
    Users["👤 USERS<br/>(id, username, role, email)"]
    Semesters["📅 SEMESTERS<br/>(id, semester#, academic_year)"]
    Subjects["📚 SUBJECTS<br/>(id, code, name, total_marks)"]
    QuestionBanks["🏦 QUESTION_BANKS<br/>(id, subject_id, semester_id)"]
    Units["📖 UNITS<br/>(id, unit_name, unit_number)"]
    Questions["❓ QUESTIONS<br/>(id, text, marks, CO, BT_level)"]
    PaperBlueprints["📋 PAPER_BLUEPRINTS<br/>(id, subject_id, rules/config)"]
    Papers["📄 QUESTION_PAPERS<br/>(id, subject_id, semester_id)"]
    PaperQuestions["🔗 PAPER_QUESTIONS<br/>(paper_id, question_id, part)"]
    AuditLogs["📝 AUDIT_LOGS<br/>(action, user_id, timestamp)"]

    Users -->|creates| Subjects
    Users -->|creates| QuestionBanks
    Users -->|creates| Papers
    Users -->|logs in| AuditLogs
    
    Subjects -->|has bank for| QuestionBanks
    Semesters -->|has bank for| QuestionBanks
    
    QuestionBanks -->|contains| Units
    QuestionBanks -->|contains| Questions
    QuestionBanks -->|defines| PaperBlueprints
    
    Units -->|group| Questions
    
    Subjects -->|used in| Papers
    Semesters -->|used in| Papers
    PaperBlueprints -->|applied to| Papers
    
    Papers -->|contains| PaperQuestions
    Questions -->|selected in| PaperQuestions

style Users fill:#e1f5ff
style Semesters fill:#f3e5f5
style Subjects fill:#fff3e0
style QuestionBanks fill:#e8f5e9
style Units fill:#fce4ec
style Questions fill:#f1f8e9
style PaperBlueprints fill:#ede7f6
style Papers fill:#fff9c4
style PaperQuestions fill:#e0f2f1
style AuditLogs fill:#f5f5f5
