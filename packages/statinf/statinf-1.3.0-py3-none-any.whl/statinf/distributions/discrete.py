import numpy as np
import math
from decimal import Decimal

import datetime

import scipy
from scipy.special import factorial, gamma, gammaln
from scipy import optimize
import warnings
from numba import njit


scipy_methods = ['BFGS', 'L-BFGS-B', 'Newton-CG', 'CG', 'Powell', 'Nelder-Mead']

# Empty object with future attributes
class _Object(object):
    pass


# Generic Discrete class for discrete probability functions
class Discrete:
    def __init__(self) -> None:
        """A generic class for discrete probability distributions
        """
        self.eps = 10e-4

        # Negative log-likelihood function
        self.nll_fun = lambda params, data: self.nloglike(params=params, data=data)

    def pmf(self, x):
        pass

    @staticmethod
    def nll(data):
        pass

    def logp(self, *args):
        return self.nll(*args)

    def _generate(self, _pmf, seed=None):
        pp = _pmf[0]
        np.random.seed(seed)
        u = np.random.uniform(0 + self.eps, 1 - self.eps)
        n = 0
        while (pp <= u):
            n += 1
            if n < len(_pmf):
                pp += _pmf[n]
            elif n > len(_pmf):
                n = self._generate(_pmf, seed=seed)
            else:
                pp += self.pmf(n)
        return n

    def _get_ranges(self):
        n = 0
        N = self.pmf(n)

        while N < 0.99999999:
            n += 1
            N += self.pmf(n)[0]
        return range(n)

    def sample(self, size, seed=None):
        _ranges = self._get_ranges()
        _pmf = self.pmf(_ranges)

        # _pmf = [_p for _p in _pmf if _p > 10e-8]

        _seed = seed if seed else datetime.datetime.now().microsecond
        np.random.seed(_seed)
        return [self._generate(_pmf, seed=_seed + i) for i in range(size)]

    def _fast_fit(self):
        raise NotImplementedError('Fast or auto fit is not allowed for this distribution, please chose another value')

    def _fit(self, data, bounds=None, init_params=np.array([1]), verbose=False, method='auto', args=()):
        if method.lower() in ['auto', 'fast']:
            res = self._fast_fit(data)
        elif method in scipy_methods:
            if args == ():
                nll_args = (data,)
            else:
                nll_args = sum(((data,), args), ())
            res = scipy.optimize.minimize(
                fun=self.nll_fun,
                x0=init_params,
                args=nll_args,
                method=method,
                bounds=bounds
            )
            self.nll = res.fun
            self.ll = -self.nll

            if verbose:
                print(res)
        else:
            raise ValueError(f"The selected method is not valid, should be on of {', '.join(scipy_methods)}")

        return res


class Poisson(Discrete):
    def __init__(self, lambda_=None, *args, **kwargs) -> None:
        """Poisson distribution.

        The Poisson distribution is the most common probability distribution for count data.

        :formula: The probability mass function is defined by

            .. math:: \\mathbb{P}(X = x | \\lambda) = \\dfrac{\\lambda^{x}}{x!} e^{- \\lambda}

        The distribution assumes equi-dispersion, meaning that :math:`\\mathbb{E}(X) = \\mathbb{V}(X)`.

        :param lambda\\_: Parameter :math:`\\lambda` representing the both location (:math:`\\mathbb{E}(X)`) and the scale (:math:`\\mathbb{V}(X)`) parameters, defaults to None
        :type lambda\\_: :obj:`float`, optional

        :example:

        >>> from statinf.distributions import Poisson
        >>> # Let us generate a random sample of size 1000
        >>> x = Poisson(lambda_=2.5).sample(size=1000)
        >>> # We can also estimate the parameter from the generated sample
        >>> # We just need to initialize the class...
        >>> poiss = Poisson()
        >>> # ... and we can fit from the generated sample. The function returns a dictionary
        >>> poiss.fit(x)
        ... {'lambda_': 2.46}
        >>> # The class stores the value of the estimated parameters
        >>> print(poiss.lambda_)
        ... 2.46
        >>> # So we can generate more samples using the fitted parameters
        >>> y = poiss.sample(200)

        :reference: * DeGroot, M. H., & Schervish, M. J. (2012). `Probability and statistics <https://www.stat.cmu.edu/~mark/degroot/index.html>`_. Pearson Education.
        """
        super(Poisson, self).__init__(*args, **kwargs)
        self.lambda_ = lambda_

    def pmf(self, x) -> float:
        """Computes the probability mass function for selected value :obj:`x`.

        :formula: The probability mass function (pmf) is computed by

            .. math:: \\mathbb{P}(X = x | \\lambda) = \\dfrac{\\lambda^{x}}{x!} e^{- \\lambda}

        :param x: Value to be evaluated
        :type x: :obj:`int`

        :return: Probability :math:`\\mathbb{P}(X = x | \\lambda, \\nu)`
        :rtype: :obj:`float`
        """
        x = [x] if type(x) in [float, int] else x

        _el = np.asarray(math.exp(-self.lambda_))
        # Compute $\lambda^{x}$
        _pow = [pow(self.lambda_, _x) for _x in x]
        try:
            _pow = [float(p) for p in _pow]
            _dec = False
        except OverflowError:
            # Inf the integers to compute are too large, we use decimal format
            # Ref: https://stackoverflow.com/questions/16174399/overflowerror-long-int-too-large-to-convert-to-float-in-python
            _pow = [Decimal(p) for p in _pow]
            _dec = True

        _fact = [math.factorial(_x) for _x in x]
        if _dec:
            # If decimal was used for power calculations, we have to use the same for factorial
            _fact = [Decimal(p) for p in _fact]

        return _el * [float(p / f) for p, f in zip(_pow, _fact)]

    @staticmethod
    def nloglike(params, data) -> float:
        """Static method to estumate the negative likelihood (used in :meth:`statinf.distributions.discrete.Poisson.fit` method).

        :formula: The log-likelihood function :math:`l` is defined by

            .. math:: \\mathcal{l}(x_1, ..., x_n | \\lambda, \\nu) = - n \\lambda + \\log(\\lambda) \\sum_{i=1}^{n} {x_i} - \\sum_{i=1}^{n} {\\log(x_i!)}

        :param params: List containing parameter :math:`\\lambda`
        :type params: :obj:`list`
        :param data: Data to evaluate the netative log-likelihood on
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`

        :return: Negative log-likelihood
        :rtype: :obj:`float`
        """
        lambda_ = params[0]
        X = data
        _n_l = -len(X) * lambda_
        _sumX_log_l = np.sum(X) * math.log(lambda_)
        _log_fact = np.sum([math.log(math.factorial(_x)) for _x in X])
        ll = _n_l + _sumX_log_l - _log_fact
        return -ll

    def _get_ranges(self) -> range:
        """Define the range of values :math:`x` to pull data from when generating a random sample

        :return: Range of values from :math:`0` to :math:`5 (\\lambda + 1)`
        :rtype: :obj:`range`
        """
        return range(0, 5 * int(self.lambda_ + 1))

    def _fast_fit(self, data) -> dict:
        """Fast estimation method to compute parameter's value based on empirical mean

        :param data: Data to estimate the paramter from
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`

        :return: Estmated parameters
        :rtype: :obj:`dict`
        """
        res = _Object()
        data = np.asarray(data)
        res.x = [data.mean()]
        return res

    def fit(self, data, method='fast', **kwargs) -> dict:
        """Estimates the parameter :math:`\\lambda` of the distribution from empirical data based on Maximum Likelihood Estimation.

        The Maximum Likihood Estimator also corresponds to the emprical mean:

            .. math:: \\hat{\\lambda}_{\\text{MLE}} = \\dfrac{1}{n} \\sum_{i=1}^{n} x_i

        The `method = 'fast'` is available to estimate the parameter directly from the emprical mean.
        Any other value for the parameter `method` will use classical MLE.

        :param data: Data to fit and estimate parameters from.
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`
        :param method: Optimization method to estimate the parameters as in the scipy library (allows 'fast' value), defaults to 'L-BFGS-B'
        :type method: :obj:`str`, optional

        :return: Estimated parameter
        :rtype: :obj:`dict`
        """
        bounds = [(self.eps, None)]
        init_params = np.array([1])

        res = self._fit(data=data, bounds=bounds, method=method, init_params=init_params, **kwargs)
        self.lambda_ = res.x[0]

        out = {'lambda_': self.lambda_}

        if method in scipy_methods:
            out.update({'loglikelihood': self.ll})

        return out


class CMPoisson(Discrete):
    def __init__(self, lambda_=None, nu_=None, j=500, *args, **kwargs) -> None:
        """Conway-Maxwell Poisson distribution.
        This class allows to generate a random variable based on selected parameters and size but also to fit some data and estimate the parameters by means of Maximum Likelihood Estimation (MLE).

        Introduced by Conway and Maxwell (1962), the Conway-Maxwell Poisson (aka CMP) is a generalization of the common Poisson distribution
        (:class:`statinf.distributions.discrete.Poisson`).
        The distribution can handle non equi-dispersion cases where :math:`\\mathbb{E}(X) \\neq \\mathbb{V}(X)`.
        The level of dispersion is captured by :math:`\\nu` such that underdispersion is captured when :math:`\\nu > 1`,
        equidispersion :math:`\\nu = 1` and overdispersion when :math:`\\nu < 1`.

        :formulae: The probability mass function (pmf) is defined by

            .. math:: \\mathbb{P}(X = x | \\lambda, \\nu) = \\dfrac{\\lambda^{x}}{(x!)^{\\nu}} \\dfrac{1}{Z(\\lambda, \\nu)}

            where :math:`Z(\\lambda, \\nu) = \\sum_{j=0}^{\\infty} \\dfrac{\\lambda^{j}}{(j!)^{\\nu}}` is calculated in :py:meth:`statinf.distributions.discrete.CMPoisson.Z`.

        Special cases of the CMP distribution include well-known distributions.

            * When :math:`\\nu = 1`, one recovers the Poisson distribution with parameter :math:`\\lambda`
            * When :math:`\\nu = 0` and :math:`\\lambda < 1` one recovers the geometric distribution with parameter :math:`p = 1 - \\lambda` for the probability of success
            * When :math:`\\nu \\rightarrow \\infty`, one finds the Bernoulli distribution with parameter :math:`p = \\frac{\\lambda}{1 + \\lambda}` for the probability of success

        :param lambda\\_: Parameter :math:`\\lambda` representing the generalized expectation, defaults to None
        :type lambda\\_: :obj:`float`, optional
        :param nu\\_: Parameter :math:`\\nu` representing the level of dispersion, defaults to None
        :type nu\\_: :obj:`float`, optional
        :param j: Length of the sum for the normalizing constant (see :meth:`statinf.distributions.discrete.CMPoisson.Z`), defaults to 250
        :type j: :obj:`int`, optional

        :example:

        >>> from statinf.distributions import CMPoisson
        >>> # Let us generate a random sample of size 1000
        >>> x = CMPoisson(lambda_=2.5, nu_=1.5).sample(size=1000)
        >>> # We can also estimate the parameters from the generated sample
        >>> # We just need to initialize the class...
        >>> cmp = CMPoisson()
        >>> # ... and we can fit from the generated sample. The function returns a dictionary
        >>> cmp.fit(x)
        ... {'lambda_': 2.7519745539344687, 'nu_': 1.5624694839612023, 'nll': 1492.0792423744383}
        >>> # The class stores the value of the estimated parameters
        >>> print(cmp.lambda_)
        ... 2.7519745539344687
        >>> # So we can generate more samples using the fitted parameters
        >>> y = cmp.sample(200)


        :reference: * Conway, R. W., & Maxwell, W. L. (1962). `A queuing model with state dependent service rates <https://archive.org/details/sim_journal-of-industrial-engineering_march-april-1961_12_2/page/132/mode/2up>`_. Journal of Industrial Engineering, 12(2), 132-136.
            * Shmueli, G., Minka, T. P., Kadane, J. B., Borle, S., & Boatwright, P. (2005). `A useful distribution for fitting discrete data: revival of the Conway-Maxwell-Poisson distribution <https://doi.org/10.1111/j.1467-9876.2005.00474.x>`_. Journal of the Royal Statistical Society: Series C (Applied Statistics), 54(1), 127-142.
            * Sellers, K. F., Swift, A. W., & Weems, K. S. (2017). `A flexible distribution class for count data <https://doi.org/10.1186/s40488-017-0077-0>`_. Journal of Statistical Distributions and Applications, 4(1), 1-21.
            * Sellers, K. (2023). `The Conway-Maxwell-Poisson Distribution <https://www.cambridge.org/core/books/conwaymaxwellpoisson-distribution/61BC55F43441FF415AEECA9F51FB4660>`_ (Institute of Mathematical Statistics Monographs). Cambridge: Cambridge University Press.
        """
        super(CMPoisson, self).__init__(*args, **kwargs)
        self.lambda_ = lambda_
        self.nu_ = nu_

        self.j = j

        self._Z = None

        if (self.lambda_ is not None) & (self.nu_ is not None):
            assert self.lambda_ >= 0, ValueError('Value for parameter lambda must be strictly greater to 0 (lambda_ > 0)')
            assert self.nu_ >= 0, ValueError('Value for parameter nu must be greater or equal to 0 (nu_ >= 0)')
            warnings.filterwarnings("ignore", message="overflow encountered")
            self._Z = self.Z(lambda_=self.lambda_, nu_=self.nu_, j=self.j)
            warnings.resetwarnings()

        self.nll_fun = lambda params, data, j: self.nloglike(params=params, data=data, j=j, Z=self.Z)

    @staticmethod
    @njit
    def Z(lambda_, nu_, j=None, log=False) -> float:
        """Compute the :math:`Z` factor, normalizing constant.

        The factor :math:`Z(\\lambda, \\nu)` serves as a normalizing constant such that the distribution satisfies the basic probability axioms (i.e. the probability mass function sums up to 1).

        .. math::

            Z(\\lambda, \\nu) = \\sum_{j=0}^{\\infty} \\dfrac{\\lambda^{j}}{(j!)^{\\nu}}

        .. note::

            For implementation purposes, the length of the sum cannot be infinity.
            The parameter :obj:`j` is chosen to be suficiently large so that the value of the sum converges to its asymptotic value.
            Note that too large values for :obj:`j` will imply longer computation time and potential errors
            (:math:`j!` may become too large and might not fit in memory).

        :param lambda\\_: First parameter :math:`\\lambda > 0` of the distribution
        :type lambda\\_: :obj:`float`, optional
        :param nu\\_: Second parameter :math:`\\nu > 0` of the distribution
        :type nu\\_: :obj:`float`, optional
        :param j: Length of the sum for the normalizing constant, if :obj:`None` then we use the value from the :obj:`__init__` method, defaults to None
        :type j: :obj:`int`, optional
        :param log: Compute :math:`\\log(Z(\\lambda, \\nu))`, defaults to False
        :type log: :obj:`bool`

        :return: Normalizing factor :math:`Z`
        :rtype: :obj:`float`
        """
        (z, log_lam, log_fac_i) = (1, np.log(lambda_), 0)
        for i in range(1, j):
            log_fac_i += np.log(i)
            z += np.exp((i * log_lam) - (nu_ * log_fac_i))

        if log:
            z = math.log(z)

        return z

    def pmf(self, x) -> float:
        """Computes the probability mass function for selected value :obj:`x`.

        :formula: The probability mass function (pmf) is computed by

            .. math:: \\mathbb{P}(X = x | \\lambda, \\nu) = \\dfrac{\\lambda^{x}}{(x!)^{\\nu}} \\dfrac{1}{Z(\\lambda, \\nu)}

            where :math:`Z(\\lambda, \\nu) = \\sum_{j=0}^{\\infty} \\dfrac{\\lambda^{j}}{(j!)^{\\nu}}` is calculated in :py:meth:`statinf.distributions.discrete.CMPoisson.Z`.

        :param x: Value to be evaluated
        :type x: :obj:`int`

        :return: Probability :math:`\\mathbb{P}(X = x | \\lambda, \\nu)`
        :rtype: :obj:`float`
        """
        x = [x] if type(x) in [float, int] else x

        # Compute $\lambda^{x}$
        _pow = [pow(self.lambda_, _x) for _x in x]

        _dec = False
        try:
            _pow = [float(p) for p in _pow]
        except OverflowError:
            # Inf the integers to compute are too large, we use decimal format
            # Ref: https://stackoverflow.com/questions/16174399/overflowerror-long-int-too-large-to-convert-to-float-in-python
            _pow = [Decimal(p) for p in _pow]
            _dec = True

        # Compute $(x!)^{\nu}$
        _fact = [np.exp(self.nu_ * np.sum(np.log(range(1, _x + 1)))) for _x in x]
        if _dec:
            _fact = [Decimal(f) for f in _fact]

        a = np.array([float(p / f) for p, f in zip(_pow, _fact)])
        return a * (1 / self._Z)

    @staticmethod
    def nloglike(params, data, Z, j=100) -> float:
        """Static method to estumate the negative likelihood (used in :meth:`statinf.distributions.discrete.CMPoisson.fit` method).

        :formula: The log-likelihood function :math:`l` is defined by

            .. math:: \\mathcal{l}(x_1, ..., x_n | \\lambda, \\nu) = \\log (\\lambda) \\sum_{i}^{n} {x_i} - \\nu \\sum_{i}^{n} {\\log (x_i!)} - n \\log (Z(\\lambda, \\nu))

        :param params: List of parameters :math:`\\lambda` and :math:`\\nu`
        :type params: :obj:`list`
        :param data: Data to evaluate the netative log-likelihood on
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`
        :param j: Length of the inifinite sum for the normalizing factor :math:`Z`, defaults to 100
        :type j: :obj:`int`, optional

        :return: Negative log-likelihood
        :rtype: :obj:`float`
        """
        lambda_ = params[0]
        nu_ = params[1]
        X = np.asarray(data)
        n = len(X)

        # Compute log(Z)
        log_Z = Z(lambda_=lambda_, nu_=nu_, j=j, log=True)

        _log_fact = np.asarray([math.log(math.factorial(_x)) for _x in X])
        ll = math.log(lambda_) * np.sum(X)
        ll += - (nu_ * np.sum(_log_fact))
        ll += - (n * log_Z)
        return -ll

    def fit(self, data, method='L-BFGS-B', init_params='auto', j=None, bounds=None) -> dict:
        """Estimates the parameters :math:`\\lambda` and :math:`\\nu` of the distribution from empirical data based on Maximum Likelihood Estimation.

        .. note::

            There is no close form to estimate the parameters nor a direct relation between the empirical moments (:math:`\\bar{X}`) and the theoretical ones.
            Therefore, only MLE is available (no fast method).

        :param data: Data to fit and estimate parameters from.
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`
        :param method: Optimization method to estimate the parameters, defaults to 'L-BFGS-B'
        :type method: :obj:`str`, optional
        :param init_params: Initial parameters for the optimization method, defaults to :obj:`np.array([1., 0.5])`
        :type init_params: :obj:`numpy.array`, optional

        :return: Estimated parameters
        :rtype: :obj:`dict`
        """
        # We transform warnings as error (for overflow) to handle in try / except: https://stackoverflow.com/questions/5644836/
        j = j if j else self.j
        data = np.asarray(data)
        if bounds is None:
            bounds = [(self.eps, None), (self.eps, None)]
        if init_params == 'auto':
            _disp = data.mean() / data.var()
            init_params = np.array([data.mean(), _disp])

        warnings.filterwarnings("ignore", message="overflow encountered")
        res = self._fit(data=data, bounds=bounds, method=method, init_params=init_params, args=(j,))
        self.lambda_ = res.x[0]
        self.nu_ = res.x[1]
        self._Z = self.Z(lambda_=self.lambda_, nu_=self.nu_, j=j)
        warnings.resetwarnings()

        out = {'lambda_': self.lambda_, 'nu_': self.nu_, 'convergence': res.success}

        if method in scipy_methods:
            out.update({'loglikelihood': self.ll})

        return out


class NegativeBinomial(Discrete):
    def __init__(self, r_=None, p_=None, *args, **kwargs) -> None:
        """Negative Binomial distribution.

        :formulae: The probability mass function (pmf) is defined by

            .. math:: \\mathbb{P}(X = x | r, p) = \\dfrac{(x + r - 1)!}{(r - 1)! x!} (1 - p)^{k} p^{r}

        :example:

        >>> from statinf.distributions import NegativeBinomial
        >>> # Let us generate a random sample of size 1000
        >>> x = NegativeBinomial(n_=5, p_=0.15).sample(size=1000)
        >>> # We can also estimate the parameters from the generated sample
        >>> # We just need to initialize the class...
        >>> nb = NegativeBinomial()
        >>> # ... and we can fit from the generated sample. The function returns a dictionary
        >>> nb.fit(x)
        ... {'r_': 5, 'p_': 0.15069905301345346, 'convergence': True, 'loglikelihood': -3972.2726626530775}
        >>> # The class stores the value of the estimated parameters
        >>> print(nb.p_)
        ... 0.15069905301345346
        >>> # So we can generate more samples using the fitted parameters
        >>> y = nb.sample(200)


        :reference: * DeGroot, M. H., & Schervish, M. J. (2012). Probability and statistics. Pearson Education.
        """
        super(NegativeBinomial, self).__init__(*args, **kwargs)
        self.r_ = r_
        self.p_ = p_

    def pmf(self, x) -> float:
        """Computes the probability mass function for selected value :obj:`x`.

        :formula: The probability mass function (pmf) is computed by

            .. math:: \\mathbb{P}(X = x | r, p) = \\dfrac{(x + r - 1)!}{(r - 1)! x!} (1 - p)^{k} p^{r}

        :param x: Value to be evaluated
        :type x: :obj:`int`

        :return: Probability :math:`\\mathbb{P}(X = x | r, p)`
        :rtype: :obj:`float`
        """
        x = [x] if type(x) in [float, int] else x

        _comb = np.array([scipy.special.comb(_x + self.r_ - 1, _x, exact=True) for _x in x])

        # _comb = np.array([_a / _b for _a, _b in zip(_num, _denom)])
        _m1 = np.array([pow(1 - self.p_, _x) for _x in x])
        _m2 = pow(self.p_, self.r_)
        return _comb * _m1 * _m2

    @staticmethod
    def nloglike(params, data, eps=10e-4) -> float:
        """Static method to estumate the negative likelihood (used in :meth:`statinf.distributions.discrete.NegativeBinomial.fit` method).

        :formula: The log-likelihood function :math:`l` is defined by

            .. math:: \\mathcal{l}(x_1, ..., x_n | r, p) &= \\sum_{i=1}^{n} {\\log(\\Gamma(x_i + r))} \\sum_{i=1}^{n} {\\log(x_i!)} - N \\log(\\Gamma(r)) \\\\ &+ \\sum_{i=1}^{n} {x_i \\log(1-p)} + N r \\log(p)

        :param params: List of parameters :math:`r` and :math:`p`
        :type params: :obj:`list`
        :param data: Data to evaluate the netative log-likelihood on
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`

        :return: Negative log-likelihood
        :rtype: :obj:`float`
        """
        r_ = params[0]
        p_ = params[1]
        X = np.asarray(data)
        n = len(X)

        ll = np.sum(gammaln(X + r_))
        ll += - np.sum(np.log(factorial(X)))
        ll += - n * (gammaln(r_))
        ll += n * r_ * np.log(p_)
        ll += np.sum(X * np.log(1 - (p_ if p_ < 1 else 1 - eps)))
        return -ll

    def fit(self, data, method='L-BFGS-B', init_params=[1, 0.5], bounds=None, **kwargs) -> dict:
        """Estimates the parameters :math:`\\lambda` and :math:`\\nu` of the distribution from empirical data based on Maximum Likelihood Estimation.

        .. note::

            There is no close form to estimate the parameters. Therefore, only MLE is available (no fast method).

        :param data: Data to fit and estimate parameters from.
        :type data: :obj:`numpy.array` or :obj:`list` or :obj:`pandas.Series`
        :param method: Optimization method to estimate the parameters, defaults to 'L-BFGS-B'
        :type method: :obj:`str`, optional
        :param init_params: Initial parameters for the optimization method, defaults to :obj:`np.array([1., 1.])`
        :type init_params: :obj:`numpy.array`, optional

        :return: Estimated parameters
        :rtype: :obj:`dict`
        """
        if bounds is None:
            bounds = [(self.eps, None), (self.eps, 1)]

        res = self._fit(data=data, bounds=bounds, method=method, init_params=init_params, **kwargs)
        self.r_ = int(round(res.x[0], 0))
        self.p_ = res.x[1]

        out = {'r_': self.r_, 'p_': self.p_, 'convergence': res.success}

        if method in scipy_methods:
            out.update({'loglikelihood': self.ll})

        return out
