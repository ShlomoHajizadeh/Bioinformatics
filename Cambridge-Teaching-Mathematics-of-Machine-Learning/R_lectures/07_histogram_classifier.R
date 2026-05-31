# Params
n <- 5000
n_test <- 10000

## Generate training data
x1 <- matrix(2*rnorm(n*2), n, 2) + rep(c(-2, 1), each=n)
x2 <- matrix(2*rnorm(n*2), n, 2) + rep(c(2, 1), each=n)
# Rotate
rot <- matrix(c(cos(1), sin(1), -sin(1), cos(1)), 2, 2)
x1 <- x1 %*% rot
x2 <- x2 %*% rot
# Nonlinear mapping
x1 <- atan(x1) / pi + 0.5
x2 <- atan(x2) / pi + 0.5

## Generate test data (used to estimate test error)
x1_test <- matrix(2*rnorm(n_test*2), n_test, 2) + rep(c(-2, 1), each=n_test)
x2_test <- matrix(2*rnorm(n_test*2), n_test, 2) + rep(c(2, 1), each=n_test)
# Rotate
rot <- matrix(c(cos(1), sin(1), -sin(1), cos(1)), 2, 2)
x1_test <- x1_test %*% rot
x2_test <- x2_test %*% rot
# Nonlinear mapping
x1_test <- atan(x1_test) / pi + 0.5
x2_test <- atan(x2_test) / pi + 0.5

# Plotting Bayes classifier
N <- 10^4
Bayes <- matrix(c(rep(0, N), seq(from=-10, to=10, length.out=N)), N, 2)
Bayes <- Bayes %*% rot
Bayes <- atan(Bayes) / pi + 0.5

# Create colours for plotting
alpha <- 50
t_red <- rgb(255, 0, 0, alpha, maxColorValue = 255)
t_blue <- rgb(0, 0, 255, alpha, maxColorValue = 255)
col_vec <- c(t_red, t_blue)

###############################

# Plot
plot(rbind(x1, x2), col=rep(c(t_red, t_blue), each=n), xlab="", ylab="")
lines(Bayes)

m <- 10

###############################
# Grid plotting
for (r in 1:(m-1)) {
  abline(v=r/m, lty=3)
  abline(h=r/m, lty=3)
}

## Add histogram classifier

test_err <- 0
train_err <- 0
for (r in 0:(m-1)) {
  for (s in 0:(m-1)) {
    class1_count <- sum((r/m <= x1[, 1]) * (x1[, 1] < (r+1)/m) * (s/m <= x1[, 2]) * (x1[, 2] < (s+1)/m))
    class2_count <- sum((r/m <= x2[, 1]) * (x2[, 1] < (r+1)/m) * (s/m <= x2[, 2]) * (x2[, 2] < (s+1)/m))
    train_err <- train_err + min(class1_count, class2_count)
    
    Y_bar <- (class2_count > class1_count) + 1 # so that it is in {1,2}
    rect(r/m, s/m, (r+1)/m, (s+1)/m, col=col_vec[Y_bar], border=NA)
    
    # compute test error
    class1_count <- sum((r/m <= x1_test[, 1]) * (x1_test[, 1] < (r+1)/m) * (s/m <= x1_test[, 2]) * (x1_test[, 2] < (s+1)/m))
    class2_count <- sum((r/m <= x2_test[, 1]) * (x2_test[, 1] < (r+1)/m) * (s/m <= x2_test[, 2]) * (x2_test[, 2] < (s+1)/m))
    test_err <- test_err + c(class1_count, class2_count)[3L-Y_bar]
  }
}

train_err <- train_err / (2*n)
test_err <- test_err / (2*n_test)
print(paste("Training error:", train_err))
print(paste("Test error:", test_err))
