set.seed(1)

# Params
#n <- 2000
n <- 40 # small example

p <- 2

## Generate data
x <- matrix(runif(2 * n, -1, 1), n, 2)
y_log <- x[, 1]^2 +x[, 2]^2 <= (2 / pi + 0.1*rnorm(n)) # TRUE / FALSE version of class label
y <- as.integer(2*(y_log - 0.5)) # in -1, 1

# grid for predictions / plotting
m_plot <- 100

# Grid on which to predict
x_plot <- matrix(c(rep(seq(from=(-1 + 1/m_plot), to=(1-1/m_plot), length.out=m_plot), each = m_plot),
                   rep(seq(from=(-1 + 1/m_plot), to=(1-1/m_plot), length.out=m_plot), m_plot)), ncol=2)


# Create colours for plotting
alpha <- 100
t_red <- rgb(255, 0, 0, alpha, maxColorValue = 255)
t_blue <- rgb(0, 0, 255, alpha, maxColorValue = 255)
col_vec <- c(t_red, t_blue)
col_vec_all <- rgb(255:0, 0, 0:255, alpha, maxColorValue = 255)

# Plot
plot(x, col=ifelse(y_log, t_red, t_blue), xlab="x1", ylab="x2", main="", xlim=c(-1, 1), ylim=c(-1,1),
     cex=2, pch=ifelse(y_log, 4, 1), lwd=2)
# lines(sqrt(2/pi) * cos(seq(0, 2*pi, length.out=100)), sqrt(2/pi) * sin(seq(0, 2*pi, length.out=100)))

# Sort x
ord1 <- apply(x, 2, order)
ord2 <- apply(x, 2, function(x) order(x, decreasing = TRUE))

# Choose M
# M <- 500
# Chose number of m to plot at
# n_plot <- 20
n_plot <- M <- 5

# Small epsilon for floating point comparisons
eps <- min(abs(apply(apply(x, 2, sort), 2, diff))) / 2

# We will store the f_m evaluated on x_plot for n_plot values of m spaced exponentially from 1 to M
# These values of m are plot_M below
plot_M <- 1:M
n_plot <- length(plot_M)

# Set up vectors for use in algorithm
min_err_c <- numeric(p)
opt_split_c <- integer(p)
opt_k_c <- logical(p) # sgn(x-a) or sgn(a-x)

# Store function (not really necessary)
beta_vec <- numeric(M)
opt_k <- logical(M)
opt_split <- numeric(M)
opt_var <- integer(M)

w <- rep(1, n)
f_cur <- rep(0, n)

f_plot_cur <- rep(0, length(x_plot))
f_plot <- h_plot <- w_plot <- matrix(nrow=length(x_plot), ncol=n_plot)

not_y_log <- !y_log
sgn_vec <- c(-1, 1)
plot_ind <- 1
for (m in 1:M) {
  for (j in 1:p) {
    # Decision stump on variable j
    cur_cumsum1 <- cumsum(w[ord1[, j]] * y[ord1[, j]])
    cur_cumsum2 <- cumsum(w[ord2[, j]] * y[ord2[, j]])
    min_cur_cumsum1 <- min(cur_cumsum1)
    min_cur_cumsum2 <- min(cur_cumsum2)
    if (min_cur_cumsum1 < min_cur_cumsum2) {
      min_err_c[j] <- min_cur_cumsum1
      opt_split_c[j] <- x[ord1[which.min(cur_cumsum1), j], j]
      opt_k_c[j] <- TRUE
    } else {
      min_err_c[j] <- min_cur_cumsum2
      opt_split_c[j] <- x[ord2[which.min(cur_cumsum2), j], j]
      opt_k_c[j] <- FALSE
    }
  }
  j_opt <- which.min(min_err_c)
  # Store output
  opt_var[m] <- j_opt
  opt_k[m] <- opt_k_c[j_opt]
  opt_split[m] <- opt_split_c[j_opt]
  
  err <- (min_err_c[j_opt] + sum(w[not_y_log])) / sum(w)
  
  if (opt_k[m]) {
    h_cur <- 2*((x[, opt_var[m]] > opt_split[m] + eps)-0.5)
  } else {
    h_cur <- -2*((x[, opt_var[m]] >= opt_split[m] - eps)-0.5)
  }
  #h_cur <- 2*((x[, opt_var[m]] > opt_split[m])-0.5) * sgn_vec[opt_k[m]+1]
  beta_vec[m] <- 0.5 * log(1/err - 1)
  
  # Update f
  f_cur <- f_cur + beta_vec[m] * h_cur
  
  # For plotting later
  h_plot_cur <- 2*((x_plot[, opt_var[m]] > opt_split[m])-0.5) * sgn_vec[opt_k[m]+1]
  f_plot_cur <- f_plot_cur + beta_vec[m] * h_plot_cur
  if (m %in% plot_M) {
    h_plot[, plot_ind] <- h_plot_cur
    f_plot[, plot_ind] <- f_plot_cur
    w_plot[, plot_ind] <- w
    plot_ind <- plot_ind + 1
  }
  
  # Update w
  w <- w * exp(-y * beta_vec[m] * h_cur)
  
}

plot_f <- function(ind, plot_w=TRUE, cex_fac=2, plot_class=FALSE) {
  cex_vec <- cex_fac*w_plot[, ind] / mean(w_plot[, ind])
  t_red <- rgb(1, 0, 0, 1, maxColorValue = 1)
  t_blue <- rgb(0, 0, 1, 1, maxColorValue = 1)
  # Plot data
  if (plot_w) {
    # plot(x, col=ifelse(y_log, t_red, t_blue),
    #      xlab="x1", ylab="x2",
    #      xlim=c(-1, 1), ylim=c(-1,1), main=paste0("m=", plot_M[ind], " weights"),
    #      cex=cex_vec, pch=ifelse(y_log, 4, 1), lwd=2)
    plot(x, col=ifelse(y_log, t_red, t_blue),
         xlab="x1", ylab="x2",
         xlim=c(-1, 1), ylim=c(-1,1), main=paste0("m=", plot_M[ind]),
         pch=ifelse(y_log, 4, 1), cex=cex_vec, lwd=2)
  } else {
    plot(x, col=ifelse(y_log, t_red, t_blue),
         xlab="x1", ylab="x2",
         xlim=c(-1, 1), ylim=c(-1,1), main=paste0("m=", plot_M[ind]),
         pch=ifelse(y_log, 4, 1), lwd=2)
  }
  
  
  # Plot predictions
  i <- 0
  if (plot_class) {
    for (r in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
      for (s in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
        i <- i + 1
        rect(r, s, r+2/m_plot, s+2/m_plot, col=col_vec[(f_plot[i, ind]<0) + 1], border=NA)
      }
    }
  } else {
    max_f <- max(f_plot[, ind])
    min_f <- min(f_plot[, ind])
    f_plot_col <- ifelse(f_plot[, ind] < 0,
                         as.integer(128 * (f_plot[, ind] / min_f + 1)),
                         1+as.integer(128 * (1 - f_plot[, ind] / max_f)))
    for (r in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
      for (s in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
        i <- i + 1
        rect(r, s, r+2/m_plot, s+2/m_plot,
             col=col_vec_all[f_plot_col[i]], border=NA)
      }
    }
  }
  #lines(sqrt(2/pi) * cos(seq(0, 2*pi, length.out=100)), sqrt(2/pi) * sin(seq(0, 2*pi, length.out=100)))
}

plot_h <- function(ind, plot_w=TRUE, cex_fac=2) {
  # Plot data
  cex_vec <- cex_fac*w_plot[, ind] / mean(w_plot[, ind])
  t_red <- rgb(1, 0, 0, 1, maxColorValue = 1)
  t_blue <- rgb(0, 0, 1, 1, maxColorValue = 1)
  if (plot_w) {
    plot(x, col=ifelse(y_log, t_red, t_blue),
         xlab="x1", ylab="x2",
         xlim=c(-1, 1), ylim=c(-1,1), main=paste0("m=", plot_M[ind], " weights"),
         cex=cex_vec, pch=ifelse(y_log, 4, 1), lwd=2)
    
  } else {
    plot(x, col=ifelse(y_log, t_red, t_blue),
         xlab="x1", ylab="x2",
         xlim=c(-1, 1), ylim=c(-1,1), main=paste0("m=", plot_M[ind]),
         pch=ifelse(y_log, 4, 1), lwd=2)
  }
  # Plot predictions
  i <- 0
  for (r in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
    for (s in seq(from=-1, to=1-2/m_plot, length.out=m_plot)) {
      i <- i + 1
      rect(r, s, r+2/m_plot, s+2/m_plot, col=col_vec[(h_plot[i, ind]<0) + 1], border=NA)
    }
  }
  #lines(sqrt(2/pi) * cos(seq(0, 2*pi, length.out=100)), sqrt(2/pi) * sin(seq(0, 2*pi, length.out=100)))
}

# Try plot_f(1), plot_h(2) etc.