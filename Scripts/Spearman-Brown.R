list.of.packages <- c("multicon")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]

library(multicon)

# Give in year and ranking
year = 2013  # Year to analyse
uni <- QS  # Ranking

dirname <- dirname(rstudioapi::getSourceEditorContext()$path)

ARWU <- read.csv(paste(dirname, "/Data/ARWU/ARWURanking_", year, "_grid.csv", sep=""),
                 header = TRUE,
                 sep = ",")
ARWU <- ARWU[,c("GRID_ID", "Alumni","Award","HiCi", "NS", "PUB")]
ARWU <-  na.omit(ARWU)

year <- year + 1

QS <- read.csv(paste(dirname, "/Data/QS/qs", year, "_grid.csv", sep=""),
               header = TRUE,
               sep = ",")
QS <- QS[,c("GRID_ID", "Academic_reputation","Employer_reputation","Faculty_Student", "International_Faculty", "International_Students", "Citations")]
QS[QS == '0'] <- NA
QS <-  na.omit(QS)

THE <- read.csv(paste(dirname, "/Data/THE/THERanking", year, "__grid.csv", sep=""),
                header = TRUE,
                sep = ",")
THE <- THE[,c("GRID_ID", "Teaching","Rechearch","Citations", "Industry_Income", "Internationals_Outlook")]
THE[THE == '-'] <- NA
THE$Industry_Income <- as.numeric(THE$Industry_Income)
THE$Internationals_Outlook <- as.numeric(THE$Internationals_Outlook)
THE <- na.omit(THE)

ARWU1 <- ARWU[,c("Alumni","Award")]
ARWU2 <- ARWU[,c("HiCi", "NS", "PUB")]

QS <-  QS[,c("Academic_reputation","Employer_reputation")]

THE <- THE[,c("Teaching","Rechearch")]

print(c(round(splithalf.r(ARWU1, sims = 500, graph = TRUE, seed = 2)[3], 2), round(splithalf.r(ARWU2, sims = 500, graph = TRUE, seed = 2)[3], 2),
        round(splithalf.r(THE, sims = 500, graph = TRUE, seed = 2)[3], 2), round(splithalf.r(QS, sims = 500, graph = TRUE, seed = 2)[3], 2)))

