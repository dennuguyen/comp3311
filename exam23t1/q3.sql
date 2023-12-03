create or replace view q3 as
select branches.location as branch
from branches
where branches.location = all(
    select customers.lives_in
    from customers
    inner join held_by on held_by.customer = customers.id
    inner join accounts on accounts.id = held_by.account
    where branches.id = accounts.held_at
);