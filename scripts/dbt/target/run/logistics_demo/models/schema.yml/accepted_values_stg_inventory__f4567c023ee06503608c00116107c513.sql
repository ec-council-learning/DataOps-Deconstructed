
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

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



  
  
      
    ) dbt_internal_test