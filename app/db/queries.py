"""
Database query utilities.

Handles:
1. Logging user interactions
2. Analytics queries
"""

from app.db.database import get_connection


def log_query(
    session_id: str,
    question: str,
    answer: str,
    confidence_score: float,
    latency_ms: float,
    answer_found: bool
):
    """
    Stores a query interaction in the database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO query_logs (
            session_id,
            question,
            answer,
            confidence_score,
            latency_ms,
            answer_found
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            question,
            answer,
            confidence_score,
            latency_ms,
            int(answer_found)
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# REQUIRED ANALYTICS
# ==========================================================

def get_most_frequent_questions(limit: int = 10):
    """
    Returns the most frequently asked questions.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            COUNT(*) AS frequency
        FROM query_logs
        GROUP BY question
        ORDER BY frequency DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    conn.close()

    return results


def get_unanswered_queries():
    """
    Returns questions for which no answer
    was found in context.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            COUNT(*) AS occurrences
        FROM query_logs
        WHERE answer_found = 0
        GROUP BY question
        ORDER BY occurrences DESC
        """
    )

    results = cursor.fetchall()

    conn.close()

    return results


def get_average_latency():
    """
    Returns average response latency in milliseconds.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(latency_ms)
        FROM query_logs
        """
    )

    result = cursor.fetchone()

    conn.close()

    return round(result[0], 2) if result[0] else 0.0



def get_total_queries():
    """
    Returns total number of queries.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM query_logs
        """
    )

    result = cursor.fetchone()

    conn.close()

    return result[0]


def get_success_rate():
    """
    Returns percentage of queries
    where an answer was found.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ROUND(
                100.0 * SUM(answer_found) / COUNT(*),
                2
            )
        FROM query_logs
        """
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result[0] else 0.0


def get_average_confidence():
    """
    Returns average retrieval score.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(confidence_score)
        FROM query_logs
        """
    )

    result = cursor.fetchone()

    conn.close()

    return round(result[0], 4) if result[0] else 0.0


def get_recent_queries(limit: int = 10):
    """
    Returns most recent queries.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            answer,
            created_at
        FROM query_logs
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    conn.close()

    return results


def get_slowest_queries(limit: int = 5):
    """
    Returns queries with the highest latency.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            latency_ms
        FROM query_logs
        ORDER BY latency_ms DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    conn.close()

    return results


def get_chat_history(
    session_id: str,
    limit: int = 3
):
    """
    Returns the last N question-answer pairs
    for a session.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            answer
        FROM query_logs
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows[::-1]