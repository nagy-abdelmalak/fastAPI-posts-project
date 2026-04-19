from psycopg_pool import ConnectionPool
from app.core.config import get_settings

pool : ConnectionPool | None = None

def get_pool() -> ConnectionPool:
    if pool is None:
        raise RuntimeError("Database pool not intialized")
    return

# # 'with' gestisce la transazione anche in caso d'errore e chiude la connessione
# with db_pool.connection() as conn:
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM posts")
#         saved_posts = cur.fetchall()
#         print(saved_posts)