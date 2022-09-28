#!/usr/bin/env Rscript
library("optparse")

option_list <- list(
  make_option(c("-s", "--seed"), type="numeric", default=NULL,
              help="random seed", metavar="numeric"),
  make_option(c("-n", "--size"), type="numeric", default=NULL,
              help="number of characters", metavar="numeric"),
  make_option(c("-o", "--output"), type="character", default="data.csv",
              help="output file name [default= %default]", metavar="character")
)

opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

stopifnot(!is.null(opt$size))

library(tibble)
library(readr)
library(poweRlaw)

if (!is.null(opt$seed)) set.seed(opt$seed)
n <- opt$size

clamp <- function(x) round(pmax(-1, pmin(1, x)), 3)
bimodal <- function(n) clamp(ifelse(runif(n) < 0.5, -0.5 + 0.2 * rnorm(n), 0.5 + 0.2 * rnorm(n)))

tibble(attack=round(pmax(1, 50 + 10 * rnorm(n)), 2),
       defense=round(pmax(1, 20 + 5 * rnorm(n)), 2),
       speed=round(runif(n, 1, 100), 2),
       health=round(100 * rplcon(n, 1, 3)),
       agressiveness=bimodal(n),
       cooperation=bimodal(n),
       leadership=bimodal(n),
       hit=as.numeric(runif(n) < 0.95),
       cure=as.numeric(runif(n) < 0.2),
       combo=as.numeric(runif(n) < 0.3),
       boost=as.numeric(runif(n) < 0.5)) %>%
  write_csv(opt$output)
