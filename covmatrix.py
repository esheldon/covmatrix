"""
module to calculate
- The Hessian matrix of a function
- The covariance matrix of log probability functions, using the Hessian
  as a Gaussian approximation

    Copyright (C) 2014  Erin Sheldon, Brookhaven National Laboratory

    This program is free software; you can redistribute it and/or modify
    it under the terms of version 2 of the the GNU General Public License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from __future__ import print_function

import numpy
from numpy import exp, array, linalg, zeros, isscalar

def calc_cov(func, x, h):
    """
    Calculate the covariance matrix of the input log probability function
    using the Hessian as a gaussian approximation.

    cov = -H^{-1}

    parameters
    ---------
    func: function
        A function representing the log(probability(x))
    x: array
        the position about which to calculate the deriviatives
    h: scalar or array
        Step size, or sizes, to use for finite differencing

        If a scalar is input, it is used for all dimensions

    returns
    -------
    The covariace matrix derived from the Hessian. See calc_hess

    restrictions
    ------------
    The Hessian must be invertible
    """
    hess = calc_hess(func, x, h)
    cov = -linalg.inv(hess)
    return cov

def calc_hess(func, x, h):
    """
    calculate the Hessian matrix

       d^2 f
    ----------
     dx_i dx_j

    parameters
    ---------
    func: function
        A function than takes an array x as the argument
    x: array
        the position about which to calculate the deriviatives
    h: scalar or array
        Step size, or sizes, to use for finite differencing

        If a scalar is input, it is used for all dimensions

    returns
    -------
    The Hessian matrix calculated via finite differences
    """

    x, h = _get_x_and_h(x, h)
    ndim=x.size

    hess=zeros( (ndim,ndim) )

    for i in range(ndim):
        for j in range(i,ndim):
            if i==j:
                hess[i,i] = calc_partial_ii(func, x, i, h[i])
            else:
                hess[i,j] = calc_partial_ij(func, x, i, j, h[i], h[j])
                hess[j,i] = hess[i,j]

    return hess

def calc_partial_ij( func, xin, i, j, h, k):
    """
    calculate the second partial with respect to a single variable.
    Four function evaluations

    f(x+h,y+k) - f(x+h,y-k) - f(x-h,y+k) + f(x-h,y-k)
    -------------------------------------------------
                         4*h*k
    """
    x=xin.copy()

    # f(x+h, y+h)
    x[i] = xin[i] + h
    x[j] = xin[j] + k
    f1=func(x)

    # f(x+h, y-h)
    #x[i] = xin[i] + h
    x[j] = xin[j] - k
    f2=func(x)

    # f(x-h, y+h)
    x[i] = xin[i] - h
    x[j] = xin[j] + k
    f3=func(x)

    # f(x-h, y-h)
    #x[i] = xin[i] - h
    x[j] = xin[j] - k
    f4=func(x)

    num = f1 - f2 - f3 + f4
    denom=4.*h*k

    deriv = num/denom
    return deriv

def calc_partial_ii( func, xin, i, h ):
    """
    calculate the second partial with respect to a single variable.

    Three function evaluations instead of 4 used in calc_partial_ij

    f(x+h) - 2*f(x) + f(x-h)
    ------------------------
              h**2
    """
    x=xin.copy()

    # f(xi+h)
    x[i] = xin[i] + h
    f1=func(x)

    # f(x)
    f2=func(xin)

    # f(xi+h)
    x[i] = xin[i] - h
    f3=func(x)

    num = f1 - 2*f2 + f3
    denom=h**2

    deriv = num/denom
    return deriv

def _get_x_and_h(x, h):
    """
    get x and h as arrays.  If h is a scalar, repeat
    it to the size of x
    """

    x=array(x, ndmin=1, copy=False)
    ndim=x.size

    if isscalar(h):
        h = zeros(ndim) + h
    else:
        h=array(h, ndmin=1, copy=False)
        if h.size != x.size:
            raise ValueError("h and x have different "
                             "dimensions: %d %d" % (h.size,x.size))

    return x, h


def test():

    covtrue=array( [ [ 400.0, 0.2, 0.1  ],
                     [ 0.2,   2.0, 0.2  ],
                     [ 0.1,   0.2, 1.0] ] )

    cinvtrue=linalg.inv(covtrue)
    xmean=array( [1.0, 2.0, 3.0] )

    def calc_lnprob(x):
        xdiff = x-xmean

        chi2 = cinvtrue.dot( xdiff ).dot( xdiff )

        return exp( -0.5*chi2 )

    h=1.0e-3

    covmeas = calc_cov(calc_lnprob, xmean, h)

    print("true cov:")
    print(covtrue)
    print("meas cov:")
    print(covmeas)

    print("frac diff:")
    print( (covmeas-covtrue)/covtrue )

if __name__=="__main__":
    test()
