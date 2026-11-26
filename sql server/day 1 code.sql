

--CREATE DATABASE--

CREATE DATABASE CompanyDB;

USE CompanyDB;


---create tables--

CREATE TABLE Employees
(
   EmployeeID INT PRIMARY KEY,
   EmployeeName VARCHAR(50),
   Department VARCHAR(50),
   Salary INT,
   City  VARCHAR(50)
);
   

--insert data--

INSERT INTO Employees
VALUES
(101,'Rahul','IT',45000,'HYDERABAD'),
(102,'Amit','HR',35000,'DELHI'),
(103,'Priya','Finance',50000,'MUMBAI'),
(104,'Neha','IT',60000,'HYDERABAD'),
(105,'Rohit','Sales',40000,'PUNE');


--Display data---

SELECT*FROM Employees;



---Display all employee records.

           SELECT *
           FROM Employees;
      


---Find employees whose salary is greater than 40,000.
     
           SELECT *
           FROM Employees
           WHERE Salary>40000 ;

---Display only employee names and departments.

           SELECT EmployeeNAME , Department
           FROM Employees;

---Find employees working in the IT department.

        SELECT *
        FROM Employees
        WHERE Department = 'IT';

--Find employees living in Hyderabad.

       SELECT * 
       FROM Employees
       WHERE City = 'HYDERABAD';