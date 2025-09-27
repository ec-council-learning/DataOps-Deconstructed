
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stock_turnover_ratio
from LOGISTICS_DEMO.gold.daily_inventory_kpis
where stock_turnover_ratio is null



  
  
      
    ) dbt_internal_test