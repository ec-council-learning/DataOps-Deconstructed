with relation_columns as (

        
        select
            cast('MOVEMENT_ID' as TEXT) as relation_column,
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
            cast('MOVEMENT_DATE' as TEXT) as relation_column,
            cast('DATE' as TEXT) as relation_column_type
        union all
        
        select
            cast('QUANTITY' as TEXT) as relation_column,
            cast('NUMBER' as TEXT) as relation_column_type
        union all
        
        select
            cast('MOVEMENT_TYPE' as TEXT) as relation_column,
            cast('VARCHAR' as TEXT) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'MOVEMENT_DATE'
            and
            relation_column_type not in ('DATE')

    )
    select *
    from test_data