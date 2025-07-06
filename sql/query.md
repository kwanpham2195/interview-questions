# SQL Query Questions

### **Scenario**

  * **`Employees`** (`employee_id`, `employee_name`, `salary`, `hire_date`, `department_id`, `manager_id`)
  * **`Departments`** (`department_id`, `department_name`)
  * **`Projects`** (`project_id`, `project_name`, `start_date`, `end_date`)
  * **`EmployeeProjects`** (`employee_id`, `project_id`)

---

### 1. Find Employees Above Department Average Salary
```sql
SELECT
    e.employee_name,
    e.salary,
    d.department_name
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id
WHERE
    e.salary > (SELECT AVG(e2.salary)
                FROM Employees e2
                WHERE e2.department_id = e.department_id);
```
*Alternatively, using a CTE:*
```sql
WITH DepartmentAverage AS (
    SELECT
        department_id,
        AVG(salary) AS avg_dept_salary
    FROM
        Employees
    GROUP BY
        department_id
)
SELECT
    e.employee_name,
    e.salary,
    d.department_name
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id
JOIN
    DepartmentAverage da ON e.department_id = da.department_id
WHERE
    e.salary > da.avg_dept_salary;
```

---

### 2. Department with the Highest Paid Employee
```sql
SELECT
    d.department_name
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id
ORDER BY
    e.salary DESC
LIMIT 1; -- For MySQL/PostgreSQL
-- Or for SQL Server: FETCH FIRST 1 ROW ONLY;
-- Or for Oracle: ROWNUM <= 1
```
*Alternatively, using a subquery:*
```sql
SELECT
    d.department_name
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id
WHERE
    e.salary = (SELECT MAX(salary) FROM Employees);
```

---

### 3. Rank Employees by Salary Within Each Department
```sql
SELECT
    e.employee_name,
    d.department_name,
    e.salary,
    DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id;
```

---

### 4. Find Managers Who Manage More Than 5 Employees
```sql
SELECT
    m.employee_name AS manager_name,
    COUNT(e.employee_id) AS number_of_managed_employees
FROM
    Employees e -- Managed employees
JOIN
    Employees m ON e.manager_id = m.employee_id -- Manager
GROUP BY
    m.employee_id, m.employee_name
HAVING
    COUNT(e.employee_id) > 5;
```

---

### 5. List Employees Not Assigned to Any Project
```sql
SELECT
    e.employee_name
FROM
    Employees e
LEFT JOIN
    EmployeeProjects ep ON e.employee_id = ep.employee_id
WHERE
    ep.project_id IS NULL;
```
*Alternatively, using `NOT EXISTS`:*
```sql
SELECT
    e.employee_name
FROM
    Employees e
WHERE NOT EXISTS (
    SELECT 1
    FROM EmployeeProjects ep
    WHERE ep.employee_id = e.employee_id
);
```

---

### 6. Find the Second Highest Salary Per Department
```sql
WITH RankedSalaries AS (
    SELECT
        e.employee_name,
        e.salary,
        d.department_name,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rnk
    FROM
        Employees e
    JOIN
        Departments d ON e.department_id = d.department_id
)
SELECT
    department_name,
    employee_name,
    salary
FROM
    RankedSalaries
WHERE
    rnk = 2;
```

---

### 7. Identify Overlapping Projects
```sql
SELECT
    P1.project_name AS project1_name,
    P2.project_name AS project2_name
FROM
    Projects P1
JOIN
    Projects P2 ON P1.project_id < P2.project_id -- To avoid duplicate pairs and self-comparison
WHERE
    P1.start_date <= P2.end_date AND P1.end_date >= P2.start_date;
```

---

### 8. Calculate the Monthly Salary Bill for Each Department
```sql
SELECT
    d.department_name,
    SUM(e.salary) AS total_monthly_salary_bill
FROM
    Employees e
JOIN
    Departments d ON e.department_id = d.department_id
GROUP BY
    d.department_name
ORDER BY
    d.department_name;
```

---

### 9. List Departments with No Employees
```sql
SELECT
    d.department_name
FROM
    Departments d
LEFT JOIN
    Employees e ON d.department_id = e.department_id
WHERE
    e.employee_id IS NULL;
```
*Alternatively, using `NOT EXISTS`:*
```sql
SELECT
    d.department_name
FROM
    Departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM Employees e
    WHERE e.department_id = d.department_id
);
```

---

### 10. Find the Most Common Salary
```sql
SELECT
    salary,
    COUNT(employee_id) AS number_of_employees
FROM
    Employees
GROUP BY
    salary
ORDER BY
    number_of_employees DESC
LIMIT 1; -- For MySQL/PostgreSQL
-- Or for SQL Server: FETCH FIRST 1 ROW ONLY;
-- Or for Oracle: ROWNUM <= 1
```

---

### 11. Find Projects with More Than 3 Employees and Calculate Resource Metrics
```sql
SELECT 
    p.project_name,
    COUNT(ep.employee_id) AS employee_count,
    SUM(ep.hours_allocated) AS total_hours_allocated,
    AVG(e.salary) AS avg_employee_salary,
    SUM(e.salary * ep.hours_allocated) / SUM(ep.hours_allocated) AS weighted_avg_salary
FROM Projects p
JOIN EmployeeProjects ep ON p.project_id = ep.project_id
JOIN Employees e ON ep.employee_id = e.employee_id
GROUP BY p.project_id, p.project_name
HAVING COUNT(ep.employee_id) > 3
ORDER BY employee_count DESC, total_hours_allocated DESC;
```

---

### 12. Find Employees Who Earn More Than Their Manager
```sql
SELECT 
    e.employee_name,
    e.salary AS employee_salary,
    m.employee_name AS manager_name,
    m.salary AS manager_salary,
    (e.salary - m.salary) AS salary_difference
FROM Employees e
JOIN Employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary
ORDER BY salary_difference DESC;
```

---

### 13. Calculate Running Total of Salaries by Department
```sql
SELECT 
    e.employee_name,
    d.department_name,
    e.salary,
    SUM(e.salary) OVER (
        PARTITION BY e.department_id 
        ORDER BY e.salary DESC 
        ROWS UNBOUNDED PRECEDING
    ) AS running_total_salary,
    ROW_NUMBER() OVER (
        PARTITION BY e.department_id 
        ORDER BY e.salary DESC
    ) AS salary_rank_in_dept
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
ORDER BY d.department_name, e.salary DESC;
```

---

### 14. Find Employees Hired in the Last 2 Years with Tenure Calculation
```sql
SELECT 
    employee_name,
    hire_date,
    DATEDIFF(CURRENT_DATE, hire_date) AS days_employed,
    FLOOR(DATEDIFF(CURRENT_DATE, hire_date) / 365) AS years_employed,
    FLOOR((DATEDIFF(CURRENT_DATE, hire_date) % 365) / 30) AS additional_months,
    CASE 
        WHEN DATEDIFF(CURRENT_DATE, hire_date) < 365 THEN 'New Employee'
        WHEN DATEDIFF(CURRENT_DATE, hire_date) < 730 THEN 'Junior Employee'
        ELSE 'Experienced Employee'
    END AS employment_category
FROM Employees
WHERE hire_date >= DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR)
ORDER BY hire_date DESC;
```

---

### 15. Advanced Department Analysis with Multiple Metrics
```sql
WITH DepartmentStats AS (
    SELECT 
        d.department_name,
        COUNT(e.employee_id) AS total_employees,
        AVG(e.salary) AS avg_salary,
        MIN(e.salary) AS min_salary,
        MAX(e.salary) AS max_salary,
        SUM(e.salary) AS total_salary_cost,
        STDDEV(e.salary) AS salary_stddev
    FROM Departments d
    LEFT JOIN Employees e ON d.department_id = e.department_id
    GROUP BY d.department_id, d.department_name
),
CompanyStats AS (
    SELECT 
        AVG(avg_salary) AS company_avg_salary,
        AVG(total_employees) AS avg_dept_size
    FROM DepartmentStats
    WHERE total_employees > 0
)
SELECT 
    ds.department_name,
    ds.total_employees,
    ds.avg_salary,
    cs.company_avg_salary,
    (ds.avg_salary - cs.company_avg_salary) AS salary_diff_from_company_avg,
    CASE 
        WHEN ds.avg_salary > cs.company_avg_salary THEN 'Above Average'
        WHEN ds.avg_salary < cs.company_avg_salary THEN 'Below Average'
        ELSE 'Average'
    END AS salary_category,
    ds.min_salary,
    ds.max_salary,
    ds.total_salary_cost,
    ROUND(ds.salary_stddev, 2) AS salary_variation
FROM DepartmentStats ds
CROSS JOIN CompanyStats cs
WHERE ds.total_employees > 0
ORDER BY ds.avg_salary DESC;
