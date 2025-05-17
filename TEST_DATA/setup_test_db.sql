-- Create test database if it doesn't exist
CREATE DATABASE IF NOT EXISTS btes_test_db;

-- Use the test database
USE btes_test_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create courses table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    instructor_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES users(id)
);

-- Create enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    grade DECIMAL(5,2) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE KEY unique_enrollment (user_id, course_id)
);

-- Create assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    due_date DATETIME NOT NULL,
    max_score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Create assignment_submissions table
CREATE TABLE IF NOT EXISTS assignment_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    user_id INT NOT NULL,
    submission_text TEXT,
    file_path VARCHAR(255),
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2) DEFAULT NULL,
    feedback TEXT,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_submission (assignment_id, user_id)
);

-- Create stored procedure for enrolling a user in a course
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS enroll_user_in_course(
    IN p_user_id INT,
    IN p_course_id INT
)
BEGIN
    DECLARE user_exists INT;
    DECLARE course_exists INT;
    DECLARE already_enrolled INT;
    
    -- Check if user exists
    SELECT COUNT(*) INTO user_exists FROM users WHERE id = p_user_id;
    
    -- Check if course exists
    SELECT COUNT(*) INTO course_exists FROM courses WHERE id = p_course_id;
    
    -- Check if already enrolled
    SELECT COUNT(*) INTO already_enrolled FROM enrollments 
    WHERE user_id = p_user_id AND course_id = p_course_id;
    
    -- Validate and insert
    IF user_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User does not exist';
    ELSEIF course_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course does not exist';
    ELSEIF already_enrolled > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User already enrolled in this course';
    ELSE
        INSERT INTO enrollments (user_id, course_id) VALUES (p_user_id, p_course_id);
    END IF;
END //
DELIMITER ;

-- Create stored procedure for submitting an assignment
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS submit_assignment(
    IN p_assignment_id INT,
    IN p_user_id INT,
    IN p_submission_text TEXT,
    IN p_file_path VARCHAR(255)
)
BEGIN
    DECLARE assignment_exists INT;
    DECLARE user_enrolled INT;
    DECLARE already_submitted INT;
    
    -- Check if assignment exists
    SELECT COUNT(*) INTO assignment_exists FROM assignments WHERE id = p_assignment_id;
    
    -- Check if user is enrolled in the course
    SELECT COUNT(*) INTO user_enrolled FROM enrollments e
    JOIN assignments a ON e.course_id = a.course_id
    WHERE a.id = p_assignment_id AND e.user_id = p_user_id;
    
    -- Check if already submitted
    SELECT COUNT(*) INTO already_submitted FROM assignment_submissions
    WHERE assignment_id = p_assignment_id AND user_id = p_user_id;
    
    -- Validate and insert
    IF assignment_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Assignment does not exist';
    ELSEIF user_enrolled = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User not enrolled in the course';
    ELSEIF already_submitted > 0 THEN
        -- Update existing submission
        UPDATE assignment_submissions
        SET submission_text = p_submission_text,
            file_path = p_file_path,
            submission_date = CURRENT_TIMESTAMP
        WHERE assignment_id = p_assignment_id AND user_id = p_user_id;
    ELSE
        -- Create new submission
        INSERT INTO assignment_submissions (assignment_id, user_id, submission_text, file_path)
        VALUES (p_assignment_id, p_user_id, p_submission_text, p_file_path);
    END IF;
END //
DELIMITER ;

-- Create stored procedure for grading an assignment
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS grade_assignment(
    IN p_submission_id INT,
    IN p_score DECIMAL(5,2),
    IN p_feedback TEXT
)
BEGIN
    DECLARE submission_exists INT;
    DECLARE max_score INT;
    
    -- Check if submission exists
    SELECT COUNT(*) INTO submission_exists FROM assignment_submissions WHERE id = p_submission_id;
    
    -- Get max score for the assignment
    SELECT a.max_score INTO max_score
    FROM assignment_submissions s
    JOIN assignments a ON s.assignment_id = a.id
    WHERE s.id = p_submission_id;
    
    -- Validate and update
    IF submission_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Submission does not exist';
    ELSEIF p_score > max_score THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Score exceeds maximum allowed';
    ELSE
        UPDATE assignment_submissions
        SET score = p_score,
            feedback = p_feedback
        WHERE id = p_submission_id;
    END IF;
END //
DELIMITER ;

-- Insert sample data for testing
-- Sample users
INSERT INTO users (username, password, email, first_name, last_name)
VALUES 
('admin', 'Admin@123', 'admin@example.com', 'Admin', 'User'),
('instructor1', 'Instructor@123', 'instructor1@example.com', 'John', 'Doe'),
('instructor2', 'Instructor@123', 'instructor2@example.com', 'Jane', 'Smith'),
('student1', 'Student@123', 'student1@example.com', 'Alice', 'Johnson'),
('student2', 'Student@123', 'student2@example.com', 'Bob', 'Brown'),
('student3', 'Student@123', 'student3@example.com', 'Charlie', 'Davis');

-- Sample courses
INSERT INTO courses (course_name, course_code, description, instructor_id)
VALUES 
('Introduction to Python', 'PY101', 'Learn the basics of Python programming', 2),
('Advanced Java', 'JV201', 'Advanced topics in Java programming', 2),
('Web Development', 'WD101', 'Introduction to HTML, CSS, and JavaScript', 3),
('Database Management', 'DB101', 'Learn SQL and database design', 3);

-- Sample enrollments
INSERT INTO enrollments (user_id, course_id, completion_status)
VALUES 
(4, 1, 'in_progress'),
(4, 3, 'not_started'),
(5, 1, 'in_progress'),
(5, 2, 'completed'),
(6, 2, 'in_progress'),
(6, 3, 'in_progress'),
(6, 4, 'not_started');

-- Sample assignments
INSERT INTO assignments (course_id, title, description, due_date, max_score)
VALUES 
(1, 'Python Basics Quiz', 'Quiz covering Python syntax and basic concepts', '2023-12-31 23:59:59', 100),
(1, 'Python Project', 'Build a simple Python application', '2024-01-15 23:59:59', 200),
(2, 'Java OOP Assignment', 'Implement object-oriented concepts in Java', '2023-12-20 23:59:59', 150),
(3, 'HTML/CSS Portfolio', 'Create a personal portfolio website', '2024-01-10 23:59:59', 200),
(4, 'Database Design Project', 'Design and implement a database for a business case', '2024-01-20 23:59:59', 250);

-- Sample assignment submissions
INSERT INTO assignment_submissions (assignment_id, user_id, submission_text, submission_date, score, feedback)
VALUES 
(1, 4, 'My Python quiz answers...', '2023-12-15 14:30:00', 85, 'Good work, but review loops and functions'),
(1, 5, 'My Python quiz answers...', '2023-12-14 09:15:00', 92, 'Excellent understanding of basic concepts'),
(3, 5, 'Java OOP implementation code...', '2023-12-18 16:45:00', 145, 'Great implementation of inheritance and polymorphism'),
(3, 6, 'Java OOP implementation code...', '2023-12-19 11:20:00', 130, 'Good work, but could improve encapsulation');
