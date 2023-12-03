import sys
import psycopg2
import re

from psycopg2.extras import NamedTupleCursor

conn = None
curs = None

if len(sys.argv) != 2:
    print("Must specify a branch location")
    exit(1)

location = sys.argv[1]

try:
    conn = psycopg2.connect("dbname=bank")
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute("select * from branches where location = %s", [location])
    branch = curs.fetchone()
    if not branch:
        print(f"No such branch {branch}")
        exit(1)

    print(f"{location} branch ({branch.id}) holds")

    curs.execute("""
        select
            accounts.id as id,
            customers.given as given,
            customers.family as family,
            customers.lives_in as lives_in,
            accounts.balance as balance
        from accounts
        inner join held_by on held_by.account = accounts.id
        inner join customers on customers.id = held_by.customer
        where held_at = %s
        order by id
        """, [branch.id])
    total = 0
    for user in curs.fetchall():
        print(f"- account {user.id} owned by {user.given} {user.family} from {user.lives_in} with ${user.balance}")
        total += user.balance

    print(f"Assets: ${total}")

    if total != branch.assets:
        print("Discrepancy between assets and sum of account balances")

except Exception as err:
    print(err)
finally:
    if curs:
        curs.close()
    if conn:
        conn.close()
