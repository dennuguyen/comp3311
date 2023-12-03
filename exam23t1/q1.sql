create or replace view q1 as
with population as (
    select
        lives_in as suburb,
        count(lives_in) as ncust
    from customers
    group by lives_in
)
select
    suburb,
    ncust
from population
where ncust = (select max(ncust) from population);