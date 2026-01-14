# 🐞 Issue Tracker API

The **Issue Tracker API** is a production-grade backend system designed to manage complex software development workflows. Built with **FastAPI** and **PostgreSQL**.

This project focuses on **high-concurrency architecture** and **data integrity**. By utilizing **Raw SQL** via the **asyncpg** driver instead of a traditional ORM, the system achieves maximum performance and gives the developer full control over database execution plans.
---

## 🚀 Features

### Core Functionality
- **Issue Management:** Create, update, and fetch issues with UUIDs for security.
- **Partial Updates:** Smart `PATCH` updates using Pydantic's `exclude_unset` logic.
- **Collaboration:** Assign issues to users and add threaded comments.
- **Atomic Operations:** Add and replace labels or update bulk statuses within SQL transactions.
- **Data Ingestion:** CSV import functionality for bulk issue creation.

### Reporting & Analytics
- **Top Assignees:** Identify workload distribution across the team.
- **Resolution Latency:** Calculate average time taken to resolve issues for performance metrics.

---

## 🏗️ Tech Stack

| Layer | Technology | Key Benefit |
|:---|:---|:---|
| **API Framework** | FastAPI | High performance & automatic OpenAPI docs. |
| **Database** | PostgreSQL | Relational integrity and advanced indexing. |
| **DB Driver** | asyncpg | High-speed, non-blocking PostgreSQL interface. |
| **SQL Style** | Raw SQL | Full control over query optimization (No ORM). |
| **Async Model** | asyncio | Concurrent request handling for high scalability. |
| **Validation** | Pydantic | Strict type safety and schema enforcement. |
| **Security** | bcrypt | Industry-standard password hashing. |

---

## 📁 Project Structure

```text
ISSUETRACKERAPI/
├── app/
│   ├── apis.py           # API route definitions
│   ├── db.py             # Async DB connection pooling  
│   ├── helper.py         # Contains helper function used
│   ├── schemas.py        # Pydantic request/response models
│   └── queries.py        # Optimized Raw SQL queries
├── main.py               # Application entry point
├── issues_sample.csv     # Sample file to test csv import              
└── README.md
```
---

## 🔗 Main API Endpoints

### User, Issues & Reports 
* `POST /issues` — Create a new issue
* `GET /issues` — List all issues with filters
* `GET /issues/{id}` — Get issue with comments & labels
* `PATCH /issues/{id}` — Partial update of an issue
* `POST /issues/bulk-status` — Batch update status for multiple issues
* `POST /issues/import` — Bulk creation via CSV import
* `POST /issues/{id}/comments` — Add a comment to an issue
* `PUT /issues/{id}/labels` — Atomic label replacement
* `GET /reports/top-assignees` — Fetch workload distribution
* `GET /reports/latency` — Resolution speed metrics

---

## 🔐 Security & Best Practices

* **ID Masking:** **UUIDs** are added in each table for saftey and to prevent ID enumeration attacks.
* **SQL Injection Defense:** All database interactions use **parameterized queries** via `asyncpg`.
* **Concurrency:** Managed **connection pooling** to prevent database exhaustion under heavy load.
* **Validation:** Strict schema enforcement and data sanitization via **Pydantic**.

---

## 🚀 Running the Project

Follow these steps to set up the environment and run the **Issue Tracker API** locally.

### 1. Database Setup
1. **Install PostgreSQL:** Download and install [PostgreSQL](https://www.postgresql.org/download/) and [pgAdmin4](https://www.pgadmin.org/download/).
2. **Setup DB:** Create a new database and configure your credentials (username, password, host) in `db.py`.
3. **Initialize Tables:** Execute the SQL queries provided in `dbtableschema.txt` to create the required tables and run the indexing queries for query performance improvement.


---

### 2. Application Setup

**Clone the repository:**
```bash
git clone [https://github.com/ikrlalit/IssueTrackerAPI.git](https://github.com/ikrlalit/IssueTrackerAPI.git)
```
Next, move to project directory -
```bash
cd IssueTrackerAPI
```
Setup Python virtual environment -
```bash
python -m venv .venv
```
Activate environement using -
- Windows
```bash
.venv\Scripts\activate
```
- Linux/MacOS
```bash
source .venv/bin/activate
```
Install required dependencies- 
```bash
pip install -r requirements.txt
```
### 3. Execution
Run the FastAPI application:
```bash
uvicorn main:app --reload
```
#### 4. API Documentation
Once the application server starts successfully, go to the link below to access the Swagger UI and interact with the APIs:
```bash
http://localhost:8000/docs
```
## 🎯 Conclusion

The **Issue Tracker API** serves as a high-performance, scalable foundation for modern project management tools. By choosing **Raw SQL** and **asyncpg** over traditional ORMs, this project demonstrates a commitment to database optimization and efficient asynchronous Python programming. 

### 💡 Why this Project Matters
* **Performance-First:** Built for speed with non-blocking I/O and direct SQL execution.
* **Production Standards:** Follows RESTful best practices, secure password hashing, and UUID-based resource handling.

---
