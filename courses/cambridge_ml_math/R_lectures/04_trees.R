set.seed(2)

n <- 500

x <- runif(2 * n)
dim(x) <- c(n, 2)

sig_fun <- function(x1, x2) ((x1 + 1) * x2)^(1.5)
# Try experimenting with different functions

sig <- sig_fun(x[, 1], x[, 2])  
y <- sig + 0.5*rnorm(n)

norm_sig <- sig - min(sig)
norm_sig <- norm_sig / max(norm_sig)


min_y <- min(y)
norm_y <- y - min_y
max_norm_y <- max(norm_y)
norm_y <- norm_y / max_norm_y
# norm_y = norm(y) - normalise y values to [0,1] for plotting
norm <- function(v) {
  (v-min_y) / max_norm_y
}

col_fun <- function(v, alpha=1) {
  rgb(norm(v), 0, 1-norm(v), alpha=alpha, maxColorValue = 1)
}
# col_fun <- function(v, alpha=1) {
#   rgb(0, 0, 0, alpha=1-norm(v), maxColorValue = 1)
# }
# col_vec <- col_fun(y)
col_vec <- rgb(norm_y, 0, 1-norm_y, maxColorValue = 1)



x1_cont <- seq(from=0, to=1, by=0.05)
z_cont <- outer(x1_cont, x1_cont, FUN=sig_fun)

contour(x1_cont, x1_cont, z_cont, lty=1, lwd=1.2,
        levels=seq(from=0, to=4, by=0.2))
points(x[, 1], x[, 2], col=col_vec, pch=19)

####################################################
# Decision tree


# contour(x1_cont, x1_cont, z_cont, lty=3,
#         levels=seq(from=0, to=4, by=0.2))
# points(x[, 1], x[, 2], col=col_vec)

# Fit decision tree
if (!require("rpart")) install.packages("rpart")
library(rpart)

out <- rpart(y ~ x, method="anova",
             control=rpart.control(maxcompete=0, maxsurrogate=0, xval=0))



########################
# For plotting splits
nsplits <- nrow(out$splits)

split_mat <- matrix(nrow = nsplits, ncol=5)
colnames(split_mat) <- c("val", "lower1", "upper1", "lower2", "upper2")
split_mat[, 1] <- out$splits[, "index"]
split_mat[1, 2:5] <- c(0, 1, 0, 1)

split_avail <- rep(2L, nsplits)
# 2 = left and right split available, 1 = only right split available, 0 = no splits available

split_var <- as.integer(unlist(strsplit(rownames(out$splits), split="x")))
split_var <- split_var[!is.na(split_var)]

ancestors <- rep(0L, nsplits)

cur_avail <- 1
cur_ind <- 1
for (i in 2:nrow(out$frame)) {
  # Find the first available
  cur_avail <- max((1:cur_ind)[split_avail[1:cur_ind] > 0])
  if (out$frame[i, "var"] != "<leaf>") {
    cur_ind <- cur_ind + 1
    ancestors[cur_ind] <- cur_avail
    split_mat[cur_ind, 2:5] <- split_mat[cur_avail, 2:5]
    if (split_avail[cur_avail] == 2) {
      if (split_var[cur_avail] == 1) {
        split_mat[cur_ind, 3] <- split_mat[cur_avail, 1]
      } else {
        split_mat[cur_ind, 5] <- split_mat[cur_avail, 1]
      }
    } else {
      if (split_var[cur_avail] == 1) {
        split_mat[cur_ind, 2] <- split_mat[cur_avail, 1]
      } else {
        split_mat[cur_ind, 4] <- split_mat[cur_avail, 1]
      }
    }
  }
  split_avail[cur_avail] <- split_avail[cur_avail] - 1
}

# Node order
node_order <- order(as.integer(rownames(out$frame)[out$frame[, "var"] != "<leaf>"]))

plot_split <- function(ind) {
  if (missing(ind)) {
    for (ind in seq_len(nrow(split_mat))) {
      if (split_var[ind] == 1) {
        x0 <- x1 <- split_mat[ind, "val"]
        y0 <- split_mat[ind, "lower2"]
        y1 <- split_mat[ind, "upper2"]
      } else {
        x0 <- split_mat[ind, "lower1"]
        x1 <- split_mat[ind, "upper1"]
        y0 <- y1 <- split_mat[ind, "val"]
      }
      segments(x0=x0, x1=x1, y0=y0, y1=y1, col="red", lwd=2)
      
      text(x=x1+0.02, y=y1-0.02, labels=as.character(ind), col="black", cex=1.5)
    }
  } else {
    ind <- node_order[ind]
    if (split_var[ind] == 1) {
      segments(x0 = split_mat[ind, "val"], y0=split_mat[ind, "lower2"], y1=split_mat[ind, "upper2"], col="red", lwd=2)
    } else {
      segments(y0 = split_mat[ind, "val"], x0=split_mat[ind, "lower1"], x1=split_mat[ind, "upper1"], col="red", lwd=2)
    }
  }
}
# Try plot_split(1), plot_split(2) etc.
# plot_split() plots all the splits at once

### Plot tree

op <- par(mfrow=c(1, 2))

contour(x1_cont, x1_cont, z_cont, lty=1, lwd=1.2,
        levels=seq(from=0, to=4, by=0.2))
points(x[, 1], x[, 2], col=col_vec, pch=19)
plot_split()

# Plot tree
if (!require("rpart.plot")) install.packages("rpart.plot")
library(rpart.plot)
#rpart.plot(out, box.palette = "BuGn")
rpart.plot(out, box.palette = "-Grays")

par(op)
