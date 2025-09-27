
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_units_shipped
from LOGISTICS_DEMO.gold.daily_inventory_kpis
where total_units_shipped is null



  
  
      
    ) dbt_internal_test