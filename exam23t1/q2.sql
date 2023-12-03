create or replace view q2 as
select
    given || ' ' || family as name,
    string_agg(id::text, ',') as ids
from customers
group by given, family
having count(*) > 1;