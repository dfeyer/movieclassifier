import sklearn as sk
import tensorflow as tf
import argparse
import logging
import sys
import os
import pickle

from pandas.io.json import json_normalize
from grakn.client import Graph

logging.basicConfig(stream=sys.stdout,
                    format='%(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def flatten_grakn_results(results):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grakn_uri', type=str, default="http://localhost:4567", help='Grakn URI')
    parser.add_argument('--keyspace', type=str, default="movieclassifier", help='Grakn keyspace')
    parser.add_argument('--max_results', type=str, default=1000, help='Number of results returned in the query')
    parser.add_argument('--model_path', type=str, default="./", help='Path where models are saved')
    parser.add_argument('--data_path', type=str, default="./", help='Path where data is saved')
    parser.add_argument('--use_cached_data', type=bool, default=True, help='If data is available on the data path, use it')
    args = parser.parse_args()

    graph = Graph(uri=args.grakn_uri, keyspace=args.keyspace)

    offset = 0
    max_results = args.max_results

    query = '''match $movie isa movie; $movie has title $title; 
($g, $movie) isa has-genre; $g has description $genre; 
($movie, director:$d) isa production-crew; $d has name $director;'''

    query += 'offset {}; limit {};'.format(offset, max_results)

    results = load_data(args, graph, query)

    logging.debug("Results of type {}".format(results[0]))

    df_results = json_normalize(results)

    labels = df_results[['genre']]
    features = ['director', 'year', '']
    features = df_results[features]
    x_train, x_test, y_train, y_test = sk.model_selection.train_test_split(features, labels, test_size=0.20)

    logger.debug(print(x_train))
    logger.debug(print(y_train))

    num_classes = y_test['genre'].nunique()
    num_features = len(features)

    logger.debug("Learning with {} classes and {} features".format(num_classes, num_features))

    params = tf.contrib.tensor_forest.python.tensor_forest.ForestHParams(num_classes=num_classes,
                                                                         num_features=num_features,
                                                                         num_trees=2, max_nodes=10)

    classifier = tf.contrib.tensor_forest.client.random_forest.TensorForestEstimator(params, model_dir=args.model_path)

    classifier.fit(x=x_train, y=y_train)
    classifier.evaluate(x=x_test, y=y_test, steps=10)


def load_data(args, graph, query):
    hq = str(hash(query))
    if os.path.exists(os.path.join(args.data_path, hq)):
        with open(hq, 'rb') as fp:
            results = pickle.load(fp)
    else:
        results = graph.execute(query)
        with open(hq, 'wb') as fp:
            pickle.dump(results, fp)
    return results


if __name__ == "__main__":
    main()
