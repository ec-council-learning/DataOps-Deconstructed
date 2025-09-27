
    
    

select
    MOVEMENT_ID as unique_field,
    count(*) as n_records

from LOGISTICS_DEMO.bronze.stg_inventory_movements
where MOVEMENT_ID is not null
group by MOVEMENT_ID
having count(*) > 1


