create or replace function q4(_acctID integer) returns text
as $$
declare
    acct record;
    cust record;
    trns record;
    trns_bal numeric := 0;
begin
    select * from accounts where accounts.id = _acctID into acct;
    if acct is null then
        return 'No such account';
    end if;

    -- Get customer using account ID.
    select * from customers
    inner join held_by on held_by.customer = customers.id
    inner join accounts on accounts.id = held_by.account
    where accounts.id = acct.id
    into cust;
    if cust is null then
        return 'No such customer';
    end if;

    for trns in (
        select * from transactions where transactions.actor = cust.id
    ) loop
        if trns.ttype = 'deposit' then
            trns_bal := trns_bal + trns.amount;
        elsif trns.ttype = 'withdrawal' then
            trns_bal := trns_bal - trns.amount;
        elsif trns.ttype = 'transfer' then
            if trsn.source = acct.id then
                trns_bal := trns_bal - trns.amount;
            elsif trns.dest = acct.id then
                trns_bal := trns_bal + trns.amount;
            end if;
        end if;
    end loop;

    if trns_bal != acct.balance then
        return 'Mismatch: calculated balance ' || trns_bal || ', stored balance ' || acct.balance;
    else
        return 'OK';
    end if;
end;
$$ language plpgsql;
