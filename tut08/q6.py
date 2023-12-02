import sys
import psycopg2
import re

conn = None
curs = None

if len(sys.argv) != 2:
    print("Usage: python3 q6.py <school>")
    exit(1)

school = sys.argv[1]

try:
    conn = psycopg2.connect("dbname=uni")
    curs = conn.cursor()

    curs.execute("""
        select
            orgunits.longname as name,
            count(subjects) as nSubjects
        from orgunits
        inner join orgunit_types on orgunit_types.id = orgunits.utype
        inner join subjects on subjects.offeredBy = orgunits.id
        where orgunit_types.name = 'School'
        and orgunits.longname ~* %s
        group by orgunits.longname
        """, [school])

    queries = curs.fetchall()

    if len(queries) == 0:
        print("No schools match")
        exit(1)

    if len(queries) == 1:
        name, nSubjects = queries[0]
        print(f"{name} teaches {nSubjects} subjects")
        exit(1)

    if len(queries) > 1:
        print("Multiple schools match")

    for name, nSubjects in queries:
        print(name)

except Exception as err:
    print(err)
finally:
    if curs:
        curs.close()
    if conn:
        conn.close()
