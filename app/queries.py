from app.helper import *
import io
import csv

async def create_user_q(pool, username, password, role):
    async with pool.acquire() as conn:
        async with conn.transaction():
            record = await conn.fetchrow(
                """
                INSERT INTO users (username, password, role)
                VALUES ($1, $2, $3)
                RETURNING useruuid, username, role, created_at
                """,
                username, password, role
            )
            return serialize_response(record)

async def create_issue_q(pool, title, description, priority):
    async with pool.acquire() as conn:
        async with conn.transaction():
            record = await conn.fetchrow(
                """
                INSERT INTO issues (title, description, priority, status)
                VALUES ($1, $2, $3, 'OPEN')
                RETURNING issueuuid, title, description, status, priority, version, created_at
                """,
                title, description, priority
            )
            return serialize_response(record)


async def list_issues_q(pool, limit, offset):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT issueuuid, title, description, status, priority, version, created_at
            FROM issues
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return serialize_response(rows)


async def get_issue_q(pool, id):
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            """
            SELECT issueuuid, title, description, status, priority, version, created_at
            FROM issues
            WHERE id = $1
            """,
            id
        )
        return serialize_response(record)


async def update_issue_q(pool, id, data: dict):
    async with pool.acquire() as conn:
        async with conn.transaction():
            record = await conn.fetchrow(
                """
                UPDATE issues
                SET
                    title = COALESCE($1, title),
                    description = COALESCE($2, description),
                    status = COALESCE($3, status),
                    priority = COALESCE($4, priority)
                WHERE id = $5 
                RETURNING issueuuid, title, description, status, priority, version, created_at
                """,
                data.get("title"),
                data.get("description"),
                data.get("status"),
                data.get("priority"),
                id
            )
            return serialize_response(record)

async def add_comment_q(pool, issue_uuid, user_id, content):
    async with pool.acquire() as conn:
        async with conn.transaction():
            record = await conn.fetchrow(
                """
                INSERT INTO comments (issue_id, user_id, content)
                SELECT id, $2, $3 FROM issues WHERE id = $1
                RETURNING id, content, created_at
                """,
                issue_uuid, user_id, content
            )
            return serialize_response(record)

# ---------------- LABELS (ATOMIC REPLACE) ----------------
async def replace_labels_q(pool, id, label_ids):
    async with pool.acquire() as conn:
        async with conn.transaction():
            issue_id = await conn.fetchval(
                "SELECT id FROM issues WHERE id = $1", id
            )

            if not issue_id:
                return None

            await conn.execute(
                "DELETE FROM issue_labels WHERE issue_id = $1",
                issue_id
            )

            for label_id in label_ids:
                await conn.execute(
                    """
                    INSERT INTO issue_labels (issue_id, label_id)
                    VALUES ($1, $2)
                    """,
                    issue_id, label_id
                )
            return True

# ---------------- BULK STATUS (TRANSACTIONAL) ----------------
async def bulk_update_status_q(pool, issue_ids, status):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE issues
                SET status = $1
                WHERE id = ANY($2::int[])
                """,
                status, issue_ids
            )
            return {"updated": len(issue_ids)}


async def import_issues_q(pool, file_content: str):
    reader = csv.DictReader(io.StringIO(file_content))

    async with pool.acquire() as conn:
        async with conn.transaction():
            for row in reader:
                await conn.execute(
                    """
                    INSERT INTO issues (title, description, priority, status,version)
                    VALUES ($1, $2, $3, $4, 1)
                    ON CONFLICT (title, description, priority, status)
                    DO UPDATE SET
                        description = EXCLUDED.description,
                        priority = EXCLUDED.priority,
                        status = EXCLUDED.status,
                        version = issues.version + 1
                    """,
                    row["title"],
                    row.get("description"),
                    row.get("priority"),
                    row.get("status", "OPEN")
                )

# -------- TOP ASSIGNEES REPORT --------
async def get_top_assignees(pool, limit: int = 5):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                u.id AS assignee_id,
                u.username,
                COUNT(i.id) AS total_issues
            FROM issues i
            JOIN users u ON u.id = i.assignee_id
            GROUP BY u.id, u.username
            ORDER BY total_issues DESC
            LIMIT $1
            """,
            limit
        )
        return serialize_response(rows)
    

# -------- LATENCY REPORT --------
async def get_latency_report(pool):
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            """
            SELECT
                ROUND(
                    AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 3600),
                    2
                ) AS average_resolution_hours
            FROM issues
            WHERE status = 'CLOSED'
            """
        )
        return serialize_response(record)