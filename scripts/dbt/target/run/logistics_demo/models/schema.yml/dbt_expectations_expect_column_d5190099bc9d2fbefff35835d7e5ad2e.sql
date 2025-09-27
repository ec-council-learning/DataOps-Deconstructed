
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  with relation_columns as (

        
        select
            cast('ORDER_ID' as TEXT) as relation_column,
            cast('VARCHAR' as TEXT) as relation_column_type
        union all
        
        select
            cast('PRODUCT_ID' as TEXT) as relation_column,
            cast('VARCHAR' as TEXT) as relation_column_type
        union all
        
        select
            cast('WAREHOUSE_ID' as TEXT) as relation_column,
            cast('VARCHAR' as TEXT) as relation_column_type
        union all
        
        select
            cast('ORDER_DATE' as TEXT) as relation_column,
            cast('DATE' as TEXT) as relation_column_type
        union all
        
        select
            cast('QUANTITY' as TEXT) as relation_column,
            cast('NUMBER' as TEXT) as relation_column_type
        union all
        
        select
            cast('SALES_CHANNEL' as TEXT) as relation_column,
            cast('VARCHAR' as TEXT) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'ORDER_DATE'
            and
            relation_column_type not in ('DATE')

    )
    select *
    from test_data
  
  
      
    ) dbt_internal_test