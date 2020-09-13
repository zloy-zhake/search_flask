import sqlite3
from .utils import get_db_absolute_path


def search_akorda_db(
    query: str, mode: str = "default", num_results: int = -1
) -> list:
    """TODO"""
    if mode == "default":
        table_name = "data"
    elif mode == "tokenized":
        table_name = "tokenized_data"

    # conn = sqlite3.connect("db/akorda.sqlite")
    conn = sqlite3.connect(database=get_db_absolute_path("akorda.sqlite"))

    cursor = conn.cursor()

    sql = (
        f"select url, section, title, date_time, text from {table_name}"
        f" where text LIKE '%{query}%'"
    )
    if num_results > 0:
        sql += f" LIMIT {num_results}"

    cursor.execute(sql)
    query_result = cursor.fetchall()

    return query_result
