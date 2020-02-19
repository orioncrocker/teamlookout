create table weather (
	id			INT NOT NULL PRIMARY key,
	lat         FLOAT(12),
	long 		FLOAT(12),
	datetime	TIMESTAMP,
	summary		VARCHAR(20),
	precipIntensity FLOAT(5),		-- The lowest number I've seen is 0.0007
	temperature FLOAT(6),		-- Fahrenheit, as we selected in API Requests
	apparentTemperature FLOAT(6),
	humidity	FLOAT(4),
	windSpeed	FLOAT(4),
	windGust	FLOAT(4),
	cloudCover	FLOAT(4),
	uvIndex		INT,
	visibility	INT
)
