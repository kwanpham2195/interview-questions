
### 1\. **Challenge: Goroutines and Channels for Fan-Out/Fan-In Pattern**

**Specific Question:**
Write a Go program that demonstrates a fan-out/fan-in concurrency pattern.

1. **Fan-Out:** Create a `generator` goroutine that sends numbers from 1 to 10 to a channel.
2. **Worker Pool:** Create three `worker` goroutines that each read numbers from the `generator` channel, double them, and send the doubled result to a `results` channel.
3. **Fan-In:** The `main` goroutine should read all results from the `results` channel and print them.
    Ensure proper synchronization using `sync.WaitGroup` to wait for all workers to finish and to close channels at the right time.

**Go Feature Focus:** Goroutines, Buffered Channels, `for...range` over channels, `sync.WaitGroup`, Fan-Out/Fan-In pattern.

**Solution:**

```go
package main

import (
 "fmt"
 "sync"
 "time"
)

// generator sends numbers from start to end to the numbers channel
func generator(start, end int, numbers chan<- int, wg *sync.WaitGroup) {
 defer wg.Done()
 fmt.Println("Generator started...")
 for i := start; i <= end; i++ {
  numbers <- i
  time.Sleep(50 * time.Millisecond) // Simulate some work
 }
 fmt.Println("Generator finished.")
}

// worker reads from the input channel, doubles the number, and sends to the output channel
func worker(id int, numbers <-chan int, results chan<- int, wg *sync.WaitGroup) {
 defer wg.Done()
 fmt.Printf("Worker %d started...\n", id)
 for n := range numbers {
  doubled := n * 2
  results <- doubled
  fmt.Printf("Worker %d processed %d -> %d\n", id, n, doubled)
  time.Sleep(100 * time.Millisecond) // Simulate work
 }
 fmt.Printf("Worker %d finished.\n", id)
}

func main() {
 const numWorkers = 3
 const totalNumbers = 10

 numbers := make(chan int, totalNumbers) // Buffered channel for generated numbers
 results := make(chan int, totalNumbers) // Buffered channel for results

 var wg sync.WaitGroup // WaitGroup to manage goroutines

 // 1. Start the generator goroutine
 wg.Add(1)
 go generator(1, totalNumbers, numbers, &wg)

 // Wait for the generator to finish (so we know numbers channel can be closed)
 go func() {
  wg.Wait()      // Wait only for the generator here
  close(numbers) // Close the numbers channel once all numbers are sent
 }()

 // 2. Start worker goroutines
 var workerWG sync.WaitGroup // Separate WaitGroup for workers
 workerWG.Add(numWorkers)
 for i := 1; i <= numWorkers; i++ {
  go worker(i, numbers, results, &workerWG)
 }

 // Wait for all workers to finish processing all numbers
 go func() {
  workerWG.Wait()  // Wait for all workers to finish
  close(results)   // Close the results channel once all results are sent
 }()

 // 3. Collect and print results (Fan-In)
 fmt.Println("\nCollecting results:")
 for r := range results {
  fmt.Printf("Collected result: %d\n", r)
 }

 fmt.Println("\nAll operations completed.")
}
```

-----

### 2\. **Challenge: Custom Error Types with `fmt.Errorf` and Error Wrapping**

**Specific Question:**
Create a Go function `processPayment(amount float64)` that simulates a payment process.

1. Define a custom error type `InsufficientFundsError` that includes the `RequestedAmount` and `AvailableBalance` as fields. This type should implement the `error` interface.
2. Inside `processPayment`, if `amount` is greater than a simulated `accountBalance` (e.g., 100.0), return an `InsufficientFundsError`.
3. Also, simulate a generic "payment gateway error" which wraps an underlying simple error (e.g., `errors.New("network issue")`) using `fmt.Errorf("%w", ...)` if `amount` is negative.
4. In `main`, call `processPayment` with different amounts and use `errors.Is` and `errors.As` to specifically handle `InsufficientFundsError` and check for the wrapped error type.

**Go Feature Focus:** Custom error types, `error` interface implementation, `fmt.Errorf("%w", err)`, `errors.Is`, `errors.As`.

**Solution:**

```go
package main

import (
 "errors"
 "fmt"
)

// InsufficientFundsError is a custom error type for insufficient funds.
type InsufficientFundsError struct {
 RequestedAmount  float64
 AvailableBalance float64
}

// Error implements the error interface for InsufficientFundsError.
func (e *InsufficientFundsError) Error() string {
 return fmt.Sprintf("insufficient funds: requested %.2f, available %.2f",
  e.RequestedAmount, e.AvailableBalance)
}

// processPayment simulates a payment transaction.
func processPayment(amount float64) error {
 const accountBalance = 100.0 // Simulated available balance

 if amount < 0 {
  // Simulate a wrapped error from an underlying issue
  gatewayErr := errors.New("payment gateway: connection lost")
  return fmt.Errorf("payment failed due to invalid amount: %w", gatewayErr)
 }

 if amount > accountBalance {
  return &InsufficientFundsError{
   RequestedAmount:  amount,
   AvailableBalance: accountBalance,
  }
 }

 fmt.Printf("Payment of %.2f processed successfully.\n", amount)
 return nil
}

func main() {
 // Test Case 1: Successful payment
 fmt.Println("--- Test Case 1: Successful Payment ---")
 err := processPayment(50.0)
 if err != nil {
  fmt.Printf("Error during payment: %v\n", err)
 }
 fmt.Println()

 // Test Case 2: Insufficient Funds
 fmt.Println("--- Test Case 2: Insufficient Funds ---")
 err = processPayment(150.0)
 if err != nil {
  fmt.Printf("Error during payment: %v\n", err)
  var ife *InsufficientFundsError // Declare a variable of the custom error type
  if errors.As(err, &ife) {        // Use errors.As to check if the error is of a specific type
   fmt.Printf("Specific Error: Insufficient Funds! You need %.2f more.\n", ife.RequestedAmount-ife.AvailableBalance)
  }
 }
 fmt.Println()

 // Test Case 3: Negative Amount (wrapped error)
 fmt.Println("--- Test Case 3: Negative Amount (Wrapped Error) ---")
 err = processPayment(-10.0)
 if err != nil {
  fmt.Printf("Error during payment: %v\n", err)
  // Check if a specific underlying error exists using errors.Is
  if errors.Is(err, errors.New("payment gateway: connection lost")) {
   fmt.Println("Specific Error: Underlying payment gateway connection issue.")
  }
 }
 fmt.Println()
}
```

-----

### 3\. **Challenge: Context for Timeout in a Goroutine**

**Specific Question:**
Create a Go program where a goroutine simulates a task that might take a long time (e.g., 5 seconds). The `main` function should start this goroutine but also use a `context.WithTimeout` of 2 seconds. If the task doesn't complete within the timeout, the `main` function should cancel it and print a timeout message. Otherwise, it should print that the task completed.

**Go Feature Focus:** `context.WithTimeout`, `select` with `<-ctx.Done()`, cancelling goroutines.

**Solution:**

```go
package main

import (
 "context"
 "fmt"
 "time"
)

// longRunningTask simulates a task that takes 'duration' to complete.
// It listens to the context's Done channel for cancellation.
func longRunningTask(ctx context.Context, duration time.Duration, resultChan chan<- string) {
 fmt.Println("Long running task started...")
 select {
 case <-time.After(duration): // Task completes after 'duration'
  resultChan <- "Task completed successfully!"
 case <-ctx.Done(): // Context was cancelled (e.g., due to timeout)
  resultChan <- "Task cancelled due to timeout!"
 }
 fmt.Println("Long running task finished.")
}

func main() {
 fmt.Println("Starting main program...")

 // Create a context with a timeout of 2 seconds
 ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
 defer cancel() // Ensure cancel is called to release context resources

 resultChan := make(chan string, 1) // Buffered channel to receive task result

 // Start the long running task in a goroutine (simulating 5 seconds of work)
 go longRunningTask(ctx, 5*time.Second, resultChan)

 // Wait for either the task to complete or the context to timeout
 select {
 case res := <-resultChan:
  fmt.Printf("Main received: %s\n", res)
 case <-ctx.Done():
  // This case executes if the context's deadline is exceeded
  // or if cancel() is called directly.
  fmt.Printf("Main detected: %s\n", ctx.Err()) // ctx.Err() tells why it was cancelled
 }

 fmt.Println("Main program finished.")
 // Give a moment for goroutines to print their messages if they haven't yet
 time.Sleep(100 * time.Millisecond)
}
```

-----

### 4\. **Challenge: Type Assertions and Type Switches on Interfaces**

**Specific Question:**
Define an interface `Animal` with a method `Speak() string`. Create two structs, `Dog` (with a `Breed` field) and `Cat` (with a `Color` field), both implementing `Animal`.
Create a slice of `Animal` interfaces. Populate it with instances of `Dog` and `Cat`.
Iterate through the slice and use a **type switch** to determine the concrete type of each `Animal`. For `Dog`, print its `Breed` and `Speak()` message. For `Cat`, print its `Color` and `Speak()` message. If an unknown type appears, print a generic message.

**Go Feature Focus:** Interfaces, Type assertions (`value, ok := interface{}.(Type)`), Type switches (`switch v := i.(type)`).

**Solution:**

```go
package main

import "fmt"

// Animal interface with a Speak method
type Animal interface {
 Speak() string
}

// Dog struct
type Dog struct {
 Name  string
 Breed string
}

// Speak method for Dog
func (d Dog) Speak() string {
 return "Woof!"
}

// Cat struct
type Cat struct {
 Name  string
 Color string
}

// Speak method for Cat
func (c Cat) Speak() string {
 return "Meow!"
}

func main() {
 // Create a slice of Animal interface types
 animals := []Animal{
  Dog{Name: "Buddy", Breed: "Golden Retriever"},
  Cat{Name: "Whiskers", Color: "Tabby"},
  Dog{Name: "Lucy", Breed: "Labrador"},
  Cat{Name: "Shadow", Color: "Black"},
  // You could even add a non-Animal here, but it wouldn't fit the interface
  // struct{ Name string }{Name: "Stone"},
 }

 fmt.Println("Processing animals:")
 for _, animal := range animals {
  // Use a type switch to determine the concrete type
  switch v := animal.(type) {
  case Dog:
   // v is now of type Dog
   fmt.Printf("%s is a Dog (Breed: %s). It says: %s\n", v.Name, v.Breed, v.Speak())
  case Cat:
   // v is now of type Cat
   fmt.Printf("%s is a Cat (Color: %s). It says: %s\n", v.Name, v.Color, v.Speak())
  default:
   // This case handles any other type that implements Animal but isn't Dog or Cat
   // Or if something unexpected got into the slice (though not possible with this setup)
   fmt.Printf("Found an unknown animal type: %T. It says: %s\n", v, v.Speak())
  }
 }

 fmt.Println("\nDemonstrating Type Assertion (single check):")
 // Type assertion for a single instance
 if d, ok := animals[0].(Dog); ok { // Assert that animals[0] is a Dog
  fmt.Printf("First animal is a Dog, its name is %s and breed is %s.\n", d.Name, d.Breed)
 } else {
  fmt.Println("First animal is not a Dog.")
 }
}
```

-----

### 5\. **Challenge: Embedding Methods from Embedded Structs**

**Specific Question:**
Define a struct `Engine` with a field `Horsepower` (int) and a method `Start() string`.
Define a struct `Car` that embeds `Engine` and also has a `Model` (string) field.
Create an instance of `Car`. Demonstrate that you can directly call the `Start()` method on the `Car` instance, even though `Start()` is defined on `Engine`. Print the `Model` and the result of `Start()`.

**Go Feature Focus:** Struct embedding, method promotion.

**Solution:**

```go
package main

import "fmt"

// Engine struct defines an engine with horsepower and a Start method.
type Engine struct {
 Horsepower int
}

// Start method for the Engine.
func (e Engine) Start() string {
 return fmt.Sprintf("Engine with %d HP starting...", e.Horsepower)
}

// Car struct embeds Engine and adds a Model field.
type Car struct {
 Engine // Embedded field (anonymous field)
 Model  string
}

func main() {
 // Create an instance of Car
 myCar := Car{
  Engine: Engine{
   Horsepower: 300,
  },
  Model: "GoGo V8",
 }

 fmt.Printf("Car Model: %s\n", myCar.Model)

 // Call the Start method directly on the Car instance.
 // This works because the Engine's Start method is "promoted" to the Car.
 fmt.Println(myCar.Start())

 // You can also access the embedded struct and its method explicitly:
 fmt.Println(myCar.Engine.Start()) // This is equivalent
}
```

-----

### 6\. **Challenge: Mutex for Concurrency Safety**

**Specific Question:**
Write a Go program where multiple goroutines (e.g., 5 goroutines) concurrently increment a shared integer counter 1000 times each. Without any synchronization, this will lead to a race condition. Implement `sync.Mutex` to protect the shared counter and ensure that the final count is accurate (i.e., `num_goroutines * increments_per_goroutine`).

**Go Feature Focus:** `sync.Mutex`, `Lock()`, `Unlock()`, Race Conditions.

**Solution:**

```go
package main

import (
 "fmt"
 "sync"
 "time"
)

// SafeCounter holds a counter and a mutex to protect it.
type SafeCounter struct {
 mu    sync.Mutex
 count int
}

// Inc increments the counter safely.
func (c *SafeCounter) Inc() {
 c.mu.Lock()   // Acquire the lock
 c.count++     // Increment the counter
 c.mu.Unlock() // Release the lock
}

// Value returns the current value of the counter safely.
func (c *SafeCounter) Value() int {
 c.mu.Lock()
 defer c.mu.Unlock() // Use defer to ensure unlock always happens
 return c.count
}

func main() {
 counter := SafeCounter{}
 const numGoroutines = 5
 const incrementsPerGoroutine = 1000

 var wg sync.WaitGroup
 wg.Add(numGoroutines)

 fmt.Printf("Starting %d goroutines, each incrementing the counter %d times.\n",
  numGoroutines, incrementsPerGoroutine)

 for i := 0; i < numGoroutines; i++ {
  go func() {
   defer wg.Done()
   for j := 0; j < incrementsPerGoroutine; j++ {
    counter.Inc()
    // Simulate some work to make race condition more apparent without mutex
    // time.Sleep(1 * time.Microsecond)
   }
  }()
 }

 wg.Wait() // Wait for all goroutines to finish

 expectedCount := numGoroutines * incrementsPerGoroutine
 finalCount := counter.Value()

 fmt.Printf("Expected final count: %d\n", expectedCount)
 fmt.Printf("Actual final count: %d\n", finalCount)

 if finalCount == expectedCount {
  fmt.Println("Result is accurate. Mutex prevented race condition.")
 } else {
  fmt.Println("Race condition detected! Final count is incorrect.")
 }

 // Uncomment the block below to demonstrate a race condition WITHOUT a mutex
 /*
 fmt.Println("\n--- Demonstrating Race Condition WITHOUT Mutex ---")
 unprotectedCount := 0
 var unprotectedWG sync.WaitGroup
 unprotectedWG.Add(numGoroutines)

 for i := 0; i < numGoroutines; i++ {
  go func() {
   defer unprotectedWG.Done()
   for j := 0; j < incrementsPerGoroutine; j++ {
    unprotectedCount++
   }
  }()
 }
 unprotectedWG.Wait()
 fmt.Printf("Unprotected final count (will likely be incorrect): %d\n", unprotectedCount)
 */
}
```

-----

### 7\. **Challenge: Using `iota` for Enums**

**Specific Question:**
Define a custom type `Weekday` and use `iota` to declare constants for the days of the week (Monday, Tuesday, ..., Sunday), starting with Monday as 1.
Create a function `isWeekend(day Weekday) bool` that checks if a given `Weekday` is a weekend day (Saturday or Sunday).
In `main`, test `isWeekend` with various days and print the results.

**Go Feature Focus:** `const`, `iota`, `type` for custom types, defining enums.

**Solution:**

```go
package main

import "fmt"

// Weekday is a custom type for days of the week.
type Weekday int

// Define constants for days of the week using iota.
const (
 Monday Weekday = iota + 1 // iota starts at 0, so +1 makes Monday = 1
 Tuesday
 Wednesday
 Thursday
 Friday
 Saturday
 Sunday
)

// String method makes Weekday values print nicely.
func (d Weekday) String() string {
 switch d {
 case Monday:
  return "Monday"
 case Tuesday:
  return "Tuesday"
 case Wednesday:
  return "Wednesday"
 case Thursday:
  return "Thursday"
 case Friday:
  return "Friday"
 case Saturday:
  return "Saturday"
 case Sunday:
  return "Sunday"
 default:
  return fmt.Sprintf("Unknown Day (%d)", d)
 }
}

// isWeekend checks if a given day is a weekend day.
func isWeekend(day Weekday) bool {
 return day == Saturday || day == Sunday
}

func main() {
 fmt.Printf("%s is weekend? %t\n", Monday, isWeekend(Monday))
 fmt.Printf("%s is weekend? %t\n", Friday, isWeekend(Friday))
 fmt.Printf("%s is weekend? %t\n", Saturday, isWeekend(Saturday))
 fmt.Printf("%s is weekend? %t\n", Sunday, isWeekend(Sunday))
 fmt.Printf("Day 8 is weekend? %t\n", isWeekend(Weekday(8))) // Demonstrating an invalid day
}
```

-----

### 8\. **Challenge: Reflection to Inspect a Struct**

**Specific Question:**
Define a struct `User` with fields `Name` (string), `Age` (int), and `Email` (string).
Create an instance of `User`.
Using the `reflect` package, write a function `printStructFields(obj interface{})` that takes any interface (which should ideally be a struct) and iterates over its fields, printing each field's name, type, and value. Handle cases where the input is not a struct.

**Go Feature Focus:** `reflect` package, `reflect.TypeOf`, `reflect.ValueOf`, `NumField`, `Field()`, `Kind()`.

**Solution:**

```go
package main

import (
 "fmt"
 "reflect" // Import the reflect package
)

// User struct
type User struct {
 Name  string
 Age   int
 Email string
 // unexportedField string // This field would not be accessible via reflection for its value
}

// printStructFields inspects the fields of a given struct using reflection.
func printStructFields(obj interface{}) {
 // Get the reflect.Value of the object
 val := reflect.ValueOf(obj)

 // If the object is a pointer, get the element it points to
 if val.Kind() == reflect.Ptr {
  val = val.Elem()
 }

 // Check if it's a struct
 if val.Kind() != reflect.Struct {
  fmt.Printf("Error: Input is not a struct, it's a %s.\n", val.Kind())
  return
 }

 fmt.Printf("Inspecting struct of type: %s\n", val.Type())
 fmt.Println("------------------------------------")

 // Get the reflect.Type of the object
 typ := val.Type()

 // Iterate over the struct's fields
 for i := 0; i < val.NumField(); i++ {
  field := val.Field(i) // Get the Value of the field
  fieldType := typ.Field(i) // Get the StructField (Type information)

  // Check if the field is exportable (first letter is uppercase) to get its value
  // If not exportable, val.Field(i).CanSet() would be false and val.Field(i).Interface() would panic.
  // However, we can still get the type and name.
  if field.CanSet() || fieldType.IsExported() { // Or just check if fieldType.IsExported()
   fmt.Printf("  Field Name: %s\n", fieldType.Name)
   fmt.Printf("  Field Type: %s\n", fieldType.Type)
   fmt.Printf("  Field Value: %v\n", field.Interface()) // Get the actual value
  } else {
   fmt.Printf("  Field Name: %s (unexported)\n", fieldType.Name)
   fmt.Printf("  Field Type: %s\n", fieldType.Type)
   fmt.Println("  Field Value: (not accessible for unexported fields)")
  }
  fmt.Println("------------------------------------")
 }
}

func main() {
 user := User{
  Name:  "Alice",
  Age:   30,
  Email: "alice@example.com",
  // unexportedField: "secret", // Would be ignored by default Marshal/Unmarshal
 }

 printStructFields(user)

 fmt.Println("\n--- Testing with a pointer to a struct ---")
 printStructFields(&user) // Also works with pointers

 fmt.Println("\n--- Testing with a non-struct type ---")
 printStructFields("hello world")
 printStructFields(123)
}
```

-----

### 9\. **Challenge: Custom `String()` Method for Structs (`fmt.Stringer`)**

**Specific Question:**
Define a struct `Book` with fields `Title` (string), `Author` (string), and `Year` (int).
Implement the `String()` method for the `Book` struct. This method should return a formatted string like `"Title: <Title>, Author: <Author> (Year: <Year>)"`.
In `main`, create an instance of `Book` and print it using `fmt.Println()`. Observe how `fmt.Println` automatically uses your custom `String()` method.

**Go Feature Focus:** `fmt.Stringer` interface, custom `String()` method, default `fmt.Print` behavior.

**Solution:**

```go
package main

import "fmt"

// Book struct represents a book.
type Book struct {
 Title  string
 Author string
 Year   int
}

// String implements the fmt.Stringer interface for the Book type.
// This method is automatically called when a Book object is printed
// using functions like fmt.Print, fmt.Println, fmt.Printf with %v, etc.
func (b Book) String() string {
 return fmt.Sprintf("Title: %s, Author: %s (Year: %d)", b.Title, b.Author, b.Year)
}

func main() {
 // Create an instance of Book
 myBook := Book{
  Title:  "The Hitchhiker's Guide to the Galaxy",
  Author: "Douglas Adams",
  Year:   1979,
 }

 anotherBook := Book{
  Title:  "The Go Programming Language",
  Author: "Alan A. A. Donovan & Brian W. Kernighan",
  Year:   2015,
 }

 fmt.Println("Printing books using fmt.Println():")
 fmt.Println(myBook)         // fmt.Println automatically calls myBook.String()
 fmt.Println(anotherBook)

 fmt.Println("\nPrinting using fmt.Printf with %v:")
 fmt.Printf("My favorite book: %v\n", myBook) // %v also uses the String() method

 fmt.Println("\nPrinting using fmt.Printf with %+v (shows field names):")
 fmt.Printf("Book details: %+v\n", myBook) // %+v will ignore String() and print fields explicitly
}
```

-----

### 10\. **Challenge: Time and Duration Operations**

**Specific Question:**
Write a Go program that demonstrates common operations with the `time` package:

1. Get and print the current time.
2. Parse a duration string (e.g., "2h30m") into a `time.Duration` and print it.
3. Calculate a future time by adding this duration to the current time and print it.
4. Calculate the duration between two specific `time.Time` values (e.g., now and a predefined past time).
5. Format a `time.Time` value into a specific string format (e.g., "YYYY-MM-DD HH:MM:SS").

**Go Feature Focus:** `time` package, `time.Now()`, `time.ParseDuration()`, `time.Parse()`, `Add()`, `Sub()`, `Format()`, `time.Duration`.

**Solution:**

```go
package main

import (
 "fmt"
 "time"
)

func main() {
 // 1. Get and print the current time
 currentTime := time.Now()
 fmt.Printf("1. Current time: %s\n", currentTime)
 fmt.Printf("   Current time (RFC3339): %s\n", currentTime.Format(time.RFC3339))

 // 2. Parse a duration string
 durationStr := "2h30m15s"
 parsedDuration, err := time.ParseDuration(durationStr)
 if err != nil {
  fmt.Printf("Error parsing duration: %v\n", err)
  return
 }
 fmt.Printf("\n2. Parsed duration '%s': %s\n", durationStr, parsedDuration)
 fmt.Printf("   Parsed duration in seconds: %.0f seconds\n", parsedDuration.Seconds())

 // 3. Calculate a future time by adding the duration
 futureTime := currentTime.Add(parsedDuration)
 fmt.Printf("\n3. Current time + %s: %s\n", parsedDuration, futureTime)

 // 4. Calculate the duration between two specific time.Time values
 // Define a past time (e.g., a specific date and time)
 // Go's Parse function uses a reference time (Jan 2 15:04:05 MST 2006) for layout.
 // You need to match the format of your string to the layout.
 pastTimeString := "2024-01-01 10:00:00"
 layout := "2006-01-02 15:04:05" // Reference time for parsing
 pastTime, err := time.Parse(layout, pastTimeString)
 if err != nil {
  fmt.Printf("Error parsing past time: %v\n", err)
  return
 }

 durationSincePast := currentTime.Sub(pastTime)
 fmt.Printf("\n4. Time now: %s\n", currentTime.Format(layout))
 fmt.Printf("   Past time: %s\n", pastTime.Format(layout))
 fmt.Printf("   Duration since past time: %s\n", durationSincePast)
 fmt.Printf("   Duration in hours: %.2f hours\n", durationSincePast.Hours())

 // 5. Format a time.Time value into a specific string format
 customFormattedTime := currentTime.Format("2006-01-02 15:04:05 MST") // Example: YYYY-MM-DD HH:MM:SS TZ
 fmt.Printf("\n5. Current time formatted as 'YYYY-MM-DD HH:MM:SS MST': %s\n", customFormattedTime)

 // Another common format: "Monday, Jan 2 2006"
 anotherCustomFormat := currentTime.Format("Monday, Jan 2 2006")
 fmt.Printf("   Current time formatted as 'DayOfWeek, Month Day Year': %s\n", anotherCustomFormat)
}
```
