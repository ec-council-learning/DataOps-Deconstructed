
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select warehouse_name
from LOGISTICS_DEMO.gold.daily_inventory_kpis
where warehouse_name is null



  
  
      
    ) dbt_internal_test