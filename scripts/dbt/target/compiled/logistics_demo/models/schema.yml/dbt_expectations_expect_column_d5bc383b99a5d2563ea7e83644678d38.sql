






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and QUANTITY >= 1 and QUANTITY <= 100
)
 as expression


    from LOGISTICS_DEMO.bronze.stg_customer_orders
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







