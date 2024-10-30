SELECT 
	   [ticker]
      ,[commodity]
      ,YEAR([date]) Year
	  , AVG (CAST([open] AS FLOAT)) [Average Open]
	  ,AVG (CAST([close] AS FLOAT)) [Average Close]
	 , AVG (CAST([volume] AS FLOAT)) [Average Volume]
	 ,SUM(CAST([volume] AS FLOAT )) [Total Volume]

  FROM [OilGasDB].[dbo].[all_fuels_data]
  GROUP BY
	[ticker],[commodity],YEAR([date])
  ORDER BY 
    year;