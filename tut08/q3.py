import sys
import psycopg2
import re

conn = None
curs = None

if len(sys.argv) != 3:
    print("Usage: python3 q3.py <zid> <term>")
    exit(1)

zid = sys.argv[1]
term = sys.argv[2]

try:
    conn = psycopg2.connect("dbname=uni")
    curs = conn.cursor()

    curs.execute("select * from students where id = %s", [zid])
    if not curs.fetchone():
        print("No such student")

    curs.execute("""
        select
            subjects.code as code,
            subjects.name as name,
            terms.code as term
        from courses
        inner join course_enrolments on courses.id = course_enrolments.course
        inner join terms on terms.id = courses.term
        inner join subjects on subjects.id = courses.subject
        where course_enrolments.student = %s
        and terms.code = %s
        """, [zid, term])

    query = curs.fetchall()
    if len(query) == 0:
        print("No courses that term")

    for code, name, _ in query:
        print(code, name)

except Exception as err:
    print(err)
finally:
    if curs:
        curs.close()
    if conn:
        conn.close()
