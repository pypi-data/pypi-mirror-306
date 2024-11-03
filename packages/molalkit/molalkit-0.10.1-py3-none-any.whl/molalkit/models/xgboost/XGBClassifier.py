#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from xgboost import XGBClassifier as XGBC
from molalkit.models.base import BaseSklearnModel


class XGBClassifier(XGBC, BaseSklearnModel):
    def fit_molalkit(self, train_data):
        return self.fit_molalkit_(train_data, self)

    def predict_uncertainty(self, pred_data):
        return self.predict_uncertainty_c(pred_data, self)

    def predict_value(self, pred_data):
        return self.predict_value_c(pred_data, self)
