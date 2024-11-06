import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from sklearn.linear_model import LinearRegression
import pytest
from axa_safeai import core, check_explainability, check_fairness, check_robustness


@pytest.fixture
def model_data():
    """Fixture to create needed data for testing the functions."""
    data = pd.DataFrame({
        'age': np.random.randint(20, 60, 100),
        'gender': np.random.choice([0, 1], 100),  # Binary encoding
        'minority': np.random.choice([0, 1], 100),
        'doubling_salary': np.random.choice([0, 1], 100),
        'salary_growth': np.random.rand(100)
                        })
    X = data.drop(["doubling_salary", "salary_growth"], axis=1)
    y_class = data["doubling_salary"]
    y_reg = data["salary_growth"]
    xtrain, xtest, ytrain_cl, ytest_cl = train_test_split(X, y_class, test_size=0.3, random_state=1)
    _, _, ytrain_rg, ytest_rg = train_test_split(X, y_reg, test_size=0.3, random_state=1)
    classification_model = CatBoostClassifier(random_state=123, verbose= False).fit(xtrain, ytrain_cl)
    regression_model = LinearRegression().fit(xtrain, ytrain_rg)
    yhat_cl = [x[1] for x in classification_model.predict_proba(xtest)]
    yhat_rg = regression_model.predict(xtest)
    return {
        "classification model": classification_model,
        "regression model": regression_model,
        "xtrain": xtrain,
        "xtest": xtest,
        "ytrain_class": ytrain_cl,
        "ytest_class": ytest_cl,
        "yhat_class": yhat_cl,
        "ytrain_reg": ytrain_rg,
        "ytest_reg": ytest_rg,
        "yhat_reg": yhat_rg,
            }


### TEST check_accuracy FUNCTIONS
def test_rga_perfect_case():
    """
    Test the rga function for the perfect case.

    This test checks if the RGrgaA function returns a score of 1.0 when the
    predicted values `yhat` exactly match the actual values `y` in terms
    of rank order.
    """
    y = [1, 2, 3, 4, 5]
    yhat = [1, 2, 3, 4, 5]
    assert core.rga(y, yhat) == 1.0  # Perfect case in which all the ranks are the same so functions should give RGA = 1

def test_rga_worst_case():
    """
    Test the rga function for the worst-case scenario.

    This test verifies that the rga function returns a score of 0.0 when
    the predicted values `yhat` are ranked in the exact opposite order
    to the actual values `y`, representing a complete misalignment.
    """
    y = [1, 2, 3, 4, 5]
    yhat = [5, 4, 3, 2, 1]
    assert core.rga(y, yhat) == 0.0  # Worst case in which there is  so functions should give RGA = 0

def test_rga_different_shapes(model_data):
    """
    Test the rga function for inputs with different shapes.

    This test ensures that the rga function raises a ValueError when
    the lengths of `y` and `yhat` do not match, as expected for valid
    input dimensions.
    """
    with pytest.raises(ValueError):
        # Test for a ckassification problem
        core.rga(model_data["ytest_class"], model_data["yhat_class"][:10])
    with pytest.raises(ValueError):
        # Test for a regression problem
        core.rga(model_data["ytest_reg"], model_data["yhat_reg"][:10])

def test_rga_with_nan(model_data):
    """
    Test the rga function with NaN values in the input.

    This test checks that the rga function raises a ValueError when
    any NaN values are present in `y` or `yhat`, since NaN values
    should be considered invalid for ranking calculations.
    """
    y_nan_class = model_data["ytest_class"]
    y_nan_class[2] = np.nan
    with pytest.raises(ValueError):
        # Test for a ckassification problem
        core.rga(y_nan_class, model_data["yhat_class"])

    y_nan_reg = model_data["ytest_reg"]
    y_nan_reg[2] = np.nan
    with pytest.raises(ValueError):
        # Test for a regression problem
        core.rga(y_nan_reg, model_data["yhat_reg"])


### TEST check_explainability FUNCTIONS
def test_rge_valid_input(model_data):
    """
    Test rge computation functions (compute_single_variable_rge, compute_group_variable_rge and compute_full_single_rge) with valid inputs.

    This test verifies that the rge computation functions `compute_single_variable_rge`,
    `compute_group_variable_rge`, and `compute_full_single_rge` roperate 
    correctly under typical conditions.
    """
    # Test compute_single_variable_rge
    # classification problem
    single_var_result_class = check_explainability.compute_single_variable_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_class"],
        model_data["classification model"], ["age"]
    )
    assert single_var_result_class is not None, "compute_single_variable_rge returned None"
    # regression problem
    single_var_result_reg = check_explainability.compute_single_variable_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"],
        model_data["regression model"], ["age"]
    )
    assert single_var_result_reg is not None, "compute_single_variable_rge returned None"

    # Test compute_group_variable_rge
    #classification problem
    group_var_result_class = check_explainability.compute_group_variable_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_class"],
        model_data["classification model"], ["age", "gender"]
    )
    assert group_var_result_class is not None, "compute_group_variable_rge returned None"
    #regression problem
    group_var_result_reg = check_explainability.compute_group_variable_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"],
        model_data["regression model"], ["age", "gender"]
    )
    assert group_var_result_reg is not None, "compute_group_variable_rge returned None"

    # Test compute_full_single_rge
    # classification problem
    full_single_result_class = check_explainability.compute_full_single_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_class"],
        model_data["classification model"]
    )
    assert full_single_result_class is not None, "compute_full_single_rge returned None"
    # regression problem
    full_single_result_reg = check_explainability.compute_full_single_rge(
        model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"],
        model_data["regression model"]
    )
    assert full_single_result_reg is not None, "compute_full_single_rge returned None"

def test_rge_variables_notlist(model_data):
    """
    Test rge computation functions (compute_single_variable_rge, compute_group_variable_rge and compute_full_single_rge) with a non-list `variables` argument.

    This test checks that `compute_single_variable_rge` and
    `compute_group_variable_rge` raise a ValueError if the `variables`
    argument is not passed as a list, ensuring type safety for this parameter.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_class"], model_data["classification model"], variables= "age")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_class"], model_data["classification model"], "age")
        # Test a regression problem
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"], model_data["regression model"], variables= "age")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"], model_data["regression model"], "age")
        
def test_rge_notavailable_variable(model_data):
    """
    Test rge computation functions (compute_single_variable_rge, compute_group_variable_rge and compute_full_single_rge) with variables not present in the dataset.

    This test checks that `compute_single_variable_rge` and 
    `compute_group_variable_rge` raise a ValueError when a variable 
    specified in `variables` does not exist in the input data.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_class"], model_data["classification model"], variables= "country")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_class"], model_data["classification model"], variables= "country")
        # Test a regression problem
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"], model_data["regression model"], variables= "country")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat_reg"], model_data["regression model"], variables= "country")
        
def test_rge_with_nan(model_data):
    """
    Test rge computation functions (compute_single_variable_rge, compute_group_variable_rge and compute_full_single_rge) with NaN values in inputs.

    This test verifies that `compute_single_variable_rge`, 
    `compute_group_variable_rge`, and `compute_full_single_rge`
    raise a ValueError when NaN values are present in `xtrain`, 
    `xtest`, or `yhat`, ensuring that these functions handle
    missing data appropriately.
    """
    #when there are nan values in xtrain to test classification
    xtrain_nan = model_data["xtrain"]  
    xtrain_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        check_explainability.compute_single_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat_class"], 
                                                         model_data["classification model"], ["age"])
        check_explainability.compute_group_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat_class"], 
                                                        model_data["classification model"], ["age"])
        check_explainability.compute_full_single_rge(xtrain_nan, model_data["xtest"], model_data["yhat_class"], 
                                                     model_data["classification model"])
        #when there are nan values in xtrain to test regression
        check_explainability.compute_single_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat_reg"], 
                                                         model_data["regression model"], ["age"])
        check_explainability.compute_group_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat_reg"], 
                                                        model_data["regression model"], ["age"])
        check_explainability.compute_full_single_rge(xtrain_nan, model_data["xtest"], model_data["yhat_reg"], 
                                                     model_data["regression model"])
    #when there are nan values in xtest to test classification
    xtest_nan = model_data["xtest"]  
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        check_explainability.compute_single_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat_class"], 
                                                         model_data["classification model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat_class"], 
                                                        model_data["classification model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], xtest_nan, model_data["yhat_class"], 
                                                     model_data["classification model"])
        #when there are nan values in xtest to test regression
        check_explainability.compute_single_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat_reg"], 
                                                         model_data["regression model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat_reg"], 
                                                        model_data["regression model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], xtest_nan, model_data["yhat_reg"], 
                                                     model_data["regression model"])

    #when there are nan values in yhat to test classification          
    yhat_nan = model_data["yhat_class"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                         model_data["classification model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                        model_data["classification model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                     model_data["classification model"])
    #when there are nan values in yhat to test regression          
    yhat_nan = model_data["yhat_reg"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                         model_data["regression model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                        model_data["regression model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                     model_data["regression model"])

               
### TEST check_fairness FUNCTIONS
def test_rga_parity_valid_input(model_data):
    """
    Test compute_rga_parity function with valid inputs.

    This test verifies that `compute_rga_parity` produces a valid, non-None 
    result when provided with appropriate inputs, including a specified 
    protected variable. Additionally, it checks that the result is a string 
    containing the expected message about RGA-based imparity.
    """
    # Test a classification problem
    result = check_fairness.compute_rga_parity(
        model_data["xtrain"], model_data["xtest"], model_data["ytest_class"],
        model_data["yhat_class"], model_data["classification model"], protectedvariable="gender"
    )
    assert result is not None, "RGA Parity computation returned None"
    assert isinstance(result, str), "Expected a string output from RGA Parity"
    assert "RGA-based imparity" in result, "Expected result to contain RGA-based imparity message"
    # Test a regression problem
    result = check_fairness.compute_rga_parity(
        model_data["xtrain"], model_data["xtest"], model_data["ytest_reg"],
        model_data["yhat_reg"], model_data["regression model"], protectedvariable="gender"
    )
    assert result is not None, "RGA Parity computation returned None"
    assert isinstance(result, str), "Expected a string output from RGA Parity"
    assert "RGA-based imparity" in result, "Expected result to contain RGA-based imparity message"

def test_rga_parity_notavailable_variable(model_data):
    """
    Test compute_rga_parity function with a non-existent protected variable.

    This test checks that `compute_rga_parity` raises a ValueError if 
    the specified `protectedvariable` is not available in the input 
    data, ensuring correct handling of invalid input.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest_class"], 
                                          model_data["yhat_class"], model_data["classification model"], protectedvariable="race")
        # Test a regression problem
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest_reg"], 
                                          model_data["yhat_reg"], model_data["regression model"], protectedvariable="race")

def test_rga_parity_with_nan(model_data):
    """
    Test compute_rga_parity function with NaN values in inputs.

    This test ensures that `compute_rga_parity` raises a ValueError 
    when NaN values are present in any of the inputs (`xtrain`, `xtest`, 
    `ytest`, or `yhat`). 
    """
    #when there are nan values in xtrain to test classification
    xtrain_nan = model_data["xtrain"]  
    xtrain_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(xtrain_nan, model_data["xtest"], model_data["ytest_class"], 
                                          model_data["yhat_class"], model_data["classification model"], protectedvariable="gender")
    #when there are nan values in xtrain to test regression
        check_fairness.compute_rga_parity(xtrain_nan, model_data["xtest"], model_data["ytest_reg"], 
                                          model_data["yhat_reg"], model_data["regression model"], protectedvariable="gender")
        
    #when there are nan values in xtest to test classification
    xtest_nan = model_data["xtest"]  
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(model_data["xtrain"], xtest_nan, model_data["ytest_class"], 
                                    model_data["yhat_class"], model_data["classification model"], protectedvariable="gender")
    #when there are nan values in xtest to test regression
        check_fairness.compute_rga_parity(model_data["xtrain"], xtest_nan, model_data["ytest_reg"], 
                                    model_data["yhat_reg"], model_data["regression model"], protectedvariable="gender")
    
    #when there are nan values in y to test classification
    y_nan = model_data["ytest_class"] 
    y_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], y_nan, 
                                    model_data["yhat_class"], model_data["classification model"], protectedvariable="gender")
    #when there are nan values in y to test regression
    y_nan = model_data["ytest_reg"] 
    y_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], y_nan, 
                                    model_data["yhat_reg"], model_data["regression model"], protectedvariable="gender")

    #when there are nan values in yhat to test classification          
    yhat_nan = model_data["yhat_class"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest_class"], 
                                          yhat_nan, model_data["classification model"], protectedvariable="gender")
    #when there are nan values in yhat to test regression          
    yhat_nan = model_data["yhat_reg"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest_reg"], 
                                          yhat_nan, model_data["regression model"], protectedvariable="gender")
        
def test_rga_parity_single_group(model_data):
    """
    Test compute_rga_parity function when the protected variable has only one unique value.

    This test verifies that `compute_rga_parity` produces a result indicating no disparity
    when the `protectedvariable` has only one 
    unique value.
    """
    # Test a classification problem
    model_data["xtrain"]["gender"] = 0
    result = check_fairness.compute_rga_parity(
        model_data["xtrain"], model_data["xtest"], model_data["ytest_class"],
        model_data["yhat_class"], model_data["classification model"], protectedvariable="gender"
    )
    assert "0" in result, "Expected no disparity since there's only one group"
    # Test a regression problem
    model_data["xtrain"]["gender"] = 0
    result = check_fairness.compute_rga_parity(
        model_data["xtrain"], model_data["xtest"], model_data["ytest_reg"],
        model_data["yhat_reg"], model_data["regression model"], protectedvariable="gender"
    )
    assert "0" in result, "Expected no disparity since there's only one group"
            

### TEST check_robustness FUNCTIONS
def test_rgr_valid_input(model_data):
    """
    Test rgr computation functions (compute_single_variable_rgr and compute_full_single_rgr) with valid input data.

    This test verifies that `compute_single_variable_rgr` and `compute_full_single_rgr`
    successfully execute and return non-None results when provided with valid input data.
    """
    # Test a classification problem
    result_single = check_robustness.compute_single_variable_rgr(
        model_data["xtest"], model_data["yhat_class"], model_data["classification model"], variables=["gender"]
    )
    result_full = check_robustness.compute_full_single_rgr(
        model_data["xtest"], model_data["yhat_class"], model_data["classification model"]
    )
    assert result_single is not None, "RGR single variable computation failed"
    assert result_full is not None, "RGR full variable computation failed"
    # Test a regression problem
    result_single = check_robustness.compute_single_variable_rgr(
        model_data["xtest"], model_data["yhat_reg"], model_data["regression model"], variables=["gender"]
    )
    result_full = check_robustness.compute_full_single_rgr(
        model_data["xtest"], model_data["yhat_reg"], model_data["regression model"]
    )
    assert result_single is not None, "RGR single variable computation failed"
    assert result_full is not None, "RGR full variable computation failed"

def test_rgr_variables_notlist(model_data):
    """
    Test rgr computation functions (compute_single_variable_rgr and compute_full_single_rgr) with a non-list variable input.

    This test checks that `compute_single_variable_rgr` raises a ValueError when the 
    `variables` parameter is not passed as a list, validating that the function handles 
    improper input types correctly.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_class"], model_data["classification model"], 
                                                     variables= "age")
        # Test a regression problem
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_reg"], model_data["regression model"], 
                                                     variables= "age")

def test_rgr_wrong_perturbation_percentage(model_data):
    """
    Test rgr computation functions (compute_single_variable_rgr and compute_full_single_rgr) with an out-of-bounds perturbation percentage.

    This test verifies that `compute_full_single_rgr` and `compute_single_variable_rgr` 
    raise a ValueError when the `perturbation_percentage` is set outside the allowed 
    range (0 to 0.5). This ensures the function correctly validates input values.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_robustness.compute_full_single_rgr(model_data["xtest"],  model_data["yhat_class"], model_data["classification model"], 
                                                 perturbation_percentage= 0.7)
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_class"], model_data["classification model"], 
                                                     variables= ["age"], perturbation_percentage= 0.7)
        # Test a regression problem
        check_robustness.compute_full_single_rgr(model_data["xtest"],  model_data["yhat_reg"], model_data["regression model"], 
                                                 perturbation_percentage= 0.7)
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_reg"], model_data["regression model"], 
                                                     variables= ["age"], perturbation_percentage= 0.7)

def test_rgr_notavailable_variable(model_data):
    """
    Test compute_single_variable_rgr function with a non-existent variable.

    This test checks that `compute_single_variable_rgr` raises a ValueError when the 
    specified `variables` input is not present in the provided data, ensuring correct 
    handling of invalid variable names.
    """
    with pytest.raises(ValueError):
        # Test a classification problem
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_class"], model_data["classification model"], 
                                                     variables= "race")
        # Test a regression problem
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat_reg"], model_data["regression model"], 
                                                     variables= "race")


def test_rgr_with_nan(model_data):
    """
    Test rgr computation functions (compute_single_variable_rgr and compute_full_single_rgr) with NaN values in the input data.

    This test ensures that `compute_single_variable_rgr` and `compute_full_single_rgr` 
    raise a ValueError when NaN values are present in either `xtest` or `yhat` data, 
    confirming proper handling of incomplete data.
    """
    #when there are nan values in xtest to test classification
    xtest_nan = model_data["xtest"]  
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        check_robustness.compute_single_variable_rgr(xtest_nan, model_data["yhat_class"], model_data["classification model"], 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(xtest_nan,  model_data["yhat_class"], model_data["classification model"])
    #when there are nan values in xtest to test regression
        check_robustness.compute_single_variable_rgr(xtest_nan, model_data["yhat_reg"], model_data["regression model"], 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(xtest_nan,  model_data["yhat_reg"], model_data["regression model"])

    #when there are nan values in yhat to test classification            
    yhat_nan = model_data["yhat_class"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_robustness.compute_single_variable_rgr(model_data["xtest"], yhat_nan, model_data["classification model"], 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(model_data["xtest"], yhat_nan, model_data["classification model"])
    #when there are nan values in yhat to test regression            
    yhat_nan = model_data["yhat_reg"] 
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        check_robustness.compute_single_variable_rgr(model_data["xtest"], yhat_nan, model_data["regression model"], 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(model_data["xtest"], yhat_nan, model_data["regression model"])


