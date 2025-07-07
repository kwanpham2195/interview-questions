# Senior Go Developer Interview Format

## Interview Overview
**Duration**: 90 minutes  
**Format**: Technical interview focusing on advanced Go mastery, system architecture, leadership, and complex problem-solving  
**Target Level**: Senior developers (5+ years Go experience, 3+ years team leadership or architecture experience)

## Interview Structure

### Part 1: Advanced Go Mastery (15 minutes)
**Objective**: Assess expert-level understanding of Go internals, performance optimization, and advanced patterns

### Part 2: Database Architecture & Performance (10 minutes)
**Objective**: Assess database performance optimization and data architecture decisions

### Part 3: Leadership & Technical Decision Making (15 minutes)
**Objective**: Evaluate technical leadership, mentoring capabilities, and decision-making processes

### Part 4: Complex System Design Challenge (25 minutes)
**Objective**: Test comprehensive system design including scalability, concurrency, and architectural thinking for real-world high-traffic systems

### Part 5: Discussion & Questions (5 minutes)
**Objective**: Clarify responses and allow candidate questions

---

## Part 1: Advanced Go Mastery (15 minutes)

### Question 1: Go Scheduler & Memory Model (6-8 minutes)
**"Explain Go's M:N threading model (Goroutines:OS Threads) and how the scheduler achieves efficient multiplexing. Then describe the Go Memory Model's 'happens-before' relationships - provide an example where concurrent code might exhibit a data race even if it appears to work correctly."**

**Expected Senior-Level Answer Points**:
- **G-M-P model**: Goroutines (G), Machines/OS threads (M), Processors (P)
- **Work-stealing scheduler**: Load balancing across processors
- **Preemption handling**: Modern Go's preemptive scheduling for CPU-bound goroutines
- **Syscall handling**: Thread detachment for blocking operations
- **Memory Model**: Happens-before relationships for memory visibility
- **Data Race Example**: Concurrent access without synchronization primitives

**Follow-up**: "How would you optimize a Go application experiencing high GC pressure?"

**Reference**: Direct reuse from [golang/hard.md - Questions 1 & 2](../golang/hard.md#1-describe-the-go-schedulers-mn-threading-model-goroutinesos-threads-how-does-it-achieve-efficient-multiplexing-discuss-specific-scenarios-where-goroutine-starvation-or-scheduling-delays-might-occur-and-how-the-scheduler-attempts-to-mitigate-them-eg-preemption-syscall-handling)

---

### Question 2: Advanced Concurrency Patterns (5-6 minutes)
**"Design a robust worker pool that handles backpressure, graceful shutdown, and dynamic scaling. How would you prevent potential deadlocks or live-locks in complex channel operations?"**

**Expected Senior-Level Answer Points**:
- **Worker pool architecture**: Job queues, worker management, context cancellation
- **Backpressure strategies**: Bounded channels, load shedding
- **Graceful shutdown**: Context propagation, channel closing patterns
- **Deadlock prevention**: Understanding channel communication patterns
- **Dynamic scaling**: Load-based worker adjustment

**Expected Code Structure**:
```go
type WorkerPool struct {
    workers    int
    jobQueue   chan Job
    workerPool chan chan Job
    quit       chan bool
    ctx        context.Context
}
```

**Follow-up**: "Provide an example of how `select` statements can lead to deadlock."

**Reference**: Enhanced from [golang/intermediate.md - Question 3](../golang/intermediate.md#3-differentiate-between-unbuffered-and-buffered-channels) with content from [golang/hard.md - Question 3](../golang/hard.md#3-how-can-a-select-statement-with-multiple-channel-operations-lead-to-a-deadlock-or-live-lock-if-not-handled-carefully-provide-an-example)

---

### Question 3: Performance Debugging (3-4 minutes)
**"You have a Go service with high CPU usage and significant GC pauses. Walk me through your systematic approach to diagnose and resolve these issues using pprof."**

**Expected Senior-Level Answer Points**:
- **CPU Profile**: Identifying hotspots, inefficient algorithms, synchronization overhead
- **Heap Profile**: Memory allocation patterns, allocation rates, leak detection  
- **Goroutine Profile**: Goroutine count, blocked goroutines, leak patterns
- **Optimization strategies**: Object pooling, allocation reduction, algorithm improvements
- **Verification**: Re-profiling to confirm improvements

**Follow-up**: "What specific anti-patterns would you look for in heap profiles?"

**Reference**: Direct reuse from [golang/hard.md - Question 4](../golang/hard.md#4-you-have-a-go-service-that-is-experiencing-high-cpu-usage-and-significant-garbage-collection-pauses-describe-your-methodical-approach-to-diagnose-and-resolve-these-issues-what-specific-profiles-would-you-examine-and-what-common-patterns-or-anti-patterns-would-you-look-for-in-each)

---

### Question 4: Error Handling Strategy (5-6 minutes)
**"Design a comprehensive error handling strategy for a microservice making multiple downstream calls. How would you propagate rich, structured error information while remaining idiomatic to Go?"**

**Expected Senior-Level Answer Points**:
- **Error wrapping**: `fmt.Errorf` with `%w` for context preservation
- **Custom error types**: Structured errors with codes, messages, trace IDs
- **Programmatic inspection**: `errors.Is` and `errors.As` usage
- **Context propagation**: Using `context.Context` for trace IDs
- **Logging strategy**: Appropriate error logging at different layers
- **User-friendly messaging**: Separating internal vs external error details

**Follow-up**: "How would you handle retry logic and circuit breaker patterns?"

**Reference**: Direct reuse from [golang/hard.md - Question 5](../golang/hard.md#5-you-are-building-a-complex-microservice-that-makes-multiple-downstream-calls-design-an-error-handling-strategy-that-propagates-rich-structured-error-information-eg-original-error-error-codes-user-friendly-messages-trace-ids-back-to-the-caller-while-adhering-to-gos-idiomatic-error-handling)

---

### Question 5: Debugging Goroutine Leaks (3-4 minutes)
**"Describe your systematic approach to identify and debug goroutine leaks in a production service beyond just monitoring `runtime.NumGoroutine()`."**

**Expected Senior-Level Answer Points**:
- **Profiling strategy**: Using `pprof` goroutine profiles, differential analysis
- **Leak patterns**: Blocked channels, unreleased mutexes, context leaks
- **Analysis techniques**: Comparing profiles over time, identifying stuck goroutines
- **Prevention strategies**: Proper context usage, clear goroutine lifecycles
- **Code inspection**: Common leak patterns in worker pools, request handlers

**Follow-up**: "What patterns in `pprof` output indicate specific types of leaks?"

**Reference**: Direct reuse from [golang/hard.md - Question 6](../golang/hard.md#6-you-suspect-a-goroutine-leak-in-a-long-running-go-service-beyond-just-looking-at-runtimenumgoroutine-describe-a-systematic-approach-to-identify-and-debug-the-source-of-the-leak-what-specific-output-or-other-runtime-metrics-would-you-consult-and-what-patterns-would-indicate-a-leak)

---

## Part 2: Database Architecture & Performance (10 minutes)

### Question 6: Database Performance Optimization (10 minutes)
**"Your production database has degrading performance. Walk me through your systematic approach to identifying and resolving bottlenecks."**

**Expected Senior-Level Answer Points**:
- **Monitoring setup**: Query performance metrics, slow query logs
- **Analysis techniques**: EXPLAIN plans, index usage analysis
- **Optimization strategies**: Index tuning, query rewriting, schema adjustments
- **Configuration tuning**: Connection pools, memory allocation, timeouts
- **Caching strategies**: Query result caching, cache invalidation patterns
- **Migration strategies**: Zero-downtime deployments, rollback procedures

**Follow-up**: "How would you handle a zero-downtime database migration?"

**Reference**: Enhanced from [sql/query.md](../sql/query.md) and [sql/design.md](../sql/design.md)

---

## Part 3: Leadership & Technical Decision Making (15 minutes)

### Question 7: Technical Leadership Scenario (7-8 minutes)
**"You're leading a team of 5 developers on a critical project. Two senior developers disagree on the technical approach - one wants a new Go framework, the other prefers the proven solution. How do you handle this?"**

**Expected Senior-Level Answer Points**:
- **Decision framework**: Risk vs benefit analysis, technical debt considerations
- **Stakeholder management**: Balancing team opinions with business requirements  
- **Evaluation criteria**: Performance, maintainability, team expertise, timeline
- **Conflict resolution**: Facilitating technical discussions, building consensus
- **Documentation**: Decision records, knowledge sharing processes
- **Fallback strategies**: Proof of concepts, incremental adoption

**Follow-up**: "How do you balance technical excellence with delivery pressure?"

---

### Question 8: Mentoring & Knowledge Transfer (7-8 minutes)
**"A junior developer is struggling with Go concurrency and introducing production bugs. How would you approach mentoring them while maintaining code quality?"**

**Expected Senior-Level Answer Points**:
- **Assessment**: Understanding specific knowledge gaps and learning style
- **Structured learning**: Pairing sessions, progressive complexity, hands-on practice
- **Code review process**: Educational feedback, pattern recognition training
- **Safety measures**: Staging environments, gradual responsibility increase
- **Knowledge sharing**: Documentation, team learning sessions, best practices
- **Performance tracking**: Clear goals, regular feedback, improvement metrics

**Follow-up**: "How do you prevent knowledge silos in your team?"

---

## Part 4: Complex System Design Challenge (25 minutes)

### Question 9: Comprehensive Ticket Booking System Design (25 minutes)
**"Design a ticket booking system like Ticketmaster that handles high-traffic events (millions of concurrent users), prevents overselling, manages seat selection, and processes payments. Focus on the core architecture and Go-specific implementation considerations."**

**Expected Senior-Level Design Components**:

#### High-Level Architecture & Scalability (8-10 minutes)
- **Microservices breakdown**: Event service, inventory service, booking service, payment service, user service, notification service
- **API Gateway**: Rate limiting, authentication, DDoS protection, request routing, traffic shaping
- **Load balancing strategies**: Session affinity, health checks, auto-scaling, geographic distribution
- **Caching layers**: Multi-level caching (CDN, Redis clusters, application-level caching)
- **Event-driven architecture**: Booking events, inventory updates, payment processing, notification delivery
- **Service mesh**: Inter-service communication, circuit breakers, timeout management, bulkheads
- **Observability**: Monitoring, distributed tracing, alerting, real-time dashboards
- **Resilience patterns**: Circuit breakers, retry policies, graceful degradation, chaos engineering

#### Inventory & Concurrency Management (10-12 minutes)
- **Seat reservation**: Temporary holds, expiration timers, atomic operations
- **Optimistic vs Pessimistic locking**: Database-level concurrency control strategies
- **Inventory sharding**: Event-based partitioning, hot partition handling
- **Queue systems**: Virtual queues for high-demand events, fair queuing algorithms
- **Cache coherency**: Inventory caching, cache invalidation, eventual consistency

#### Data Architecture & Consistency (8-10 minutes)
- **Database scaling**: Read replicas, sharding strategies, CQRS pattern implementation
- **ACID compliance**: Payment transactions, inventory updates, booking confirmations
- **Database sharding**: Event-based sharding, cross-shard transactions, hot partition handling
- **Read replicas**: Search queries, analytics, reporting without affecting bookings
- **Event sourcing**: Audit trails, booking history, state reconstruction, replay capabilities
- **Data consistency**: Strong consistency for payments, eventual consistency for analytics
- **Cache coherency**: Database-cache synchronization, cache invalidation strategies

**Guided Interview Questions**:

**Architecture & Scalability Design (8-10 minutes)**:
- "Walk me through your overall system architecture. What are the key services and how do they interact?"
- "How would you handle a flash sale scenario where 1 million users hit the system simultaneously?"
- "What's your strategy for geographic distribution and global scalability?"
- "How do you ensure the system remains responsive during peak traffic?"
- "Describe your load balancing strategy. How would you handle a sudden 10x traffic spike?"
- "What caching layers would you implement and how do you ensure cache coherency?"
- "How would you design the system to gracefully degrade under extreme load?"

**Inventory Management & Concurrency (10-12 minutes)**:
- "How would you prevent overselling when 100,000 users try to book the last 10 tickets?"
- "Explain your seat reservation strategy. How long do you hold seats and why?"
- "What's the difference between optimistic and pessimistic locking in this context? When would you use each?"
- "How would you handle inventory updates across multiple database shards?"
- "Describe your approach to implementing a virtual queue system for high-demand events."
- "What happens when a user's session expires while they have seats on hold?"

**Data Consistency & Transactions (8-10 minutes)**:
- "How do you ensure ACID compliance across your booking and payment flows?"
- "What's your strategy for handling payment failures and partial bookings?"
- "How would you implement distributed transactions across multiple services?"
- "Describe your approach to eventual consistency vs strong consistency trade-offs."
- "How do you handle data corruption or inconsistency scenarios?"

**Performance & Scalability (Additional probing)**:
- "How would you implement caching without creating cache coherency issues?"
- "What's your database sharding strategy and how do you handle hot partitions?"
- "How do you handle read replicas and potential read-after-write consistency issues?"
- "Describe your approach to auto-scaling during unexpected traffic spikes."

**Edge Cases & Error Handling**:
- "What happens if the payment service is down but inventory has been reserved?"
- "How do you handle users trying to book seats that are no longer available?"
- "What's your strategy for handling duplicate booking requests?"
- "How would you implement refunds and cancellations at scale?"

---

## Scoring Guidelines (100 Points Total)

### Part 1: Advanced Go Mastery (25 points)
- **Exceptional (23-25)**: Expert-level Go internals knowledge with performance insights
- **Strong (18-22)**: Solid advanced Go understanding with good optimization awareness
- **Adequate (13-17)**: Good Go knowledge but limited advanced concepts
- **Weak (0-12)**: Insufficient advanced Go knowledge for senior role

### Part 2: Database Architecture (10 points)
- **Exceptional (9-10)**: Advanced database performance optimization and architecture
- **Strong (7-8)**: Good database optimization with performance awareness
- **Adequate (5-6)**: Basic database optimization skills
- **Weak (0-4)**: Limited database performance knowledge

### Part 3: Leadership & Decision Making (20 points)
- **Exceptional (18-20)**: Strong leadership with clear decision frameworks
- **Strong (14-17)**: Good leadership understanding with examples
- **Adequate (10-13)**: Basic leadership awareness
- **Weak (0-9)**: Limited leadership experience

### Part 4: System Design (20 points)
- **Exceptional (18-20)**: Comprehensive system design with detailed Go-specific implementation
- **Strong (14-17)**: Good system design with solid architectural components
- **Adequate (10-13)**: Basic system design with some implementation details
- **Weak (0-9)**: Limited system design capability

## Evaluation Criteria

### Green Flags (Hire Indicators)
- **Deep Technical Knowledge**: Expert Go understanding with performance optimization experience
- **Architectural Maturity**: Comprehensive system design with scalability considerations
- **Leadership Evidence**: Concrete examples of technical leadership and mentoring
- **Production Experience**: Real-world scaling and debugging experience
- **Communication Skills**: Clear explanation of complex technical concepts
- **Decision-Making**: Systematic approach to technical choices with trade-off analysis

### Red Flags (Concerns)
- **Shallow Knowledge**: Cannot explain advanced Go concepts or performance considerations
- **Limited Leadership**: No concrete examples of team leadership or mentoring
- **Poor Architecture**: Cannot design scalable systems or discuss trade-offs
- **Communication Issues**: Cannot explain technical decisions clearly
- **No Production Experience**: Lacks real-world system scaling experience

## Minimum Passing Score
- **Total Score**: 75/100 points
- **Must score at least 18/25 in Advanced Go Mastery**
- **Must score at least 18/25 in System Architecture**  
- **Must score at least 14/20 in Leadership & Decision Making**
- **Must score at least 14/20 in System Design**

## Interviewer Notes

### Preparation Checklist
- [ ] Review candidate's leadership experience and team size managed
- [ ] Prepare system design whiteboard/digital tools
- [ ] Have Go performance profiling examples ready
- [ ] Review candidate's production system experience
- [ ] Prepare follow-up questions based on candidate background

### Time Management
- **Strict 90-minute format**: Each section has firm time boundaries
- **Flexibility within sections**: Can adjust individual question timing based on candidate responses
- **Quality over quantity**: Better to go deep on fewer topics than surface-level on many
- **Leave buffer time**: Save last 5 minutes for clarification and candidate questions

### Alternative Questions (If Needed)
Choose based on candidate background and time constraints:

#### Alternative Go Questions
- **Memory Debugging**: "Debug a memory leak using pprof step-by-step"
- **Build Optimization**: "Structure a large Go monorepo with multiple services"
- **Testing Strategy**: "Design integration testing for a microservices architecture"

#### Alternative Architecture Questions  
- **Event Sourcing**: "When would you choose event sourcing over traditional CRUD?"
- **API Versioning**: "Design a backward-compatible API versioning strategy"
- **Observability**: "Design monitoring and alerting for distributed systems"

This streamlined 90-minute format maximizes the value of questions from `hard.md` while maintaining comprehensive senior-level assessment across all critical areas. 