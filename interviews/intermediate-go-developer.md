# Intermediate Go Developer Interview Format

## Interview Overview
**Duration**: 60 minutes  
**Format**: Technical interview focusing on advanced Go concepts, SQL skills, system design, and complex coding challenges  
**Target Level**: Intermediate developers (2-5 years Go experience)

## Interview Structure

### Part 1: Advanced Go Concepts (15 minutes)
**Objective**: Assess deep understanding of Go internals, concurrency, and advanced patterns

### Part 2: SQL Design & Query Skills (12 minutes)
**Objective**: Evaluate database design thinking and query writing abilities

### Part 3: System Design & Architecture (8 minutes)
**Objective**: Assess architectural thinking and caching strategy

### Part 4: Complex Coding Challenge (20 minutes)
**Objective**: Test advanced problem-solving skills and Go best practices

### Part 5: Discussion & Questions (5 minutes)
**Objective**: Clarify responses and allow candidate questions

---

## Part 1: Advanced Go Concepts (15 minutes)

### Question 1: Pointers vs Values (5 minutes)
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

### Question 2: Goroutines vs OS Threads (5 minutes)
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

### Question 3: Channels - Buffered vs Unbuffered (5 minutes)
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

## Part 2: SQL Design & Query Skills (12 minutes)

### Database Schema Design (5 minutes)
**Present this scenario for database design:**

### Scenario: E-commerce Order Management System
**"Design a database schema for an e-commerce platform that needs to handle:"**
- **Products** with categories and pricing
- **Users** who can place orders
- **Orders** containing multiple products with quantities
- **Order status tracking** (pending, processing, shipped, delivered)

### Expected Schema Design
**Candidate should identify these key tables:**

```sql
-- Core entities
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
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
```

### Evaluation Criteria for Schema Design
- **Entity Identification**: Correctly identifies main entities and relationships
- **Normalization**: Proper normalization (avoiding redundancy)
- **Primary/Foreign Keys**: Appropriate key relationships
- **Data Types**: Suitable data types for each field

**Follow-up**: "What indexes would you add for performance optimization?"

**Reference**: See [sql/design.md - Question 1](../sql/design.md#question-1-online-course-platform) for similar schema design patterns

---

### SQL Queries (7 minutes)
**Present this schema for query questions:**

```sql
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    salary DECIMAL(10,2),
    department_id INT,
    manager_id INT
);

CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE EmployeeProjects (
    employee_id INT,
    project_id INT,
    hours_allocated INT,
    PRIMARY KEY (employee_id, project_id)
);
```

### SQL Query 1: Advanced Aggregation (3-4 minutes)
**"Find all employees who earn more than the average salary in their department."**

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
    d.department_name
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
JOIN DepartmentAverage da ON e.department_id = da.department_id
WHERE e.salary > da.avg_dept_salary
ORDER BY e.salary DESC;
```

### SQL Query 2: Window Functions (3 minutes)
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

**Reference**: See [sql/query.md](../sql/query.md) for more complex query examples

---

## Part 3: System Design & Architecture (8 minutes)

### Question: Caching Strategy (8 minutes)
**"You have a Go web service that's experiencing high database load. Design a caching strategy to improve performance. What types of caching would you implement and why?"**

**Expected Answer Points**:
- **Multi-layer caching approach**: Application-level, database query result caching, HTTP response caching
- **Cache storage options**: In-memory (sync.Map, local cache), distributed (Redis, Memcached)
- **Caching patterns**: Cache-aside, write-through, write-behind, read-through
- **Cache key design**: Hierarchical keys, namespace strategies, key expiration
- **Performance considerations**: TTL strategies, cache warming, thundering herd prevention
- **Invalidation strategies**: Time-based, event-driven, manual invalidation

**Follow-up Questions**:
1. **"How would you handle cache invalidation when data is updated?"**
   - *Looking for*: Event-driven invalidation, cache tags, versioning strategies, distributed cache coordination

2. **"What would you do to prevent the 'thundering herd' problem when a popular cache key expires?"**
   - *Looking for*: Cache locks, staggered expiration, cache refresh ahead of expiration, circuit breaker patterns

3. **"How would you implement caching in Go code? Show me a simple cache-aside pattern."**
   - *Looking for*: Basic Go implementation with proper error handling, goroutine safety, interface design

4. **"What metrics would you monitor to measure cache effectiveness?"**
   - *Looking for*: Hit/miss ratios, cache response times, memory usage, eviction rates, business impact metrics

**Bonus Follow-up**: "How would you handle cache consistency in a distributed system with multiple service instances?"

---

## Part 4: Complex Coding Challenge (20 minutes)

### Challenge: Worker Pool Implementation
**"Design and implement a worker pool pattern that can process jobs concurrently with proper resource management and graceful shutdown."**

### Problem Statement
**"Create a Go program that:**
1. **Implements a worker pool with configurable number of workers**
2. **Processes jobs from a queue concurrently**
3. **Handles graceful shutdown and cleanup**
4. **Provides basic result collection and error handling**

### Expected Solution Structure
```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type Job struct {
    ID   int
    Data string
}

type Result struct {
    Job    Job
    Output string
    Error  error
}

type WorkerPool struct {
    workers    int
    jobQueue   chan Job
    resultChan chan Result
    ctx        context.Context
    cancel     context.CancelFunc
    wg         sync.WaitGroup
}

func NewWorkerPool(workers int, queueSize int) *WorkerPool {
    ctx, cancel := context.WithCancel(context.Background())
    return &WorkerPool{
        workers:    workers,
        jobQueue:   make(chan Job, queueSize),
        resultChan: make(chan Result, queueSize),
        ctx:        ctx,
        cancel:     cancel,
    }
}

func (wp *WorkerPool) Start() {
    for i := 0; i < wp.workers; i++ {
        wp.wg.Add(1)
        go wp.worker(i)
    }
}

func (wp *WorkerPool) worker(id int) {
    defer wp.wg.Done()
    for {
        select {
        case job, ok := <-wp.jobQueue:
            if !ok {
                return // Channel closed
            }
            result := wp.processJob(job)
            wp.resultChan <- result
        case <-wp.ctx.Done():
            return // Context cancelled
        }
    }
}

func (wp *WorkerPool) processJob(job Job) Result {
    // Simulate work
    time.Sleep(100 * time.Millisecond)
    return Result{
        Job:    job,
        Output: fmt.Sprintf("Processed job %d: %s", job.ID, job.Data),
        Error:  nil,
    }
}

func (wp *WorkerPool) Submit(job Job) {
    wp.jobQueue <- job
}

func (wp *WorkerPool) Shutdown() {
    close(wp.jobQueue)  // Signal no more jobs
    wp.cancel()         // Cancel context
    wp.wg.Wait()        // Wait for all workers to finish
    close(wp.resultChan)
}
```

### Evaluation Criteria
- **Concurrency Control**: Proper use of goroutines, channels, and worker pool pattern
- **Resource Management**: Proper job queue management and worker lifecycle
- **Graceful Shutdown**: Implementation of clean shutdown with context handling
- **Code Structure**: Clean, maintainable code with proper separation of concerns

### Follow-up Questions (Choose 1-2)
1. "How would you modify this to handle job priorities?"
2. "What if you needed to process millions of jobs? How would you scale this?"
3. "How would you add basic monitoring to this worker pool?"

---

## Part 5: Discussion & Questions (5 minutes)

### Essential Wrap-up Questions
1. "What Go packages or frameworks have you used in production?"
2. "How do you approach testing in Go? What testing patterns do you follow?"
3. "How do you handle database migrations and schema changes in Go applications?"
4. "Do you have any questions about our architecture, tech stack, or the role?"

---

## Alternative Questions (If Needed)

### Alternative Go Concepts Questions
**If candidate struggles with advanced concepts, choose from:**

#### Alternative 1: Basic Go Interfaces (5 minutes)
**"Explain interfaces in Go and their importance. How do they differ from interfaces in other languages?"**

**Expected Answer Points** *(from general-questions.md)*:
- **Implicit Implementation**: No explicit `implements` keyword; any type providing all methods satisfies the interface
- **Polymorphism**: Allows writing functions that operate on any type satisfying an interface
- **Decoupling**: Enables loose coupling by depending on abstractions rather than concrete implementations
- **Testing**: Makes it easy to mock dependencies during testing
- **Duck Typing**: "If it walks like a duck and quacks like a duck, it's a duck"

**Follow-up**: "Can you give an example of how you'd use interfaces for dependency injection in Go?"

#### Alternative 2: Go Error Handling (5 minutes)
**"How does Go handle error management? What are some best practices you follow?"**

**Expected Answer Points** *(from general-questions.md)*:
- **Multiple Return Values**: Conventionally, last return value is an `error` interface
- **Explicit Checking**: Always check for errors immediately (`if err != nil`)
- **Sentinel Errors**: Use exported `var` errors for known conditions (`errors.Is`)
- **Error Wrapping**: Use `fmt.Errorf("%w", err)` to add context while preserving original error
- **Custom Error Types**: Define structured error types for more information
- **Return Up Stack**: Don't print and exit unless in `main` function

**Follow-up**: "How would you handle errors in a chain of function calls?"

#### Alternative 3: Go Context Package (4 minutes)
**"What is the `context` package in Go, and why is it crucial for web development?"**

**Expected Answer Points** *(from general-questions.md)*:
- **Purpose**: Carries deadlines, cancellation signals, and request-scoped values across API boundaries
- **Timeouts/Deadlines**: Ensures operations don't block indefinitely
- **Cancellation**: Allows graceful shutdown when clients disconnect
- **Request-Scoped Values**: Passing request-specific data (user ID, trace IDs) without explicit parameters
- **Microservices**: Vital for logging and tracing in distributed systems

**Follow-up**: "How would you use context for request timeouts in an HTTP handler?"

### Alternative SQL Questions
**If candidate struggles with advanced SQL, choose from:**

#### Alternative 1: Basic SQL Joins (4 minutes)
**"Explain the different types of SQL joins and when you would use them."**

**Expected Answer Points** *(from general-questions.md)*:
- **INNER JOIN**: Returns rows with matching values in both tables
- **LEFT JOIN**: Returns all rows from left table, matching rows from right (NULLs for no match)
- **RIGHT JOIN**: Returns all rows from right table, matching rows from left
- **FULL JOIN**: Returns all rows when there's a match in either table

**Follow-up**: "Give me a practical example of when you'd use a LEFT JOIN vs INNER JOIN."

#### Alternative 2: Database Normalization (5 minutes)
**"What is database normalization and why is it important?"**

**Expected Answer Points** *(from general-questions.md)*:
- **Purpose**: Organizing tables to minimize data redundancy and improve integrity
- **1NF**: Each column contains atomic values, no repeating groups
- **2NF**: No partial dependencies on primary key
- **3NF**: No transitive dependencies between non-key attributes
- **Benefits**: Reduces anomalies, improves data integrity

**Follow-up**: "What are the trade-offs between normalization and denormalization?"

#### Alternative 3: ACID Properties (4 minutes)
**"Explain the ACID properties of database transactions."**

**Expected Answer Points** *(from general-questions.md)*:
- **Atomicity**: All operations succeed or none do (indivisible unit)
- **Consistency**: Transaction brings database from one valid state to another
- **Isolation**: Concurrent transactions execute as if sequential
- **Durability**: Committed changes survive system failures

**Follow-up**: "Why are ACID properties important for financial applications?"

### Alternative System Design Questions
**If candidate struggles with caching, choose from:**

#### Alternative 1: Horizontal vs Vertical Scaling (4 minutes)
**"What's the difference between horizontal and vertical scaling? When would you use each?"**

**Expected Answer Points** *(from general-questions.md)*:
- **Vertical Scaling (Scale Up)**: Increasing resources of single server (CPU, RAM)
  - *Pros*: Simpler, no distributed system complexity
  - *Cons*: Hardware limits, single point of failure, expensive at scale
- **Horizontal Scaling (Scale Out)**: Adding more servers/instances
  - *Pros*: Nearly limitless scalability, fault tolerance, cost-effective
  - *Cons*: Distributed system complexity, data consistency challenges

**Follow-up**: "How would you decide when to scale horizontally vs vertically?"

#### Alternative 2: Load Balancing Basics (4 minutes)
**"Explain load balancing and describe a few common algorithms."**

**Expected Answer Points** *(from general-questions.md)*:
- **Purpose**: Distribute traffic across multiple servers to prevent bottlenecks
- **Round Robin**: Sequential distribution to each server
- **Weighted Round Robin**: More requests to stronger servers
- **Least Connection**: Directs to server with fewest active connections
- **IP Hash**: Same client IP goes to same server (session affinity)

**Follow-up**: "What happens if one of your backend servers fails?"

### Alternative Coding Challenges
**If candidate struggles with worker pool, choose from:**

#### Alternative 1: Simple Channel Communication (10 minutes)
**"Implement a simple producer-consumer pattern using goroutines and channels. One goroutine produces numbers 1-10, another consumes and prints them."**

**Expected Solution Structure**:
```go
package main

import (
    "fmt"
    "sync"
)

func producer(ch chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    defer close(ch)
    for i := 1; i <= 10; i++ {
        ch <- i
    }
}

func consumer(ch <-chan int, wg *sync.WaitGroup) {
    defer wg.Done()
    for num := range ch {
        fmt.Printf("Consumed: %d\n", num)
    }
}

func main() {
    ch := make(chan int)
    var wg sync.WaitGroup
    
    wg.Add(2)
    go producer(ch, &wg)
    go consumer(ch, &wg)
    
    wg.Wait()
}
```

#### Alternative 2: Basic Concurrency with Mutex (10 minutes)
**"Create a thread-safe counter that can be incremented by multiple goroutines simultaneously."**

**Expected Solution Structure**:
```go
package main

import (
    "fmt"
    "sync"
)

type SafeCounter struct {
    mu    sync.Mutex
    value int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

func main() {
    counter := &SafeCounter{}
    var wg sync.WaitGroup
    
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }
    
    wg.Wait()
    fmt.Printf("Final count: %d\n", counter.Value())
}
```

### Usage Guidelines for Alternative Questions
- **Use when**: Primary question proves too challenging for the candidate's current level
- **Maintain rigor**: Alternative questions should still assess core competencies
- **Document choice**: Note which alternatives were used in evaluation
- **Time management**: Ensure alternatives fit within allocated time slots
- **Progressive difficulty**: Can use multiple alternatives to find candidate's appropriate level

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

### System Design & Architecture (15 points)
- **Excellent (14-15)**: Clear caching strategy with trade-off considerations
- **Good (11-13)**: Good caching understanding with minor oversights
- **Fair (6-10)**: Basic caching knowledge but lacks depth
- **Poor (0-5)**: Cannot design effective caching strategies

### Complex Coding Challenge (25 points)
- **Excellent (22-25)**: Clean, concurrent solution with proper error handling
- **Good (17-21)**: Working solution with good Go practices
- **Fair (10-16)**: Solution works but has concurrency or design issues
- **Poor (0-9)**: Cannot implement concurrent solution

### Discussion & Communication (5 points)
- **Excellent (5)**: Clear communication, thoughtful questions, good production experience
- **Good (4)**: Good communication with some production experience
- **Fair (2-3)**: Basic communication, limited production experience
- **Poor (0-1)**: Poor communication or no relevant experience

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
- [ ] Prepare SQL query environment or whiteboard
- [ ] Have system design whiteboard or digital tool ready
- [ ] Review recent Go best practices and patterns

### During Interview
- [ ] Start with advanced concepts to gauge depth
- [ ] Allow thinking time for design questions
- [ ] Focus on reasoning and trade-offs, not just correct answers
- [ ] Observe problem-solving approach and code organization
- [ ] Keep strict time limits to maintain 60-minute schedule

### Red Flags
- Cannot explain Go concurrency fundamentals
- Unable to design basic database schemas
- Cannot write intermediate-level SQL queries
- No understanding of caching strategies
- Cannot implement concurrent solutions
- Doesn't consider error handling or edge cases
- Shows no experience with production Go applications

### Green Flags
- Demonstrates deep Go knowledge and best practices
- Designs well-normalized database schemas
- Writes efficient SQL queries with proper joins and aggregations
- Understands caching strategies and trade-offs
- Implements clean, concurrent solutions
- Considers error handling, testing, and maintainability
- Shows experience with production systems
- Asks thoughtful questions about requirements

**Reference**: See [golang/intermediate.md](../golang/intermediate.md) for detailed answers to conceptual questions and [golang/coding.md](../golang/coding.md) for more complex coding examples.

This streamlined format provides a comprehensive assessment for intermediate Go developers within a 60-minute timeframe while maintaining focus on all essential skill areas. 