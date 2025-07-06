# Junior Go Developer Interview Format

## Interview Overview
**Duration**: 60-75 minutes  
**Format**: Technical interview focusing on Go fundamentals, SQL problem-solving, and practical coding  
**Target Level**: Junior developers (0-2 years Go experience)

## Interview Structure

### Part 1: Go Fundamentals (20-25 minutes)
**Objective**: Assess basic Go knowledge and understanding of core concepts

### Part 2: SQL Problem Solving (15-20 minutes)
**Objective**: Evaluate database query skills and logical thinking

### Part 3: Coding Challenge (20-25 minutes)
**Objective**: Test practical programming skills and problem-solving approach

### Part 4: Discussion & Questions (5-10 minutes)
**Objective**: Clarify responses and allow candidate questions

---

## Part 1: Go Fundamentals (20-25 minutes)

### Question 1: Go Basics (5 minutes)
**"What is Go and what are its main features that make it suitable for backend development?"**

**Expected Answer Points**:
- Open-source language developed by Google
- Statically typed with garbage collection
- Built-in concurrency support (goroutines, channels)
- Fast compilation and execution
- Strong standard library
- Simple syntax and explicit error handling

**Follow-up**: "Can you name a few companies or use cases where Go is commonly used?"

**Reference**: See [golang/junior.md - Question 1](../golang/junior.md#1-what-is-go-and-what-are-its-main-features) for detailed answer

---

### Question 2: Data Types - Arrays vs Slices (5 minutes)
**"Explain the difference between arrays and slices in Go. When would you use each?"**

**Expected Answer Points**:
- Arrays: Fixed size, value types, size part of type
- Slices: Dynamic size, reference types, built on arrays
- Slices more commonly used due to flexibility
- Arrays useful for fixed-size data or performance-critical code

**Follow-up**: "What happens when you append to a slice that's at capacity?"

**Reference**: See [golang/junior.md - Question 2](../golang/junior.md#2-explain-the-difference-between-a-slice-and-an-array-in-go) for detailed answer

---

### Question 3: Error Handling (5 minutes)
**"How does Go handle errors? Can you write a simple function that demonstrates Go's error handling pattern?"**

**Expected Answer Points**:
- Multiple return values with error as last return
- Explicit error checking with `if err != nil`
- No exceptions, errors are values
- `fmt.Errorf` for error creation and wrapping

**Expected Code Example**:
```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}
```

**Reference**: See [golang/junior.md - Question 3](../golang/junior.md#3-how-do-you-handle-errors-in-go-provide-an-example) for detailed answer with complete example

---

### Question 4: Concurrency Basics (5-10 minutes)
**"What are goroutines and how do they differ from traditional threads? Can you show a simple example?"**

**Expected Answer Points**:
- Lightweight concurrent functions
- Managed by Go runtime, not OS
- Much cheaper than OS threads
- Communicate via channels
- Use `go` keyword to start

**Expected Code Example**:
```go
func main() {
    go fmt.Println("Hello from goroutine")
    time.Sleep(time.Second) // Wait for goroutine
}
```

**Follow-up**: "What is the purpose of channels in Go?"

**Reference**: See [golang/junior.md - Question 4](../golang/junior.md#4-what-are-goroutines-and-how-do-they-differ-from-threads) for detailed answer with complete example

---

### Alternative Questions (Choose 1-2 based on time and candidate background)

### Question 5A: Interfaces (5 minutes)
**"Explain the concept of interfaces in Go. How are they different from interfaces in other languages?"**

**Expected Answer Points**:
- Interface is a type that specifies method signatures
- Implicit implementation (no `implements` keyword)
- Enables polymorphism and decoupling
- Empty interface `interface{}` or `any` can hold any value

**Reference**: See [golang/junior.md - Question 5](../golang/junior.md#5-explain-the-concept-of-interfaces-in-go-and-provide-an-example) for detailed answer with example

### Question 5B: Defer Statement (5 minutes)
**"What is the purpose of the `defer` statement in Go? Can you provide an example?"**

**Expected Answer Points**:
- Schedules function call to execute before surrounding function returns
- LIFO order for multiple defers
- Commonly used for cleanup (closing files, unlocking mutexes)
- Arguments evaluated when defer is executed

**Reference**: See [golang/junior.md - Question 6](../golang/junior.md#6-what-is-the-purpose-of-the-defer-statement-in-go-provide-an-example) for detailed answer with example

### Question 5C: Pointers (5 minutes)
**"What are pointers in Go and why would you use them?"**

**Expected Answer Points**:
- Variable that stores memory address of another variable
- Used for modifying function arguments
- Efficiency for large data structures
- Can be `nil` to represent empty/zero values

**Reference**: See [golang/junior.md - Question 8](../golang/junior.md#8-what-is-a-pointer-and-why-would-you-use-it) for detailed answer with example

---

## Part 2: SQL Problem Solving (15-20 minutes)

### Database Schema
Present this schema for the SQL questions:

```sql
-- Employees table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    salary DECIMAL(10,2),
    department_id INT,
    hire_date DATE
);

-- Departments table
CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

### SQL Question 1: Basic Query (5 minutes)
**"Write a query to find all employees with a salary greater than 50,000, ordered by salary descending."**

**Expected Answer**:
```sql
SELECT * FROM employees 
WHERE salary > 50000 
ORDER BY salary DESC;
```

**Reference**: Similar to queries in [sql/query.md](../sql/query.md) - basic WHERE and ORDER BY patterns

---

### SQL Question 2: JOIN Operation (5-7 minutes)
**"Write a query to show employee names along with their department names."**

**Expected Answer**:
```sql
SELECT e.name, d.name as department_name
FROM employees e
JOIN departments d ON e.department_id = d.id;
```

**Follow-up**: "What if we want to include employees who don't have a department assigned?"

**Expected Answer**: Use `LEFT JOIN` instead of `JOIN`

**Reference**: See [sql/query.md - Question 5](../sql/query.md#5-list-employees-not-assigned-to-any-project) for LEFT JOIN examples

---

### SQL Question 3: Aggregation (5-8 minutes)
**"Write a query to find the average salary for each department."**

**Expected Answer**:
```sql
SELECT d.name, AVG(e.salary) as avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.id, d.name;
```

**Follow-up**: "How would you find departments with an average salary above 60,000?"

**Expected Answer**: Add `HAVING AVG(e.salary) > 60000`

**Reference**: See [sql/query.md - Question 1](../sql/query.md#1-find-employees-above-department-average-salary) for aggregation examples and [sql/query.md - Question 8](../sql/query.md#8-calculate-the-monthly-salary-bill-for-each-department) for GROUP BY patterns

---

## Part 3: Coding Challenge (20-25 minutes)

### Challenge: Simple String and Slice Operations
**"Let's solve a practical problem step by step."**

### Problem Statement
**"Write a Go function that takes a slice of strings and returns a new slice containing only the strings that are longer than 3 characters, with all strings converted to lowercase. Also, count how many strings were filtered out."**

### Example
```
Input: ["Hello", "Go", "World", "AI", "Programming"]
Output: (["hello", "world", "programming"], 2)
```

### Expected Solution
```go
func filterAndCount(strings []string) ([]string, int) {
    var filtered []string
    filteredOut := 0
    
    for _, s := range strings {
        if len(s) > 3 {
            filtered = append(filtered, strings.ToLower(s))
        } else {
            filteredOut++
        }
    }
    
    return filtered, filteredOut
}
```

**Note**: There's a bug in the above solution - `strings.ToLower(s)` should be `strings.ToLower(s)` from the `strings` package, or better yet, use `strings.ToLower(s)` after importing the `strings` package.

**Corrected Solution**:
```go
import "strings"

func filterAndCount(input []string) ([]string, int) {
    var filtered []string
    filteredOut := 0
    
    for _, s := range input {
        if len(s) > 3 {
            filtered = append(filtered, strings.ToLower(s))
        } else {
            filteredOut++
        }
    }
    
    return filtered, filteredOut
}
```

### Evaluation Criteria
- **Correct Logic**: Properly filters strings by length
- **Go Idioms**: Uses range loop, proper variable naming
- **Error Handling**: Handles empty slice gracefully
- **Code Quality**: Clean, readable code structure

### Follow-up Questions
1. "What would happen if the input slice is nil?"
2. "How would you modify this to handle Unicode characters properly?"
3. "Can you write a simple test for this function?"

### Bonus Challenge (if time permits)
**"Now make the function concurrent - process the strings in parallel using goroutines."**

**Expected Approach**:
- Use goroutines for processing
- Use channels for communication
- Proper synchronization with WaitGroup or channel closing

**Reference**: See [golang/junior-coding-challenges.md](../golang/junior-coding-challenges.md) for complete solution examples and alternative challenges

---

## Part 4: Discussion & Questions (5-10 minutes)

### Wrap-up Questions
1. "What Go packages have you used or are familiar with?"
2. "How do you typically structure a Go project?"
3. "What's your experience with Go's testing framework?"
4. "Do you have any questions about Go, our tech stack, or the role?"

---

## Scoring Guidelines

### Go Fundamentals (40 points)
- **Excellent (35-40)**: Clear understanding of all concepts, good examples
- **Good (25-34)**: Understands most concepts, minor gaps
- **Fair (15-24)**: Basic understanding, some confusion
- **Poor (0-14)**: Limited understanding, major gaps

### SQL Problem Solving (30 points)
- **Excellent (25-30)**: All queries correct, understands JOINs and aggregation
- **Good (20-24)**: Most queries correct, minor syntax issues
- **Fair (10-19)**: Basic queries work, struggles with complex operations
- **Poor (0-9)**: Cannot write basic SQL queries

### Coding Challenge (30 points)
- **Excellent (25-30)**: Clean, correct solution with good Go practices
- **Good (20-24)**: Working solution with minor issues
- **Fair (10-19)**: Solution works but has significant issues
- **Poor (0-9)**: Cannot produce working solution

### Overall Assessment
- **Total Score**: 100 points
- **Passing Score**: 60+ points
- **Strong Candidate**: 80+ points

---

## Interviewer Notes

### Preparation Checklist
- [ ] Review candidate's resume and background
- [ ] Prepare coding environment (shared screen/IDE)
- [ ] Have schema diagram ready for SQL questions
- [ ] Prepare follow-up questions based on candidate's experience

### During Interview
- [ ] Start with easier questions to build confidence
- [ ] Allow thinking time, don't rush
- [ ] Ask for clarification of thought process
- [ ] Note problem-solving approach, not just final answer
- [ ] Be encouraging and supportive

### Red Flags
- Cannot explain basic Go concepts (goroutines, error handling)
- Unable to write simple SQL queries
- Cannot structure basic Go code
- Doesn't ask clarifying questions for coding challenge
- Shows no curiosity about Go or the technology stack

### Green Flags
- Demonstrates understanding of Go idioms
- Asks good clarifying questions
- Shows problem-solving approach
- Admits when unsure but attempts to reason through
- Shows enthusiasm for learning Go

---

## Alternative Questions (For Variety)

### Go Alternatives
- **Interfaces and their implicit implementation**
- **The `defer` statement and its use cases**
- **Go modules and dependency management**
- **Struct embedding vs inheritance**

### SQL Alternatives
- **Finding duplicate records**
- **Date/time queries with hire_date**
- **Subqueries vs JOINs**
- **Basic indexing concepts**

### Coding Alternatives
- **Palindrome checker** - Check if a string reads the same forwards and backwards
- **Simple calculator** - Basic arithmetic operations with error handling
- **Word counter** - Count occurrences of words in a text
- **Number finder** - Find min/max values in a slice
- **String reverser** - Reverse a string using Go idioms
- **Struct methods** - Define a struct with methods for basic operations

**Reference**: See [golang/coding.md](../golang/coding.md) for more complex examples. For junior-specific challenges, see [golang/junior-coding-challenges.md](../golang/junior-coding-challenges.md).

This format provides a comprehensive yet approachable assessment for junior Go developers while maintaining consistency across interviews. 