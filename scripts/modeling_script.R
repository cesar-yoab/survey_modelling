##### MODELING SCRIPT
# File contains code used to generate data used 
# for the report "report.pdf", before running this
# code make sure you have installed all the libraries used
# TO use this file properly follow the instructions
# in the README.md file located inside the 'scripts' folder.

### LIBS ####
library(tidyverse) # Contains useful functions and ggplot
library(rjson) # To parse profiles data-set
library(cesR) # To generate values from the CES 

#### MODELING DATA ####
# Load youtube data
# We 
youtube_data <- fromJSON(file = "scripts/yt-response.json")$items
yt_likes <- 0
yt_dlikes <- 0

for ( i in 1:5 ) {
  yt_likes <- yt_likes + as.numeric(youtube_data[[i]]$statistics$likeCount)
  yt_dlikes <- yt_dlikes + as.numeric(youtube_data[[i]]$statistics$dislikeCount)
}
rm(i)
yt_n <- yt_likes + yt_dlikes



## Generating values to model data
set.seed(23948) # For generation of random numbers

yt_likes <- yt_likes / yt_n # Youtube ratio of likes
yt_dlikes <- yt_dlikes  / yt_n # Youtube ratio of dislikes


# Generate the amount of eligible voters
q1 <- rbernoulli(n = 10000, 0.9)


# We will assume that 90% of respondents where eligible voters
# with this information we can model question 2 which is:
# "If you are ok with it, we'd like to know for whom did you vote in the 2019
# Canadian federal elections?"

# Initial probabilities are based on
# Canadian election results taken from:
# https://enr.elections.ca/National.aspx?lang=e
q2_prop <- list("Liberal" = 0.464, "Conservative" = 0.358, "ndp" = 0.071,
                "BlocQubc" = 0.095, "Green" = 0.034, "PreferNot" = 0.02, 
                "Other" =  0.002)

q2 <- rmultinom(n = sum(q1), size=1, prob = q2_prop) # Data generation

# Next we generate responses for the 3 question which everyone answers,
# it states: How do you feel about the general direction of our contry at
# the moment?
q3_prop <- list("Wrong" = yt_dlikes * 0.6, "Standstill" = yt_dlikes * 0.4,
                "Right" = yt_likes * 0.8, "Unsure" = yt_likes * 0.2)

q3 <- rmultinom(n = 10000, size = 1, prob = q3_prop) # Data generation


# Question 4 asks: How much did the COVID-19 pandemic influence your response
# to the last question?
# This is hard to simulate since its from a range however we will use the
# collected youtube information to generate such numbers. The goal is to
# achieve normal distribution like probabilities.
q4_prop <- list("1" = yt_likes * 0.3, "2" = yt_likes * 0.5, 
                "3" = (yt_likes * 0.2) + (yt_dlikes * 0.2),
                "4" = yt_dlikes * 0.5, "5" = yt_dlikes * 0.3)
q4 <- rmultinom(n = 10000, size = 1, prob = q4_prop) # Data generation

# Question 5 is only asked to the people that identified as eligible voters
# It asks: If there was a general election tomorrow, which party would you
# vote for?
q5_prop <- list("Liberal" = yt_likes, "Conservative" = yt_dlikes * 0.6, 
                "ndp" = yt_dlikes * 0.13,
                "BlocQubc" = yt_dlikes * 0.12, "Green" = yt_dlikes * 0.12, 
                "Other" =  yt_dlikes * 0.03)

q5 <- rmultinom(n = sum(q1), size = 1, prob = q5_prop)


### Generate data-set for report

# The following set of functions generate
# the required labels to be inserted
# to the data frame
get_q2_lab <- function(x, i) {
  if(x[1, i]) return("Liberal")
  else if(x[2, i]) return("Conservative")
  else if(x[3, i]) return("ndp")
  else if(x[4, i]) return("BlocQbc")
  else if(x[5, i]) return("Green")
  else if(x[6, i]) return("PreferNot")
  else return("Other")
}

get_q3_lab <- function(x, i) {
  if(x[1, i]) return("Wrong")
  else if(x[2, i]) return("Standstill")
  else if(x[3, i]) return("Right")
  else return("Unsure")
}

get_q4_lab <- function(x, i) {
  if(x[1, i]) return(1)
  else if(x[2, i]) return(2)
  else if(x[3, i]) return(3)
  else if(x[4, i]) return(4)
  else return(5)
}

get_q5_lab <- function(x, i) {
  if(x[1, i]) return("Liberal")
  else if(x[2, i]) return("Conservative")
  else if(x[3, i]) return("ndp")
  else if(x[4, i]) return("BlocQbc")
  else if(x[5, i]) return("Green")
  else return("Other")
}

# All simulated data will go in this dataframe
dataset <- data.frame(Q1 = numeric(0), Q2 = character(0),
                      Q3 = character(0), Q4 = numeric(0),
                      Q5 = character(0), stringsAsFactors = FALSE)
  
small_counter <- 1
# Adds data to dataframe
for ( i in 1:10000 ) {
  if (q1[i]) { # Eligible voters
    dataset[i, ] <- c(1, get_q2_lab(q2, small_counter),
                      get_q3_lab(q3, i), get_q4_lab(q4, i),
                      get_q5_lab(q5, small_counter))
    small_counter <- small_counter + 1
  } else { # Non-Eligible voters
    dataset[i, ] <- c(0, NA,
                      get_q3_lab(q3, i), get_q4_lab(q4, i),
                     NA)
  }
}
rm(i)

# Write data to a .csv file
write.csv(dataset, "./survey_data.csv")

#### CLEAN UP ####
# Done!
rm(list = ls())
