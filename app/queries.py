from app.helper import *

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
