# Week08 Tutorial - Python/Psycopg2

## Q1

What is the difference between a connection and a cursor in Psycopg2? How do you create each?

### Ans

```py
# Connection is a connection to the database.
conn = psycopg2.connect(db=dbname)

# Cursor is a pipeline between Python and Postgresql DB.
curs = conn.cursor()
```

## Q2

The following Python script (in a executable file called opendb) aims to open a connection to a database whose name is specified on the command line:
```py
#!/usr/bin/python3
import sys
import psycopg2
if len(sys.argv) < 2:
    print("Usage: opendb DBname")
    exit(1)
db = sys.argv[1]
try:
    conn = psycopg2.connect(f"dbname={db}")
    print(conn)
    cur = conn.cursor()
except psycopg2.Error as err:
    print("database error: ", err)
finally:
    if conn is not None:
        conn.close()
    print("finished with the database")
```

When invoked with an existing database, it behaves as follows
```bash
$ ./opendb beers2
<connection object at 0x7fac401799f0; dsn: 'dbname=beers2', closed: 0>
finished with the database
```

but when invoked with a non-existent database it produces
```bash
$ ./opendb nonexistent
database error:  FATAL:  database "nonexistent" does not exist

Traceback (most recent call last):
  File "./opendb", line 16, in 
    if conn :
NameError: name 'conn' is not defined
```

rather than
```bash
$ ./opendb nonexistent
database error:  FATAL:  database "nonexistent" does not exist

finished with the database
```

What is the problem? And how can we fix it?

### Ans

```py
conn = None
try:
    conn = psycopg2.connect(f"dbname={db}")
```

## Q3

The following questions make use of the uni database used in lectures. A database dump for the uni database can be found in `uni.dump`. The following gives enough of the schema to answer the questions below:

```sql
People(id, family, given, fullname, birthday, origin)

Students(id)

Subjects(id, code, name, uoc, offeredby, ...)
Courses(id, subject, term, homepage)
Streams(id, code, name, offeredby, stype, ...)
Programs(id, code, name, uoc, offeredby, ...)

Terms(id, year, ttype, code, name, starting, ending)

Course_enrolments(student, course, mark, grade)
Stream_enrolments(part_of_prog_enr, stream)
Program_enrolments(id, student, term, program, ...)

OrgUnits(id, utype, name, longname, unswid)
OrgUnit_Types(id, name)
```

Using the uni database, write a Python/Psycopg2 script called courses-studied that prints the subjects that a specified student studied in a given term. There is no need to check whether the student was enrolled in the given term; simply print that they studied no courses in that term. Examples of use:

```bash
$ ./courses-studied
Usage: ./courses-studied studentID term

$ ./courses-studied 1234567 18s1
No such student

$ ./courses-studied 9300035 20T1
No such student

$ ./courses-studied 5137295 17s2
COMP1521 Computer Systems Fundamentals
COMP1531 Software Eng Fundamentals
MATH1231 Mathematics 1B

$ ./courses-studied 5137295 20T1
COMP3231 Operating Systems
SENG3011 Software Eng Workshop 3
```

### Ans


