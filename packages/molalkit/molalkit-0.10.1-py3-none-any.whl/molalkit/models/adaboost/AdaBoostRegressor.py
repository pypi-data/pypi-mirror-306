#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import AdaBoostRegressor as AdaBoostR
from molalkit.models.base import BaseSklearnModel


class AdaBoostRegressor(AdaBoostR, BaseSklearnModel):
    def fit_molalkit(self, train_data):
        return self.fit_molalkit_(train_data, self)

    def predict_uncertainty(self, pred_data):
        X = pred_data.X
        # TODO
        raise NotImplementedError

    def predict_value(self, pred_data):
        X = pred_data.X
        return super().predict(X)
