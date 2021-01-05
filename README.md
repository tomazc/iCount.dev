[![Netlify Status](https://api.netlify.com/api/v1/badges/c4f22164-5bb0-41be-88d0-08889b81e69a/deploy-status)](https://app.netlify.com/sites/icount/deploys)


# iCount landing page

Build with [Hugo](https://gohugo.io/), shipped by [netlify](https://www.netlify.com), available at https://icount.dev.

## To start hugo server

`hugo server -D`


## To build

`hugo -D # builds the static pages in subfolder public`


## To run in docker

`docker run --rm --name "iCount.dev" -it -p 1313:1313 -v $(pwd):/src klakegg/hugo:0.80.0-ext server`
