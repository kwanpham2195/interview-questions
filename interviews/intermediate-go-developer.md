# Intermediate Go Developer Interview Format

## Interview Overview
**Duration**: 75-90 minutes  
**Format**: Technical interview focusing on advanced Go concepts, SQL skills, system design, and complex coding challenges  
**Target Level**: Intermediate developers (2-5 years Go experience)

## Interview Structure

### Part 1: Advanced Go Concepts (20-25 minutes)
**Objective**: Assess deep understanding of Go internals, concurrency, and advanced patterns

### Part 2: SQL Design & Query Skills (15-20 minutes)
**Objective**: Evaluate database design thinking and complex query writing abilities

### Part 3: System Design & Architecture (10-15 minutes)
**Objective**: Assess architectural thinking and system design fundamentals

### Part 4: Complex Coding Challenge (25-30 minutes)
**Objective**: Test advanced problem-solving skills and Go best practices

### Part 5: Discussion & Questions (5-10 minutes)
**Objective**: Clarify responses and allow candidate questions

---

## Part 1: Advanced Go Concepts (20-25 minutes)

### Question 1: Pointers vs Values (5-6 minutes)
**"Explain the difference between passing a value and passing a pointer to a function in Go. When would you choose one over the other, and what are the performance implications?"**

**Expected Answer Points**:
- Value types create independent copies when passed
- Pointer types pass memory addresses, allowing modifications
- Performance considerations: large structs benefit from pointers
- Memory safety: pointers can be nil, values cannot
- Method receivers: value vs pointer receivers

**Follow-up**: "What happens when you have a method with a pointer receiver but call it on a value?"

**Reference**: See [golang/intermediate.md - Question 1](../golang/intermediate.md#1-explain-the-difference-between-passing-a-value-and-passing-a-pointer-to-a-function-in-go) for detailed answer

---

### Question 2: Goroutines vs OS Threads (5-6 minutes)
**"Explain the difference between goroutines and OS threads. How does Go's scheduler work, and what are the advantages of the M:N threading model?"**

**Expected Answer Points**:
- Goroutines are lightweight, managed by Go runtime
- OS threads are heavier, managed by operating system
- M:N model: M goroutines multiplexed onto N OS threads
- Go scheduler handles blocking I/O efficiently
- Memory efficiency: goroutines start with small stacks

**Follow-up**: "What happens when a goroutine makes a blocking system call?"

**Reference**: See [golang/intermediate.md - Question 2](../golang/intermediate.md#2-explain-the-difference-between-a-goroutine-and-an-operating-system-os-thread) for detailed answer

---

### Question 3: Channels - Buffered vs Unbuffered (5-6 minutes)
**"Differentiate between unbuffered and buffered channels. When would you choose one over the other, and what are the potential implications of incorrect buffering?"**

**Expected Answer Points**:
- Unbuffered channels provide synchronization (rendezvous)
- Buffered channels decouple sender and receiver
- Blocking behavior differences
- Use cases: throttling, queuing, coordination
- Dangers of over-buffering and under-buffering

**Follow-up**: "How would you implement a worker pool using channels?"

**Reference**: See [golang/intermediate.md - Question 3](../golang/intermediate.md#3-differentiate-between-unbuffered-and-buffered-channels) for detailed answer

---

### Question 4: Context Package (5-7 minutes)
**"Explain the purpose of the context package. How would you use it to cancel a long-running operation and pass request-scoped values?"**

**Expected Answer Points**:
- Context propagates cancellation signals and deadlines
- Hierarchical structure: parent cancellation affects children
- WithCancel, WithTimeout, WithDeadline functions
- WithValue for request-scoped data
- Best practices: context as first parameter

**Expected Code Example**:
```go
func processWithTimeout(ctx context.Context, data string) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    
    select {
    case <-doWork(data):
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}
```

**Reference**: See [golang/intermediate.md - Question 6](../golang/intermediate.md#6-the-context-package-is-crucial-for-managing-requests-across-api-boundaries-and-goroutines) for detailed answer

---

### Alternative Questions (Choose 1-2 based on time and candidate background)

### Question 5A: Slice Internals (5-7 minutes)
**"Explain the underlying data structure of a Go slice. How does it differ from arrays in terms of memory allocation and behavior?"**

**Expected Answer Points**:
- Slice header: pointer, length, capacity
- Backing array concept
- Slice growth and reallocation
- Sharing underlying arrays
- Memory implications of slice operations

**Reference**: See [golang/intermediate.md - Question 7](../golang/intermediate.md#7-explain-the-underlying-data-structure-of-a-go-slice) for detailed answer

### Question 5B: Interface Implementation (5-7 minutes)
**"Go interfaces are implicitly implemented. Explain what this means and provide an example where this leads to more flexible code."**

**Expected Answer Points**:
- No explicit "implements" keyword
- Type satisfies interface by having required methods
- Enables polymorphism and decoupling
- "Accept interfaces, return concrete types" principle
- Example with io.Writer interface

**Reference**: See [golang/intermediate.md - Question 5](../golang/intermediate.md#5-go-interfaces-are-implicitly-implemented) for detailed answer

### Question 5C: Error Handling Patterns (5-7 minutes)
**"Describe advanced error handling patterns in Go. How do you wrap errors and handle different error types?"**

**Expected Answer Points**:
- fmt.Errorf with %w for wrapping
- errors.Is and errors.As for inspection
- Custom error types
- Error chains and unwrapping
- Sentinel errors vs dynamic errors

**Reference**: See [golang/intermediate.md - Question 4](../golang/intermediate.md#4-how-do-you-handle-errors-in-go-provide-an-example) for detailed answer

---

## Part 2: SQL Design & Query Skills (15-20 minutes)

### Database Schema Design (8-10 minutes)
**Present this scenario for database design:**

### Scenario: E-commerce Order Management System
**"Design a database schema for an e-commerce platform that needs to handle:"**
- **Products** with categories, pricing, and inventory
- **Users** who can place orders
- **Orders** containing multiple products with quantities
- **Order status tracking** (pending, processing, shipped, delivered)
- **Product reviews** by users

### Expected Schema Design
**Candidate should identify these key tables:**

```sql
-- Core entities
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Junction table for order items
CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    UNIQUE (user_id, product_id) -- One review per user per product
);
```

### Evaluation Criteria for Schema Design
- **Entity Identification**: Correctly identifies main entities and relationships
- **Normalization**: Proper normalization (avoiding redundancy)
- **Primary/Foreign Keys**: Appropriate key relationships
- **Data Types**: Suitable data types for each field
- **Constraints**: Proper use of constraints (UNIQUE, CHECK, NOT NULL)
- **Junction Tables**: Correctly handles many-to-many relationships

**Follow-up Questions:**
1. "How would you handle product variants (size, color) in this schema?"
2. "What indexes would you add for performance optimization?"
3. "How would you modify this to support multiple currencies?"

**Reference**: See [sql/design.md - Question 1](../sql/design.md#question-1-online-course-platform) for similar schema design patterns

---

### Complex SQL Queries (7-10 minutes)
**Present this enhanced schema for query questions:**

```sql
-- Enhanced schema for queries
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    salary DECIMAL(10,2),
    hire_date DATE,
    department_id INT,
    manager_id INT
);

CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE Projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2)
);

CREATE TABLE EmployeeProjects (
    employee_id INT,
    project_id INT,
    role VARCHAR(50),
    hours_allocated INT,
    PRIMARY KEY (employee_id, project_id)
);
```

### SQL Query 1: Advanced Aggregation (3-4 minutes)
**"Find all employees who earn more than the average salary in their department, and show their salary difference from the department average."**

**Expected Answer:**
```sql
WITH DepartmentAverage AS (
    SELECT 
        department_id,
        AVG(salary) AS avg_dept_salary
    FROM Employees
    GROUP BY department_id
)
SELECT 
    e.employee_name,
    e.salary,
    d.department_name,
    da.avg_dept_salary,
    (e.salary - da.avg_dept_salary) AS salary_difference
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
JOIN DepartmentAverage da ON e.department_id = da.department_id
WHERE e.salary > da.avg_dept_salary
ORDER BY salary_difference DESC;
```

**Reference**: See [sql/query.md - Question 1](../sql/query.md#1-find-employees-above-department-average-salary) for detailed explanation

### SQL Query 2: Window Functions (2-3 minutes)
**"Rank employees by salary within each department and show only the top 2 highest-paid employees per department."**

**Expected Answer:**
```sql
WITH RankedEmployees AS (
    SELECT 
        e.employee_name,
        e.salary,
        d.department_name,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank
    FROM Employees e
    JOIN Departments d ON e.department_id = d.department_id
)
SELECT 
    department_name,
    employee_name,
    salary,
    salary_rank
FROM RankedEmployees
WHERE salary_rank <= 2
ORDER BY department_name, salary_rank;
```

**Reference**: See [sql/query.md - Question 3](../sql/query.md#3-rank-employees-by-salary-within-each-department) for window function examples

### SQL Query 3: Complex JOIN with Subquery (2-3 minutes)
**"Find projects that have more than 3 employees assigned and show the total hours allocated and average salary of employees on each project."**

**Expected Answer:**
```sql
SELECT 
    p.project_name,
    COUNT(ep.employee_id) AS employee_count,
    SUM(ep.hours_allocated) AS total_hours,
    AVG(e.salary) AS avg_employee_salary
FROM Projects p
JOIN EmployeeProjects ep ON p.project_id = ep.project_id
JOIN Employees e ON ep.employee_id = e.employee_id
GROUP BY p.project_id, p.project_name
HAVING COUNT(ep.employee_id) > 3
ORDER BY employee_count DESC;
```

### Alternative SQL Questions (Choose 1-2 based on time)

### Query 4A: Self-Join
**"Find all employees who earn more than their manager."**

**Expected Answer:**
```sql
SELECT 
    e.employee_name,
    e.salary,
    m.employee_name AS manager_name,
    m.salary AS manager_salary
FROM Employees e
JOIN Employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;
```

### Query 4B: Date Functions
**"Find employees hired in the last 2 years and calculate their tenure in months."**

**Expected Answer:**
```sql
SELECT 
    employee_name,
    hire_date,
    DATEDIFF(CURRENT_DATE, hire_date) / 30 AS tenure_months
FROM Employees
WHERE hire_date >= DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR)
ORDER BY hire_date DESC;
```

**Reference**: See [sql/query.md](../sql/query.md) for more complex query examples

---

## Part 3: System Design & Architecture (10-15 minutes)

### Question 1: Microservices Communication (5-7 minutes)
**"Design a simple microservices architecture for an e-commerce system. How would you handle communication between services, and what are the trade-offs of different approaches?"**

**Expected Answer Points**:
- Service boundaries: User, Product, Order, Payment services
- Communication patterns: HTTP/REST, gRPC, message queues
- Synchronous vs asynchronous communication
- Service discovery and load balancing
- Data consistency challenges

**Follow-up**: "How would you handle a scenario where the payment service is down but users are still placing orders?"

---

### Question 2: Caching Strategy (3-5 minutes)
**"You have a Go web service that's experiencing high database load. Design a caching strategy to improve performance. What types of caching would you implement and why?"**

**Expected Answer Points**:
- Application-level caching (in-memory, Redis)
- Database query result caching
- HTTP response caching
- Cache invalidation strategies
- Cache-aside vs write-through patterns
- Considerations: TTL, cache warming, thundering herd

**Follow-up**: "How would you handle cache invalidation when data is updated?"

---

### Question 3: Database Design (2-3 minutes)
**"Design a database schema for a social media platform where users can follow each other and post messages. How would you optimize for read-heavy workloads?"**

**Expected Answer Points**:
- Core entities: Users, Posts, Follows, Likes
- Relationship modeling: many-to-many for follows
- Indexing strategies for common queries
- Denormalization for read performance
- Partitioning/sharding considerations
- Timeline generation approaches

**Follow-up**: "How would you generate a user's timeline efficiently?"

---

## Part 4: Complex Coding Challenge (25-30 minutes)

### Challenge: Concurrent Web Scraper
**"Design and implement a concurrent web scraper that can fetch multiple URLs simultaneously while respecting rate limits."**

### Problem Statement
**"Create a Go program that:**
1. **Takes a list of URLs to scrape**
2. **Fetches them concurrently with a maximum of 5 concurrent requests**
3. **Implements rate limiting (max 10 requests per second)**
4. **Handles timeouts and errors gracefully**
5. **Returns results in a structured format**

### Expected Solution Structure
```go
package main

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "sync"
    "time"
)

type Result struct {
    URL      string
    Content  string
    Error    error
    Duration time.Duration
}

type Scraper struct {
    client      *http.Client
    rateLimiter chan struct{}
    semaphore   chan struct{}
}

func NewScraper(maxConcurrent int, rateLimit int) *Scraper {
    // Implementation details
}

func (s *Scraper) ScrapeURLs(ctx context.Context, urls []string) []Result {
    // Implementation with goroutines, channels, and proper error handling
}
```

### Evaluation Criteria
- **Concurrency Control**: Proper use of goroutines, channels, and synchronization
- **Rate Limiting**: Implementation of rate limiting mechanism
- **Error Handling**: Graceful handling of network errors and timeouts
- **Resource Management**: Proper cleanup and resource management
- **Code Structure**: Clean, maintainable code with good separation of concerns

### Follow-up Questions
1. "How would you modify this to handle retries for failed requests?"
2. "What if you needed to scrape millions of URLs? How would you scale this?"
3. "How would you add metrics and monitoring to this scraper?"

### Alternative Challenges (Choose based on candidate background)

### Challenge B: Event Processing System
**"Design a system that processes events from multiple sources, applies transformations, and routes them to different destinations based on event type."**

### Challenge C: Cache with TTL
**"Implement a thread-safe cache with TTL (time-to-live) functionality that automatically expires entries."**

---

## Part 5: Discussion & Questions (5-10 minutes)

### Wrap-up Questions
1. "What Go packages or frameworks have you used in production?"
2. "How do you approach testing in Go? What testing patterns do you follow?"
3. "What's your experience with Go's profiling tools (pprof)?"
4. "How do you handle database migrations and schema changes in Go applications?"
5. "What databases have you worked with? Any experience with ORMs vs raw SQL?"
6. "How do you approach database performance optimization in your applications?"
7. "Do you have any questions about our architecture, tech stack, or the role?"

---

## Scoring Guidelines

### Advanced Go Concepts (30 points)
- **Excellent (26-30)**: Deep understanding of Go internals, concurrency, and advanced patterns
- **Good (20-25)**: Solid understanding with minor gaps in advanced topics
- **Fair (12-19)**: Basic understanding but struggles with complex concepts
- **Poor (0-11)**: Limited understanding of intermediate-level Go concepts

### SQL Design & Query Skills (25 points)
- **Excellent (22-25)**: Clean schema design, complex queries with optimization awareness
- **Good (17-21)**: Good database design sense, can write most queries correctly
- **Fair (10-16)**: Basic SQL knowledge but struggles with complex joins/subqueries
- **Poor (0-9)**: Cannot design schemas or write intermediate-level queries

### System Design & Architecture (20 points)
- **Excellent (18-20)**: Clear architectural thinking, considers trade-offs, scalability
- **Good (14-17)**: Good design sense with minor oversights
- **Fair (8-13)**: Basic design understanding but lacks depth
- **Poor (0-7)**: Cannot think architecturally or design systems

### Complex Coding Challenge (25 points)
- **Excellent (22-25)**: Clean, concurrent solution with proper error handling
- **Good (17-21)**: Working solution with good Go practices
- **Fair (10-16)**: Solution works but has concurrency or design issues
- **Poor (0-9)**: Cannot implement concurrent solution

### Overall Assessment
- **Total Score**: 100 points
- **Passing Score**: 70+ points
- **Strong Candidate**: 85+ points

---

## Interviewer Notes

### Preparation Checklist
- [ ] Review candidate's resume and Go experience
- [ ] Prepare coding environment with Go workspace
- [ ] Have database schema diagrams ready for SQL questions
- [ ] Prepare SQL query environment or whiteboard for writing queries
- [ ] Have system design whiteboard or digital tool ready
- [ ] Prepare follow-up questions based on candidate's background
- [ ] Review recent Go best practices and patterns

### During Interview
- [ ] Start with advanced concepts to gauge depth
- [ ] Allow thinking time for system design questions
- [ ] Focus on reasoning and trade-offs, not just correct answers
- [ ] Observe problem-solving approach and code organization
- [ ] Ask for clarification of design decisions

### Red Flags
- Cannot explain Go concurrency fundamentals
- Unable to design basic database schemas
- Cannot write intermediate-level SQL queries
- No understanding of system design principles
- Cannot implement concurrent solutions
- Doesn't consider error handling or edge cases
- Shows no experience with production Go applications
- Cannot discuss trade-offs or architectural decisions

### Green Flags
- Demonstrates deep Go knowledge and best practices
- Designs well-normalized database schemas
- Writes efficient SQL queries with proper joins and aggregations
- Thinks architecturally about system design
- Implements clean, concurrent solutions
- Considers error handling, testing, and maintainability
- Shows experience with production systems
- Asks thoughtful questions about requirements
- Discusses trade-offs and alternative approaches

---

## Alternative Questions (For Variety)

### Advanced Go Alternatives
- **Memory model and happens-before relationships**
- **Go scheduler internals and preemption**
- **Reflection and its performance implications**
- **Build tags and conditional compilation**
- **Garbage collector tuning and optimization**

### SQL Design Alternatives
- **Design a social media platform database (users, posts, follows, likes)**
- **Design a library management system (books, authors, borrowers, loans)**
- **Design a hotel booking system (hotels, rooms, reservations, customers)**
- **Design a financial transaction system (accounts, transactions, balances)**

### System Design Alternatives
- **Design a URL shortener service**
- **Design a chat application with real-time messaging**
- **Design a distributed cache system**
- **Design a metrics collection and monitoring system**

### Coding Challenge Alternatives
- **Implement a connection pool with health checking**
- **Build a simple load balancer with different algorithms**
- **Create a distributed task queue system**
- **Implement a circuit breaker pattern**
- **Build a simple database query planner**

**Reference**: See [golang/intermediate.md](../golang/intermediate.md) for detailed answers to conceptual questions and [golang/coding.md](../golang/coding.md) for more complex coding examples.

This format provides a comprehensive assessment for intermediate Go developers while maintaining consistency with the junior format structure. The questions progress from advanced language concepts to system thinking and complex implementation challenges. 