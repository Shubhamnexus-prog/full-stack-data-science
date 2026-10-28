-- creating table

CREATE TABLE emp
(
  empid  SMALLINT,
  ename  VARCHAR(10),
  job    VARCHAR(10),
  sal    SMALLMONEY,
  hiredate  DATE,
  dept   VARCHAR(10)
)
--insert valuse in single

INSERT INTO emp VALUES(100,'SHUBHAM','Clerk',4000,'2020-04-10','hr')
INSERT INTO emp VALUES(101,'Priya','analyst',9000,getdate(),'IT')

select*from emp

--multiple value insert

INSERT INTO emp VALUES(102,'ARVIND','manager',8000,'2018-02-20','hr'),(103,'david','clerk',5000,'2019-05-20','sales')
select*from emp


--null value insert method 1 exceplycity

INSERT INTO emp VALUES(104,'VIJAY',NULL,NULL,'2021-05-12','IT')

select*from emp

--null values insert method 2 implicity

INSERT INTO emp(empid,ename,hiredate,dept) VALUES(105,'sonu','2022-03-18','sales')

select*from emp

--display ename and salary

SELECT ename,sal FROM emp

--display name,salary,job

SELECT ename,sal,job FROM emp

--display all data from emp table


SELECT *FROM emp

---where clause--

SELECT*FROM emp WHERE empid=103

SELECT ename,sal FROM emp WHERE empid=103

--name is vijay--

SELECT * FROM emp WHERE ename='vijay'

--earning more than 5000 

SELECT * FROM emp WHERE sal>=5000

-- joined after 2020

SELECT* FROM emp WHERE hiredate>='2020-12-31'

--before 2020

SELECT * FROM emp WHERE hiredate<'2020-01-01'

--not working as clerk

SELECT * FROM emp WHERE job<>'clerk'

--
SELECT * FROM emp WHERE job='clerk'

SELECT * FROM emp WHERE job='clerk' AND job='manager'


SELECT * FROM emp WHERE job='clerk' OR job='manager'



SELECT *FROM emp WHERE empid=100 OR empid=103 OR empid=105

-- earning more than 5000

SELECT * FROM emp WHERE dept='hr' AND sal>5000

--display sales manager

SELECT *FROM emp WHERE dept='sales' AND job='manager'

--display employee earning more than 5000 and less than 10000

SELECT *FROM emp WHERE sal>5000 AND sal<10000

--employee joined 2020

SELECT *FROM emp WHERE hiredate>='2020-01-01' AND hiredate<='2020-12-31'

SELECT *
FROM emp
WHERE (job ='clerk' OR job = 'manager')
  AND sal > 5000;

  --display employee whose id 103,100,105--

SELECT * FROM emp WHERE empid IN(100,103,105)

--employ as working cleark manager--
SELECT *FROM emp WHERE job IN('clerk','manager')

--employee as not working clerk manager


--BETWEEN --

SELECT * FROM emp WHERE sal BETWEEN 5000 AND 10000

SELECT * FROM emp WHERE hiredate BETWEEN '2020-01-01' AND '2020-12-31'

SELECT * FROM emp WHERE hiredate  NOT BETWEEN '2020-01-01' AND '2020-12-31'

SELECT*
FROM emp
WHERE job IN ('clerk','manager')
      AND
      sal BETWEEN 5000 AND 10000
      AND
      hiredate NOT BETWEEN '2020-01-01' AND '2020-12-31'
      AND
      dept NOT IN ('hr','IT')

--LIKE OPERATOR--

SELECT * FROM emp WHERE ename LIKE 's%'

SELECT * FROM emp WHERE ename LIKE '%d'

SELECT *FROM emp WHERE ename LIKE '%a%'

SELECT* FROM emp WHERE ename LIKE '___a%'

SELECT *FROM emp WHERE ename LIKE '%a___'

SELECT*FROM emp WHERE dept in ('hr','IT')

SELECT *FROM emp WHERE ename LIKE '[adks]%'

SELECT * FROM emp WHERE ename LIKE '[a-p]%'

SELECT *FROM emp WHERE sal LIKE '____.00'

--oct month--

SELECT * FROM emp WHERE hiredate LIKE '_____10___'

SELECT *FROM emp WHERE hiredate LIKE '%_10_%'

SELECT *FROM emp WHERE hiredate LIKE '2020%'

--IS OPERATOR--

SELECT* FROM emp

SELECT *FROM emp WHERE sal IS NULL

SELECT * FROM emp WHERE sal IS NOT NULL

SELECT *FROM emp

--ALIAS--

--diaplay annual salary--

SELECT ename ,sal*12 as annualsalary FROM emp

SELECT ename ,sal*12 as [annual salary] FROM emp

--display hra da tax and total sal--

SELECT ename,sal,
       sal*0.2 as hra,
       sal*0.4 as da,
       sal*0.1 as tax,
       sal+(sal*0.2)+(sal*0.4)-(sal*0.1) as totsal
FROM emp

select*from emp

--order by--
--assending order

SELECT *
FROM emp
ORDER BY ename

--descending order--
SELECT * 
       FROM emp
       ORDER BY sal


SELECT * 
       FROM emp
       ORDER BY hiredate

SELECT * 
FROM emp
ORDER BY hiredate

--RENAME TABLE NAME

SP_RENAME 'emp','EMPLOYEE';

SELECT*FROM EMPLOYEE;



