# Junior Go Developer Coding Challenges

## Overview
These coding challenges are designed specifically for junior Go developers (0-2 years experience). They focus on fundamental Go concepts, basic problem-solving, and proper Go idioms.

**Time Allocation**: 15-25 minutes per challenge  
**Difficulty**: Beginner to easy intermediate  
**Focus**: Go syntax, basic data structures, error handling, and simple algorithms

---

## Challenge 1: String and Slice Operations

### Problem Statement
Write a Go function that takes a slice of strings and returns a new slice containing only the strings that are longer than 3 characters, with all strings converted to lowercase. Also, count how many strings were filtered out.

### Example
```
Input: ["Hello", "Go", "World", "AI", "Programming"]
Output: (["hello", "world", "programming"], 2)
```

### Expected Solution
```go
package main

import (
    "fmt"
    "strings"
)

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

func main() {
    input := []string{"Hello", "Go", "World", "AI", "Programming"}
    result, count := filterAndCount(input)
    fmt.Printf("Filtered: %v, Count filtered out: %d\n", result, count)
}
```

### Evaluation Points
- Correct use of `range` loop
- Proper slice operations with `append`
- String manipulation with `strings.ToLower`
- Multiple return values
- Proper variable naming (Go conventions)

---

## Challenge 2: Palindrome Checker

### Problem Statement
Write a Go function that checks if a given string is a palindrome (reads the same forwards and backwards). The function should ignore case and spaces.

### Example
```
Input: "A man a plan a canal Panama"
Output: true

Input: "race a car"
Output: false
```

### Expected Solution
```go
package main

import (
    "fmt"
    "strings"
)

func isPalindrome(s string) bool {
    // Remove spaces and convert to lowercase
    cleaned := strings.ReplaceAll(strings.ToLower(s), " ", "")
    
    // Check if string reads the same forwards and backwards
    length := len(cleaned)
    for i := 0; i < length/2; i++ {
        if cleaned[i] != cleaned[length-1-i] {
            return false
        }
    }
    return true
}

func main() {
    test1 := "A man a plan a canal Panama"
    test2 := "race a car"
    
    fmt.Printf("'%s' is palindrome: %t\n", test1, isPalindrome(test1))
    fmt.Printf("'%s' is palindrome: %t\n", test2, isPalindrome(test2))
}
```

### Evaluation Points
- String manipulation and cleaning
- Loop logic and indexing
- Boolean return values
- Edge case handling (empty strings, single characters)

---

## Challenge 3: Simple Calculator with Error Handling

### Problem Statement
Create a simple calculator that performs basic arithmetic operations (add, subtract, multiply, divide) with proper error handling for division by zero.

### Example
```
calculate("add", 5, 3) -> (8, nil)
calculate("divide", 10, 0) -> (0, error)
```

### Expected Solution
```go
package main

import (
    "fmt"
    "errors"
)

func calculate(operation string, a, b float64) (float64, error) {
    switch operation {
    case "add":
        return a + b, nil
    case "subtract":
        return a - b, nil
    case "multiply":
        return a * b, nil
    case "divide":
        if b == 0 {
            return 0, errors.New("division by zero")
        }
        return a / b, nil
    default:
        return 0, fmt.Errorf("unknown operation: %s", operation)
    }
}

func main() {
    operations := []struct {
        op string
        a, b float64
    }{
        {"add", 5, 3},
        {"subtract", 10, 4},
        {"multiply", 6, 7},
        {"divide", 15, 3},
        {"divide", 10, 0}, // This should cause an error
    }
    
    for _, op := range operations {
        result, err := calculate(op.op, op.a, op.b)
        if err != nil {
            fmt.Printf("Error: %v\n", err)
        } else {
            fmt.Printf("%.2f %s %.2f = %.2f\n", op.a, op.op, op.b, result)
        }
    }
}
```

### Evaluation Points
- Switch statement usage
- Error handling with custom errors
- `fmt.Errorf` for formatted errors
- Multiple return values (result, error)
- Proper error checking in main function

---

## Challenge 4: Word Counter

### Problem Statement
Write a function that counts the occurrences of each word in a given text string. Return a map where keys are words and values are their counts.

### Example
```
Input: "hello world hello go world"
Output: map[string]int{"hello": 2, "world": 2, "go": 1}
```

### Expected Solution
```go
package main

import (
    "fmt"
    "strings"
)

func countWords(text string) map[string]int {
    wordCount := make(map[string]int)
    
    // Split text into words and convert to lowercase
    words := strings.Fields(strings.ToLower(text))
    
    for _, word := range words {
        wordCount[word]++
    }
    
    return wordCount
}

func main() {
    text := "hello world hello go world"
    result := countWords(text)
    
    fmt.Printf("Word counts: %v\n", result)
    
    // Print in a more readable format
    for word, count := range result {
        fmt.Printf("'%s': %d\n", word, count)
    }
}
```

### Evaluation Points
- Map creation and manipulation
- String splitting with `strings.Fields`
- Range over map
- Map increment pattern (`wordCount[word]++`)

---

## Challenge 5: Number Operations

### Problem Statement
Write a function that takes a slice of integers and returns the minimum, maximum, and sum of all numbers.

### Example
```
Input: []int{3, 1, 4, 1, 5, 9, 2, 6}
Output: (min: 1, max: 9, sum: 31)
```

### Expected Solution
```go
package main

import (
    "fmt"
    "math"
)

func analyzeNumbers(numbers []int) (min, max, sum int, err error) {
    if len(numbers) == 0 {
        return 0, 0, 0, fmt.Errorf("empty slice provided")
    }
    
    min = numbers[0]
    max = numbers[0]
    sum = 0
    
    for _, num := range numbers {
        if num < min {
            min = num
        }
        if num > max {
            max = num
        }
        sum += num
    }
    
    return min, max, sum, nil
}

func main() {
    numbers := []int{3, 1, 4, 1, 5, 9, 2, 6}
    
    min, max, sum, err := analyzeNumbers(numbers)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    fmt.Printf("Numbers: %v\n", numbers)
    fmt.Printf("Min: %d, Max: %d, Sum: %d\n", min, max, sum)
}
```

### Evaluation Points
- Slice iteration and processing
- Multiple return values with named returns
- Error handling for edge cases
- Basic algorithm implementation

---

## Challenge 6: Simple Struct with Methods

### Problem Statement
Create a `Person` struct with fields for name and age. Implement methods to:
1. Get a greeting message
2. Check if the person is an adult (18 or older)
3. Have a birthday (increment age)

### Example
```go
p := Person{Name: "Alice", Age: 17}
fmt.Println(p.Greet())        // "Hello, I'm Alice"
fmt.Println(p.IsAdult())      // false
p.HaveBirthday()
fmt.Println(p.IsAdult())      // true
```

### Expected Solution
```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() string {
    return fmt.Sprintf("Hello, I'm %s", p.Name)
}

func (p Person) IsAdult() bool {
    return p.Age >= 18
}

func (p *Person) HaveBirthday() {
    p.Age++
}

func main() {
    person := Person{Name: "Alice", Age: 17}
    
    fmt.Println(person.Greet())
    fmt.Printf("Is adult: %t\n", person.IsAdult())
    
    person.HaveBirthday()
    fmt.Printf("After birthday - Age: %d, Is adult: %t\n", 
        person.Age, person.IsAdult())
}
```

### Evaluation Points
- Struct definition and initialization
- Method definition with receiver
- Value receiver vs pointer receiver
- Method calls and struct field access

---

## Challenge 7: String Reverser

### Problem Statement
Write a function that reverses a string. Handle Unicode characters properly.

### Example
```
Input: "Hello, 世界"
Output: "界世 ,olleH"
```

### Expected Solution
```go
package main

import (
    "fmt"
)

func reverseString(s string) string {
    runes := []rune(s)
    length := len(runes)
    
    for i := 0; i < length/2; i++ {
        runes[i], runes[length-1-i] = runes[length-1-i], runes[i]
    }
    
    return string(runes)
}

func main() {
    test := "Hello, 世界"
    reversed := reverseString(test)
    
    fmt.Printf("Original: %s\n", test)
    fmt.Printf("Reversed: %s\n", reversed)
}
```

### Evaluation Points
- Understanding of runes vs bytes
- Slice manipulation and swapping
- Unicode handling
- Type conversion (string to []rune and back)

---

## Challenge 8: Simple Goroutine Example

### Problem Statement
Create a program that uses goroutines to print numbers from 1 to 5 concurrently with letters from A to E. Use proper synchronization to wait for all goroutines to complete.

### Expected Solution
```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func printNumbers(wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 1; i <= 5; i++ {
        fmt.Printf("Number: %d\n", i)
        time.Sleep(100 * time.Millisecond)
    }
}

func printLetters(wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 'A'; i <= 'E'; i++ {
        fmt.Printf("Letter: %c\n", i)
        time.Sleep(150 * time.Millisecond)
    }
}

func main() {
    var wg sync.WaitGroup
    
    wg.Add(2)
    go printNumbers(&wg)
    go printLetters(&wg)
    
    wg.Wait()
    fmt.Println("All goroutines completed")
}
```

### Evaluation Points
- Goroutine creation with `go` keyword
- WaitGroup usage for synchronization
- Defer statement for cleanup
- Pointer usage for WaitGroup
- Basic concurrency understanding

---

## Interview Tips for Evaluators

### What to Look For
- **Correct Syntax**: Proper Go syntax and conventions
- **Error Handling**: Appropriate error checking and handling
- **Go Idioms**: Use of range loops, proper variable naming
- **Problem Solving**: Logical approach to breaking down problems
- **Code Organization**: Clean, readable code structure

### Common Mistakes to Watch For
- Forgetting to import required packages
- Incorrect slice/map operations
- Missing error handling
- Confusion between value and pointer receivers
- Not handling edge cases (empty slices, nil values)

### Scoring Guidance
- **Excellent**: Clean, correct solution with proper Go idioms
- **Good**: Working solution with minor issues or suboptimal approach
- **Fair**: Partial solution or significant issues but shows understanding
- **Poor**: Cannot produce working solution or major conceptual errors

These challenges provide a good foundation for evaluating junior Go developers while maintaining consistency across interviews. 