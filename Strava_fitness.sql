select * from activity;

SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Activity'
ORDER BY ORDINAL_POSITION;

SELECT COUNT(*) AS TotalRows
FROM Activity;

SELECT TOP 5 *
FROM Activity;

SELECT ROUND(TotalDistance, 2) AS TotalDistance
FROM Activity;

SELECT COUNT(*) AS TotalRows
FROM sleep;

SELECT TOP 5 *
FROM sleep;

SELECT COUNT(*) AS TotalRows
FROM Weight;

SELECT TOP 5 *
FROM Weight;

1. What is the average numberof steps users record perday?

SELECT 
    ROUND(AVG(TotalSteps), 0) AS AverageDailySteps
FROM Activity;

2.What is the average daily distance traveled and calories burned?

SELECT
    ROUND(AVG(TotalDistance), 2) AS AverageDailyDistance,
    ROUND(AVG(Calories), 0) AS AverageDailyCalories
FROM Activity;

3.What is the averagetime users spend in each activity category perday?

SELECT
    ROUND(AVG(VeryActiveMinutes), 1) AS AvgVeryActiveMinutes,
    ROUND(AVG(FairlyActiveMinutes), 1) AS AvgFairlyActiveMinutes,
    ROUND(AVG(LightlyActiveMinutes), 1) AS AvgLightlyActiveMinutes,
    ROUND(AVG(SedentaryMinutes), 1) AS AvgSedentaryMinutes
FROM Activity;

4.Which users have the highest average daily step_count?

SELECT TOP 5
    Id,
    ROUND(AVG(TotalSteps), 0) AS AverageDailySteps
FROM Activity
GROUP BY Id
ORDER BY AverageDailySteps DESC;

5.Which users have the lowest average daily step_count?

SELECT TOP 5
    Id,
    ROUND(AVG(TotalSteps), 0) AS AverageDailySteps
FROM Activity
GROUP BY Id
ORDER BY AverageDailySteps asc;

6.On_which_days do users record higher or lower_average steps?

SELECT
    DATENAME(WEEKDAY, ActivityDate) AS DayOfWeek,
    ROUND(AVG(TotalSteps), 0) AS AverageDailySteps
FROM Activity
GROUP BY DATENAME(WEEKDAY, ActivityDate)
ORDER BY AverageDailySteps DESC;

7.What is the average sleep duration and average time_spent in bed?

SELECT
    ROUND(AVG(TotalMinutesAsleep), 0) AS AverageMinutesAsleep,
    ROUND(AVG(TotalTimeInBed), 0) AS AverageMinutesInBed
FROM sleep;

8.Which users have higher or lower_average sleep duration?

SELECT
    Id,
    ROUND(AVG(TotalMinutesAsleep), 0) AS AverageMinutesAsleep
FROM sleep
GROUP BY Id
ORDER BY AverageMinutesAsleep DESC;

9.What are the average_weight and BMI_values among users who recorded weight_data?

SELECT
    ROUND(AVG(WeightKg), 2) AS AverageWeightKg,
    ROUND(AVG(BMI), 2) AS AverageBMI
FROM weight;

10.What is the average BMI_for each_user?

SELECT
    Id,
    ROUND(AVG(BMI), 2) AS AverageBMI
FROM weight
GROUP BY Id
ORDER BY AverageBMI DESC;

11.Do users daily activity levels vary_with their sleep duration?

SELECT a.ID,
       a.ActivityDate,
       a.TotalSteps,
       s.TotalMinutesAsleep,
       s.TotalTimeInBed
FROM Activity as a
Inner Join Sleep as s
on a.id = s.id AND
a.ActivityDate=s.SleepDay;

12. Count_the Matched Activity + Sleep Records

SELECT
    COUNT(*) AS MatchedRecords
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id
    AND a.ActivityDate = s.SleepDay; 

13.Among users_days whereboth activity and sleep_data are available, what are the average steps and sleep duration?

SELECT
    ROUND(AVG(a.TotalSteps), 0) AS AverageSteps,
    ROUND(AVG(s.TotalMinutesAsleep), 0) AS AverageMinutesAsleep
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id
    AND a.ActivityDate = s.SleepDay;

14.Do average daily steps differ between people with shorter and longer sleep?

SELECT
    CASE
        WHEN s.TotalMinutesAsleep < 360 THEN 'Less than 6 hours'
        WHEN s.TotalMinutesAsleep < 480 THEN '6 to 8 hours'
        ELSE '8 hours or more'
    END AS SleepGroup,
    COUNT(*) AS Records,
    ROUND(AVG(a.TotalSteps), 0) AS AverageSteps
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id
    AND a.ActivityDate = s.SleepDay
GROUP BY
    CASE
        WHEN s.TotalMinutesAsleep < 360 THEN 'Less than 6 hours'
        WHEN s.TotalMinutesAsleep < 480 THEN '6 to 8 hours'
        ELSE '8 hours or more'
    END
ORDER BY AverageSteps DESC;

15.Among the matched Activity + Sleep records, how does sedentary time vary across sleep-duration groups?

SELECT
    CASE
        WHEN s.TotalMinutesAsleep < 360 THEN 'Less than 6 hours'
        WHEN s.TotalMinutesAsleep < 480 THEN '6 to 8 hours'
        ELSE '8 hours or more'
    END AS SleepGroup,
    COUNT(*) AS Records,
    ROUND(AVG(a.SedentaryMinutes), 0) AS AverageSedentaryMinutes
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id
    AND a.ActivityDate = s.SleepDay
GROUP BY
    CASE
        WHEN s.TotalMinutesAsleep < 360 THEN 'Less than 6 hours'
        WHEN s.TotalMinutesAsleep < 480 THEN '6 to 8 hours'
        ELSE '8 hours or more'
    END
ORDER BY AverageSedentaryMinutes DESC;

16.For users who recorded weight data, what are their average steps and BMI?

WITH UserActivity AS (
    SELECT
        Id,
        AVG(TotalSteps) AS AverageDailySteps
    FROM Activity
    GROUP BY Id
),
UserWeight AS (
    SELECT
        Id,
        AVG(BMI) AS AverageBMI
    FROM Weight
    GROUP BY Id
)
SELECT
    a.Id,
    ROUND(a.AverageDailySteps, 0) AS AverageDailySteps,
    ROUND(w.AverageBMI, 2) AS AverageBMI
FROM UserActivity AS a
INNER JOIN UserWeight AS w
    ON a.Id = w.Id
ORDER BY w.AverageBMI DESC;

17.How does average daily activity differ across BMI groups?

WITH UserActivity AS (
    SELECT
        Id,
        AVG(TotalSteps) AS AverageDailySteps
    FROM Activity
    GROUP BY Id
),
UserBMI AS (
    SELECT
        Id,
        AVG(BMI) AS AverageBMI
    FROM Weight
    GROUP BY Id
)
SELECT
    CASE
        WHEN AverageBMI < 18.5 THEN 'Underweight'
        WHEN AverageBMI < 25 THEN 'Normal'
        WHEN AverageBMI < 30 THEN 'Overweight'
        ELSE 'Obese'
    END AS BMIGroup,
    COUNT(*) AS Users,
    ROUND(AVG(AverageDailySteps), 0) AS AverageDailySteps
FROM UserActivity AS a
INNER JOIN UserBMI AS b
    ON a.Id = b.Id
GROUP BY
    CASE
        WHEN AverageBMI < 18.5 THEN 'Underweight'
        WHEN AverageBMI < 25 THEN 'Normal'
        WHEN AverageBMI < 30 THEN 'Overweight'
        ELSE 'Obese'
    END
ORDER BY AverageDailySteps DESC;

18.How many activity days did each user record?

SELECT
    Id,
    COUNT(DISTINCT ActivityDate) AS ActivityDays
FROM Activity
GROUP BY Id
ORDER BY ActivityDays DESC;

19.How many users have low, moderate, or high numbers of recorded activity days?

WITH UserActivity AS (
    SELECT
        Id,
        COUNT(DISTINCT ActivityDate) AS ActivityDays
    FROM Activity
    GROUP BY Id
)
SELECT
    CASE
        WHEN ActivityDays < 20 THEN 'Low Tracking'
        WHEN ActivityDays < 30 THEN 'Moderate Tracking'
        ELSE 'High Tracking'
    END AS TrackingGroup,
    COUNT(*) AS Users
FROM UserActivity
GROUP BY
    CASE
        WHEN ActivityDays < 20 THEN 'Low Tracking'
        WHEN ActivityDays < 30 THEN 'Moderate Tracking'
        ELSE 'High Tracking'
    END
ORDER BY Users DESC;

20.How many users have records in both Activity and Sleep datasets?

SELECT
    COUNT(DISTINCT a.Id) AS UsersWithActivityAndSleep
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id;

21.How many users have recorded Activity + Sleep + Weight/BMI data?

SELECT
    COUNT(DISTINCT a.Id) AS UsersWithAllThree
FROM Activity AS a
INNER JOIN sleep AS s
    ON a.Id = s.Id
INNER JOIN weight AS w
    ON a.Id = w.Id;