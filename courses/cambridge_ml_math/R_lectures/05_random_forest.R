set.seed(101)

n <- 1000
x <- runif(n)
y <- x + 0.2*rnorm(n)

plot(x, y, col="grey")
abline(c(0, 1), col="red", lwd=2)

library(rpart)

minsplit_vec <- c(500, 250, 100, 20)

tree_list <- list(4)

for (i in seq_along(minsplit_vec)) {
  tree_list[[i]] <- rpart(y ~ x, method="anova",
                          control=rpart.control(minsplit = minsplit_vec[i],
                                                minsplitmaxcompete=0,
                                                maxsurrogate=0,
                                                xval=0,
                                                cp=0))
}

x_plot <- seq(from=0, to=1, length.out=1001)

for (i in seq_along(minsplit_vec)) {
  y_plot <- predict(tree_list[[i]], newdata=data.frame("x"=x_plot))
  plot(x, y, col="grey")
  abline(c(0, 1), col="red", lwd=2)
  lines(x_plot, y_plot, col="blue", lwd=2)
}

# average tree split 200
B <- 100
tree_list_av <- list(B)
for (b in 1:B) {
  x <- runif(n)
  y <- x + 0.2*rnorm(n)
  tree_list_av[[b]] <- rpart(y ~ x, method="anova",
                          control=rpart.control(minsplit = 200,
                                                minsplitmaxcompete=0,
                                                maxsurrogate=0,
                                                xval=0,
                                                cp=0))
}
y_plot <- rowMeans(sapply(tree_list_av,
                 function(tree) predict(tree, newdata=data.frame("x"=x_plot))))
plot(x, y, col="white")
abline(c(0, 1), col="red", lwd=2)
lines(x_plot, y_plot, col="blue", lwd=2)

# Random forest
library(randomForest)

out <- randomForest(x=as.matrix(x), y=y, nodesize=200, ntree=1000)
y_plot <- predict(out, newdata=matrix(x_plot))
points(x, y, col="grey")
# abline(c(0, 1), col="red", lwd=2)
lines(x_plot, y_plot, col="black", lwd=2)


