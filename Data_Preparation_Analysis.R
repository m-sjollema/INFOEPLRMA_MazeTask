expdf <- read.csv("") #The csv-file should be added here
library(tidyverse)
library(dplyr)
library(lme4)
library(ggplot2)
library(lmerTest)
library(car)
library(emmeans)
library(MuMIn)  

# Identify koppel_id values that should be removed for each participant
ids_to_remove <- expdf %>%
  filter(correct == FALSE) %>%
  select(ParticipantNumber, koppel_id) %>%
  distinct()

# Filter out the rows where participant and koppel_id match the identified ones
df_filtered <- expdf %>%
  anti_join(ids_to_remove, by = c("ParticipantNumber", "koppel_id"))

# Print result
print(df_filtered)

#Filter out the fillers, primes, practice
df_filteredtar <- filter(df_filtered, df_filtered$condition !="filler")
df_filteredtarge <- filter(df_filteredtar, df_filteredtar$target_prime !="prime")
df_filteredtarget <- filter(df_filteredtarge, df_filteredtarge$condition !="practice")

#Filter the data of the third word.
df_target <- filter(df_filteredtarget, word_id == "3") 

#Calculate reaction time to log reaction time
df_target$reaction_time <- as.numeric(df_target$reaction_time)
df_target <- mutate(df_target, logRT = log(reaction_time))

#Test the model
m1 <- lmer(logRT ~ 1+target_structure + prime_structure + target_structure*prime_structure + (1+target_structure | ParticipantNumber) + (1 | item_id), data = df_target)
summary(m1)

#Visualisation of the data
ggplot(df_target, aes(x = target_structure, y = logRT, fill = prime_structure)) +
  geom_boxplot(position = position_dodge(width = 0.8)) +
  scale_fill_manual(values = c("L" = "pink", "A" = "lightblue", "U" = "darkseagreen2")) +
  theme_minimal()

#Create a new csv file with the data of the critical word only
write.csv(df_target,"~/df_target.csv", row.names = FALSE)

#Pairwise comparisons
emmeans(m1,pairwise~target_structure)
emmeans(m1,pairwise~prime_structure)
emmeans(m1,pairwise~prime_structure|target_structure)

# plot of the interactions between model
emmip(m1,target_structure~prime_structure) + ylab("logRT")


#Calculate and check the non-log reaction times as real times and as percentiles 
# Only for the significant results, namely A - L.
filter_AA<- filter(df_target, target_structure== "A", prime_structure== "A")
filter_AL <- filter(df_target, target_structure== "A", prime_structure== "L")

mean(filter_AA$reaction_time)-mean(filter_AL$reaction_time)

hist(filter_AA$reaction_time)
hist(filter_AL$reaction_time)

(mean(filter_AA$reaction_time)-mean(filter_AL$reaction_time))*100/mean(filter_AA$reaction_time)
mean(filter_AA$reaction_time)

# check assumptions
# normality and homoscedasticity
hist(residuals(m1))
plot(fitted(m1), residuals(m1))
qqnorm(residuals(m1))
qqline(residuals(m1))

# collinearity
vif(m1)

# estimates of model fit
r.squaredGLMM(m1)
