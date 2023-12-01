# Week07 Tutorial - Constraints, Triggers, and Aggregates

## Q1

Consider a schema for an organisation

```sql
Employee(id:integer, name:text, works_in:integer, salary:integer, ...)
Department(id:integer, name:text, manager:integer, ...)
```

Where works_in is a foreign key indicating which Department an Employee works in, and manager is a foreign key indicating which Employee is the manager of a Department.

A manager must work in the Department they manage. Can this be checked by standard SQL table constraints? If not, why not?

If it cannot be checked by standard SQL constraints, write an assertion to ensure that each manager also works in the department they manage. Define using a standard SQL assertion statement like:

```sql
create assertion manager_works_in_department
check  ...
```

### Ans

Can't check if manager works in department they manage in postgresql.

In 
```sql
create assertion manager_works_in_department
check(not exists(select * from Employee e join Department d on d.manager = e.id where e.works_in <> d.id))
```

## Q2

Using the same schema from the previous question, write an assertion to ensure that no employee in a department earns more than the manager of their department. Define using a standard SQL assertion statement like:

```sql
create assertion employee_manager_salary
check  ...
```

### Ans

```sql

```

## Q3

What is the SQL command used in PostgreSQL to define a trigger? And what is the SQL command to remove it?

### Ans

```sql
-- trigger function
create function function_name() returns trigger
as $$
declare
begin
end;
$$ language plpgsql;

-- trigger before
create trigger trigger_name
  before operation -- insert, delete or update
  on table_name for each row
  execute procedure function_name();

-- trigger after
create trigger trigger_name
  after operation -- insert, delete or update
  on table_name for each row
  execute procedure function_name();

-- dropping trigger
drop trigger trigger_name on table_name;
```

## Q4

Trigers can be defined as BEFORE or AFTER. What exactly are they before or after?

### Ans

- fire all BEFORE triggers, possibly modifying any new tuple
- do standard SQL constraint checks
- fire all AFTER triggers, possibly updating other tables

If trigger function raises exceptions, change is aborted and rolled back.

## Q5

Give examples of when you might use a trigger BEFORE and AFTER...
- an insert operation
- an update operation
- a delete operation

### Ans

Before triggers can:
- check for valid field values
- generate additional values for newly-inserted tuple

After triggers can:
  - Make additional DB updates for semantic consistency

## Q6

Consider the following relational schema:

```sql
create table R(a int, b int, c text, primary key(a, b));
create table S(x int primary key, y int);
create table T(j int primary key, k int references S(x));
```

State how you could use triggers to implement the following constraint checking (hint: revise the material on Constraint Checking from the Relational Data Model and ER-Relational Mapping extended notes)
- primary key constraint on relation `R`
- foreign key constraint between `T.j` and `S.x`

### Ans

```sql
-- primary key constraint on relation `R`
create function R_pk_check() returns trigger
as $$
begin
  if (new.a is null or new.b is null) then
    raise exception 'Missing primary key for R';
  end if;

  -- Ignore update.
  if (TG_OP = 'UPDATE' and old.a = new.a and old.b = new.b) then
    return;
  end if;

  -- Check keys on insert.
  
  if exists(select * from R where a = new.a and b = new.b) then
    raise exception 'Duplicate primary key for R';
  end if;
end;
$$ language plpgsql;

create trigger R_pk_check
  before insert or update
  on R for each row
  execute procedure R_pk_check();

-- foreign key constraint between T.j and S.x
create function T_fk_check() returns trigger
as $$
begin
  if not exists(select * from S where x = new.k) then
    raise exception 'Non-existent S.x key in T';
  end if;
end;
$$ language plpgsql;

create trigger T_fk_check
  before insert or update
  on T for each row
  execute procedure T_fk_check();
```

## Q7

Explain the difference between these triggers

```sql
create trigger updateS1 after update on S
for each row execute procedure updateS();

create trigger updateS2 after update on S
for each statement execute procedure updateS();
```

when executed with the following statements. Assume that S contains primary keys (1,2,3,4,5,6,7,8,9).
- `update S set y = y + 1 where x = 5;`
- `update S set y = y + 1 where x > 5;`

### Ans

`update S set y = y + 1 where x = 5;`
- No difference between `row` and `statement`.

`update S set y = y + 1 where x > 5;`
- `updateS1` will trigger for each affected tuple.
- `updateS2` will trigger once after all affected tuples have been modified and before updates have been committed.

## Q8

What problems might be caused by the following pair of triggers?

```sql
create trigger T1 after insert on Table1
for each row execute procedure T1trigger();

create trigger T2 after update on Table2
for each row execute procedure T2trigger();

create function T1trigger() returns trigger
as $$
begin
update Table 2 set Attr1 = ...;
end; $$ language plpgsql;

create function T2trigger() returns trigger
as $$
begin
insert into Table1 values (...);
end; $$ language plpgsql;
```

### Ans

Infinite loop.

## Q9

Given a table:

```sql
Emp(empname:text, salary:integer, last_date:timestamp, last_usr:text)
```

Define a trigger that ensures that any time a row is inserted or updated in the table, the current user name and time are stamped into the row. The trigger should also ensure that an employee's name is given and that the salary has a positive value.

The two PostgreSQL builtin functions user() and now() will provide the values that you need for the "stamp".

### Ans


