USE companyDB;

SELECT*FROM Employees;


--- FIND the highest salary--

   SELECT MAX(Salary) AS HighestSalary
   FROM Employees



----find the lowest salary--

   SELECT MIN(Salary) AS lowestSalary
   FROM Employees


--- find the total number of employees--

    SELECT COUNT(*) AS TotalEmployees
    FROM Employees

----find the average of salary---

    SELECT AVG(Salary) AS AverageSalary
    FROM Employees


---find employees  with salaries between 40000 and 50000

    SELECT*
    FROM Employees
    WHERE Salary BETWEEN 40000 AND 50000;


---Find employees whose name start with R

     SELECT *
     FROM Employees
     WHERE EmployeeName LIKE 'R%';


---find employees whose department is IT or HR

     SELECT*
     FROM Employees
     WHERE Department IN ('IT','HR');


---Display employees in descending order of salary.

     SELECT* 
     FROM Employees
     ORDER BY Salary DESC

--- DISPLAY  employees salary in assending order of salary

    SELECT*
    FROM Employees
    ORDER BY Salary ASC


--- find the second highest salary--

   SELECT MAX(Salary) AS SecondHighestSalary
   FROM Employees
   WHERE Salary < (
        SELECT MAX(Salary)
        FROM Employees
   ); 


--- find employees whose salary is greater than the average salary

  SELECT*
  FROM Employees
  WHERE Salary > (
       SELECT AVG(Salary)
       FROM Employees
 );

----- find the total salary department -wise---
    
     SELECT
       Department,
       SUM(Salary) AS TotalSalary
     FROM Employees
     GROUP BY Department;


---Find employees whose names end with a

   SELECT *
   FROM Employees
   WHERE EmployeeName LIKE '%A';


---Find the number of employees in each department

  SELECT
      Department,
      COUNT(*) AS TotalEmployees
  FROM Employees
  GROUP BY Department



