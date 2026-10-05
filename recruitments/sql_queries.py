from django.db import connection


def candidates_by_skill(skill: str) -> list[tuple[object, ...]]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, email FROM recruitments_candidate WHERE skills ILIKE %s", [f"%{skill}%"])
        return cursor.fetchall()


def role_candidate_counts() -> list[tuple[object, ...]]:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT applied_role_id, COUNT(*)
            FROM recruitments_candidate
            GROUP BY applied_role_id
            ORDER BY COUNT(*) DESC
            """)
        return cursor.fetchall()