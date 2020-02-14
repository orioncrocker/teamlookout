CREATE TABLE detector (
	highwayid INT NOT NULL,
	stationid INT NOT NULL,
	detectorid INT,
	lane_num INT,
	agency_lane INT,
	location varchar(100),
	milepost FLOAT
)
