
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select report_date
from LOGISTICS_DEMO.gold.daily_inventory_kpis
where report_date is null



  
  
      
    ) dbt_internal_test