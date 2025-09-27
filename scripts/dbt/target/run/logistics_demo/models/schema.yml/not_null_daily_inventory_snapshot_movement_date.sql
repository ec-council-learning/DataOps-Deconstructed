
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select movement_date
from LOGISTICS_DEMO.silver.daily_inventory_snapshot
where movement_date is null



  
  
      
    ) dbt_internal_test