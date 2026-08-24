# Technical Summary — Support Ticket EDA

## Dataset

The dataset contains 4,012 support-ticket records with information about ticket IDs, creation timestamps, assigned agents, priority levels, resolution times, and communication channels.

## Data Quality

The raw dataset contained 121 missing `agent_id` values, 193 missing `channel` values, 12 duplicate rows, 25 negative resolution times, 15 extreme resolution-time values of 999 hours, and inconsistent capitalization in the priority categories.

Missing agent IDs were removed because the responsible agent could not be reliably inferred. Missing channels were labeled as `Unknown` so that otherwise useful tickets were retained. Priority categories were standardized, negative resolution times were removed, 999-hour outliers were replaced with the median valid resolution time, and duplicate records were removed.

## Key Findings

The cleaned dataset has an overall average resolution time of approximately 12.04 hours and a median of 10.24 hours. The difference between the mean and median indicates some right-skew in the resolution-time distribution.

Average resolution time differs moderately across priorities. Low-priority tickets have the highest average resolution time at approximately 12.19 hours, followed by High at approximately 12.13 hours and Medium at approximately 11.70 hours.

After cleaning, resolution times range from 0.10 to 62.03 hours.

## Limitation

The dataset is artificially generated for assessment purposes and may not represent real-world support-ticket behavior. In addition, the available variables do not include factors such as issue complexity, agent experience, ticket subject, or customer type, which could influence resolution time.