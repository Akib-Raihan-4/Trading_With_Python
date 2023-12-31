import pandas as pd

def drawdown(return_series: pd.Series):
    """Takes a time series of asset returns
    Computes and returns a DataFrame that contains:
    the wealth index
    previous peaks
    percent drawdowns"""

    wealth_index = 1000*(1+return_series).cumprod()

    previous_peaks = wealth_index.cummax()

    drawdowns = (wealth_index - previous_peaks) / previous_peaks

    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peaks": previous_peaks,
        "Drawdown":drawdowns
    })

def get_ffme_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """

    me_m = pd.read_csv('data/Portfolios_Formed_on_ME_monthly_EW.csv',
                       header= 0, index_col=0, na_values=99.99)
    
    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets /= 100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period('M')
    return rets

def get_hfi_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """

    hfi = pd.read_csv('data/edhec-hedgefundindices.csv',
                       header= 0, index_col=0, parse_dates = True)
    
    hfi /= 100
    hfi.index = hfi.index.to_period('M')
    return hfi

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied Series or DataFrame
    Returns a float or a Series
    """

    demeaned_r = r - r.mean()
    
    #Use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/(sigma_r**3)

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series or DataFrame
    Returns a float or a Series
    """

    demeaned_r = r - r.mean()
    
    #Use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/(sigma_r**4)

import scipy

def is_normal_distributed(r, level = 0.01):
    """Applies the jarque-bera test to determine if a Series is normal or not.
    Test is applied at the 1% level by default
    Returns True if the hypothesis of normality is accepted, False otherwise
    """
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value>level

def semi_deviation(r):
    """Returns the Semi Deviation aka negative semi deviation of r.
    r must be a Series or a DataFrame, else raise a TypeError"""

    excess = r-r.mean()
    excess_negative = excess[excess<0]
    excess_negative_square = excess_negative**2
    n_negative = (excess<0).sum()
    return (excess_negative_square.sum()/n_negative)**0.5


import numpy as np
def var_historic(r, level = 5):
    """
    Returns the historic Value at Risk at a specified level
    i.e. returns the number such that "level" percent of the returns
    fall below that number, and the (100-level) percent are above
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level = level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, level)
    else:
        raise TypeError("Expected r to be Series or Dataframe")


def var_gaussian(r, level = 5, modified = False):
    """Returns the Parametric Gaussian VaR of a Series or DataFrame"""

    z = scipy.stats.norm.ppf(level/100)

    if modified:
        s = skewness(r)
        k = kurtosis(r)
        z = (z + (z**2 - 1)*s/6 +
                (z**3 - 3*z)*(k-3)/24 -
                (2*z**3 - 5*z)*(s**2)/36
        )
    return -(r.mean() + z*r.std(ddof=0))

def cvar_historic(r, level = 5):
    """
    Computes the Conditional VaR of Series or DataFrame
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level = level)
    elif isinstance(r, pd.Series):
        is_beyond = r<= -var_historic(r,level=level)
        return -r[is_beyond].mean()
    else:
        raise TypeError("Expected r to be Series or Dataframe")
