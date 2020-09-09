import sqlite3
from .utils import get_db_absolute_path


def search_akorda_db(query: str, mode: str = "default") -> list:
    """TODO"""
    if mode == "default":
        table_name = "data"
    elif mode == "tokenized":
        table_name = "tokenized_data"

    # conn = sqlite3.connect("db/akorda.sqlite")
    conn = sqlite3.connect(database=get_db_absolute_path("akorda.sqlite"))

    cursor = conn.cursor()

    # sql = "select id, doc_name from abay_words where doc_text LIKE '%" + query + "%';"
    sql = f"select url, section, title, date_time from {table_name} where text LIKE '%{query}%';"
    # sql = f"select count(*) from {table_name};"
    cursor.execute(sql)
    query_result = cursor.fetchall()  # or use fetchone()

    return query_result
