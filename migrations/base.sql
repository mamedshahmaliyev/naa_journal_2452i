

-- Create tables, examples of DDL

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    gender TEXT CHECK (gender IN ('male', 'female') or gender IS NULL),
    birth_date DATE,
    admission_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE (first_name, last_name, middle_name)
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    gender TEXT CHECK (gender IN ('male', 'female') or gender IS NULL),
    birth_date DATE,
    academic_rank TEXT CHECK (academic_rank IN ('lecturer', 'docent', 'professor') or academic_rank IS NULL),
    scientific_degree TEXT CHECK (scientific_degree IN ('bachelor', 'master', 'phd') or scientific_degree IS NULL),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE (first_name, last_name, middle_name)
);

CREATE TABLE IF NOT EXISTS student_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    starosta_student_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    hours INT NOT NULL,
    credits INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kafedra TEXT,
    student_group_id INTEGER,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS student_ids__student_group_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_group_id INTEGER
);

CREATE TABLE IF NOT EXISTS journal_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journal_id INTEGER,
    teacher_id INTEGER,
    subject_id INTEGER,
    student_id INTEGER,
    record_date DATE,
    hour INTEGER,
    record_type TEXT NOT NULL CHECK (record_type IN ('lecture', 'lab', 'seminar', 'kollokvium')),
    presence TEXT NOT NULL CHECK (record_type IN ('i.e', 'q.iş', 'ü.z', 'q.b')),
    mark INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
); 

    