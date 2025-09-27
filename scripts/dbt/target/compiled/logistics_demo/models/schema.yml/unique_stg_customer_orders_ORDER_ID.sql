
    
    

select
    ORDER_ID as unique_field,
    count(*) as n_records

from LOGISTICS_DEMO.bronze.stg_customer_orders
where ORDER_ID is not null
group by ORDER_ID
having count(*) > 1


