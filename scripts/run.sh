#!/bin/bash
wget https://grakn.ai/download/latest -O grakn_latest.zip
tar xvf grakn_latest.zip
rm grakn_latest.zip
mv grakn-dist-* grakn
grakn/bin/grakn.sh start
wget https://raw.githubusercontent.com/graknlabs/sample-datasets/master/movies/schema.gql
wget https://raw.githubusercontent.com/graknlabs/sample-datasets/master/movies/large-dataset/movie-data.gql
grakn/bin/graql.sh -k movieclassifier -f schema.gql
grakn/bin/graql.sh -k movieclassifier -b movie-data.gql