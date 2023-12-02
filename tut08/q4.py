import sys
import psycopg2
import re

conn = None
curs = None

if len(sys.argv) != 3:
    print("Usage: python3 q4.py <subject> <term>")
    exit(1)

subject = sys.argv[1]
term = sys.argv[2]

try:
    conn = psycopg2.connect("dbname=uni")
    curs = conn.cursor()

    curs.execute("""
        select
            people.id as id,
            people.family as last_name,
            people.given as first_name
        from people
        inner join course_enrolments on course_enrolments.student = people.id
        inner join courses on courses.id = course_enrolments.course
        inner join subjects on subjects.id = courses.subject
        inner join terms on terms.id = courses.term
        where subjects.code = %s
        and terms.code = %s
        """, [subject, term])

    print(subject, term)

    queries = curs.fetchall()
    if len(queries) == 0:
        print("No students")
        exit(1)

    for id, last_name, first_name in queries:
        print(f"{id} {last_name}, {first_name}")

except Exception as err:
    print(err)
finally:
    if curs:
        curs.close()
    if conn:
        conn.close()
