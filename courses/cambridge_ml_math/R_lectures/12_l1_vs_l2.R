set.seed(1)
n <- 1000; p <- 500; s <- 10
# Try e.g. s=10, s=p

beta_star <- rep(10/sqrt(s), s)

n_test <- 10000 # for test data


nreps <- 50

library(doParallel)
library(foreach)

# test data
x_test <- matrix(runif(n_test * p, min = -1, max = 1), n_test, p)
prob <- 1 / (1+exp(-as.numeric(x_test[, 1:s] %*% beta_star)))
y_test <- rbinom(n_test, 1, prob=prob)

nlambda <- 50

registerDoParallel(10)

out <- foreach(1:nreps, .packages='glmnet') %dopar% {
  # training data
  x <- matrix(runif(n * p, min=-1, max=1), n, p)
  
  prob <- 1 / (1+exp(-as.numeric(x[, 1:s] %*% beta_star)))
  
  y <- rbinom(n, 1, prob=prob)
  
  outl1 <- glmnet(x, y, family="binomial", alpha=0.95, nlambda = nlambda, lambda.min.ratio=.001)
  outl2 <- glmnet(x, y, family="binomial", alpha=0, nlambda = nlambda, lambda.min.ratio=.000001)
  
  predl1 <- as.integer(predict(outl1, newx=x_test, type="class"))
  predl2 <- as.integer(predict(outl2, newx=x_test, type="class"))
  
  dim(predl1) <- dim(predl2) <- c(n_test, nlambda)
  
  errl1 <- colMeans(abs(y_test - predl1))
  errl2 <- colMeans(abs(y_test - predl2))
  
  c(errl1, errl2)
}

out_all <- matrix(unlist(out), nrow=length(out), byrow=TRUE)

out_mean_all <- colMeans(out_all)
out_sd_all <- apply(out_all, 2, sd) / sqrt(nreps)

out_mean_l1 <- out_mean_all[1:nlambda]
out_sd_l1 <- out_sd_all[1:nlambda]

out_mean_l2 <- out_mean_all[(nlambda+1):(2*nlambda)]
out_sd_l2 <- out_sd_all[(nlambda+1):(2*nlambda)]


op <- par(mfrow=c(2, 1))

# Bayes error
bayes_err <- mean(abs(y_test - as.integer(prob > 1/2)))


plot(out_mean_l1, type="l", main="l_1", ylim=c(bayes_err-0.02, 0.5))
lines(out_mean_l1 + 2*out_sd_l1, col="red", lty=2)
lines(out_mean_l1 - 2*out_sd_l1, col="red", lty=2)
abline(h=bayes_err, col="blue", lty=5)

plot(out_mean_l2, type="l", main="l_2", ylim=c(bayes_err-0.02, 0.5))
lines(out_mean_l2 + 2*out_sd_l2, col="red", lty=2)
lines(out_mean_l2 - 2*out_sd_l2, col="red", lty=2)
abline(h=bayes_err, col="blue", lty=5)


par(op)
