##### MODELING SCRIPT
# File contains code used to generate data used 
# for the report "report.pdf", before running this
# code make sure you have installed all the libraries used
# TO use this file properly follow the instructions
# in the README.md file located inside the 'scripts' folder.

### LIBS ####
library(tidyverse) # Contains usefule functions and ggplot
library(rjson) # To parse profiles dataset
library(cesR) # To generate values from the CES 

#### MODELING DATA ####
# Extract information from txt file
provinces <- read_lines(file = "scripts/provinces.txt")

# Split string by "Province Name : Population"
provinces <- strsplit(provinces, ":")

# Generate stratum sample sizes
N <- as.numeric(provinces[[1]][2]); n <- 10000
n_h <- c()

# Calculates n_h for each province
for( i in 2:14) {
  N_h <- as.numeric(provinces[[i]][2])
  
  n_h <- c(n_h, (n/N)*N_h)
}
rm(N_h)

# Load profile data
# 10000 list of lists with 9 elements each
profiles <- fromJSON(file = "scripts/profiles.json")$results




#### CLEAN UP ####
rm(list = ls())
