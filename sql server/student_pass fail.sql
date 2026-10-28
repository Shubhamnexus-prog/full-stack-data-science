CREATE TABLE student
(
    s_no INT PRIMARY KEY,
    s_name VARCHAR(20),
    S1 INT,
    S2 INT,
    S3 INT
);

INSERT INTO student VALUES
(1, 'A', 80, 90, 70),
(2, 'B', 30, 60, 50),
(3, 'C', 60, 20, 30),
(4, 'D', 10, 20, 30);

SELECT * FROM student;

--total avg and result
SELECT s_no, s_name,
       S1 + S2 + S3 AS total,
       (S1 + S2 + S3) / 3.0 AS avg,
       CASE
           WHEN S1 >= 35 AND S2 >= 35 AND S3 >= 35
           THEN 'PASS'
           ELSE 'FAIL'
       END AS result
FROM student;

