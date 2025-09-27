






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and stock_turnover_ratio >= 0 and stock_turnover_ratio <= 100
)
 as expression


    from LOGISTICS_DEMO.gold.daily_inventory_kpis
    

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







