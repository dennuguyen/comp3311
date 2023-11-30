# Week05 Tutorial -  Stored Functions in SQL and PLpgSQL

## Q1

Write a simple PLpgSQL function that returns the square of its argument value. It is used as follows:

```sql
mydb=> select sqr(4);
 sqr 
-----
  16
(1 row)

mydb=> select sqr(1000);
   sqr 
---------
 1000000
(1 row)
```

Could we use this function in any of the following ways?

```sql
select sqr(5.0);
select(5.0::integer);
select sqr('5');
```

If not, how could we write a function to achieve this?

### Ans

```sql
create or replace function sqr(n numeric) returns numeric
as $$
begin
  return n * n;
end;
$$ language plpgsql;
```

## Q2

Write a PLpgSQL function that "spreads" the letters in some text. It is used as follows:

```sql
mydb=> select spread('My Text');
     spread
----------------
 M y   T e x t
(1 row)
```

### Ans

```sql
create or replace function spread(str text) returns text
as $$
declare
  retval text := '';
begin
  for i in 1..length(str) loop
    retval := retval || substr(str, i, 1) || ' ';
  end loop;
  return retval;
end;
$$ language plpgsql;
```

Test with:
```sql
select spread('text');
```

## Q3

Write a PLpgSQL function to return a table of the first n positive integers.

The fuction has the following signature:

```sql
create or replace function seq(n integer) returns setof integer
```

and is used as follows:

```sql
mydb=> select * from seq(5);
 seq
-----
  1
  2
  3
  4
  5
(5 rows)
```

### Ans

```sql
create or replace function seq(n integer) returns setof integer
as $$
begin
  for i in 1..n loop
    return next i;
  end loop;
end;
$$ language plpgsql;
```

Run:
```sql
select seq(5);
```

## Q4

Generalise the previous function so that it returns a table of integers, starting from lo up to at most hi, with an increment of inc. The function should also be able to count down from lo to hi if the value of inc is negative. An inc value of 0 should produce an empty table. Use the following function header:

```sql
create or replace function seq(lo int, hi int, inc int) returns setof integer
```

and the function would be used as follows:

```sql
mydb=> select * from seq(2,7,2);
 val
-----
  2
  4
  6
(3 rows)
```

Some other examples, in a more compact representation:

```sql
seq(1,5,1)   gives   1  2  3  4  5
seq(5,1,-1)  gives   5  4  3  2  1
seq(9,2,-3)  gives   9  6  3
seq(2,9,-1)  gives   empty
seq(1,5,0)   gives   empty
```

### Ans

```sql
create or replace function seq(lo int, hi int, inc int) returns setof integer
as $$
declare
  i integer := lo;
begin
  while i <= hi loop
    return next i;
    i := i + inc;
  end loop;
end;
$$ language plpgsql;
```

## Q5

Re-implement the seq(int) function from above as an SQL function, and making use of the generic seq(int,int,int) function defined above.

### Ans

```sql
create or replace function seq(n integer) returns setof integer
as $$
select seq(1, n, 1);
$$ language sql;
```

## Q6

Create a factorial function based on the above sequence returning functions.

```sql
create function fac(n int) returns integer
```

Implement it as an SQL function (not a PLpgSQL function). The obvious solution to this problem requires a product aggregate, analogous to the sum aggregate. PostgreSQL does not actually have a product aggregate, but for the purposes of this question, you can assume that it does, and has the following interface:

```sql
product(list of integers) returns integer
```

### Ans

```sql
create or replace function prod(s int[]) returns int
as $$
declare
  retval int := 1;
  i int;
begin
  foreach i in array s loop
    retval := retval * i;
  end loop;
  return retval;
end;
$$ language plpgsql;

create or replace function fac(n int) returns int
as $$
  select prod(array(select seq from seq(n)));
$$ language sql;
```

## Q7

<blockquote>
  Use the old Beers/Bars/Drinkers database in answering the following questions. A summary schema for this database:

  ```sql
  Beers(name:string, manufacturer:string)
  Bars(name:string, address:string, license#:integer)
  Drinkers(name:string, address:string, phone:string)
  Likes(drinker:string, beer:string)
  Sells(bar:string, beer:string, price:real)
  Frequents(drinker:string, bar:string)
  ```

  Primary key attributes are in bold. Foreign key attributes are in bold italic.

  The examples below assume that the user is connected to a database called beer containing an instance of the above schema.
</blockquote>

Write a PLpgSQL function called hotelsIn() that takes a single argument giving the name of a suburb, and returns a text string containing the names of all hotels in that suburb, one per line.

```sql
create function hotelsIn(_addr text) returns text
```

The function is used as follows:

```sql
beer=> select hotelsIn('The Rocks');
    hotelsin     
-----------------
 Australia Hotel+
 Lord Nelson    +
 
(1 row)
```

Can you explain what the '+'at the end of each line is? And why it says (1 row)?

Note that the output from functions returning a single text string and looks better if you turn off psql's output alignment (via psql's \a command) and column headings (via psql's \t command).

Compare the aligned output above to the unaligned output below:

```sql
beer=> \a
Output format is unaligned.
beer=> \t
Showing only tuples.
beer=> select hotelsIn('The Rocks');
Australia Hotel
Lord Nelson
```

From now on, sample outputs for functions returning text will assume that we have used \a and \t.

### Ans

```sql
create or replace function hotelsIn(_addr text) returns text
as $$
declare
  r record;
  retval text := '';
begin
  for r in (select * from bars where addr = _addr) loop
    retval := retval || r.name || e'\n';
  end loop;
  return retval;
end;
$$ language plpgsql;
```

## Q8

Write a new PLpgSQL function called hotelsIn() that takes a single argument giving the name of a suburb and returns the names of all hotels in that suburb. The hotel names should all appear on a single line, as in the following examples:

```sql
beer=> select hotelsIn('The Rocks');
Hotels in The Rocks:  Australia Hotel  Lord Nelson 

beer=> select hotelsIn('Randwick');
Hotels in Randwick:  Royal Hotel 

beer=> select hotelsIn('Rendwik');
There are no hotels in Rendwik
```

### Ans

```sql
create or replace function hotelsIn(_addr text) returns text
as $$
declare
  r record;
  retval text := '';
begin
  if not exists(select * from bars where addr = _addr) then
    retval := 'There are no hotels in ' || _addr;
    return retval;
  end if;

  retval := 'Hotels in ' || _addr || ': ';
  for r in (select * from bars where addr = _addr) loop
    retval := retval || r.name || '  ';
  end loop;
  return retval;
end;
$$ language plpgsql;
```

## Q9

Write a PLpgSQL procedure happyHourPrice that accepts the name of a hotel, the name of a beer and the number of dollars to deduct from the price, and returns a new price. The procedure should check for the following errors:
- non-existent hotel (invalid hotel name)
- non-existent beer (invalid beer name)
- beer not available at the specified hotel
- invalid price reduction (e.g. making reduced price negative) 

Use to_char(price,'$9.99') to format the prices.

```sql
beer=> select happyHourPrice('Oz Hotel','New',0.50);
There is no hotel called 'Oz Hotel'

beer=> select happyHourPrice('Australia Hotel','Newer',0.50);
There is no beer called 'Newer'

beer=> select happyHourPrice('Australia Hotel','New',0.50);
The Australia Hotel does not serve New

beer=> select happyHourPrice('Australia Hotel','Burragorang Bock',4.50);
Price reduction is too large; Burragorang Bock only costs $ 3.50

beer=> select happyHourPrice('Australia Hotel','Burragorang Bock',1.50);
Happy hour price for Burragorang Bock at Australia Hotel is $ 2.00
```

### Ans

```sql
create or replace function happyHourPrice(_bar text, _beer text, _deduct numeric) returns text
as $$
declare
  price numeric;
begin
  if not exists(select * from bars where name = _bar) then
    return 'There is no hotel called ''' || _bar || '''';
  end if;

  if not exists(select * from beers where name = _beer) then
    return 'There is no beer called ''' || _beer || '''';
  end if;

  select sells.price from sells where bar = _bar and beer = _beer into price;
  if price is null then
    return 'The' || _bar || ' does not serve ' || _beer;
  end if;

  if (price - _deduct < 0) then
    return 'Price reduction is too large; ' || _bar || ' only costs' || to_char(price, '$9.99');
  end if;

  return 'Happy hour price for ' || _beer || ' at ' || _bar || ' is ' || to_char(price - _deduct, '$9.99');
end;
$$ language plpgsql;
```

## Q10

The hotelsIn function above returns a formatted string giving details of the bars in a suburb. If we wanted to return a table of records for the bars in a suburb, we could use a view as follows:

```sql
beer=> create or replace view HotelsInTheRocks as
    -> select * from Bars where addr = 'The Rocks';
CREATE VIEW
beer=> select * from HotelsInTheRocks;
      name       |   addr    | license 
-----------------+-----------+---------
 Australia Hotel | The Rocks |  123456
 Lord Nelson     | The Rocks |  123888
(2 rows)
```

Unfortunately, we need to specify a suburb in the view definition. It would be more useful if we could define a "parameterised view" which we could use to generate a table for any suburb, e.g.

```sql
beer=> select * from HotelsIn('The Rocks');
      name       |   addr    | license 
-----------------+-----------+---------
 Australia Hotel | The Rocks |  123456
 Lord Nelson     | The Rocks |  123888
(2 rows)
beer=> select * from hotelsIn('Coogee');
       name       |  addr  | license 
------------------+--------+---------
 Coogee Bay Hotel | Coogee |  966500
(1 row)
```

Such a parameterised view can be implemented via an SQL function, defined as:

```sql
create or replace function hotelsIn(text) returns setof Bars
as $$ ... $$ language sql;
```

Complete the definition of the SQL function.

### Ans

```sql
create or replace function hotelsIn(_addr text) returns setof Bars
as $$
  select * from bars where addr = _addr;
$$ language sql;
```

## Q11

The function for the previous question can also be implemented in PLpgSQL. Give the PLpgSQL definition. It would be used in the same way as the above.

### Ans

```sql
create or replace function hotelsIn(_addr text) returns setof Bars
as $$
declare
  r record;
begin
  for r in (select * from bars where addr = _addr) loop
    return next r;
  end loop;
end;
$$ language plpgsql;
```

## Q12

<blockquote>
  Use the Bank Database in answering the following questions. A summary schema for this database:

  ```sql
  Branches(location:text, address:text, assets:real)
  Accounts(holder:text, branch:text, balance:real)
  Customers(name:text, address:text)
  Employees(id:integer, name:text, salary:real)
  ```

  The examples below assume that the user is connected to a database called bank containing an instance of the above schema.
</blockquote>

For each of the following, write both an SQL and a PLpgSQL function to return the result:
- salary of a specified employee
- all details of a particular branch
- names of all employees earning more than $sal
- all details of highly-paid employees

### Ans

```sql
-- salary of specified employees
```
