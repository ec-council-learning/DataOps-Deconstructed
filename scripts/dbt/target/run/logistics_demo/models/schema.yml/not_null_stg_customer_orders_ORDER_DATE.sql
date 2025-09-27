
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ORDER_DATE
from LOGISTICS_DEMO.bronze.stg_customer_orders
where ORDER_DATE is null



  
  
      
    ) dbt_internal_test