SELECT
    column_name,
    is_nullable,
    data_type
FROM
    {catalog}.INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_SCHEMA = '{schema}'
    AND TABLE_NAME = '{table_name}'
