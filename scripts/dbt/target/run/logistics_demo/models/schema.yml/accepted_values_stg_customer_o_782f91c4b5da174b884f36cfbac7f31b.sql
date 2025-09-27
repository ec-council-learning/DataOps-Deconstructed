
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        SALES_CHANNEL as value_field,
        count(*) as n_records

    from LOGISTICS_DEMO.bronze.stg_customer_orders
    group by SALES_CHANNEL

)

select *
from all_values
where value_field not in (
    'online','retail','wholesale'
)



  
  
      
    ) dbt_internal_test