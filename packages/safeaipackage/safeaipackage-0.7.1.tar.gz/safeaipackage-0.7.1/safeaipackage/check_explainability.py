import pandas as pd
import numpy as np
from typing import Union
from .core import rga
from .util.utils import manipulate_testdata, validate_variables, convert_to_dataframe, check_nan, find_yhat
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.base import is_classifier, is_regressor
from sklearn.base import BaseEstimator
from xgboost import XGBClassifier, XGBRegressor


def compute_rge_values(xtrain: pd.DataFrame, 
                        xtest: pd.DataFrame, 
                        yhat: list, 
                        model: Union[CatBoostClassifier, CatBoostRegressor, XGBClassifier, XGBRegressor, BaseEstimator], 
                        variables: list,
                        group: bool = False):
    """
    Compute RANK GRADUATION EXPLAINABILITY (RGE) MEASURE for variables.

    Parameters
    ----------
    xtrain : pd.DataFrame
            A dataframe including train data.
    xtest : pd.DataFrame
            A dataframe including test data.
    yhat : list
            A list of predicted values.
    model : Union[CatBoostClassifier, CatBoostRegressor, XGBClassifier, XGBRegressor, BaseEstimator]
            A trained model, which could be a classifier or regressor. 
    variables : list
            A list of variables.
    group : Boolean. 
            If it is True, RGE value is found for the group of variables. 
            Otherwise, RGE is calculated for each variable individualy.

    Returns
    -------
    pd.DataFrame
            The RGE value.
    """
    # Convert inputs to DataFrames and concatenate them
    xtrain, xtest, yhat = convert_to_dataframe(xtrain, xtest, yhat)
    # check for missing values
    check_nan(xtrain, xtest, yhat)
    # variables should be a list
    validate_variables(variables, xtrain)
    
    if group:
        # Apply manipulate_testdata iteratively for each variable in the group
        for variable in variables:
            xtest = manipulate_testdata(xtrain, xtest, model, variable)
        
        # Calculate yhat after manipulating variables 
        yhat_rm = find_yhat(model, xtest)
        
        # Calculate a single RGE for the entire group
        rge = 1 - (rga(yhat, yhat_rm))
        return pd.DataFrame([rge], index=[str(variables)], columns=["RGE"])

    else:
        # Calculate RGE for each variable individually
        rge_list = []
        for variable in variables:
            xtest_rm = manipulate_testdata(xtrain, xtest, model, variable)
            yhat_rm = find_yhat(model, xtest_rm)
            rge_list.append(1 - (rga(yhat, yhat_rm)))
        
        return pd.DataFrame(rge_list, index=variables, columns=["RGE"]).sort_values(by="RGE", ascending=False)