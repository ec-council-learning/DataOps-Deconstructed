
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select warehouse_id
from LOGISTICS_DEMO.silver.daily_inventory_snapshot
where warehouse_id is null



  
  
      
    ) dbt_internal_test