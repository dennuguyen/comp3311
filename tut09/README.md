# Week09 Tutorial - Relational Design Theory

<blockquote>
  Notation: in the relational schemas below, primary key attributes are underlined (e.g. pk), foreign key attributes are shown in italic font (e.g. fk) and primary key attributes that are also foreign keys are underlined and in italic font (e.g. pk+fk).

  Example:

  ```
  Student(id, name, degreeCode)
  Degree(code, name, requirements)
  Subject(code, name, syllabus)
  Marks(studentId, subjectCode, teachingTerm, mark)
  ```

  In their respective relations, the student id, the degree code and the subject code are primary keys. In the Student relation, the degree code is a foreign key. In the Marks relation, the three attributes student id, subject code and teaching term together form the primary key; the first two (student id and subject code) are also foreign keys. 
</blockquote>

## Q1

Functional dependencies.
1. What functional dependencies are implied if we know that a set of attributes X is a candidate key for a relation R?
1. What functional dependencies can we infer do not hold by inspection of the following relation?
    ```
    A B C
    a 1 x
    b 2 y
    c 1 z
    d 2 x
    a 1 y
    b 2 z
    ```
1. Suppose that we have a relation schema R(A,B,C) representing a relationship between two entity sets E and F with keys A and B respectively, and suppose that R has (at least) the functional dependencies A → B and B → A. Explain what this tells us about the relationship between E and F.

### Ans

1.
    - X -> R(X)
    - X functionally determines all other attributes of R
1.
    - Pivot A(a)
        - Select (a,1,x) and (a,1,y)
        - A->C does not hold
    - Pivot B(1)
        - Select (a,1,x) and (c,1,z)
        - B->A does not hold
        - B->C does not hold
    - Pivot C(x)
        - Select (a,1,x) and (d,2,x)
        - C->A does not hold
        - C->B does not hold
    - Pivot AB(a,1)
        - Select (a,1,x) and (a,1,y)
        - AB->C does not hold
    - Can't find pivot for AC
    - Can't find pivot for BC
1.
    - If A->B and B->A then there is a 1:1 relationship between A and B.
    - There is a value A in R that has exactly one corresponding B in R, and vice versa.

<blockquote>
Process for determining which FDs do not hold:

1. Pick a tuple and a pivot (column) in the tuple.
1. Find all other tuples with the same pivot.
1. If any columns in the tuple varies, then the pivot and the target column cannot form a functional dependency for their respective attributes.
1. Repeat above steps but add an additional attribute/column to pivot.

Keys need to map unique values
</blockquote>

## Q2

Consider the relation R(A,B,C,D,E,F,G) and the set of functional dependencies F = { A → B, BC → F, BD → EG, AD → C, D → F, BEG → FA } compute the following:
1. A+
1. ACEG+
1. BD+

### Ans

1. A+
    - Given {A}
    - Using A->B gives {A,B}
    - Therefore A+ = {A,B}
1. ACEG+
    - Given {A,C,E,G}
    - Using A->B gives {A,B,C,E,G}
    - Therefore ACEG+ = {A,B,C,E,G}
1. BD+
    - Given {B,D}
    - Using D->F gives {B,D,F}
    - Using BD->EG gives {B,D,F,E,G}
    - Using BEG->FA gives {B,D,E,F,G,F,A} = {A,B,D,E,F,G}
    - Using AD->C gives {A,B,D,E,F,G,C}
    - Therefore BD+ = {A,B,C,D,E,F,G}

Note that BD is a candidate key because its closure (BD+) contains all the attributes of R

<blockquote>
    X+ is closure i.e. the complete set of attributes that are functionally determined by X according to a set of functional dependencies F.
</blockquote>

## Q3

Consider the relation R(A,B,C,D,E) and the set set of functional dependencies F = { A → B, BC → E, ED → A }
1. List all of the candidate keys for R.
1. Is R in third normal form (3NF)?
1. Is R in Boyce-Codd normal form (BCNF)?

### Ans

1. Candidate keys for R
    - Case 1:
        - Start with ABCDE
        - Reducing with A->B gives ACDE
        - Reducing with ED->A gives CDE
        - Therefore CDE is a potential candidate key
    - Case 2:
        - Start with ABCDE
        - Reducing with BC->E gives ABCD
        - Reducing with A->B gives ACD
        - Therefore ACD is a potential candidate key
    - Case 3:
        - Start with ABCDE
        - Reducing with ED->A gives BCDE
        - Reducing with BC->E gives BCD
        - Therefore BCD is a potential candidate key
    - No other pathways to be seen by inspection
    - Therefore ACD, BCD, CDE are candidate keys
- Is R 3NF?
    - Yes because RHS of all FDs (i.e. B,E,A) are elements of candidate keys.
- Is R BCNF?
    - No because LHS of any of FDs (i.e. A, BC, ED) does not contains candidate keys.

Note that max number of candidate keys is `2^(num_attr - num_fd)`.

<blockquote>
Process for determining candidate keys in R:

1. Start with the full set of attributes (X+) of R.
1. Apply FD to X+ s.t. for A->B if A is present in X+ then remove B from X+.
1. Keep applying FDs until X+ cannot be further reduced.
    - X+ is a candidate key of R when no more attributes can be removed (but they can be swapped).
1. Repeat for each applicable FD computation and start. Imagine a tree that we must calculate.
</blockquote>

<blockquote>
Process for determining if R is BCNF:

1. Check if all LHS of FD contains a candidate key set.
</blockquote>

<blockquote>
Process for determining if R is 3NF:

1. Check if all RHS of FD contains an element of any candidate key set.
</blockquote>

## Q4

Consider a relation R(A,B,C,D). For each of the following sets of functional dependencies, assuming that those are the only dependencies that hold for R, do the following:
1. List all of the candidate keys for R.
1. Show whether R is in Boyce-Codd normal form (BCNF)?
1. Show whether R is in third normal form (3NF)?

Sets of functional dependencies:
1. C → D,   C → A,   B → C
1. B → C,   D → A
1. ABC → D,   D → A
1. A → B,   BC → D,   A → C
1. AB → C,   AB → D,   C → A,   D → B
1. A → BCD

### Ans

1. C → D,   C → A,   B → C
    - Candidate keys of R:
        - Case 1:
            - Start with ABCD
            - Reduce with C->D gives ABC
            - Reduce with C->A gives AD
            - Reduce with B->C gives {B}
            - {B} is a potential candidate key
        - Case 2:
            - Start with ABCD
            - Reduce with C->D gives ABC
            - Reduce with B->C gives AB
            - AB is a potential candidate key
            - Disregard since AB is superset of {B}
        - Case 3:
            - Start with ABCD
            - Reduce with C->A gives BCD
            - Reduce with B->C gives {B,D}
            - {B,D} is a potential candidate key
            - Disregard since {B,D} is superset of {B}
        - Case 4:
            - Start with ABCD
            - Reduce with C->A gives BCD
            - Reduce with C->D gives AD
            - Reduce with B->C gives {B}
            - Already computed
        - Case 5:
            - Start with ABCD
            - Reduce with B->C gives ABD
            - ABD is a potential candidate key
            - Disregard since ABD is superset of {B}
        - No other pathways to be seen by inspection.
        - Therefore {B} is a candidate key
    - Is BCNF?
        - No because not all LHS{C->D, C->A, B->C} contains set {B}
    - Is 3NF?
        - No because not all RHS{C->D, C->A, B->C} contains element of {B}
1. B → C,   D → A
    - Candidate keys of R:
        - Case 1:
            - Start with ABCD
            - Reduce with B->C gives ABD
            - Reduce with D->A gives {B,D}
            - {B,D} is a candidate key
        - No other pathways to be seen by inspection
    - Is BCNF?
        - No because not all LHS{B->C, D->A} contains set {B,D}
    - Is 3NF?
        - No because not all RHS{B->C, D->A} contains element of {B,D}
1. ABC → D,   D → A
    - Candidate keys of R:
        - Case 1:
            - Start with ABCD
            - Reduce with ABC->D gives ABC
            - ABC is a potential candidate key
        - Case 2:
            - Start with ABCD
            - Reduce with D->A gives BCD
            - BCD is a potential candidate key
        - No other pathways by inspection
        - Therefore ABC and BCD are candidate keys
    - Is BCNF?
        - No because not all LHS{ABC->D, D->A} contains candidate key set
    - Is 3NF?
        - Yes because all RHS{ABC->D, D->A} contains element of a candidate key
1. A → B,   BC → D,   A → C
    - Candidate keys of R:
        - Case 1:
            - Start with ABCD
            - Reduce with A->B gives ACD
            - Reduce with A->C gives AD
            - AD is a potential candidate key
            - Disregard because AC is superset of A
        - Case 2:
            - Start with ABCD
            - Reduce with BC->D gives ABC
            - Reduce with A->B gives AC
            - AC is a potential candidate key
            - Disregard because AC is superset of A
        - Case 3:
            - Start with ABCD
            - Reduce with BC->D gives ABC
            - Reduce with A->C gives AB
            - Reduce with A->B gives A
            - A is a potential candidate key
        - No other pathways
        - Therefore A are candidate keys
    - Is BCNF?
        - No because not all LHS{A->B, BC->D, A->C} contains candidate key set
    - Is 3NF?
        - No because not all RHS{A->B, BC->D, A->C} contains element of candidate key
1. AB → C,   AB → D,   C → A,   D → B
    - Candidate keys of R:
        - Case 1:
            - Start with ABCD
            - Reduce with AB->C gives ABD
            - Reduce with AB->D gives AB
            - AB is potential candidate key
        - Case 2:
            - Start with ABCD
            - Reduce with AB->C gives ABD
            - Reduce with D->B gives AD
            - AD is potential candidate key
        - Case 3:
            - Start with ABCD
            - Reduce with AB->D gives ABC
            - Reduce with C->A gives AD
            - AD is potential candidate key
        - Case 4:
            - Start with ABCD
            - Reduce with C->A gives BCD
            - Reduce with D->B gives CD
            - CD is potential candidate key
        - No other pathways
        - Therefore AB, AD, AD, CD are candidate keys
    - Is BCNF?
        - No because not all LHS{AB->C, AB->D, C->A, D->B} contains candidate key set
    - Is 3NF?
        - Yes because all RHS{AB->C, AB->D, C->A, D->B} contains element of candidate key
1. A → BCD
    - Candidate keys of R
        - Case 1:
            - Start with ABCD
            - Reduce with A->BCD gives A
            - A is a candidate key
    - Is BCNF?
        - Yes because all LHS{A->BCD} contains candidate key set A
        - or all LHS are superkeys
    - Is 3NF?
        - Yes because all LHS are superkeys

## Q5

Specify the non-trivial functional dependencies for each of the relations in the following Teams-Players-Fans schema and then show whether the overall schema is in BCNF.

```
Team(**name**, captain)
Player(**name**, teamPlayedFor)
Fan(**name**, address)
TeamColours(**teamName**, **colour**)
FavouriteColours(**fanName**, **colour**)
FavouritePlayers(**fanName**, **playerName**)
FavouriteTeams(**fanName**, **teamName**)
```

### Ans

Let:
- Team(name) be A
- Team(captain) be B
- Player(name) be C
- Player(teamPlayedFor) be D
- Fan(name) be E
- Fan(address) be F

FDs:
- A->B
- C->D
- E->F

Note:
- TeamColours has no non-trivial FDs
- FavouriteColours has no non-trivial FDs
- FavouritePlayers has no non-trivial FDs
- FavouriteTeams has no non-trivial FDs

Candidate keys are {A, C, E} by inspection.

Is BCNF because all LHS of {A->B, C->D, E->F} contains a candidate key set.

## Q6

Specify the non-trivial functional dependencies for each of the relations in the following Trucks-Shipments-Stores schema and then show whether the overall schema is in BCNF.

```
Warehouse(**warehouse#**, address)
Source(**trip**, **warehouse**)
Trip(**trip#**, date, truck)
Truck(**truck#**, maxvol, maxwt)
Shipment(**shipment#**, volume, weight, trip, store)
Store(**store#**, storename, address)
```

Let schema be:
```
Warehouse(**A**, B)
Source(**C**, A)
Trip(**C**, D, E)
Truck(**F**, G, H)
Shipment(**I**, J, K, L, M)
Store(**N**, O, P)
```

FDs:
- A->B
- C->A
- C->DE
- F->GH
- I->JKLM
- N->OP

Note:
- Source has no non-trivial FDs

Candidate keys are {A, C, F, I, N} by inspection.

Is BCNF because all LHS of FDs contain a candidate key set.

## Q7

For each of the sets of dependencies in question 4:
1. if R is not already in 3NF, decompose it into a set of 3NF relations
1. if R is not already in BCNF, decompose it into a set of BCNF relations

Sets of functional dependencies:
1. C → D,   C → A,   B → C
1. B → C,   D → A
1. ABC → D,   D → A
1. A → B,   BC → D,   A → C
1. AB → C,   AB → D,   C → A,   D → B
1. A → BCD

### Ans

1. C → D,   C → A,   B → C
    - Candidate keys: {B}
    - Decompose into 3NF
        - {CD, CA, BC}
    - Decompose into BCNF
        - {A, B, C, D}
        - Pick C->D so D=>CD: {ABC, CD}
        - Pick C->A so A=>AC: {AC, BC, CD}
1. B → C,   D → A
    - Candidate keys: {B,D}
    - Decompose into 3NF
        - {BC, DA, BD}
    - Decompose into BCNF
        - {A, B, C, D}
        - Pick B->C so C=>BC: {BC, ABD}
        - Pick D->A so A=>DA: {BC, DA, BD}
1. ABC → D,   D → A
    - Candidate keys: ABC and BCD
    - Decompose into 3NF
        - R already 3NF: {ABCD, DA}
    - Decompose into BCNF
        - {A, B, C, D}
        - Pick D->A so A=>DA: {DA, BCD}
1. A → B,   BC → D,   A → C
    - Candidate keys: A
    - Decompose into 3NF
        - {AB, BCD, AC}
    - Decompose into BCNF
        - {A, B, C, D}
        - Pick BC->D so D=>BCD: {ABC, BCD}
1. AB → C,   AB → D,   C → A,   D → B
    - Candidate keys: AB, AD, AD, CD
    - Decompose into 3NF
        - R already 3NF: {ABC, ABD, CA, DB}
    - Decompose into BCNF
        - {A, B, C, D}
        - Pick D->B so B=>DB: {ACD, DB}
        - Pick C->A so A=>CA: {CA, CD, DB}
1. A → BCD
    - Candidate keys: A
    - Decompose into 3NF
        - R already 3NF: {ABCD}
    - Decompose into BCNF
        - R already BCNF: {ABCD}
    
<blockquote>
Process for 3NF decomposition

1. If there is common LHS then merge FDs together e.g.
    A->B, C->B, D->E => AC->B, D->E
1. Combine FD LHS and RHS into a key e.g.
    AC->B, D->E => ACB, DE
1. If new keys are not connected then join them using the candidate key e.g.
    AB, CD => AB, CD, AC
</blockquote>

<blockquote>
Process for BCNF decomposition

1. For each FD (X->Y) that violates BCNF.
1. Replace Y with XY and merge all other attributes.
</blockquote>

## Q8

Consider (yet another) banking application that contains information about accounts, branches and customers. Each account is held at a specific branch, but a customer may hold more than one account and an account may have more than one associated customer.

Consider an unnormalised relation containing all of the attributes that are relevant to this application:

- acct# - unique account indentifier
- branch# - unique branch identifier
- tfn - unique customer identifier (tax file number)
- kind - type of account (savings, cheque, ...)
- balance - amount of money in account
- city - city where branch is located
- name - customer's name 

i.e. consider the relation R(acct#, branch#, tfn, kind, balance, city, name)

Based on the above description:
1. Devise a suitable set of functional dependencies among these attributes.
1. Using these functional dependencies, decompose R into a set of 3NF relations.
1. State whether the new relations are also in BCNF.

## Q13

Compute a minimal cover for:

F   =   { B → A,  D → A,  AB → D }

### Ans

AB->D = AB->A = B->A

B->A, AB->D = B->D

1. Consider canonical cover:
    {B->A, D->A, AB->D}
1. Eliminate redundant attributes:
    B->A, AB->D = B->D
1. Eliminate redundant dependencies:
    F = {B->A, D->A, AB->D}
      = {D->A, B->D} since B->D, D->A => B->A

Fc = {D->A, B->D}

## Q15

Consider the schema R and set of fds F

R  =  ABCDEFGH
F  =  { ABH → C,  A → DE,  BGH → F,  F → ADH,  BH → GE }

Produce a BCNF decomposition of R.

### Ans

Candidate keys: BH

BCNF decomposition:
1. A->DE violates BCNF so DE=>ADE: {ABCFGH, ADE}
1. Considering ABCFGH:
    1. F->ADH => F->D, F->AH
    1. F->AH violates BCNF so AH=>FAH: {AFH, BCFG}
1. Considered all violated keys, therefore BCNF decomposition is {AFH, BCFG, ADE}

## Q17

Consider the schema R and set of fds F

R  =  ABCDEFGH
F  =  { ABH → C,  A → D,  C → E,  BGH → F,  F → AD,  E → F,  BH → E }
Fc  =  { BH → C,  A → D,  C → E,  F → A,  E → F,  BH → E }

Produce a 3NF decomposition of R.

### Ans

Fc = {BH->CE, A->D, C->E, F->A, E->F}
3NF = {BCHE, AD, CE, FA, EF}
