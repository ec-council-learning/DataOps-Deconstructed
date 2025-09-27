
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select QUANTITY
from LOGISTICS_DEMO.bronze.stg_inventory_movements
where QUANTITY is null



  
  
      
    ) dbt_internal_test