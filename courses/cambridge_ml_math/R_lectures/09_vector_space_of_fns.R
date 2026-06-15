# Params
n <- 500
n_test <- 10000

poly_deg <- 5
m <- 10

op <- par(mfrow=c(1, 2))

## Generate data
x1 <- matrix(2*rnorm(n*2), n, 2) + rep(c(-2, 1), each=n)
x2 <- matrix(2*rnorm(n*2), n, 2) + rep(c(2, 1), each=n)
# Rotate
rot <- matrix(c(cos(1), sin(1), -sin(1), cos(1)), 2, 2)
x1 <- x1 %*% rot
x2 <- x2 %*% rot
# Nonlinear mapping
x1 <- atan(x1) / pi + 0.5
x2 <- atan(x2) / pi + 0.5

# Plotting Bayes classifier
N <- 10^4
Bayes <- matrix(c(rep(0, N), seq(from=-10, to=10, length.out=N)), N, 2)
Bayes <- Bayes %*% rot
Bayes <- atan(Bayes) / pi + 0.5

# Create colours for plotting
alpha <- 100
t_red <- rgb(255, 0, 0, alpha, maxColorValue = 255)
t_blue <- rgb(0, 0, 255, alpha, maxColorValue = 255)
col_vec <- c(t_red, t_blue)

# Plot
plot(rbind(x1, x2), col=rep(c(t_red, t_blue), each=n), xlab="", ylab="",
     main=paste0("Histogram classifier with m=", m))
lines(Bayes)


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


# Histogram classifier
#########################
## Overlay histogram classifier
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
    test_err <- test_err + c(class1_count, class2_count)[3-Y_bar]
  }
}
train_err <- train_err / (2*n)
test_err <- test_err / (2*n_test)

print(paste("Histogram classifier Training error:", train_err))
print(paste("Histogram classifier Test error:", test_err))
print(paste("Histogram classifier difference:", test_err - train_err))


##################################################################
# Plot
plot(rbind(x1, x2), col=rep(c(t_red, t_blue), each=n), xlab="", ylab="",
     main=paste("Polynomials with degree at most", poly_deg))
lines(Bayes)


# Polynomial classifier
##################################################################
## Prepare data for fitting logistic regression on data transformed with
# polynomials
all_x <- rbind(x1, x2)
y <- c(rep(1, nrow(x1)), rep(0, nrow(x2)))
x_mat <- poly(all_x, degree = poly_deg, raw=FALSE)

# Fit an l_2 penalised / constrained logistic regression
library(glmnet)
out <- glmnet(x_mat, y, family="binomial", alpha=0)

m_plot <- 100

# Grid on which to predict
x_plot <- matrix(c(rep(seq(from=(0.5/m_plot), to=(1-0.5/m_plot), length.out=m_plot), each = m_plot),
                   rep(seq(from=(0.5/m_plot), to=(1-0.5/m_plot), length.out=m_plot), m_plot)), ncol=2)

s_pred <- 95
# Compute predictions on grid (using an almost unconstrained / unpenalised fit with s=s_pred)
y_pred <- predict(out, poly(x_plot, degree=poly_deg, raw=FALSE), s=s_pred, type="class")
y_pred <- 2 - as.integer(y_pred)

# Plot predictions
i <- 0
for (r in 0:(m_plot-1)) {
  for (s in 0:(m_plot-1)) {
    i <- i + 1
    rect(r/m_plot, s/m_plot, (r+1)/m_plot, (s+1)/m_plot, col=col_vec[y_pred[i]], border=NA)
  }
}

# Training and test error
test_err <- mean(abs(as.integer(predict(out, poly(rbind(x1_test, x2_test), degree=poly_deg,
                                                  raw=FALSE), s=s_pred, type="class"))
                    - c(rep(1, nrow(x1_test)), rep(0, nrow(x2_test)))))
train_err <- mean(abs(as.integer(predict(out, x_mat, s=s_pred, type="class")) - y))
cat("\n")
print(paste("Polynomial classifier Training error:", train_err))
print(paste("Ploynomial classifier Test error:", test_err))
print(paste("Polynomial classifier difference:", test_err - train_err))
par(op)
