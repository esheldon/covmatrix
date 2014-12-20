covmatrix
=========

Code to calculate ovariance matrices of probability distributions

examples
--------
```python
#
# calculate the covariance matrix
#

h=1.0e-6
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

#
# calculate the hessian matrix
#

hess = calc_hess(calc_lnprob, xmean, h)
```
