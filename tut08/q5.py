import sys
import psycopg2
import re

conn = None
curs = None

if len(sys.argv) != 3:
    print("Usage: python3 q5.py <subject> <term>")
    exit(1)

subject = sys.argv[1]
term = sys.argv[2]

try:
    conn = psycopg2.connect("dbname=uni")
    curs = conn.cursor()

    curs.execute("select id from subjects where code = %s", [subject])
    subject_id = curs.fetchone()
    if not subject_id:
        print(f"Invalid subject {subject}")
        exit(1)

    curs.execute("select id from terms where code = %s", [term])
    term_id = curs.fetchone()
    if not term_id:
        print(f"Invalid term {term}")
        exit(1)

    curs.execute("""
        select subjects.longname as name
        from courses
        inner join subjects on subjects.id = courses.subject
        where subject = %s
        and term = %s
        """, [subject_id, term_id])
    [course_name] = curs.fetchone()
    if not course_name:
        print(f"No course offering: {subject} {term}")
        exit(1)

    curs.execute("""
        select
            people.id as id,
            people.family as last_name,
            people.given as first_name
        from people
        inner join course_enrolments on course_enrolments.student = people.id
        inner join courses on courses.id = course_enrolments.course
        where courses.subject = %s
        and courses.term = %s
        """, [subject_id, term_id])

    print(subject, term, course_name)

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
