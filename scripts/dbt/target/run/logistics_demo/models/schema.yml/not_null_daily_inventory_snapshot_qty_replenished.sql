
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select qty_replenished
from LOGISTICS_DEMO.silver.daily_inventory_snapshot
where qty_replenished is null



  
  
      
    ) dbt_internal_test