"""
Read/write vectors of correlated data from/to a csv file.

These data are stored in a dictionary, whose values are numpy arrays
with elements which may be strings, floats, or floats with associated uncertainties
as defined in the [uncertainties](https://pypi.org/project/uncertainties) library.
"""


__author__    = 'Mathieu Daëron'
__contact__   = 'mathieu@daeron.fr'
__copyright__ = 'Copyright (c) 2024 Mathieu Daëron'
__license__   = 'MIT License - https://opensource.org/licenses/MIT'
__date__      = '2024-11-02'
__version__   = '1.6.0'


import os as _os
import numpy as _np
import uncertainties as _uc

from typing import Callable, Hashable, Any
from uncertainties.unumpy import nominal_values as nv

nv = nv
"""Alias for [`uncertainties.unumpy.nominal_values()`](https://pythonhosted.org/uncertainties/numpy_guide.html#uncertainties-and-nominal-values)"""

class uarray(_np.ndarray):

	__doc__ = """
	1-D [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
	of [UFloat](https://pythonhosted.org/uncertainties/tech_guide.html) values
	"""

	def __new__(cls, a):
		obj = _np.asarray(a).view(cls)
		return obj
	
	@property
	def nv(self):
		"""Return the array of nominal values (read-only)."""
		return _uc.unumpy.nominal_values(_np.array(self))

	@property
	def se(self):
		"""Return the array of standard errors (read-only)"""
		return _uc.unumpy.std_devs(_np.array(self))

	@property
	def correl(self):
		"""Return the correlation matrix of the array elements (read-only)"""
		return _np.array(_uc.correlation_matrix(self))

	@property
	def covar(self):
		"""Return the covariance matrix of the array elements (read-only)"""
		return _np.array(_uc.covariance_matrix(self))
	
	@property
	def mahalanobis(self):
		"""Return the squared Mahalanobis distance from zero of the array (read-only)"""
		flatself = self.n.flatten().reshape((1, self.size))
		return (flatself @ _np.linalg.inv(self.covar) @ flatself.T)[0,0]
	
	n = nv
	"Alias for `uarray.nv`"
	
	s = se
	"Alias for `uarray.se`"
	
	cor = correl
	"Alias for `uarray.correl`"
	
	cov = covar
	"Alias for `uarray.covar`"
	
	m = mahalanobis
	"Alias for `uarray.mahalanobis`"


def is_symmetric_positive_semidefinite(M: _np.ndarray) -> bool:
	'''
	Test whether 2-D array `M` is symmetric and positive semidefinite.
	'''
	ev = _np.linalg.eigvals(M)
	return (
		_np.allclose(M, M.T) # M is symmetric
		and _np.all(
			(ev > 0) | _np.isclose(ev, 0)
		) # all eignevalues are either real and strictly positive or close to zero
	)


def smart_type(s: str) -> (int | float | str):
	'''
	Tries to convert string `s` to an `int`, or to an `float` if that fails.
	If both fail, return the original string unchanged.
	'''
	try: return int(s)
	except: pass
	try: return float(s)
	except: pass
	return s


def read_data(data: str, sep: str = ',', validate_covar: bool = True):
	'''
	Read correlated data from a CSV-like string.
	
	Column names are interpreted in the following way:
	* In most cases, each columns is converted to a dict value, with the corresponding
	dict key being the column's label.
	* Columns whose label starts with `SE` are interpreted as specifying the standard
	error for the latest preceding data column.
	* Columns whose label starts with `correl` are interpreted as specifying the
	correlation matrix for the latest preceding data column. In that case, column labels
	are ignored for the rest of the columns belonging to this matrix.
	* Columns whose label starts with `covar` are interpreted as specifying the
	covariance matrix for the latest preceding data column. In that case, column labels
	are ignored for the rest of the columns belonging to this matrix.
	* `SE`, `correl`, and `covar` may be specified for any arbitrary variable other than
	the latest preceding data column, by adding an underscore followed by the variable's
	label (ex: `SE_foo`, `correl_bar`, `covar_baz`).
	* `correl`, and `covar` may also be specified for any pair of variable, by adding an
	underscore followed by the two variable labels, joined by a second underscore
	(ex: `correl_foo_bar`, `covar_X_Y`). The elements of the first and second variables
	correspond, respectively, to the lines and columns of this matrix.
	* Exceptions will be raised, for any given variable:
		- when specifying both `covar` and any combination of (`SE`, `correl`)
		- when specifying `correl` without `SE`

	**Arguments**
	- `data`: a CSV-like string
	- `sep`: the CSV separator
	- `validate_covar`: whether to check that the overall covariance matrix
	is symmetric and positive semidefinite. Specifying `validate_covar = False`
	bypasses this computationally expensive step.
	
	**Example**
	```py
	import correldata
	data  = """
	Sample, Tacid,  D47,   SE,         correl,,,  D48, covar,,,          correl_D47_D48
	   FOO,   90., .245, .005,      1, 0.5, 0.5, .145,  4e-4, 1e-4, 1e-4, 0.5,   0,   0
	   BAR,   90., .246, .005,    0.5,   1, 0.5, .146,  1e-4, 4e-4, 1e-4,   0, 0.5,   0
	   BAZ,   90., .247, .005,    0.5, 0.5,   1, .147,  1e-4, 1e-4, 4e-4,   0,   0, 0.5
	"""[1:-1]
	print(correldata.read_data(data))
	
	# yields:
	# 
	# > {
	#     'Sample': array(['FOO', 'BAR', 'BAZ'], dtype='<U3'),
	#     'Tacid': array([90., 90., 90.]),
	#     'D47': uarray([0.245+/-0.004999999999999998, 0.246+/-0.004999999999999997, 0.247+/-0.005], dtype=object),
	#     'D48': uarray([0.145+/-0.019999999999999993, 0.146+/-0.019999999999999993, 0.147+/-0.019999999999999997], dtype=object)
	#   }
	```
	'''

	data = [[smart_type(e.strip()) for e in l.split(sep)] for l in data.split('\n')]
	N = len(data) - 1

	values, se, correl, covar = {}, {}, {}, {}
	j = 0
	while j < len(data[0]):
		field = data[0][j]
		if not (
			field.startswith('SE_')
			or field.startswith('correl_')
			or field.startswith('covar_')
			or field == 'SE'
			or field == 'correl'
			or field == 'covar'
			or len(field) == 0
		):
			values[field] = _np.array([l[j] for l in data[1:]])
			j += 1
			oldfield = field
		elif field.startswith('SE_'):
			se[field[3:]] = _np.array([l[j] for l in data[1:]])
			j += 1
		elif field == 'SE':
			se[oldfield] = _np.array([l[j] for l in data[1:]])
			j += 1
		elif field.startswith('correl_'):
			correl[field[7:]] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field == 'correl':
			correl[oldfield] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field.startswith('covar_'):
			covar[field[6:]] = _np.array([l[j:j+N] for l in data[1:]])
			j += N
		elif field == 'covar':
			covar[oldfield] = _np.array([l[j:j+N] for l in data[1:]])
			j += N

	nakedvalues = {}
	for k in [_ for _ in values]:
		if (
			k not in se
			and k not in correl
			and k not in covar
		):
			nakedvalues[k] = values.pop(k)

	for x in values:
		if x in covar:
			if x in se:
				raise KeyError(f'Too much information: both SE and covar are specified for variable "{x}".')
			if x in correl:
				raise KeyError(f'Too much information: both correl and covar are specified for variable "{x}".')
		if x in correl:
			if x not in se:
				raise KeyError(f'Not enough information: correl is specified without SE for variable "{x}".')

	for x in correl:
		if x in values:
			covar[x] = _np.diag(se[x]) @ correl[x] @ _np.diag(se[x])
		else:
			for x1 in values:
				for x2 in values:
					if x == f'{x1}_{x2}':
						if x1 in se:
							se1 = se[x1]
						else:
							if x1 in covar:
								se1 = _np.diag(covar[x1])**0.5
							else:
								raise KeyError(f'Not enough information: correl_{x} is specified without SE for variable "{x1}".')
						if x2 in se:
							se2 = se[x2]
						else:
							if x2 in covar:
								se2 = _np.diag(covar[x2])**0.5
							else:
								raise KeyError(f'Not enough information: correl_{x} is specified without SE for variable "{x1}".')

						covar[x] = _np.diag(se1) @ correl[x] @ _np.diag(se2)

	for x in se:
		if x in values and x not in correl:
			covar[x] = _np.diag(se[x]**2)

	for k in [_ for _ in covar]:
		if k not in values:
			for j1 in values:
				for j2 in values:
					if k == f'{j1}_{j2}':
						covar[f'{j2}_{j1}'] = covar[f'{j1}_{j2}'].T

	X = _np.array([_ for k in values for _ in values[k]])
	CM = _np.zeros((X.size, X.size))
	for i, vi in enumerate(values):
		for j, vj in enumerate(values):
			if vi == vj:
				if vi in covar:
					CM[N*i:N*i+N,N*j:N*j+N] = covar[vi]
			else:
				if f'{vi}_{vj}' in covar:
					CM[N*i:N*i+N,N*j:N*j+N] = covar[f'{vi}_{vj}']

	s = _np.diag(CM)**.5
	s[s==0] = 1.
	invs = _np.diag(s**-1)

	if (
		validate_covar
		and not (
			is_symmetric_positive_semidefinite(CM)
			or is_symmetric_positive_semidefinite(invs @ CM @ invs)
		)
	):
		raise _np.linalg.LinAlgError('The complete covariance matrix is not symmetric positive-semidefinite.')

	corvalues = uarray(_uc.correlated_values(X, CM))

	allvalues = nakedvalues

	for i, x in enumerate(values):
		allvalues[x] = corvalues[i*N:i*N+N]

	return allvalues


def read_data_from_file(filename: str | _os.PathLike, **kwargs):
	'''
	Read correlated data from a CSV file.

	**Arguments**
	- `filename`: `str` or path to the file to read from
	- `kwargs`: passed to correldata.read_data()
	'''
	with open(filename) as fid:
		return read_data(fid.read(), **kwargs)


def f2s(
	x: Any,
	f: (str | Callable | dict),
	k: Hashable = None,
	fb: (str | Callable) = 'z.6g',
) -> str:
	'''
	Format `x` according to format `f`
	
	* If `f` is a string, return `f'{x:{f}}'`
	* If `f` is a callable, return `f(x)`
	* If `f` is a dict and optional argument `k` is a hashable,
	  return f2s(x, f[k]), otherwise return f2s(x, fb)
	'''
	if isinstance (x, str):
		return x
	if isinstance (f, str):
		return f'{x:{f}}'
	if isinstance (f, Callable):
		return f(x)
	if isinstance (f, dict):
		if k in f:
			return f2s(x, f[k])
		if isinstance (fb, str):
			return f'{x:{fb}}'
		if isinstance (fb, Callable):
			return fb(x)
	raise TypeError(f'f2s() formatting argument f = {repr(f)} is neither a string nor a dict nor a callable.')
	


def data_string(
	data: dict,
	sep: str = ',',
	include_fields: list = None,
	exclude_fields: list = [],
	float_format: (str | dict | Callable) = 'z.6g',
	correl_format: (str | dict | Callable) = 'z.6f',
	default_float_format: (str | Callable) = 'z.6g',
	default_correl_format: (str | Callable) = 'z.6f',
	show_nv: bool = True,
	show_se: bool = True,
	show_correl: bool = True,
	show_mixed_correl: bool = True,
	align: str = '>',
	atol: float = 1e-12,
	rtol: float = 1e-12,
):
	'''
	Generate CSV-like string from correlated data

	**Arguments**
	- `data`: dict of arrays with strings, floats or correlated data
	- `sep`: the CSV separator
	- `include_fields`: subset of fields to write; if `None`, write all fields
	- `exclude_fields`: subset of fields to ignore (takes precedence over `include_fields`);
	  to exclude only the SE for field `foo`, include `SE_foo`; same goes for `correl_foo`
	- `float_format`: formatting for float values. May be a string (ex: `'z.3f'`), a callable
	  (ex: `lambda x: '.2f' if x else '0'`), or a dictionary of strings and/or callables, with dict keys
	  corresponding to different fields (ex: `{'foo': '.2e', 'bar': (lambda x: str(x))}`).
	- `correl_format`: same as `float_format`, but applies to correlation matrix elements
	- `default_float_format`: only used when `float_format` is a dict; in that case, fields
	  missing from `float_format.keys()` will use `default_float_format` instead.
	  corresponding to different fields (ex: `{'foo': '.2e', 'bar': `lambda x: str(x)`}`).
	- `default_correl_format`: same as `default_float_format`, but applies to `correl_format`
	- `show_nv`: show nominal values
	- `show_se`: show standard errors
	- `show_correl`: show correlations for any given field (ex: `correl_X`)
	- `show_mixed_correl`: show correlations between different fields (ex: `correl_X_Y`)
	- `align`: right-align (`>`), left-align (`<`), or don't align (empty string) CSV values
	- `atol`: passed to [numpy.allclose()](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html)
	  when deciding whether a matrix is equal to the identity matrix or to the zero matrix
	- `rtol`: passed to [numpy.allclose()](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html)
	  when deciding whether a matrix is equal to the identity matrix or to the zero matrix
	
	
	**Example**
	
	```py
	from correldata import _uc
	from correldata import _np
	from correldata import *
	
	X = uarray(_uc.correlated_values([1., 2., 3.], _np.eye(3)*0.09))
	Y = uarray(_uc.correlated_values([4., 5., 6.], _np.eye(3)*0.16))
	
	data = dict(X=X, Y=Y, Z=X+Y)
	
	print(data_string(data, float_format = 'z.1f', correl_format = 'z.1f'))
	
	# yields:
	# 
	#   X, SE_X,   Y, SE_Y,   Z, SE_Z, correl_X_Z,    ,    , correl_Y_Z,    ,    
	# 1.0,  0.3, 4.0,  0.4, 5.0,  0.5,        0.6, 0.0, 0.0,        0.8, 0.0, 0.0
	# 2.0,  0.3, 5.0,  0.4, 7.0,  0.5,        0.0, 0.6, 0.0,        0.0, 0.8, 0.0
	# 3.0,  0.3, 6.0,  0.4, 9.0,  0.5,        0.0, 0.0, 0.6,        0.0, 0.0, 0.8
	```
	'''
	if include_fields is None:
		include_fields = [_ for _ in data]
	cols, ufields = [], []
	for f in include_fields:
		if f in exclude_fields:
			continue
		if isinstance(data[f], uarray):
			ufields.append(f)
			N = data[f].size
			if show_nv:
				cols.append([f] + [f2s(_, float_format, f, default_float_format) for _ in data[f].n])
			if show_se and (f'SE_{f}' not in exclude_fields):
				cols.append([f'SE_{f}'] + [f2s(_, float_format, f, default_float_format) for _ in data[f].s])
			if show_correl and (f'correl_{f}' not in exclude_fields):
				CM = _uc.correlation_matrix(data[f])
				if not _np.allclose(CM, _np.eye(N), atol = atol, rtol = rtol):
					for i in range(N):
						cols.append(
							['' if i else f'correl_{f}']
							+ [
								f2s(
									CM[i,j],
									correl_format,
									f,
									default_correl_format,
								)
								for j in range(N)
							]
						)
		elif show_nv:
				cols.append([f] + [f2s(_, float_format, f, default_float_format) for _ in data[f]])

	if show_mixed_correl:
		for i in range(len(ufields)):
			for j in range(i):
				if f'correl_{ufields[i]}_{ufields[j]}' in exclude_fields or f'correl_{ufields[j]}_{ufields[i]}' in exclude_fields:
					continue
				CM = _uc.correlation_matrix((*data[ufields[i]], *data[ufields[j]]))[:N, -N:]
				if not _np.allclose(CM, _np.zeros((N, N)), atol = atol, rtol = rtol):
					for k in range(N):
						cols.append(
							['' if k else f'correl_{ufields[j]}_{ufields[i]}']
							+ [
								f2s(
									CM[k,l],
									correl_format,
									f,
									default_correl_format,
								)
								for l in range(N)
							]
						)

	lines = list(map(list, zip(*cols)))

	if align:
		lengths = [max([len(e) for e in l]) for l in cols]
		for l in lines:
			for k,ln in enumerate(lengths):
				l[k] = f'{l[k]:{align}{ln}s}'
		return '\n'.join([(sep+' ').join(l) for l in lines])

	return '\n'.join([sep.join(l) for l in lines])


def save_data_to_file(data, filename, **kwargs):
	'''
	aaa
	
	Write correlated data to a CSV file.

	**Arguments**
	- `data`: dict of arrays with strings, floats or correlated data
	- `filename`: `str` or path to the file to read from
	- `kwargs`: passed to correldata.data_string()
	'''
	with open(filename, 'w') as fid:
		return fid.write(data_string(data, **kwargs))


def as_uarray(
	X: (uarray | _np.ndarray | _uc.UFloat | float),
	Xse: (_np.ndarray | float | None) = None,
	CM: (_np.ndarray | None) = None,
) -> uarray:
	"""
	Convert the input to an uarray. If the input is a single float or
	[UFloat](https://pythonhosted.org/uncertainties/tech_guide.html),
	yields an uarray of size 1.
	
	**Arguments**
	* `X`: nominal value(s)
	* `CM`: covariance matrix of X; not needed if elements of X are of type
		[`UFloat`](https://pythonhosted.org/uncertainties/tech_guide.html)
		or if `Xse` is specified.
	* `Xse`,: SE of X; not needed if elements of X are of type
		[`UFloat`](https://pythonhosted.org/uncertainties/tech_guide.html)
		or if `CM` is specified.
	
	If neither `CM` nor `Xse` are specified, assume SE = 0.
	"""
	
	if isinstance(X, uarray):
		return X

	if isinstance(X, _np.ndarray):
		if _np.all([isinstance(_, _uc.UFloat) for _ in X]):
			return uarray(X)
		else:
			X = X.astype(float)
			
			if CM is not None:
				if Xse is not None: raise ValueError('Too much information: Xse is redundant because CM is already specified.')

			if CM is None:
				if Xse is None:
					Xse = X * 0

				CM = _np.diag((*Xse,))**2

			return uarray(_uc.correlated_values(X, CM))
				
	if isinstance(X, _uc.UFloat):
		return uarray([X])

	if isinstance(X, (float, int)):

		if CM is not None:
			if Xse is not None: raise ValueError('Too much information: Xse is redundant because CM is already specified.')
			Xse = CM[0,0]**0.5

		return uarray([_uc.ufloat(X, Xse)])


def as_pair_of_uarrays(
	X: (uarray | _np.ndarray | _uc.UFloat | float),
	Y: (uarray | _np.ndarray | _uc.UFloat | float),
	Xse: (_np.ndarray | float | None) = None,
	Yse: (_np.ndarray | float | None) = None,
	CM: (_np.ndarray | None) = None,
) -> uarray:
	"""
	Convert the input to a pair of uarrays.
	
	**Arguments**
	* `X`: x values
	* `Y`: y values
	* `CM`: covariance matrix of `(*X, *Y)`; not needed if elements of X and Y are of type
		[`uncertainties.UFloat`](https://pythonhosted.org/uncertainties/tech_guide.html)
		or if (`Xse`, `Yse`) are specified.
	* `Xse`, `Yse`: SE of X and Y; not needed if elements of X and Y are of type
		[`uncertainties.UFloat`](https://pythonhosted.org/uncertainties/tech_guide.html)
		or if `CM` is specified.
	
	If neither `CM`, `Xse` nor `Yse` are specified, assume SE = 0.
	"""
	
	if type(X) is not type(Y):
		raise TypeError(f'X ({type(X)}) and Y ({type(Y)}) must have the same type.')

	if isinstance(X, uarray):
		return (X, Y)

	if isinstance(X, _np.ndarray):
		if (
			_np.all([isinstance(_, _uc.UFloat) for _ in X])
			and
			_np.all([isinstance(_, _uc.UFloat) for _ in Y])
		):
			return uarray(X), uarray(Y)
		else:
			X = X.astype(float)
			Y = Y.astype(float)
			
			if CM is not None:
				if Xse is not None: raise ValueError('Too much information: Xse is redundant because CM is already specified.')
				if Yse is not None: raise ValueError('Too much information: Yse is redundant because CM is already specified.')

			if CM is None:
				if Xse is None:
					Xse = X * 0
				if Yse is None:
					Yse = Y * 0

				CMx = _np.diag((*Xse,))**2
				CMy = _np.diag((*Yse,))**2			
				return uarray(_uc.correlated_values(X, CMx)), uarray(_uc.correlated_values(Y, CMy))

			else:
				XY = uarray(_uc.correlated_values([*X, *Y], CM))
				return XY[:X.size], XY[X.size:]
				
	if isinstance(X, _uc.UFloat):
		return uarray([X]), uarray([Y])

	if isinstance(X, (float, int)):

		if CM is not None:
			if Xse is not None: raise ValueError('Too much information: Xse is redundant because CM is already specified.')
			if Yse is not None: raise ValueError('Too much information: Yse is redundant because CM is already specified.')

		if CM is None:
			if Xse is None: raise ValueError('Not enough information: specify either CM or Xse.')
			if Yse is None: raise ValueError('Not enough information: specify either CM or Yse.')				

			CM = _np.diag([Xse, Yse])**2

		XY = uarray(_uc.correlated_values([X, Y], CM))
		return XY[:1], XY[1:]
