library(data.table)
library(ggplot2)
library(caret)
library(dplyr)



counties <- fread("/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/COVID-19_Community_Vulnerability_Crosswalk_-_Crosswalk_by_Census_Tract.csv")

data3 <- counties %>%
  filter(ST_ABBR == "PA")

df = subset(data3, select = -c(3,5,7,10, 16,17))
df2 = subset(df, select = -c(8,9), )

df2[df2 == "Manual Verification Required"] <- 0

data =  df2 %>% group_by(COUNTY)  %>%
  summarise(FIPS = max(`County FIPS`),
            TotalScore = max(`Total Score`, na.rm = TRUE),
            MaxScore = mean(`Max Possible Score`, na.rm = TRUE),
            HHAScore = mean(`HHA Score`, na.rm = TRUE),
            PoveryPer = mean(`Low Income Area (LIA) Census Tract (Poverty Percentage)`, na.rm = TRUE),
            LIA_Score = max(`Low Income Area (LIA) Census Tract - Score`, na.rm = TRUE),
            Rural = mean(Rural, na.rm = TRUE),
            Rural_Score = mean(`Rural - Score`, na.rm = TRUE))

write.csv(data,"/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_Community_Vulnerability.csv", row.names = FALSE)

transmissions <- fread("/Users/jacob/Downloads/United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv")

transmissions <- transmissions %>%
  filter(state_name == "Pennsylvania")

transmissions <- subset(transmissions, select = -c(1,4))

transmissions[transmissions == "low"] <- 1
transmissions[transmissions  == "moderate"] <- 2
transmissions[transmissions  == "substantial"] <- 3
transmissions[transmissions  == "high"] <- 4

transmissions[is.na(transmissions)] = 0
transmissions[transmissions  == "suppressed"] <- 0
na.omit(transmissions)

transmissions$cases_per_100K_7_day_count_change <- as.numeric(transmissions$cases_per_100K_7_day_count_change)
transmissions$community_transmission_level <- as.numeric(transmissions$community_transmission_level)
transmissions2 = transmissions %>% group_by(county_name) %>%
  summarise(FIPS = max(fips_code),
            Cases_Per_100k = mean(cases_per_100K_7_day_count_change, na.rm = TRUE),
            percent_tested_positive = mean(percent_test_results_reported_positive_last_7_days, na.rm = TRUE),
            transmission_level = mean(community_transmission_level, na.rm=TRUE))

write.csv(transmissions2,"/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_transmission_rates.csv", row.names = FALSE)


vaccines <- fread("/Users/jacob/Downloads/COVID-19_Vaccinations_in_the_United_States_County.csv")
vaccines <- vaccines %>%
  filter(Recip_State == "PA")

vaccines <- subset(vaccines, select = -c(1,3,5), na.rm = TRUE)
vaccines[is.na(vaccines)] = 0

vaccines <- select(vaccines, -c(SVI_CTGY, Metro_status))

vaccines2 = vaccines %>% group_by(Recip_County) %>%
  summarise(FIPS = max(FIPS),
            Completeness_pct = max(Completeness_pct),
            Administered_Dose1_Recip = max(Administered_Dose1_Recip),
            Administered_Dose1_Recip_5Plus = max(Administered_Dose1_Recip_5Plus),
            Administered_Dose1_Recip_5PlusPop_Pct = max(Administered_Dose1_Recip_5PlusPop_Pct),
            Administered_Dose1_Recip_12Plus = max(Administered_Dose1_Recip_12Plus),
            Administered_Dose1_Recip_12PlusPop_Pct = max(Administered_Dose1_Recip_12PlusPop_Pct),
            Administered_Dose1_Recip_18Plus = max(Administered_Dose1_Recip_18Plus),
            Administered_Dose1_Recip_18PlusPop_Pct = max(Administered_Dose1_Recip_18PlusPop_Pct),
            Administered_Dose1_Recip_65Plus = max(Administered_Dose1_Recip_65Plus),
            Administered_Dose1_Recip_65PlusPop_Pct = max(Administered_Dose1_Recip_65PlusPop_Pct),
            Series_Complete_Yes = max(Series_Complete_Yes),
            Series_Complete_Pop_Pct = max(Series_Complete_Pop_Pct),
            Series_Complete_5Plus = max(Series_Complete_5Plus),
            Series_Complete_5PlusPop_Pct =max(Series_Complete_5PlusPop_Pct),
            Series_Complete_12Plus = max(Series_Complete_12Plus),
            Series_Complete_12PlusPop_Pct = max(Series_Complete_12PlusPop_Pct),
            Series_Complete_18Plus = max(Series_Complete_18Plus),
            Series_Complete_18PlusPop_Pct = max(Series_Complete_18PlusPop_Pct),
            Series_Complete_65Plus = max(Series_Complete_65Plus),
            Series_Complete_65PlusPop_Pct = max(Series_Complete_65PlusPop_Pct),
            Booster_Doses = max(Booster_Doses),
            Booster_Doses_Vax_Pct = max(Booster_Doses_Vax_Pct),
            Booster_Doses_12Plus = max(Booster_Doses_12Plus),
            Booster_Doses_12Plus_Vax_Pct = max(Booster_Doses_12Plus_Vax_Pct),
            Booster_Doses_18Plus = max(Booster_Doses_18Plus),
            Booster_Doses_18Plus_Vax_Pct = max(Booster_Doses_18Plus_Vax_Pct),
            Booster_Doses_50Plus = max(Booster_Doses_50Plus_Vax_Pct),
            Booster_Doses_50Plus_Vax_Pct = max(Booster_Doses_50Plus_Vax_Pct),
            Booster_Doses_65Plus = max(Booster_Doses_65Plus),
            Booster_Doses_65Plus_Vax_Pct = max(Booster_Doses_65Plus_Vax_Pct),
            Series_Complete_Pop_Pct_SVI = max(Series_Complete_Pop_Pct_SVI),
            Series_Complete_5PlusPop_Pct_SVI = max(Series_Complete_5PlusPop_Pct_SVI),
            Series_Complete_12PlusPop_Pct_SVI = max(Series_Complete_12PlusPop_Pct_SVI),
            Series_Complete_18PlusPop_Pct_SVI = max(Series_Complete_18PlusPop_Pct_SVI),
            Series_Complete_65PlusPop_Pct_SVI = max(Series_Complete_65PlusPop_Pct_SVI),
            Series_Complete_Pop_Pct_UR_Equity = max(Series_Complete_Pop_Pct_UR_Equity),
            Series_Complete_5PlusPop_Pct_UR_Equity = max(Series_Complete_5PlusPop_Pct_UR_Equity),
            Series_Complete_12PlusPop_Pct_UR_Equity = max(Series_Complete_12PlusPop_Pct_SVI),
            Series_Complete_18PlusPop_Pct_UR_Equity = max(Series_Complete_18PlusPop_Pct_UR_Equity),
            Series_Complete_65PlusPop_Pct_UR_Equity = max(Series_Complete_65PlusPop_Pct_UR_Equity))

write.csv(transmissions2,"/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_County_Vaccine.csv", row.names = FALSE)
rm(list=ls())

PA_data <- fread("/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/COVID-19_Aggregate_Cases_Current_Daily_County_Health.csv")
PA_Community_Vulnerability <- fread("/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_Community_Vulnerability.csv")
PA_transmission_data <- fread("/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_transmission_rates.csv")
PA_vaccine_data <- fread("/Users/jacob/Covid19-Analysis-Modeling/PA-Aggregated-Data/PA_County_Vaccine.csv")

PA_data <- subset(PA_data, select = -c(2,4,11,12,13), na.rm = TRUE)

PA_data2 = PA_data %>% group_by(Jurisdiction) %>%
  summarise(seven_day_avg_cases = mean(`7-day Average New Cases`),
            Population = max(`Population (2019)`),
            New Case Rate= mean(`New Case Rate`),
            seven_day_avg_case_rate = mean(`7-Day Average New Case Rate`).
            Cumulative_Case_Rate = max(`Cumulative Case Rate`),
            FIPS = max(`County FIPS Code`)

