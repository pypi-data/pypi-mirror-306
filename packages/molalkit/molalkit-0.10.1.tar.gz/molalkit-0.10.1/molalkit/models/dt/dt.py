from sklearn.tree import DecisionTreeClassifier as DTC
from molalkit.models.base import BaseSklearnModel


class DecisionTreeClassifier(DTC, BaseSklearnModel):
    def fit_molalkit(self, train_data):
        return self.fit_molalkit_(train_data, self)

    def predict_uncertainty(self, pred_data):
        return self.predict_uncertainty_c(pred_data, self)

    def predict_value(self, pred_data):
        return self.predict_value_c(pred_data, self)
