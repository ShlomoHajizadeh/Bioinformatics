### Code for running gradient boosting and subsequent plotting

Scale <- function(x) {
  x <- scale(x, scale=FALSE)
  x <- x / rep(sqrt(colMeans(x^2)), each=nrow(x))
  return(x)
}

FS_eta <- function(x, y, M=100, eta=ifelse(grad,0.1, 0.01), grad=FALSE) {
  resid <- y-mean(y)
  x <- Scale(x)
  beta_mat <- matrix(0, nrow=ncol(x), ncol=M)
  lambda <- rep(0, M)
  
  FS_eta_iter <- function(beta) {
    k_hat <- which.max(abs(colMeans(resid*x)))
    gamma_hat <- mean(resid*x[, k_hat])
    if (grad) {
      beta_change <- eta*gamma_hat
    } else {
      beta_change <- eta*sign(gamma_hat)
    }
    beta[k_hat] <- beta[k_hat] + beta_change
    resid <<- resid - beta_change*x[, k_hat]
    return(list("beta"=beta, "gamma_hat"=gamma_hat))
  }
  for (m in 2:M) {
    out <- FS_eta_iter(beta_mat[, m-1])
    beta_mat[, m] <- out$beta
    lambda[m-1] <- abs(out$gamma_hat)
  }
  return(list("beta_mat"=beta_mat, "lambda"=lambda))
}

plot_FS <- function(FS_obj, ...) {
  matplot(log10(1:ncol(FS_obj$beta_mat)), t(FS_obj$beta_mat), type="l", lty=1, ylab="",
          xlab="log10 iteration", ...)
}

###################################################
# Simulation example

set.seed(1)
n <- 200; p <- 80

x <- matrix(rnorm(n*p), n, p)
x[, -1] <- x[, -1] + 0.4*x[, -ncol(x)] # introduce some mild correlations
x <- Scale(x)

beta_vec <- c(1, 2, 3, -1, -2)
s <- length(beta_vec)
sig <- as.numeric(x[, 1:s] %*% beta_vec)
y <- sig + rnorm(n)

col_vec <- rainbow(s)
# Gradient boosting with linear regression
out_FS <- FS_eta(x, y, M=10000, eta=0.5, grad=TRUE)

# Plotting
plot_FS(out_FS, col = c(col_vec, rep("grey", p-s)), ylim=c(min(beta_vec)-0.5, max(beta_vec)+0.5),
        lwd=c(rep(3, s), rep(1, p-s)))

for (k in 1:length(beta_vec)) {
  abline(h=beta_vec[k], col=col_vec[k], lty=2, lwd=2)
}

plot_iter <- 5
for (i in seq_len(plot_iter)) {
  abline(v = log10(i), col="grey", lty=3, lwd=2)
}

# min risk
abline(v = log10(which.min(colMeans((x %*% out_FS$beta_mat - sig)^2))),
     col="black", lwd=3)




