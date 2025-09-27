
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select product_id
from LOGISTICS_DEMO.silver.daily_inventory_snapshot
where product_id is null



  
  
      
    ) dbt_internal_test