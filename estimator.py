class Estimator:
    def __init__(self, estimator_model, x_attributes, y_attribute):
        try:
            import pandas
        except ImportError:
            print('pandas not available, the results will not contain estimated attributes')
        if hasattr(estimator_model, "predict"):
            self.estimator_model = estimator_model
        else:
            raise Exception("The estimator model requires a predict method")
        self.x_attributes = x_attributes
        self.y_attribute = y_attribute

    def predict(self, x):
        normalized_x = pandas.io.json.json_normalize(x)
        return self.estimator_model.predict(x=normalized_x)
