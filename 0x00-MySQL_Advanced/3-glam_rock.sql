-- lists all bands with glamrock as their main style, ranked by longevity
SELECT
    band_name,
    CASE
	WHEN split IS NULL OR split > 2022 THEN 2022 - formed
	ELSE split - formed
    END AS lifespan
FROM metal_bands WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
