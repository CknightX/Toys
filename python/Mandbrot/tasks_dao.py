import sqlite3


def create_db(name):
    conn=sqlite3.connect(name)
    cur=conn.cursor()
    cur.execute("""
    create table if not exists tasks(
        task_id text primary key,
        status int default 0
    );
    """)
    return conn

def get_task_status(conn,task_id):
    """
    return: status if exist else None
    """
    cur=conn.cursor()
    cur.execute(f"""
    select * from tasks where task_id='{task_id}';
    """)
    res=cur.fetchone()
    if not res:
        return None
    return res[1]

def get_all_unfinished_task(conn):
    cur=conn.cursor()
    cur.execute(f"""
    select * from tasks where status=0;
    """)
    res=cur.fetchall()
    return res


def set_task_status(conn,task_id,status):
    cur=conn.cursor()
    cur.execute(f"""
    select * from tasks where task_id='{task_id}';
    """)
    res=cur.fetchone()
    if not res:
        cur.execute(f"""
        insert into tasks values ('{task_id}',{status});
        """)
    cur.execute(f"""
    update tasks set status={status} where task_id='{task_id}';
    """)
    conn.commit()