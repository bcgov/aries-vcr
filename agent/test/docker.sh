#!/bin/sh

pushd $(dirname $0)

docker build -t indy-cat-test -f Dockerfile ..

popd

docker run --rm -ti --name indy-cat-runner indy-cat-test
