list.of.packages <- c("Hmisc")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(Hmisc)

# Give in year and ranking
year = 2018  # Year to analyse

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

ARWU$Reputation_ARWU <- (ARWU$Alumni + ARWU$Award) / 2
ARWU$Publication_ARWU <- (ARWU$HiCi + ARWU$NS + ARWU$PUB) / 3
ARWU <- ARWU[,c("GRID_ID", "Reputation_ARWU", "Publication_ARWU")]

THE$Reputation_THE <- (THE$Teaching + THE$Rechearch) / 2
THE$Publication_THE <- THE$Citations
THE <- THE[,c("GRID_ID", "Reputation_THE", "Publication_THE")]

QS$Reputation_QS <- (QS$Academic_reputation + QS$Employer_reputation) / 2
QS$Publication_QS <- QS$Citations
QS <- QS[,c("GRID_ID", "Reputation_QS", "Publication_QS")]

df <- merge(x = ARWU, y = THE, by = "GRID_ID")
df <- merge(x = df, y = QS, by = "GRID_ID")
df <- df[,c("Publication_ARWU", "Publication_THE", "Publication_QS", "Reputation_ARWU", "Reputation_THE", "Reputation_QS")]

rcorr(as.matrix(df), type='spearman')
