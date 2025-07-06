# REST API Interview Questions

## 1. What is REST and what are its core architectural principles?

REST (Representational State Transfer) is an architectural style that employs standard conventions and protocols, emphasizing scalability, generality, independent deployment, reduced latency through caching, and security. It defines a service's resources as collections of items. 

### Key principles and characteristics include:

- **Resource**: Everything in REST is a resource, identified by URIs (typically URLs), with a type, associated data, relationships, and methods that operate on it.
- **CRUD Operations**: REST services often map directly to Create, Read, Update, and Delete operations on resources.
- **HTTP Methods**: Standard HTTP methods like GET, POST, PUT, PATCH, and DELETE are used.
- **Status Codes**: Standard HTTP status codes indicate the success or failure of an API request.
- **Stateless**: Each client request to the server must contain all necessary information for processing, and the server should not store any client state between requests.
- **Client-Server**: The client manages the user interface, while the server handles requests, business logic, and data storage.
- **Cacheable**: Server responses can be cached by the client if indicated by the server.
- **Layered System**: Clients interact with the system without needing to know if they are connected directly to the end server or an intermediary, which can improve scalability.
- **HATEOAS (Hypermedia As The Engine Of Application State)**: Clients interact and navigate through the application entirely based on hypermedia provided dynamically by the server.

## 2. Explain the common HTTP methods (GET, POST, PUT, PATCH, DELETE) in the context of RESTful API design

### GET
- **Purpose**: Used to retrieve a resource or list a collection of resources
- **Expected Response**: 200-OK for successful retrieval
- **Special Cases**: 304-Not Modified if conditional GET request's If-None-Match ETag matches

### POST
- **Purpose**: Used to create a new resource (where the ID is typically set by the service) or to perform an action on a resource or collection
- **Expected Response**: 
  - 201-Created for resource creation (along with the URL of the newly created resource)
  - 200-OK for actions (ideally with a response body, even if empty)
  - 202-Accepted if initiating a long-running operation

### PUT
- **Purpose**: Used to create or entirely replace a resource
- **Expected Response**: 
  - 200-OK for replacement
  - 201-Created for creation
  - 202-Accepted if initiating a long-running operation

### PATCH
- **Purpose**: Used to partially modify an existing resource, typically using a JSON Merge Patch
- **Expected Response**: 200-OK or 201-Created
- **Note**: PATCH operations should not be implemented as long-running operations

### DELETE
- **Purpose**: Used to remove a resource
- **Expected Response**: 
  - 204-No Content (response body should be empty)
  - 202-Accepted if initiating a long-running operation
- **Note**: Should return 204 even if the resource doesn't exist (avoid 404-Not Found)

## 3. What does "statelessness" mean in the context of RESTful APIs?

In REST, statelessness dictates that each request from a client to a server must be self-contained, meaning it includes all necessary information for the server to understand and process it. The server should not store any client-specific context or session state between requests. HTTP is inherently stateless. 

### Why is statelessness important?

- **Scalability**: Any server can handle any request, as there's no dependency on previous interactions, enabling easy horizontal scaling
- **Reliability**: If a server fails, other servers can seamlessly pick up requests without losing session data
- **Simplicity**: It simplifies server design by eliminating the need for complex session management mechanisms

## 4. How should RESTful APIs handle errors?

RESTful APIs should leverage standard HTTP status codes to convey the outcome of an operation.

### Success Codes
- **200-OK**: General success
- **201-Created**: Resource successfully created
- **202-Accepted**: Request accepted for asynchronous processing (e.g., Long-Running Operations)
- **204-No Content**: Successful DELETE operation, no content in response body
- **304-Not Modified**: Conditional GET when the resource has not changed

### Client Error Codes (4xx)
- **400-Bad Request**: For improperly formed requests, invalid query parameters, unrecognized JSON fields, or attempting to set read-only fields. Also returned if the api-version parameter is missing or unsupported
- **401-Unauthorized**: Authentication required or failed
- **403-Forbidden**: User does not have access, unless this leaks sensitive information about resource existence, in which case 404-Not Found is preferred
- **404-Not Found**: Resource not found
- **405-Method Not Allowed**: HTTP method not supported for the resource
- **409-Conflict**: If a create-only field doesn't match an existing value, or an Operation-Id matches an existing operation that is not a retry scenario
- **412-Precondition Failed**: For conditional requests where the precondition (e.g., If-Match) is not met
- **414-URI Too Long**: If a URL exceeds 2083 characters

### Server Error Codes (5xx)
- **500-Internal Server Error**: General server-side issue
- **501-Not Implemented**: If the service does not support a feature, e.g., repeatability headers

### Error Response Structure
- **x-ms-error-code header**: Services must return this response header with a unique string error code. These codes are part of the API contract and should not change for the same conditions in future versions
- **Response Body**: A response body should be provided with an error object containing an ErrorDetail. The code field within the ErrorDetail must be identical to the x-ms-error-code header's value. The ErrorDetail can include message, target, and details fields, and may also include additional properties for diagnostic data

## 5. JSON Best Practices for REST APIs

### Field Naming Conventions
- **DO use camel case** for all JSON field names (e.g., `firstName` instead of `first_name` or `first-name`)
- **DO treat JSON field names with case-sensitivity**
- **DO treat JSON field values with case-sensitivity**, with rare exceptions
- **DO treat JSON field values representing unique IDs** (like UUIDs, CUIDs) as opaque string values and compare them case-sensitively

### Handling Null Values
- **DO NOT send JSON fields with a null value** from the service to the client; instead, omit the field entirely to reduce payload size
- **DO accept JSON fields with a null value only for PATCH operations** using a JSON Merge Patch payload. In this context, a null value instructs the service to delete the field
- If the field cannot be deleted, return 400-Bad Request

### General JSON Practices
- **DO make fields simple and maintain a shallow hierarchy**
- **DO use RFC 3339 for date/time values**
- **DO ensure that information exchanged is "round-trippable"** across multiple programming languages
- **YOU SHOULD use JSON objects instead of arrays** whenever possible, as arrays can be difficult and inefficient with JSON Merge Patch

## 6. API Versioning in REST

Azure REST API guidelines emphasize that services change over time, requiring consistent versioning to avoid breaking customer workloads and allow for new feature adoption without mandatory code changes.

### Required api-version Query Parameter
- Clients must specify the API version using a required query parameter named `api-version` on every request

### Date-Based Versioning
- The recommended format for api-version values is **YYYY-MM-DD**
- Preview versions use a `-preview` suffix (e.g., `2021-06-04-preview`)
- A GA (General Availability) version must have a date later than its corresponding preview version
- Preview features should either go GA or be removed within one year of introduction

### Error Handling for Versioning
- If the `api-version` query parameter is omitted, the service must return HTTP 400 with the error code "MissingApiVersionParameter"
- If an unrecognized `api-version` value is provided, the service must return HTTP 400 with the error code "UnsupportedApiVersionValue", listing supported stable and the latest public preview versions

### Extensible Enums for Evolution
- For string fields with a predefined set of values (enums) that might grow over time, extensible enumerations (marked with `modelAsString: true` in OpenAPI/Swagger) should be used
- This signals to clients that new, undocumented values may be returned in the future
- Removing values from an enumeration list is considered a breaking change

### Breaking Changes
- Any API changes, especially breaking changes, must be reviewed by the Azure API Stewardship Board
- New top-level error codes should not be added to an existing API version without bumping the service version

## 7. Idempotency in REST

Idempotency in REST means that making the same request multiple times has the same effect as making it once. In cloud applications, where failures are embraced, idempotency is crucial for enabling customers to write fault-tolerant applications.

### Why Idempotency is Important
- Allows clients to safely retry requests (e.g., due to network issues or timeouts) without risking unintended consequences
- Provides an "exactly once" semantic for operations

### Idempotent HTTP Methods
- **PUT and PATCH**: These methods are inherently idempotent. When used for creating or replacing resources, they are simpler to implement idempotently, and allow the client to specify the resource's ID

### Making POST Idempotent
- **POST** is not inherently idempotent when used to create a resource or perform an action
- Services may use POST for resource creation or actions if they ensure it behaves idempotently
- This can be achieved by supporting the `Repeatability-Request-ID` (a unique request identifier) and `Repeatability-First-Sent` (the timestamp of the first request attempt) headers
- If these headers are supported, the service should process subsequent identical requests within a tracked time window (at least 5 minutes) as retries of the original
- If an operation does not support these headers but receives them, it should return a 501 (Not Implemented) response

## 8. Security Considerations for RESTful APIs

Securing APIs is critical. Here are key considerations relevant to RESTful APIs:

### Authentication and Authorization
- **Use Authorization headers** with Bearer tokens (e.g., from Azure Active Directory, OAuth 2.0, or JWT) to identify the caller and grant access to protected resources
- **OpenID Connect (OIDC)**, an identity layer on top of OAuth 2.0, is designed to verify user identity and obtain profile information
- For access control, return 403-Forbidden if a user lacks access, but return 404-Not Found if 403 would reveal sensitive information about resource existence

### Data Protection
- **Always use HTTPS** (https://) for communication to ensure data encryption with SSL/TLS
- **JWTs are digitally signed** for verification and trust. However, they should not contain sensitive information as the content is exposed
- **Access Tokens should have short lifespans** to minimize risk if compromised
- **Refresh Tokens** should employ strategies like "Refresh Token Rotation" for enhanced security
- **Securely store client secrets** and refresh tokens in locations only accessible by your application

### Input Validation and CSRF Mitigation
- **DO validate all query parameters, request headers, and JSON field values**, returning 400-Bad Request if invalid
- In OAuth 2.0 flows, the **state parameter should be used** to maintain state between the authorization request and response, mitigating Cross-Site Request Forgery (CSRF) attacks

### Handling Unrecognized Data
- **DO NOT reject requests containing unrecognized headers**, as they might be added by API gateways or middleware
- **DO NOT use "x-" prefixes** for custom headers unless they are already in production

### OWASP API Security
- "Broken Authentication" is a top API security risk
- OpenID Connect helps address this by removing the responsibility of managing passwords from developers

## 9. REST vs Other API Architectural Styles

### REST (Representational State Transfer)
**Description**: An architectural style widely used for web services, relying on standard HTTP methods and protocols (HTTP/HTTPS) and supporting formats like XML, JSON, HTML, plain text. It's resource-oriented, mapping operations to CRUD on identified resources.

**Strengths**:
- Easy to understand and implement due to standard conventions
- Good for general web services, mobile applications, Single Page Applications (SPAs), and system integrations

**Limitations**:
- Can be bulky and inefficient for inter-process communication due to text-based protocols
- Lack of strongly typed interfaces, leading to potential runtime errors across polyglot systems
- The architectural style is hard to enforce, leading to many "RESTful" services being merely HTTP services

**When to Choose**: General-purpose web APIs, public-facing APIs with well-defined resource models, simple CRUD operations

### GraphQL
**Description**: A query language for APIs and a runtime for fulfilling those queries, typically over HTTP/HTTPS using JSON. It allows clients to request exactly the data they need in a single request, minimizing over-fetching.

**Strengths**:
- Flexible for frontends (especially mobile, bandwidth-constrained)
- Efficient data fetching
- Capable of aggregating data from multiple microservices
- Suitable for real-time applications
- Enables version-free APIs (by adding new fields without breaking changes)

**When to Choose**: APIs where clients need fine-grained control over data, complex data graphs, mobile backends, or as an aggregation layer for microservices

### gRPC (Google RPC)
**Description**: A modern, open-source Remote Procedure Call (RPC) framework that uses HTTP/2 for transport and Protocol Buffers for defining service interfaces and message types.

**Strengths**:
- Designed for low latency and high throughput
- Excellent for inter-process communication in distributed systems and microservices architectures
- Strong contracts and compile-time checks
- Supports various streaming communication patterns

**Limitations**:
- May not be suitable for external-facing services as external consumers are more familiar with REST/HTTP
- Smaller ecosystem compared to REST/HTTP
- Browser and mobile application support still developing

**When to Choose**: High-performance internal microservice communication, cross-language service integration, real-time applications requiring streaming

## 10. Additional REST API Best Practices

### Resource Naming
- Use nouns for resource names, not verbs
- Use plural nouns for collections (e.g., `/users`, `/orders`)
- Use consistent naming conventions throughout the API

### HTTP Status Code Usage
- Use appropriate status codes that accurately reflect the outcome
- Provide meaningful error messages in response bodies
- Include correlation IDs for debugging

### Pagination
- Implement pagination for large datasets
- Use consistent pagination patterns (limit/offset or cursor-based)
- Include pagination metadata in responses

### Caching
- Implement appropriate caching strategies
- Use ETags for conditional requests
- Set appropriate cache headers

### Rate Limiting
- Implement rate limiting to prevent abuse
- Provide clear rate limit information in headers
- Use appropriate HTTP status codes (429 Too Many Requests)