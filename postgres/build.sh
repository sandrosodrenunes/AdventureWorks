#!/bin/bash

echo "Building postgres docker image."
docker build --progress=plain . -t chriseaton/adventureworks:postgres -t chriseaton/adventureworks:postgres-16