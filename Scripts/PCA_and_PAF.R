list.of.packages <- c("psych", "GPArotation", "rrcov")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(psych)
library(GPArotation)
library(rrcov)

# Give in year ranking and number of components
year = 2018  # Year to analyse
ncomp <- 2  # Number of components to extract 
uni <- THE # Ranking

dirname <- dirname(rstudioapi::getSourceEditorContext()$path)

ARWU <- read.csv(paste(dirname, "/Data/ARWU/ARWURanking_", year, "_grid.csv", sep=""),
                 header = TRUE,
                 sep = ",")
ARWU <- ARWU[,c("GRID_ID", "Alumni","Award","HiCi", "NS", "PUB")]
ARWU <-  na.omit(ARWU)
ARWU <- ARWU[,c("Alumni","Award","HiCi", "NS", "PUB")]

year <- year + 1

QS <- read.csv(paste(dirname, "/Data/QS/qs", year, "_grid.csv", sep=""),
               header = TRUE,
               sep = ",")
QS <- QS[,c("Academic_reputation","Employer_reputation","Faculty_Student", "International_Faculty", "International_Students", "Citations")]
QS[QS == '0'] <- NA
QS <-  na.omit(QS)
QS <- QS[,c("Academic_reputation","Employer_reputation","Faculty_Student", "International_Faculty", "International_Students", "Citations")]

THE <- read.csv(paste(dirname, "/Data/THE/THERanking", year, "__grid.csv", sep=""),
                header = TRUE,
                sep = ",")
THE <- THE[,c("GRID_ID", "Teaching","Rechearch","Citations", "Industry_Income", "Internationals_Outlook")]
THE[THE == '-'] <- NA
THE$Industry_Income <- as.numeric(THE$Industry_Income)
THE$Internationals_Outlook <- as.numeric(THE$Internationals_Outlook)
THE <- na.omit(THE)
THE <- THE[,c("Teaching","Rechearch","Citations", "Industry_Income", "Internationals_Outlook")]

nrows <- ncol(uni)

# Robust PCA
robtest <- PcaHubert(uni, k=ncomp, alpha =0.95, scale=TRUE, signflip = TRUE, outliers=TRUE)

sdev <- sqrt(robtest@eigenvalues) #compute SD of PCs from eigenvalues
rawload <- robtest@loadings[,1:ncomp] %*% diag(sdev, ncomp, ncomp) #convert to raw loadings
vmxload <- oblimin(rawload)$loadings #oblique rotate loadings
vmxload <- as.data.frame(round(vmxload,2))

# Principal Axis Factoring
fa <- fa(uni, nfactors = ncomp, rotate = 'oblimin', max.iter = 1, fm = 'pa', SMC=TRUE, scores=TRUE)
faloadings <- fa$loadings
faloadings <- as.data.frame(faloadings[1:nrows,])
faloadings <- round(faloadings, 2)

# print robust pca and paf loadings
vmxload
faloadings