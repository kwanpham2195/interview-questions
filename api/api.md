# API Design Interview Questions

Here are 10 interview questions related to API designs, along with their answers, drawing on the provided sources:

### 1. Explain the difference between OAuth 2.0 and OpenID Connect (OIDC).

- **OAuth 2.0**: This is an **authorization framework** that enables an application to obtain limited access to a user's resources hosted by another server, **without** the user sharing their credentials with the client application. Its primary purpose is to allow a user to delegate specific access rights to a client. OAuth 2.0 uses **Access Tokens** to represent these delegated permissions.
- **OpenID Connect (OIDC)**: This is an **identity layer built directly on top of OAuth 2.0**. Its main function is to provide a standardized way for clients to **verify the identity of end-users** based on authentication performed by an Authorization Server, and to obtain basic user profile information in an interoperable manner. OIDC introduces the **ID Token**, which is a core artifact containing verifiable assertions (claims) about the authenticated user and the authentication event itself. While OAuth 2.0 focuses on *authorization* (what an application can do), OIDC focuses on *authentication* (who the user is).

### 2. Describe the typical flow for user authentication using OpenID Connect.

The OpenID Connect protocol, in abstract, follows these steps for user authentication and information retrieval:

1. **User Initiates Sign-in**: An end user navigates to a website or web application via a browser and clicks a sign-in button, often typing their username and password.
2. **Relying Party (Client) Sends Request**: The application (known as the Relying Party or RP) sends an authentication request to the OpenID Provider (OP). This typically involves redirecting the user's browser to the OP's authorization endpoint with specific parameters like `scope=openid`.
3. **OP Authenticates User**: The OpenID Provider (acting as the Authorization Server) authenticates the user and obtains their authorization for the requested information. This may involve showing a consent screen to the user.
4. **OP Responds with Tokens**: Upon successful authentication and authorization, the OP responds by redirecting the user back to the RP with an **Identity Token (ID Token)** and typically an **Access Token**. The ID Token contains claims (e.g., `iss`, `sub`, `aud`, `exp`) about the end-user and the authentication event.
5. **RP Requests User Information (Optional)**: The Relying Party can then use the Access Token to make a request to the OP's **UserInfo Endpoint**.
6. **UserInfo Endpoint Returns Claims**: The UserInfo Endpoint returns additional claims (user profile information) about the end-user, as consented to by the user.

### 3. What are JSON Web Tokens (JWTs), and how are they used in modern API authentication/authorization?

- **Definition**: A **JSON Web Token (JWT)** is an **open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information** between parties as a JSON object. The information within a JWT can be **verified and trusted because it is digitally signed**. JWTs can be signed using a secret (e.g., HMAC algorithm) or a public/private key pair (e.g., RSA or ECDSA).
- **Structure**: A JWT consists of three parts, separated by dots: a **header**, a **payload**, and a **signature**.
  - The **header** typically specifies the signing algorithm (e.g., HS256) and the token's type (JWT).
  - The **payload** contains "claims," which are statements about an entity (e.g., a user) and additional data. Claims can be registered (predefined), public (user-defined but registered to avoid collisions), or private (custom, agreed-upon by parties).
  - The **signature** is created by signing the encoded header and payload with a secret or private key, enabling verification of the token's integrity.
- **Usage in APIs**:
  - **Identity Representation**: JWTs are commonly used to represent **digital identity information**, such as OpenID Connect ID Tokens, conveying user identity to client applications.
  - **Access Tokens**: They are often used as **OAuth 2.0 access tokens**, which clients use to make secure calls to API servers on behalf of a user. The self-contained nature of JWTs allows the resource server to **validate the token's signature directly** without needing to query a central session store, making JWT authentication **stateless, faster, and more scalable**.
  - **Stateless Authentication**: Because JWTs carry all necessary information, the server doesn't need to maintain session state, which is particularly beneficial for distributed systems like microservices.
  - **Security Considerations**: While self-contained, it's crucial **not to put secret information directly within the token's payload**, as the information is exposed to users or other parties, even though it cannot be changed once signed.

### 4. Compare and contrast session-based authentication with JWT authentication, including their advantages and disadvantages, and when to use each.

### Session-Based Authentication
- **Mechanism**: Relies on the **server to maintain a record of the user's authentication state**. When a user logs in, the server creates a unique session record, stores it (e.g., in a database), and sends a unique **SessionID (typically in a cookie)** to the client. For subsequent requests, the client sends the SessionID, which the server validates against its stored session data.
- **Advantages**:
  - **Simple and reliable** due to centralized server control over authentication state.
  - Enables **real-time revocation** by simply deleting or invalidating the session record on the server.
- **Disadvantages**:
  - Can introduce **latency and high resource consumption** in distributed systems, as every request requires a server-side lookup or syncing across multiple servers.
  - **Security risk** of session hijacking if session cookies are stolen.
  - **Less suitable for mobile apps and APIs** due to challenges in managing cookies across devices and increased server load.
- **When to Use**: Best for **applications requiring real-time session control** (e.g., banking) and **single-server or small-scale systems** without significant scalability needs.

### JWT (JSON Web Token) Authentication
- **Mechanism**: Embeds all relevant user information directly into a **stateless token**. After successful authentication, the server generates a JWT (comprising a header, payload, and signature) and sends it to the client for storage (e.g., in `localStorage` or `sessionStorage`). Subsequent API requests include the JWT in the `Authorization` header, and the **server verifies the token's signature and claims without needing to query a central session store**.
- **Advantages**:
  - **Fast and scalable** due to statelessness and client-side validation, eliminating server-side session lookups.
  - **Enhanced security** through digital signing and optional encryption.
  - Ideal for **Single Sign-On (SSO)** and **cross-domain authentication**, allowing users to access multiple services with the same token.
  - **Mobile-friendly** as tokens can be stored on the device and sent with each API request, improving efficiency.
  - Well-suited for **microservices architectures**, where each service can independently validate tokens without a central session store.
- **Disadvantages**:
  - **Statelessness complicates real-time revocation** (e.g., user sign-out, password changes) before the token expires, often requiring strategies like short expiration times, token blacklists, or specific revocation endpoints.
  - Requires careful handling of token storage on the client side to prevent compromise.
- **When to Use**: Recommended for **applications prioritizing scalability, efficiency, and distributed systems**, such as SPAs, mobile applications, microservices, and RESTful APIs that need cross-domain authentication.

### 5. What is a Refresh Token in the context of OAuth 2.0/OpenID Connect, and why is it important for security and user experience?

A **Refresh Token** is a **credential artifact that enables a client application to obtain new access tokens (and optionally new ID tokens) without requiring the user to re-authenticate or log in again**. It is typically issued by the authorization server during the initial authorization flow, especially when the client requests "offline access" (by setting the `access_type` parameter to `'offline'`).

### Importance for Security
- **Enables Short-Lived Access Tokens**: For security best practices, **access tokens are often designed to have a short lifespan** (e.g., 15 minutes, hours, or days). This minimizes the impact if an access token is compromised, as an attacker would only have a limited window to use it.
- **Reduces Exposure of Sensitive Credentials**: Instead of the client application needing to store and reuse the user's actual username and password for repeated authentication, the refresh token acts as a more secure, long-lived credential for silently obtaining new access tokens. This keeps the user's primary login credentials private and reduces the risk of credential-based data breaches.

### Importance for User Experience
- **Seamless User Experience**: By allowing the client to silently "refresh" expired access tokens in the background, refresh tokens **prevent the user from having to frequently log in again**. This provides a much smoother and more convenient user experience, which can help reduce website abandonment rates.
- **Offline Access**: For applications that need to perform actions or access resources when the user is not actively present (e.g., background data synchronization, scheduled tasks), refresh tokens are essential. They allow the application to maintain access to APIs without continuous user interaction.

While refresh tokens offer great benefits, they are powerful and often long-lived, so they **must be stored securely** by the client application, typically in a persistent database on the server-side for web applications, or encrypted storage for native apps. Security companies like Auth0 implement mechanisms such as **Refresh Token Rotation** to further enhance their security.

### 6. Explain gRPC and its key advantages over traditional RESTful APIs for inter-process communication, particularly in microservices architectures.

### gRPC Definition
**gRPC** (gRPC Remote Procedure Calls) is a **modern, open-source inter-process communication (IPC) technology** that enables distributed and heterogeneous applications to communicate by invoking procedures (methods/functions) on remote servers as easily as making a local function call. It is built upon **HTTP/2** as its transport protocol and uses **Protocol Buffers** as its Interface Definition Language (IDL) and efficient message serialization format.

### Key Advantages Over RESTful APIs for Microservices

#### Efficiency
- **Binary Protocol (HTTP/2)**: gRPC utilizes **HTTP/2**, which is a fully multiplexed binary transport protocol. This means it can send multiple requests and responses in parallel over a single TCP connection, reducing overhead and improving latency and throughput compared to HTTP/1.x, which REST often uses.
- **Efficient Serialization (Protocol Buffers)**: gRPC uses **Protocol Buffers** to define service interfaces and serialize structured data. This results in **smaller, binary payloads** that are faster to serialize/deserialize than text-based formats like JSON or XML commonly used in REST, making it highly efficient for service-to-service communication.

#### Strongly Typed Contracts
gRPC enforces a **contract-first development approach** through Protocol Buffers, providing clear and **strongly typed service definitions**. This generates client-side stubs and server-side skeletons in various programming languages, ensuring **strict adherence to API contracts** and reducing runtime errors and interoperability issues often associated with REST APIs, where schema definitions might be an afterthought.

#### Polyglot Support
gRPC is designed to be **language-agnostic**. A single Protocol Buffer service definition can be used to generate code for clients and servers in numerous programming languages (e.g., Go, Java, Python, C++), allowing different microservices to be built with optimal technologies while seamlessly interoperating.

#### Advanced Communication Patterns
Beyond the simple unary (request-response) RPC, gRPC natively supports **server-streaming, client-streaming, and bidirectional-streaming RPCs**. This enables more complex, real-time data flows, which are often challenging or less efficient to implement with traditional REST architectures.

#### Built-in Features (Batteries Included)
gRPC provides **built-in support for common cross-cutting concerns** vital in distributed systems, such as authentication, encryption (TLS), request deadlines/timeouts, metadata exchange, compression, load balancing, and service discovery. This reduces the boilerplate code developers need to write.

In microservices architectures, gRPC is **most commonly used for internal service-to-service communication**, where its performance, strong typing, and built-in features offer significant advantages. For external-facing APIs, REST or GraphQL might still be used, often with a **gRPC Gateway** or HTTP/JSON transcoding to translate requests.

### 7. How do you handle API versioning in a RESTful service, especially considering backward compatibility and client workloads?

In designing RESTful services, especially within the Microsoft Azure guidelines, API versioning is crucial to ensure both backward compatibility for existing client workloads and the ability to introduce new features.

### Version Identification
The primary method for clients to specify the API version is by including a **required query parameter named `api-version` on every operation**.

### Version Format
- Versions are typically represented as **`YYYY-MM-DD` date values**.
- For **preview versions**, a `-preview` suffix is appended (e.g., `2024-03-17-preview`).
- Each new preview or general availability (GA) version **MUST use a later date** than its predecessors.

### Handling Missing/Unsupported Versions
- If a client omits the `api-version` parameter, the service **MUST return HTTP `400-Bad Request`** with a "MissingApiVersionParameter" error code.
- If a client provides an unrecognized `api-version` value, the service **MUST return HTTP `400-Bad Request`** with an "UnsupportedApiVersionValue" error code and list the currently supported stable and latest preview API versions.

### Backward Compatibility and Breaking Changes
- A core principle is that **already-running customer workloads MUST NOT break** due to service changes, and customers should be able to adopt new versions without code changes for existing features.
- The guidelines strongly advise **DO NOT introduce any breaking changes** to an existing API version. If a breaking change is unavoidable (e.g., for security/compliance and approved by the Azure Breaking Change Reviewers), it must be communicated with ample notice and a lengthy deprecation period.
- **Version numbers should NOT be included as part of the URL path** to avoid rigid coupling and allow for easier evolution.
- Changes like removing values from enumeration lists or returning polymorphic type properties not defined for the requested API version are considered breaking changes and **MUST NOT be done**.

### Deprecation Notification
When a breaking change is approved and implemented, the deprecated API version **DOES include an `azure-deprecating` response header**. This header contains a semicolon-delimited string informing the client about the deprecation, its timeline, and a URL to more detailed information, guiding users to update their calls. This header is primarily informational for humans, not for client-side parsing.

### 8. Explain the concept of idempotency in API design and how it's achieved, especially for POST requests.

### Idempotency Definition
In API design, **idempotency means that an operation can be executed multiple times without causing different results or side effects** beyond the first execution. It's a critical concept for **building fault-tolerant applications**, as it allows clients to safely retry requests without fear of unintended consequences, even if they don't receive an initial response. The goal is to achieve an "exactly once" semantic for operations.

### Inherently Idempotent HTTP Methods
- **GET**: Retrieving data multiple times yields the same result.
- **PUT**: Used for creating or replacing a *whole* resource. Applying the same PUT request multiple times will result in the resource being in the same state (either created or entirely replaced to the specified state).
- **PATCH**: Used for applying *partial* modifications to a resource. Repeated PATCH requests for the same modification will result in the resource reaching the same final state.
- **DELETE**: Removing a resource. Repeated DELETE requests for the same resource will result in the resource being removed (or remaining removed), leaving the system in a consistent state.

### Making POST Requests Idempotent
- **POST** operations, typically used for creating new resources where the ID is generated by the service, or for invoking actions, are **NOT inherently idempotent**. Repeated POSTs without specific handling could create duplicate resources or trigger an action multiple times.
- To achieve idempotency for POST requests, services **SHOULD support specific HTTP headers defined by standards like OASIS Repeatable Requests**:
  - **`Repeatability-Request-ID`**: The client includes a **unique, client-generated identifier** for the request in this header (e.g., a GUID). The server uses this ID to identify and track individual requests.
  - **`Repeatability-First-Sent`**: The client includes a **timestamp** indicating when the request was first sent. This helps the server manage a time window (e.g., at least 5 minutes) during which it will remember the request and its outcome.
- **Server-Side Handling**: If a server receives a POST request with these headers and finds that a request with the same `Repeatability-Request-ID` was successfully processed within the defined time window, it will **return the original response without re-processing the operation**, thus ensuring idempotency.
- If an API operation does not support these repeatability headers, it **should return a `501 Not Implemented` response** if such headers are present in the request.

### 9. Describe different types of API streaming patterns supported by gRPC, providing a use case for each.

gRPC provides native, first-class support for various communication patterns, offering more flexibility than traditional HTTP/REST for handling continuous data flows.

### 1. Simple RPC (Unary RPC)
- **Description**: This is the most fundamental gRPC communication pattern. The **client sends a single request message to the server, and the server responds with a single response message**. This is similar to a traditional request-response model in HTTP.
- **Use Case**: A `getProduct(ProductID)` operation in an e-commerce service, where the client sends one product ID, and the server returns the details of that single product.

### 2. Server-Streaming RPC
- **Description**: The **client sends a single request message, but the server responds with a stream of messages**. After the initial request, the server can continuously push multiple messages back to the client. The connection remains open until the server decides to close it or there are no more messages to send.
- **Use Case**: A `searchOrders(searchTerm)` function. The client sends a single search query, and the server streams back all matching orders as they are found, rather than sending a single, potentially large, response once all results are aggregated. This is useful for large datasets or real-time updates.

### 3. Client-Streaming RPC
- **Description**: The **client sends a stream of messages to the server, and the server responds with a single response message** once it has processed all (or a sufficient part of) the client's incoming stream.
- **Use Case**: An `updateOrders(stream Order)` operation for a bulk update. A client can stream multiple order updates to the server (e.g., as changes happen), and the server processes them, finally sending a single confirmation or summary status once all updates are received or a specific condition is met.

### 4. Bidirectional-Streaming RPC
- **Description**: Both the **client and the server send independent streams of messages to each other simultaneously**. After the client initiates the call, both sides can read from and write to their respective streams independently. The communication continues until both sides decide to close their streams.
- **Use Case**: A `processOrders(stream Order) returns (stream CombinedShipment)` for real-time order processing. The client continuously streams new orders for processing, and the server simultaneously streams back combined shipment details as orders are grouped and ready for dispatch. This is ideal for real-time, interactive scenarios like chat applications or live data synchronization.

### 10. Discuss essential security considerations for designing and implementing APIs, drawing from OWASP and other sources.

Designing and implementing secure APIs is paramount due to their role as system entry points, making them prime targets for attacks. Key security considerations include:

### Authentication and Authorization
- **Verifying Identity and Controlling Access**: APIs must authenticate who is making a request and authorize what they are allowed to do.
- **Token-Based Authentication**: Modern APIs largely rely on token-based mechanisms like **OAuth 2.0** for access delegation and **JSON Web Tokens (JWTs)** for identity and access tokens. JWTs are self-contained, allowing resource servers to validate them by signature without constant communication with an authentication server.
- **OpenID Connect (OIDC)**: Builds on OAuth 2.0 by adding a standardized identity layer, providing verifiable assertions about user identity.
- **Token Security**: It is crucial **not to put sensitive or secret information directly into JWT payloads** as they are exposed to the client. Tokens should have **short expiration times** to minimize the impact of compromise, often coupled with Refresh Tokens for seamless re-authentication. Refresh Tokens themselves must be stored securely.
- **OWASP Top 10 API Security Risks**: "API2:2023 Broken Authentication" highlights the critical importance of robust authentication mechanisms.

### Secure Communication Channels (Encryption)
- **TLS/SSL Encryption**: All API communication **MUST be encrypted using Transport Layer Security (TLS)** (e.g., `HTTPS` for REST, `WSS` for WebSockets, or TLS for gRPC) to ensure privacy, data integrity, and prevent eavesdropping or tampering.
- **Mutual TLS (mTLS)**: For enhanced security, especially in internal service-to-service communication, **mTLS can be implemented where both the client and server authenticate each other** using cryptographic certificates.

### Input Validation and Error Handling
- **Comprehensive Input Validation**: **All input data, including query parameters, request headers, and JSON body fields, MUST be rigorously validated** to prevent improperly formed requests, injection attacks (e.g., SQL, LDAP, SSRF), and unexpected behavior. Invalid inputs should result in a `400-Bad Request` response with clear error details.
- **Structured Error Responses**: API error responses should be informative yet not leak sensitive data. They should include **standard HTTP status codes** and custom, descriptive error codes (e.g., `x-ms-error-code`) to help clients diagnose and self-recover from issues. OWASP's "API8:2023 Security Misconfiguration" implicitly covers proper error handling and logging configurations.

### Idempotency and Retry Mechanisms
- **Designing Idempotent Operations**: All API operations, especially those that modify state (like `POST` requests), **MUST be designed to be idempotent**. This means repeated identical requests should produce the same outcome as the first. For `POST` requests, this is often achieved by clients providing unique `Repeatability-Request-ID` and `Repeatability-First-Sent` headers that servers use to de-duplicate requests within a time window. Idempotency is crucial for building robust, fault-tolerant applications in distributed environments.

### Protection Against Specific Attacks
- **Cross-Site Request Forgery (CSRF)**: For OAuth flows, the **`state` parameter should be used** to maintain state between the authorization request and response, verifying that the response correlates to the original request and preventing CSRF attacks.
- **Server-Side Request Forgery (SSRF)**: When handling URLs from client-controlled data (e.g., in JWT claims like `jku` or `x5u`), APIs must implement safeguards like **whitelisting allowed domains** and ensuring no sensitive cookies are sent, to prevent the server from being coerced into making unauthorized internal requests.
- **Sensitive Data Exposure**: **Sensitive fields (e.g., passwords) should NEVER be returned in `GET` responses**. Careful consideration of data exposure, even in error messages or logging, is vital.

### API Design Best Practices for Security
- **Minimize Data Sent**: Services should **NOT send JSON fields with `null` values**; instead, omit them to reduce payload size and potential information leakage.
- **Version Management**: While not directly a security control, a well-managed API versioning strategy (e.g., using `api-version` query parameters and clear deprecation policies) helps ensure that clients are using up-to-date, secure versions of the API and prevents the lingering use of potentially vulnerable older versions.
- **Least Privilege**: APIs should be designed to request and grant only the necessary permissions (scopes) for an operation, leveraging incremental authorization when possible.