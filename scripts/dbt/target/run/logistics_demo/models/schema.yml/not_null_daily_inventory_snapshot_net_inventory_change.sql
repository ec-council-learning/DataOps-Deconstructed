
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select net_inventory_change
from LOGISTICS_DEMO.silver.daily_inventory_snapshot
where net_inventory_change is null



  
  
      
    ) dbt_internal_test