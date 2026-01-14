# 🐞 Issue Tracker API

A **production-grade Issue Tracking backend** built with **FastAPI**, **PostgreSQL**, and **asyncpg**.

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
ISSUETRAKERAPI/
├── app/
│   ├── apis.py           # API route definitions
│   ├── db.py             # Async DB connection pooling  
│   ├── helper.py         # Contains helper function used
│   ├── schemas.py        # Pydantic request/response models
│   └── queries.py   # Optimized Raw SQL queries
│ 
├── main.py               # Application entry point
└── README.md

