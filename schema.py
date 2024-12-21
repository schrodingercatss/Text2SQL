# 定义数据库描述
STUDENT_DB_SCHEMA = """
SQL: -- 学生信息表
students: 
    student_id (INT, PK), 
    name (VARCHAR), 
    gender (ENUM), 
    date_of_birth (DATE), 
    age (INT), 
    address (VARCHAR), 
    phone_number (VARCHAR)

-- 课程信息表
courses: 
    course_id (INT, PK), 
    course_name (VARCHAR), 
    course_description (TEXT), 
    credits (INT)

-- 成绩记录表
grades: 
    grade_id (INT, PK), 
    student_id (INT, FK -> students.student_id), 
    course_id (INT, FK -> courses.course_id), 
    grade (FLOAT), 
    semester (VARCHAR)

-- 教师信息表
teachers: 
    teacher_id (INT, PK), 
    name (VARCHAR), 
    gender (ENUM), 
    phone_number (VARCHAR), 
    email (VARCHAR), 
    department (VARCHAR)

-- 教师与课程关联表
teacher_courses: 
    teacher_course_id (INT, PK), 
    teacher_id (INT, FK -> teachers.teacher_id), 
    course_id (INT, FK -> courses.course_id)
"""

BOOK_DB_SCHEMA = """
SQL: -- 用户信息表
users: 
    user_id (INT, PK), 
    name (VARCHAR), 
    gender (ENUM), 
    date_of_birth (DATE), 
    address (VARCHAR), 
    phone_number (VARCHAR), 
    email (VARCHAR), 
    join_date (DATE)

-- 图书信息表
books: 
    book_id (INT, PK), 
    title (VARCHAR), 
    author (VARCHAR), 
    genre (VARCHAR), 
    publication_year (YEAR), 
    publisher (VARCHAR), 
    isbn (VARCHAR), 
    total_copies (INT), 
    available_copies (INT)

-- 借阅记录表
borrow_records: 
    borrow_id (INT, PK), 
    user_id (INT, FK -> users.user_id), 
    book_id (INT, FK -> books.book_id), 
    borrow_date (DATE), 
    return_date (DATE), 
    status (ENUM)

-- 管理员信息表
librarians: 
    librarian_id (INT, PK), 
    name (VARCHAR), 
    phone_number (VARCHAR), 
    email (VARCHAR), 
    hire_date (DATE)

-- 图书库存操作记录表
inventory_logs: 
    log_id (INT, PK), 
    book_id (INT, FK -> books.book_id), 
    librarian_id (INT, FK -> librarians.librarian_id), 
    operation (ENUM), 
    operation_date (TIMESTAMP), 
    notes (TEXT)
"""

# 固定内容
FIXED_PROMPT = """
你是一个智能数据库助手，可以根据人类的自然语言以及数据库的建库数据完成下列任务。请以JSON格式返回。
"""