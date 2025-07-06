# SQL Schema Design Questions

Here are a few immediate interview questions related to designing SQL schemas based on real-world use cases, along with their detailed answers. These questions aim to assess your understanding of normalization, data types, primary keys, foreign keys, and handling relationships.

---

### Question 1: Online Course Platform

**Use Case:** You need to design a database for a simplified online course platform.
Here are the core requirements:

* **Users:** Can register, log in, and view courses.
* **Instructors:** Can create and teach multiple courses. Each course has one primary instructor.
* **Courses:** Have a title, description, price, and are taught by one instructor.
* **Lessons:** Each course is made up of multiple lessons, in a specific order. Each lesson has a title and content.
* **Enrollment:** Users can enroll in multiple courses.

**Your Task:** Design the SQL schema (tables, columns, data types, primary keys, foreign keys, and relationships) for this platform.

---

### Answer 1: Online Course Platform

Here's a possible SQL schema design:

```sql
-- Table: Users
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each user
    username VARCHAR(50) UNIQUE NOT NULL, -- User's chosen username (must be unique)
    email VARCHAR(100) UNIQUE NOT NULL, -- User's email address (must be unique)
    password_hash VARCHAR(255) NOT NULL, -- Hashed password for security
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date and time of registration
);

-- Table: Instructors
CREATE TABLE Instructors (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each instructor
    instructor_name VARCHAR(100) NOT NULL, -- Instructor's full name
    bio TEXT, -- A short biography of the instructor
    email VARCHAR(100) UNIQUE NOT NULL -- Instructor's email address (must be unique)
);

-- Table: Courses
CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each course
    instructor_id INT NOT NULL, -- Foreign Key to Instructors table
    course_title VARCHAR(255) NOT NULL, -- Title of the course
    course_description TEXT, -- Detailed description of the course
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Price of the course (e.g., 59.99)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date and time course was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Last updated time

    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)
);

-- Table: Lessons
CREATE TABLE Lessons (
    lesson_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each lesson
    course_id INT NOT NULL, -- Foreign Key to Courses table
    lesson_title VARCHAR(255) NOT NULL, -- Title of the lesson
    lesson_content TEXT, -- Content of the lesson (e.g., text, URL to video)
    lesson_order INT NOT NULL, -- Order of the lesson within the course (e.g., 1, 2, 3)

    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    UNIQUE (course_id, lesson_order) -- Ensures unique order within a course
);

-- Junction Table: Enrollments (Many-to-Many relationship between Users and Courses)
CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each enrollment (optional, but good practice)
    user_id INT NOT NULL, -- Foreign Key to Users table
    course_id INT NOT NULL, -- Foreign Key to Courses table
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date and time of enrollment
    completion_status VARCHAR(20) DEFAULT 'In Progress', -- e.g., 'In Progress', 'Completed'

    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    UNIQUE (user_id, course_id) -- Ensures a user can only enroll in a course once
);
```

**Explanation of Design Choices:**

* **Normalization:** The design follows basic normalization principles (3NF) to reduce data redundancy. For example, `instructor_details` are stored once in `Instructors` and linked to `Courses` via a foreign key.
* **Primary Keys:** Each table has an `INT` `AUTO_INCREMENT` primary key for unique identification and efficient indexing.
* **Foreign Keys:** Clearly defined to enforce referential integrity between related tables (e.g., a `Course` must have an existing `Instructor`).
* **Data Types:** Appropriate data types are chosen (e.g., `VARCHAR` for names, `TEXT` for longer descriptions, `DECIMAL` for currency, `TIMESTAMP` for dates).
* **`UNIQUE` Constraints:** Used for `username`, `email` in `Users` and `Instructors` to ensure uniqueness where needed. Also used on `(course_id, lesson_order)` in `Lessons` to maintain unique ordering, and on `(user_id, course_id)` in `Enrollments` to prevent duplicate enrollments.
* **Junction Table (`Enrollments`):** Necessary to resolve the many-to-many relationship between `Users` and `Courses`, allowing a user to enroll in many courses and a course to have many users.
* **`password_hash`:** Storing hashed passwords is crucial for security.
* **Default Values:** `DEFAULT CURRENT_TIMESTAMP` for creation dates is common.

---

### Question 2: Restaurant Reservation System

**Use Case:** You need to design a database for a basic restaurant reservation system.
Here are the core requirements:

* **Restaurants:** Each restaurant has a name, address, and phone number.
* **Customers:** Customers can make reservations. Each customer has a name, email, and phone number.
* **Reservations:** A reservation is made by a customer for a specific restaurant, on a specific date and time, for a certain number of guests. Reservations can have a status (e.g., 'Confirmed', 'Cancelled', 'Completed').

**Your Task:** Design the SQL schema for this system.

---

### Answer 2: Restaurant Reservation System

Here's a possible SQL schema design:

```sql
-- Table: Restaurants
CREATE TABLE Restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique ID for each restaurant
    name VARCHAR(255) NOT NULL, -- Name of the restaurant
    address VARCHAR(255) NOT NULL, -- Physical address
    phone_number VARCHAR(20), -- Contact phone number
    email VARCHAR(100) UNIQUE, -- Restaurant's email (optional, but good for contact)
    cuisine_type VARCHAR(50) -- e.g., 'Italian', 'Japanese', 'Vietnamese'
);

-- Table: Customers
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique ID for each customer
    first_name VARCHAR(100) NOT NULL, -- Customer's first name
    last_name VARCHAR(100) NOT NULL, -- Customer's last name
    email VARCHAR(100) UNIQUE NOT NULL, -- Customer's email (must be unique for login/contact)
    phone_number VARCHAR(20) UNIQUE NOT NULL, -- Customer's phone number (must be unique)
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date and time of registration
);

-- Table: Reservations
CREATE TABLE Reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique ID for each reservation
    customer_id INT NOT NULL, -- Foreign Key to Customers table
    restaurant_id INT NOT NULL, -- Foreign Key to Restaurants table
    reservation_date DATE NOT NULL, -- The date of the reservation
    reservation_time TIME NOT NULL, -- The time of the reservation
    number_of_guests INT NOT NULL CHECK (number_of_guests > 0), -- Number of people in the party
    status VARCHAR(50) DEFAULT 'Confirmed', -- e.g., 'Confirmed', 'Pending', 'Cancelled', 'Completed', 'No-Show'
    special_requests TEXT, -- Any special notes from the customer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the reservation was made

    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
    -- Consider adding a UNIQUE constraint for (restaurant_id, reservation_date, reservation_time, number_of_guests)
    -- to prevent exact duplicate reservations, though exact time might not be unique if multiple parties arrive at once.
);
```

**Explanation of Design Choices:**

* **Normalization:** Adheres to normalization by separating `Restaurant`, `Customer`, and `Reservation` entities.
* **Primary and Foreign Keys:** Standard usage for unique identification and referential integrity.
* **Data Types:** `DATE` for date, `TIME` for time. `VARCHAR` for names/addresses, `INT` for numbers of guests. `TEXT` for longer requests.
* **`UNIQUE` Constraints:** `email` and `phone_number` for `Customers` are marked `UNIQUE` as they often serve as identifiers for customer accounts. `email` for `Restaurants` if it's considered unique.
* **`CHECK` Constraint:** Added `CHECK (number_of_guests > 0)` to ensure logical data integrity for the number of guests.
* **`status` Field:** A `VARCHAR` field with a `DEFAULT` value for the reservation status, allowing flexibility for future states. In a more advanced system, this might be a foreign key to a `ReservationStatuses` lookup table.
* **No `Tables` Table:** For a *basic* reservation system, direct mapping to specific physical tables might be overkill. Reservations are often handled based on `number_of_guests` and overall restaurant capacity for a given time slot. If the requirement was to assign specific tables, a `Tables` table and potentially a `ReservationTables` junction table would be needed.

---

### General Tips for SQL Schema Design Interviews

1. **Understand the Entities:** Identify all the main "things" in the problem (e.g., User, Course, Instructor). These usually become your tables.
2. **Identify Attributes:** For each entity, list the relevant pieces of information (e.g., User has name, email, password). These become your columns.
3. **Determine Primary Keys (PKs):** Every table needs a PK for unique identification. Auto-incrementing integers (`INT PRIMARY KEY AUTO_INCREMENT` or `SERIAL`) are common and good defaults.
4. **Identify Relationships:**
      * **One-to-Many (1:M):** (e.g., One Instructor teaches many Courses). The "many" side (Courses) gets a Foreign Key (FK) column referencing the "one" side's PK (Instructor ID).
      * **Many-to-Many (M:N):** (e.g., Many Users enroll in many Courses). This requires a separate **junction table** (e.g., `Enrollments`) that contains FKs to the PKs of the two related tables. This junction table often gets its own PK too.
      * **One-to-One (1:1):** Less common, but usually implemented by putting all attributes in one table, or by having an FK on one table that is also unique.
5. **Choose Appropriate Data Types:**
      * Strings: `VARCHAR(length)` for variable-length strings, `TEXT` for very long strings.
      * Numbers: `INT` for whole numbers, `DECIMAL(precision, scale)` for currency or precise numbers, `FLOAT`/`DOUBLE` for less precise floating-point numbers.
      * Dates/Times: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`.
      * Booleans: `BOOLEAN` or `TINYINT(1)`.
6. **Constraints:**
      * `NOT NULL`: For columns that must always have a value.
      * `UNIQUE`: For columns where values must be unique (e.g., email addresses).
      * `DEFAULT`: For setting default values (e.g., `CURRENT_TIMESTAMP`).
      * `CHECK`: For enforcing specific value rules (e.g., `age > 0`).
7. **Indexes:** Mentioning that Primary Keys and Foreign Keys are automatically indexed is good. Suggesting additional indexes on frequently queried columns (e.g., `username`, `email`, search fields) shows a deeper understanding of performance.
8. **Normalization:** Briefly explain how your design reduces redundancy and improves data integrity (e.g., breaking down entities into separate tables).
9. **Ask Clarifying Questions:** In a real interview, don't be afraid to ask about specific business rules, edge cases, or data volume expectations. This shows critical thinking.

---

### Question 3: E-commerce Order Management System

**Use Case:** You need to design a database for an e-commerce platform that handles online orders.
Here are the core requirements:

* **Users:** Customers who can register, log in, and place orders.
* **Categories:** Product categories for organization (e.g., Electronics, Clothing, Books).
* **Products:** Items for sale with pricing, inventory, and category association.
* **Orders:** Customer orders containing multiple products with quantities.
* **Order Status:** Track order progression (pending, processing, shipped, delivered).
* **Reviews:** Customers can review products they have purchased.

**Your Task:** Design the SQL schema (tables, columns, data types, primary keys, foreign keys, and relationships) for this e-commerce platform.

---

### Answer 3: E-commerce Order Management System

Here's a comprehensive SQL schema design:

```sql
-- Table: Users (Customers)
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: Categories
CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id INT, -- For subcategories
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_category_id) REFERENCES Categories(category_id)
);

-- Table: Products
CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    sku VARCHAR(100) UNIQUE, -- Stock Keeping Unit
    weight DECIMAL(8, 2), -- For shipping calculations
    dimensions VARCHAR(50), -- e.g., "10x5x3 cm"
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    INDEX idx_category (category_id),
    INDEX idx_active_price (is_active, price)
);

-- Table: Orders
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    shipping_address TEXT NOT NULL,
    billing_address TEXT NOT NULL,
    payment_method VARCHAR(50),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP NULL,
    delivered_date TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_user_date (user_id, order_date),
    INDEX idx_status (order_status),
    
    CHECK (order_status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
);

-- Junction Table: Order Items (Many-to-Many between Orders and Products)
CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

-- Table: Reviews
CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    order_id INT NOT NULL, -- Link to the order where the product was purchased
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_title VARCHAR(255),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    UNIQUE (user_id, product_id, order_id), -- One review per user per product per order
    INDEX idx_product_rating (product_id, rating),
    INDEX idx_user (user_id)
);

-- Table: User Addresses (Optional - for multiple shipping addresses)
CREATE TABLE UserAddresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_type VARCHAR(20) DEFAULT 'shipping', -- 'shipping' or 'billing'
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, address_type),
    
    CHECK (address_type IN ('shipping', 'billing'))
);
```

**Explanation of Design Choices:**

* **Normalization:** The design follows 3NF principles to eliminate redundancy while maintaining data integrity.
* **Hierarchical Categories:** The `parent_category_id` in Categories allows for subcategories (e.g., Electronics > Smartphones).
* **Order Status Tracking:** The Orders table includes status field with CHECK constraint and timestamp fields for tracking order progression.
* **Flexible Addressing:** Separate UserAddresses table allows users to have multiple shipping/billing addresses.
* **Inventory Management:** Products table includes stock tracking with CHECK constraints to prevent negative inventory.
* **Review Verification:** Reviews are linked to specific orders to ensure only customers who purchased the product can review it.
* **Performance Optimization:** Strategic indexes on frequently queried columns (category, user, status, etc.).
* **Data Integrity:** Comprehensive foreign key relationships and CHECK constraints ensure data consistency.
* **Audit Trail:** Created/updated timestamps on key tables for tracking changes.
* **Generated Columns:** OrderItems uses a generated column for total_price to maintain consistency.

**Additional Considerations:**
* **Product Variants:** For products with variants (size, color), you might add a ProductVariants table.
* **Inventory Tracking:** Consider adding an InventoryTransactions table for detailed stock movement tracking.
* **Promotions/Discounts:** Additional tables for coupons, discounts, and promotional pricing.
* **Payment Processing:** Separate tables for payment transactions and payment methods.
* **Search Optimization:** Full-text indexes on product names and descriptions for search functionality.
