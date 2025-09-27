
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select QUANTITY
from LOGISTICS_DEMO.bronze.stg_customer_orders
where QUANTITY is null



  
  
      
    ) dbt_internal_test