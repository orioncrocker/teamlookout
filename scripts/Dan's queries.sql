--- Practicing how to join crashes and weather
select crashid, weather.summary
from i5north_bycrash crashes join weather on (crashes.date + crashes.hour = weather.datetime)
group by crashid, weather.summary


--- Count number of hours with each weather type
select summary as WeatherSummary, count(datetime) as CountOfHoursWithWeather1Type
into CountOfHoursWithWeatherType
from weather 
where summary <> ''
group by summary 
order by summary


--- Get Crashes/hour with each weather type
select milepost, weather1, (CrashCount / countofhourswithweathertype.countofhourswithweather1type) as CrashesPerHour
into CrashesPerHourByWeatherByMilepost
from (
	select milepost, (count(crashid) + 0.0000001) as CrashCount, weather1
	from i5north_bycrash 
	group by milepost, weather1
	order by milepost) as CrashCounts join countofhourswithweathertype on weather1 = weathersummary
order by milepost, weather1
	