
    
    

with child as (
    select PRODUCT_ID as from_field
    from LOGISTICS_DEMO.bronze.stg_customer_orders
    where PRODUCT_ID is not null
),

parent as (
    select product_id as to_field
    from LOGISTICS_DEMO.None.products
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


