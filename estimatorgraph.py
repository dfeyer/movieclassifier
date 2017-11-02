from grakn.client import Graph
from typing import Any


class EstimatorGraph(Graph):
    def __init__(self, uri: str = Graph.DEFAULT_URI, keyspace: str = 'grakn', estimator=None):
        Graph.__init__(self, uri=uri, keyspace=keyspace)
        if hasattr(estimator, "predict"):
            self.estimator = estimator
        else:
            raise Exception("Estimator is expected to have a predict method")

    def execute(self, query: str) -> Any:
        result = Graph.execute(self, query=query)
        return self.estimator.predict(result)
