
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select PRODUCT_ID
from LOGISTICS_DEMO.bronze.stg_customer_orders
where PRODUCT_ID is null



  
  
      
    ) dbt_internal_test