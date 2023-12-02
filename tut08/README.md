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

[q3.py](q3.py)

## Q4

Using the uni database, write a Python/Psycopg2 script called course-roll that takes two command-line arguments (subject code and term code) and produces a list of students enrolled in that course. Each line should contain: studentID, name. The name should appear as "familyName, givenNames" and the list should be ordered by familyName then by givenName. e.g.

```bash
$ ./course-roll COMP1521
Usage: course-roll subject term

$ ./course-roll COMP1511 16s1
COMP1511 16s1
No students

$ ./course-roll COMP1151 16s1
COMP1151 17s1
No students

$ ./course-roll PSYC1022 19T0
PSYC1022 19T0
5154325 Georgas, Jose
5141408 Hordern, Priyanshi
5134420 Hulst, Stan
5159982 Madanimelak, Siavash
5163692 Watson, Carine

$ ./course-roll COMP3211 20T1
COMP3211 20T1
5167571 Ahmad Bakir, Nabilah
5160470 Bashir, Zeeshan
5132438 Bown, Yelgun
5147435 Chen, Manjiang
5137415 Hang, Zheren
5134504 Hiwilla, Libin
5182987 Krueger, Isabel
5149728 Lim, Sang
5160734 Maslin, Jocelyn
5160049 McTigue, Courtney
5159809 Murdani, Elsan
5171168 Nadol, Rowan
5169891 Niu, Zihui
5166832 Pong, Chi-Kuang
5161703 Schachat, Kalie
5215073 Shang, Chan
5173714 Strickland, Vanya
5129717 Styer, Sharon
5208366 Suo, Junjian
5178112 Tandan, Ray
5164849 Thattai, Kajalben
5168959 Virdi, Jawad
```

### Ans

[q4.py](q4.py)

## Q5

The script in the previous question was a little bit sloppy in its error detection, and the messages did not distinguish between a real course with no students and a bad value for either the subject code or the term code, or a valid pair of codes for which there was no course offering. The script should also now print the long name of the subject. Improve the script so it behaves as follows:

```bash
$ ./course-roll1 COMP1151 18s1
Invalid subject COMP1151

$ ./course-roll1 COMP1511 88xx
Invalid term 88xx

$ ./course-roll1 COMP3211 20T2
No offering: COMP3211 20T2

$ ./course-roll1 MATH2601 20T2
MATH2601 20T2 Higher Linear Algebra
5194739 Boddam-Whetham, Billi
5160543 Chao, Sixiang
5188339 Ghebrial, Christina
5220431 Lopez Castro, Feyza
5196254 McWilliam, Lianne

$ ./course-roll1 COMP3821 17s1
COMP3821 17s1 Extended Algorithms and Programming Techniques
5143563 Aurik, Rumana
5128387 Barsoum, Rona
5128243 Bartlett, Gregg
5133001 Black, Samim
5126171 Demiri, Florida
5128296 Donney, Lisita
5133189 Essam, Swisszanah
5135130 Ghislain, Thien-Ngan
5143373 Howard, Alanna
5141297 MAI, Tiancong
5132763 MAI, Xueqi
5143439 Manolios Reichert, Janette
5141860 Matsuo, Ryann
5125264 Mock, Na-Ima
5128275 Mohd Hassan, Xiao
5147571 Morsalin, Amir
5129681 Neo, Fenzhi
5128164 Park, Toshiki
5142705 Rabelo Castello, Tamara
5142618 Saldanha, Sai
5143532 Sethuramasamy, Tanvi
5141585 Twine, Hughie
5142688 Wenzel, Sohaib
5145043 Wijeratne, Joyce
5127997 Zhen, Kaijian
```

### Ans

[q5.py](q5.py)

## Q6

Using the uni database, write a Python/Psycopg2 script called nsubjects that takes the name (or part of the name) of a School and prints the number of subjects offered by that school. Use the command-line argument as a pattern, and do case-insensitive matching. If more than one school matches the pattern, indicate that multiple schools match.

Examples of usage:

```bash
$ python3 nsubjects 'Computer Science'
School of Computer Science and Engineering teaches 138 subjects

$ python3 nsubjects 'Chem'
Multiple schools match:
School of Chemical Engineering
School of Chemistry

$ python3 nsubjects 'Chemistry'
School of Chemistry teaches 11 subjects

$ python3 nsubjects 'Math'
School of Mathematics & Statistics teaches 85 subjects
```

### Ans

[q6.py](q6.py)
