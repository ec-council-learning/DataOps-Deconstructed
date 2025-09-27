
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ORDER_ID
from LOGISTICS_DEMO.bronze.stg_customer_orders
where ORDER_ID is null



  
  
      
    ) dbt_internal_test