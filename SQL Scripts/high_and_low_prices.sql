SELECT 
    og.[commodity],
    MAX(CAST(og.[close] AS FLOAT)) AS max_close,
    MIN(CAST(og.[close] AS FLOAT)) AS min_close,
    max_data.max_close_date,
    min_data.min_close_date
FROM 
    [OilGasDB].[dbo].[all_fuels_data] AS og
OUTER APPLY (
    SELECT TOP 1 [date] AS max_close_date
    FROM [OilGasDB].[dbo].[all_fuels_data]
    WHERE [commodity] = og.[commodity]
    ORDER BY CAST([close] AS FLOAT) DESC
) AS max_data
OUTER APPLY (
    SELECT TOP 1 [date] AS min_close_date
    FROM [OilGasDB].[dbo].[all_fuels_data]
    WHERE [commodity] = og.[commodity]
    ORDER BY CAST([close] AS FLOAT) ASC
) AS min_data
GROUP BY 
    og.[commodity],
    max_data.max_close_date,
    min_data.min_close_date;
