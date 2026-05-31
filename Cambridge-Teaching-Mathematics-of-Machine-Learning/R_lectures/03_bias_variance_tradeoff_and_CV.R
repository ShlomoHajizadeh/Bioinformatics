# Params
set.seed(101)
sigma <- 0.2
n <- 200

# Signal
f <- function(x) sin(4*x)^2 / (2.5+(cos(2*x)))

# Plot signal
x_plot <- seq(from=0, to=1, length.out = 1001)
y_plot <- f(x_plot)
plot(x_plot, y_plot, type="l", ylim=c(min(y_plot) - sigma, max(y_plot + sigma)),
     xlab="", ylab="", lwd=2)

# # Approximation
# poly_deg <- 20 # try changing this
# approx_out <- lm(y_plot ~ poly(x_plot, degree=poly_deg))
# lines(x_plot, predict(approx_out), col="blue")


# Plot points
x <- runif(n)
ord_x <- order(x)
y <- f(x) + sigma*rnorm(n)
points(x, y, col="darkgrey")

# Degree
poly_deg <- 15
col_red <- rgb(255, 0, 0, 100,maxColorValue = 255) # slightly transparent red
col_red_trans <- rgb(255, 0, 0, 15,maxColorValue = 255) # very transparent red


fit_out <- lm(y ~ poly(x, degree=poly_deg))
lines(x_plot, predict(fit_out, newdata=data.frame(x=x_plot)), col=col_red)

# average curve
nreps <- 10000
Phi <- model.matrix(fit_out)
Hat_matrix <- tcrossprod(svd(Phi, nv=0)$u)

y_mat <- f(x) + sigma * matrix(rnorm(n * nreps), n, nreps)
all_fits <- Hat_matrix %*% y_mat


lines(x[ord_x], all_fits[ord_x, 1], col=col_red)
lines(x[ord_x], all_fits[ord_x, 2], col=col_red)
lines(x[ord_x], all_fits[ord_x, 3], col=col_red)

n_curves <- 200
for (i in 1:n_curves) {
  lines(x[ord_x], all_fits[ord_x, i], col=col_red_trans)
}


fit_average <- rowMeans(all_fits)

lines(x[ord_x], fit_average[ord_x], lwd=2, col="blue")

# Bias--variance tradeoff
deg_max <- 15
bias <- variance <- numeric(deg_max)

for (poly_deg in 1:deg_max) {
  fit_out <- lm(y ~ poly(x, degree=poly_deg))
  Phi <- model.matrix(fit_out)
  Hat_matrix <- tcrossprod(svd(Phi, nv=0)$u)
  fits <- Hat_matrix %*% y_mat
  
  fit_average <- rowMeans(fits)
  
  variance[poly_deg] <- mean((fits - fit_average)^2)
  bias[poly_deg] <- mean((fit_average - f(x))^2)
}

bias_var <- variance+bias

plot(bias_var, type="l", ylim=c(0, max(bias_var)), xlab="degree", ylab="error")

lines(bias, col="red")

lines(variance, col="blue")


#################################################
opt_deg <- which.min(bias_var)

nreps <- 100

nfolds <- 10
foldid <- rep(1:nfolds, n/nfolds)

cv_errs <- matrix(0, nrow=nreps, ncol=deg_max)
cv_opt <- numeric(nreps)

for (i in 1:nreps) {
  x <- runif(n)
  y <- f(x) + sigma*rnorm(n)
  
  for (fold in 1:nfolds) {
    cur_fold <- which(foldid == fold)
    x_fit <- x[-cur_fold]
    for (poly_deg in 1:deg_max) {
      fit_out <- lm(y[-cur_fold] ~ poly(x_fit, degree=poly_deg))
      cv_errs[i, poly_deg] <- cv_errs[i, poly_deg] +
        mean((y[cur_fold] - predict(fit_out, newdata=data.frame(x_fit=x[cur_fold])))^2)
      # plot
      # plot(x, y, col="grey")
      # points(x[cur_fold], y[cur_fold], col="blue", pch=19)
      # lines(x_plot, predict(fit_out, newdata=data.frame(x_fit=x_plot)), col=col_red)
    }
  }
  cv_opt[i] <- which.min(cv_errs[i, ])
}

barplot(table(cv_opt))

# Version with permuting
cv_errs_perm <- matrix(0, nrow=nreps, ncol=deg_max)
cv_opt_perm <- numeric(nreps)
nperm <- 5
for (i in 1:nreps) {
  x <- runif(n)
  y <- f(x) + sigma*rnorm(n)
  for (perm in 1:nperm) {
    perm_obs <- sample.int(n)
    x <- x[perm_obs]
    y <- y[perm_obs]
    for (fold in 1:nfolds) {
      cur_fold <- which(foldid == fold)
      for (poly_deg in 1:deg_max) {
        x_fit <- x[-cur_fold]
        fit_out <- lm(y[-cur_fold] ~ poly(x_fit, degree=poly_deg))
        cv_errs_perm[i, poly_deg] <- cv_errs_perm[i, poly_deg] +
          mean((y[cur_fold] - predict(fit_out, newdata=data.frame(x_fit=x[cur_fold])))^2)
      }
    }
  }
  cv_opt_perm[i] <- which.min(cv_errs_perm[i, ])
}

barplot(table(cv_opt_perm))









