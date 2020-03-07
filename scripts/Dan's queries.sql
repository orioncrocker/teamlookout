--- Practicing how to join crashes and weather
select crashid, weather.summary
from i5north_bycrash crashes join weather on (crashes.date + crashes.hour = weather.datetime)
group by crashid, weather.summary


-- Count crashes per milepost to normalize some data
select count(distinct crashid) as crashCount, milepost, 'North' as direction
into crashesperMilepost 
from i5north_bycrash 
group by milepost
order by milepost;
-- ...and add Southbound
insert into crashesperMilepost
select count(distinct crashid)as crashCount, milepost, 'South' as direction
from i5south_bycrash 
group by milepost
order by milepost;
-- Sanity check... there should be 694 unique crashes
select sum(crashCount) from crashesperMilepost;



--- Count number of hours with each weather type
select summary as WeatherSummary, count(datetime) as CountOfHoursWithWeather1Type
into CountOfHoursWithWeatherType
from weather 
where summary <> ''
group by summary 
order by summary


--- Get Crashes/hour with each weather type
select milepost, weather1, 'North' as direction, (1000 * CrashCount / countofhourswithweathertype.countofhourswithweather1type) as CrashesPerThousandHours
into CrashesPerHourByWeatherByMilepost
from (
	select milepost, (count(distinct crashid) + 0.0000000001) as CrashCount, weather1
	from i5north_bycrash 
	group by milepost, weather1
	order by milepost) as CrashCounts join countofhourswithweathertype on weather1 = weathersummary
order by milepost, weather1;
--- ...and Southbound
insert into CrashesPerHourByWeatherByMilepost
select milepost, weather1, 'South' as direction, 
	(1000 * CrashCount / countofhourswithweathertype.countofhourswithweather1type) as CrashesPerThousandHours
from (
	select milepost, (count(distinct crashid) + 0.0000000001) as CrashCount, weather1
	from i5south_bycrash 
	group by milepost, weather1
	order by milepost) as CrashCounts join countofhourswithweathertype on weather1 = weathersummary
order by milepost, weather1;
---



--- This tried and failed to find "hotspots" for specific weather types. There should be 
--- some calculation that normalizes a number of crashes using the avg crashes for that 
--- weather and the avg crashes at that milepost. But... I never found it.
select milepost, weather1, direction, (byWeather.CrashesPerThousandHours / byMilepost.crashCount) as correctedCrashCount
into crashesperhourcorrectedbymilepost
from CrashesPerHourByWeatherByMilepost as byWeather natural join crashesperMilepost as byMilepost
order by milepost, direction;

	

--- Count number of hours with each visibility level
select visibility, count(datetime) as CountOfHours
into CountOfHoursWithVisibilityLevel
from weather 
where visibility is not null
group by visibility
order by visibility


--- Get Crashes/hour with each visibility level
select milepost, visibility, 'North' as direction, 
	(1000 * CrashCount / CountOfHoursWithVisibilityLevel.CountOfHours) as CrashesPerThousandHours
into CrashesPerHourByVisibilityLevelAndMilepost
from (
	select milepost, (count(distinct crashid) + 0.0000001) as CrashCount, visibility
	from i5north_bycrash 
	group by milepost, visibility
	order by milepost) as CrashCounts natural join CountOfHoursWithVisibilityLevel
order by milepost, visibility;
--- add Southbound
insert into CrashesPerHourByVisibilityLevelAndMilepost
select milepost, visibility, 'South' as direction, 
	(1000 * CrashCount / CountOfHoursWithVisibilityLevel.CountOfHours) as CrashesPerThousandHours
from (
	select milepost, (count(distinct crashid) + 0.0000001) as CrashCount, visibility
	from i5south_bycrash 
	group by milepost, visibility
	order by milepost) as CrashCounts natural join CountOfHoursWithVisibilityLevel
order by milepost, visibility;
