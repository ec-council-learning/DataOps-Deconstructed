
    
    

with all_values as (

    select
        MOVEMENT_TYPE as value_field,
        count(*) as n_records

    from LOGISTICS_DEMO.bronze.stg_inventory_movements
    group by MOVEMENT_TYPE

)

select *
from all_values
where value_field not in (
    'replenishment','outbound','adjustment'
)


