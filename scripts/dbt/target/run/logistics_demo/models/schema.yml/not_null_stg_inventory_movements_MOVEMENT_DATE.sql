
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select MOVEMENT_DATE
from LOGISTICS_DEMO.bronze.stg_inventory_movements
where MOVEMENT_DATE is null



  
  
      
    ) dbt_internal_test