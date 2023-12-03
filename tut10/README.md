# Week10 Tutorial - Relational Algebra, Transaction Processing

## Q1

Relational algebra operators can be composed. What precisely does this mean? And why is it important?

### Ans

Operators can be chained so that more complex logic can be built.

Chaining = result of an operator can be used as an argument for another operator.

## Q2

The natural join ( R Join S ) joins two tables on their common attributes. Consider a theta-join ( R Join[C] S ) where the join condition C is a conjunction of R.A = S.A for each attribute A appearing in the schemas of both R and S (i.e. it joins on the common attributes). What is the difference between the above natural join and theta join?

### Ans

Natural join will join attributes with the same name in each relationship.

Theta join allows arbitrary comparison.

## Q3

The definition of relational algebra in lectures was based on sets of tuples. In practice, commercial relational database management systems deal with bags (or multisets) of tuples.

Consider the following relation that describes a collection of PCs

```
PCs
Model   Speed   RAM Disk    Price
1001    700     64  10      799
1002    1500    128 60      2499
1003    1000    128 20      1499
1004    1000    256 40      1999
1005    700     64  30      999
```

Consider a projection of this relation on the processor speed attribute, i.e. Proj[speed](PCs).

- What is the value of the projection as a set?
- What is the value of the projection as a bag?
- What is the average speed if the projection is a set?
- What is the average speed if the projection is a bag?
- Is the minimum/maximum speed different between the bag and set representation?

### Ans


- What is the value of the projection as a set?
    - {700, 1000, 1500}
- What is the value of the projection as a bag?
    - {700, 700, 1000, 1000, 1500}
- What is the average speed if the projection is a set?
    - 1067
- What is the average speed if the projection is a bag?
    - 980
- Is the minimum/maximum speed different between the bag and set representation?
    - No

## Q4

Consider the following two relations:

```
R                       S
A	B	C               B	C
a1	b1	c1              b1	c1
a1	b2	c2              b2	c2
a2	b1	c1              
```

Give the relation that results from each of the following relational algebra expressions on these relations:
- `R Div S`
- `R Div (Sel[B != b1](S))`
- `R Div (Sel[B != b2](S))`
- `(R × S) - (Sel[R.C=S.C](R Join[B=B] S)`

### Ans

- `R Div S = `
    ```
    A
    a1
    ```
- `R Div (Sel[B != b1](S)) = `
    ```
    A
    a1
    ```
- `R Div (Sel[B != b2](S)) = `
    ```
    A
    a1
    a2
    ```
- `(R × S) - (Sel[R.C=S.C](R Join[B=B] S)) = `
    ```
    R Join[B=B] S = a1 b1 c1 b1 c1
                    a1 b2 c2 b2 c2
                    a2 b1 c1 b1 c1

    Sel[R.C=S.C](R Join[B=B] S) = a1 b1 c1 b1 c1
                                  a1 b2 c2 b2 c2
                                  a2 b1 c1 b1 c1

    R × S = a1 b1 c1 b1 c1
            a1 b1 c1 b2 c2
            a1 b2 c2 b1 c1
            a1 b2 c2 b2 c2
            a2 b1 c1 b1 c1
            a2 b1 c1 b2 c2
    
    (R × S) - (Sel[R.C=S.C](R Join[B=B] S)) = a1 b1 c1 b2 c2
                                              a1 b2 c2 b1 c1
                                              a2 b1 c1 b2 c2
    ```

## Q5

Consider two relations R1 and R2, where R1 contains N1 tuples and R2 contains N2 tuples, and N1 > N2 > 0. Give the minimum and maximum possible sizes (in tuples) for the result relation produced by each of the following relational algebra expressions. In each case state any assumptions about the schemas of R1 and R2 that are needed to make the expression meaningful.
- `R1 Union R2`
- `R1 Intersect R2`
- `R1 - R2`
- `R1 × R2`
- `Sel[a=5](R1)`
- `Proj[a](R1)`
- `R1 Div R2`

### Ans

- `Range(R1 Union R2) = [N1, N1+N2]`
- `Range(R1 Intersect R2) = [0, N2]`
- `Range(R1 - R2) = [N1-N2, N1]`
- `Range(R1 × R2) = [N1*N2, N1*N2]`
- `Range(Sel[a=5](R1)) = [0, N1]`
- `Range(Proj[a](R1)) = [1, N1]`
- `Range(R1 Div R2) = [0, floor(N1/N2)]`

## Q6

Let A and B be two arbitrary relations. In terms of the keys of A and B, state the keys for each of the following RA expressions. Assume in each case that A and B meet the requirements of the operation (e.g. they are union-compatible for the Union and Intersect operations).
- `Sel[cond](A),   where cond is any condition`
- `Proj[attrs](A),   where attrs is any set of atributes`
- `A × B`
- `A Union B`
- `A Intersect B`
- `A - B`
- `A Div B`

### Ans

- `Sel[cond](A),   where cond is any condition`
    - Any subset of A will inherit the candidate keys of A
- `Proj[attrs](A),   where attrs is any set of atributes`
    - Project includes key of A if key was included in projection attributes.
- `A × B`
    - Every combination of candidate key for A and B is a candidate key for product.
- `A Union B`
    - Candidate key may be candidate key of A or B or the entire set of attributes.
- `A Intersect B`
    - Any subset of A will inherit the candidate keys of A
- `A - B`
    - Any subset of A will inherit the candidate keys of A
- `A Div B`
    - Division is selection then projection operations.

## Q7

Consider the following relational schema:

```
Suppliers(sid, sname, address)
Parts(pid, pname, colour)
Catalog(supplier, part, cost)
```

Assume that the ids are integers, that cost is a real number, that all other attributes are strings, that the supplier field is a foreign key containing a supplier id, and that the part field is a foreign key containing a part id. Write a relational algebra expression to answer each of the following queries:

1. Find the names of suppliers who supply some red part.
1. Find the sids of suppliers who supply some red or green part.
1. Find the sids of suppliers who supply some red part or whose address is 221 Packer Street.
1. Find the sids of suppliers who supply some red part and some green part.
1. Find the sids of suppliers who supply every part.
1. Find the sids of suppliers who supply every red part.
1. Find the sids of suppliers who supply every red or green part.
1. Find the sids of suppliers who supply every red part or supply every green part.
1. Find the pids of parts that are supplied by at least two different suppliers.
1. Find pairs of sids such that the supplier with the first sid charges more for some part than the supplier with the second sid.
1. Find the pids of the most expensive part(s) supplied by suppliers named "Yosemite Sham".
1. Find the pids of parts supplied by every supplier at a price less than 200 dollars (if any supplier either does not supply the part or charges more than 200 dollars for it, the part should not be selected).

### Ans

1. ```
    SelParts = Proj[pid](Sel[colour='red'](Parts))
    SelSuppliers = Proj[supplier](SelParts Join[pid = part] Catalog)
    Answer = Proj[sname](SelSuppliers Join[sid = supplier](Suppliers) Suppliers)
    ```
1. ```
    SelParts = Proj[pid](Sel[colour='red' OR colour='green'](Parts))
    Answer = Proj[supplier](SelParts Join[SelParts.pid = part] Catalog)
    ```
1. ```
    SelParts = Proj[pid](Sel[colour='red'](Parts))
    SuppliersByPart = Proj[supplier](SelParts Join[pid = part] Catalog) 
    SuppliersByStreet = Proj[sid](Sel[address='221 Packer Street'](Suppliers))
    Answer = SuppliersByPart Union SuppliersByStreet
    ```
1. ```
    RedParts = Proj[pid](Sel[colour='red'](Parts))
    GreenParts = Proj[pid](Sel[colour='green'](Parts))
    RedSuppliers = Proj[supplier](RedParts Join[pid = part] Catalog)
    GreenSuppliers = Proj[supplier](GreenParts Join[pid = part] Catalog)
    Answer = RedSuppliers Intersect GreenSuppliers
    ```
1. ```
    AllParts = Proj[pid](Parts)
    PartSuppliers = Proj[supplier, part](Catalog)
    Answer = PartSuppliers / AllParts
    ```
1. ```
    SelParts = Proj[pid](Sel[colour='red'](Parts))
    PartSuppliers = Proj[supplier, pid](Catalog)
    Answer = PartSuppliers / SelParts
    ```
1. ```
    SelParts = Proj[pid](Sel[colour='red' OR colour='green'](Parts))
    PartSuppliers = Proj[supplier, pid](Catalog)
    Answer = PartSuppliers / SelParts
    ```
1. ```
    RedParts = Proj[pid](Sel[colour='red'](Parts))
    GreenParts = Proj[pid](Sel[colour='green'](Parts))
    PartSuppliers = Proj[supplier, pid](Catalog)
    RedSuppliers = PartSuppliers / RedParts
    GreenSuppliers = PartSuppliers / GreenParts
    Answer = RedSuppliers Union GreenSuppliers
    ```
1. ```
    C1 = Catalog
    C2 = Catalog
    Answer = Proj[C1.part](Sel[C1.supplier != C2.supplier](C1 join[C1.part = C2.part] C2))
    ```
1. ```
    ```

## Q10

Give a brief definition for each of the following terms:
1. transaction
1. serializable schedule
1. conflict-serializable schedule
1. view-serializable schedule

### Ans

1. transaction: An execution of a program that performs an action that is treated atomically.
1. serializable schedule: A schedule over a set of transactions that produces a result that is the same as its serial execution of the transactions.
1. conflict-serializable schedule: A schedule that is conflict-equivalent to some serial schedule where:
    - Involve same set of actions and
    - Order every pair of conflicting actions the same way
1. view-serializable schedule: A schedule that is view-equivalent to some serial schedule where:
    - Initial value of any object is read by same transaction in both schedules and
    - Final value of any object is written by same transaction in both schedules and
    - Any shared object is written-then-read by same pair of transactions in both schedules

## Q11

Draw the precedence graph for the following schedule (where C means "commit"):

```
T1:      R(A) W(Z)                C
T2:                R(B) W(Y)        C
T3: W(A)                     W(B)     C
```

### Ans

```
A: T3->T1
B: T2->T3
Y:
Z:
Therefore: T2->T3 ->T1
```

## Q12

Consider the following incomplete schedule S:

```
T1: R(X) R(Y) W(X)           W(X)
T2:                R(Y)           R(Y)
T3:                     W(Y)
```

- Determine (by using a precedence graph) whether the schedule is conflict-serializable
- Modify S to create a complete schedule that is conflict-serializable

### Ans

```
X: T1->T1 (ignore self)
Y: T1->T3, T2->T3, T3->T2
```

There is a cycle (T2->T3->T2) so schedule is not conflict-serialisable.

Need abort actions to abort either T2 or T3 to make schedule conflict-serialisable.

## Q13

For each of the following schedules, state whether it is conflict-serializable and/or view-serializable. If you cannot decide whether a schedule belongs to either class, explain briefly. The actions are listed in the order they are scheduled, and prefixed with the transaction name.
1. `T1:R(X) T2:R(X) T1:W(X) T2:W(X)`
1. `T1:W(X) T2:R(Y) T1:R(Y) T2:R(X)`
1. `T1:R(X) T2:R(Y) T3:W(X) T2:R(X) T1:R(Y)`
1. `T1:R(X) T1:R(Y) T1:W(X) T2:R(Y) T3:W(Y) T1:W(X) T2:R(Y)`
1. `T1:R(X) T2:W(X) T1:W(X) T3:W(X)`

### Ans

1. `T1:R(X) T2:R(X) T1:W(X) T2:W(X)`
    - Is conflict-serialisable?
        - Precedence graph: T1->T2, T2->T1
        - Not conflict-serialisable because cyclic
    - Is view-serialisable?
        - Consider serial schedule: `T1:R(X) T1:W(X) T2:R(X) T2:W(X)`
        - X is NOT written-then-read by same pair of transactions in both schedules
        - Not view-serialisable
1. `T1:W(X) T2:R(Y) T1:R(Y) T2:R(X)`
    - Is conflict-serialisable?
        - Precedence graph: T1->T2
        - Yes because no cycles
    - Is view-serialisable?
        - Yes because conflict-serialisable
1. `T1:R(X) T2:R(Y) T3:W(X) T2:R(X) T1:R(Y)`
    - Is conflict-serialisable?
        - Precedence graph: T1->T3, T3->T2
        - Yes because no conflicts
    - Is view-serialisable?
        - Yes because conflict-serialisable
1. `T1:R(X) T1:R(Y) T1:W(X) T2:R(Y) T3:W(Y) T1:W(X) T2:R(Y)`
    - Is conflict-serialisable?
        - Precedence graph: T1->T3, T2->T3, T3->T2
        - No because cycle T2->T3->T2
    - Is view-serialisable?
        - Consider serial schedule: `T1:R(X) T1:R(Y) T1:W(X) T1:W(X) T2:R(Y) T2:R(Y) T3:W(Y)`
        - X is written-then-read by same pair of transactions in both schedules
        - Y is NOT written-then-read by same pair of transactions in both schedules
        - No
1. `T1:R(X) T2:W(X) T1:W(X) T3:W(X)`
    - Is conflict-serialisable?
        - Precedence graph: T1->T2, T2->T1, T2->T3, T1->T3
        - No because cycle
    - Is view-serialisable?
        - Consider serial schedule: `T1:R(X) T1:W(X) T2:W(X) T3:W(X)`
        - X is written-then-read by same pair of transaction in both schedules
        - Yes

<blockquote>
Process for determining conflict-serialisability:

1. Draw precedence graph
    - Don't draw edge if it's read followed by read operation
1. If there are cycles then is conflict-serialisable
</blockquote>

<blockquote>
Process for determining view-serialisability:

1. If satisfies following:
    - Initial value of any object is read by same transaction in both schedules and
    - Final value of any object is written by same transaction in both schedules and
    - Any shared object is written-then-read by same pair of transactions in both schedules
1. Or is conflict-serialisable so must be view-serialisable
</blockquote>

## Q14

Is the following schedule serializable? Show your working.

```
T1:             R(X)W(X)W(Z)        R(Y)W(Y)
T2: R(Y)W(Y)R(Y)            W(Y)R(X)        W(X)R(V)W(V)
```

### Ans

Consider precedence graph:
```
X: T1->T2
Y: T2->T1
Z: 
V: 
```

Schedule is not conflict-serialisable because there is a cycle T1->T2->T1.

Consider serial schedule:
```
T1: R(X)W(X)W(Z)R(Y)W(Y)
T2:                     R(Y)W(Y)R(Y)W(Y)R(X)W(X)R(V)W(V)
```

Check if any shared object is written-then-read by same pair of transactions in both schedules:
- X yes
- Y yes
- Z is not shared
- V yes
Therefore is view-serialisable.
