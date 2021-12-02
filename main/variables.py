# Standard Packages
from copy import deepcopy
import sys
sys.path.insert(0, '../')
# 3rd Party Packages
import numpy as np
import scipy.ndimage
from multipledispatch import dispatch
# Local Packages
import settings

# Parent class for input and output variables
class Variables:
    def __str__(self):
        return str(self.get_nonzero_variables())

    def get_variables(self):
        return [var for var in dir(self) if not callable(getattr(self, var)) and not var.startswith("__")]
        
    def get_nonzero_variables(self):
        vars = self.get_variables()
        return [var for var in vars if getattr(self, var).values is not None]

    def print_nonzero_variables(self):
        vars = self.get_nonzero_variables()
        for var in vars:
            print(var + ", "
                  + str(getattr(self, var).name) + ", "
                  + str(getattr(self, var).desc) + ", " 
                  + str(getattr(self, var).units) + ", "
                  + str(getattr(self, var).values.shape) + ", "
                  + str(getattr(self, var).dimensions))

# Variables obtained from a CDF
class InputVariables(Variables):
    def __init__(self):
        # CDF Independent Variables
        self.time = Variable('Time', cdfvar='TIME') # TODO: What is TIME3 in CDF?
        self.x = Variable('X', cdfvar='X', label=r'$x$')
        self.xb = Variable('XB', cdfvar='XB', label=r'$x_\mathrm{B}$')

        # CDF Variables needed for calculations
        self.aimp = Variable('AIMP', cdfvar='AIMP', label=r'$\overline{M}_\mathrm{imp}$', smooth=1)
        self.arat = Variable('Aspect Ratio', cdfvar='ARAT', smooth=1)
        self.bz = Variable('BZ', cdfvar='BZ', smooth=1)
        self.elong = Variable('Elongation', cdfvar='ELONG', label=r'$\kappa$', smooth=1)
        self.omega = Variable('OMEGA', cdfvar='OMEGA', smooth=1)
        self.ne = Variable('Electron Density', cdfvar='NE', label=r'$n_\mathrm{e}$', smooth=1)
        self.nf = Variable('Fast Ion Density', cdfvar='BDENS', label=r'$n_\mathrm{f}$', smooth=1)
        self.nd = Variable('Deuterium Ion Density', cdfvar='ND', label=r'$n_d$', smooth=1)
        self.ni = Variable('Thermal Ion Density', cdfvar='NI', label=r'$n_\mathrm{i}$', smooth=1)
        self.nz = Variable('Impurity Density', cdfvar='NIMP', label=r'$n_z$', smooth=1)
        self.q = Variable('Safety Factor', cdfvar='Q', label=r'$q$', smooth=2)
        self.rmaj = Variable('Major Radius', cdfvar='RMJMP', label=r'$R$', smooth=None)
        self.te = Variable('Electron Temperature', cdfvar='TE', label=r'$T_\mathrm{e}$', smooth=1)
        self.tepro = Variable('Electron Temperature', cdfvar='TEPRO', label=r'$T_\mathrm{e}$', smooth=1)
        self.ti = Variable('Thermal Ion Temperature', cdfvar='TI',label=r'$T_\mathrm{i}$', smooth=1)
        self.tipro = Variable('Thermal Ion Temperature', cdfvar='TIPRO', label=r'$T_\mathrm{i}$', smooth=1)
        self.vpold = Variable('VPOL', cdfvar='VPOLD_NC', smooth=1)
        self.vpolh = Variable('VPOL', cdfvar='VPOLH_NC', smooth=1)
        self.wexbs = Variable('ExB Shear Rate', cdfvar='SREXBA', label=r'$\omega_{E \times B}$', smooth=1)
        self.zimp = Variable('Mean Charge of Impurities', cdfvar='XZIMP', label=r'$\overline{Z}_\mathrm{imp}$', smooth=1)

        # Additional CDF variables for comparisons
        self.betat = Variable('BETAT', cdfvar='BETAT', smooth=1)

        # Calculated Variables (some are also in the CDF)
        self.aimass = Variable('Thermal Ion Mean Atomic Mass', label=r'$\overline{M}_\mathrm{i}$')
        self.ahyd = Variable('Hydrogenic Ion Mean Atomic Mass', label=r'$\overline{M}_\mathrm{h}$')
        self.alphamhd = Variable('Alpha MHD', label=r'$\alpha_\mathrm{MHD}$')
        self.beta = Variable('Pressure Ratio', cdfvar='BETAT', label=r'$\beta$')
        self.betae = Variable('Electron Pressure Ratio', cdfvar='BETAE', label=r'$\beta_\mathrm{\,e}$') 
        self.btor = Variable('Toroidal Magnetic Field', label=r'$B_\mathrm{T}$')
        self.eps = Variable('Inverse Aspect Ratio')
        self.etae = Variable('Electron Gradient Ratio', cdfvar='ETAE', label=r'$\eta_\mathrm{\,e}$')
        self.etai = Variable('Ion Gradient Ratio', cdfvar='ETAI', label=r'$\eta_\mathrm{\,i}$')
        self.etaih = Variable('Hydrogenic Gradient Ratio', cdfvar='ETAIH', label=r'$\eta_\mathrm{\,ih}$')
        self.etaid = Variable('ETAID', cdfvar='', label=r'$\eta_\mathrm{\,id}$')
        self.etaie = Variable('ETAIE', cdfvar='ETAIE', label=r'$\eta_\mathrm{\,ie}$')
        self.nh = Variable('Hydrogenic Ion Density', cdfvar='NH', smooth=1, label=r'$n_\mathrm{h}$')
        self.nuei = Variable('Collision Frequency')
        self.nuei2 = Variable('NUEI2')
        self.nuste = Variable('Electron Collisionality', cdfvar='NUSTE', label=r'$\nu^{*}_\mathrm{e}$')
        self.nusti = Variable('Ion Collisionality', cdfvar='NUSTI', label=r'$\nu^{*}_\mathrm{i}$')
        self.p = Variable('Plasma Pressure', cdfvar='PPLAS', label=r'$p$') 
        self.raxis = Variable('RAXIS')
        self.rho = Variable('Radius', label=r'$\rho$')
        self.rmin = Variable('Minor Radius', label=r'$r$')
        self.shat = Variable('Effective Magnetic Shear', cdfvar='SHAT', label=r'$\hat{s}$')
        self.shear = Variable('Magnetic Shear', label=r'$s$')
        self.vpar = Variable('Parallel Velocity')
        self.vpol = Variable('Poloidal Velocity', label=r'$v_\theta$')
        self.vtor = Variable('Toroidal Velocity', label=r'$v_\phi$')
        self.tau = Variable('Temperature Ratio', label=r'$\tau$')
        self.zeff = Variable('Effective Charge', cdfvar='ZEFF', label=r'$Z_\mathrm{eff}$')
        self.zgmax = Variable('ZGMAX')
        self.zgyrfi = Variable('Ion Gyrofrequency')
        self.zlog = Variable('Coulomb Logarithm', cdfvar='CLOGE', label=r'$\ln\, \Lambda_\mathrm{e}$')
        self.zvthe = Variable('Electron Thermal Velocity')
        self.zvthi = Variable('Ion Thermal Velocity')

        # Calculated Gradients
        self.gne = Variable('Electron Density Gradient', label=r'$g_{n_\mathrm{e}}$')
        self.gnh = Variable('Hydrogenic Ion Density Gradient', label=r'$g_{n_\mathrm{h}}$')
        self.gni = Variable('Thermal Ion Density Gradient', smooth=0, label=r'$g_{n_\mathrm{i}}$')
        self.gnz = Variable('Impurity Density Gradient', label=r'$g_{n_\mathrm{z}}$')
        self.gnd = Variable('Deuterium Ion Density Gradient', label=r'$g_{n_\mathrm{d}}$')
        self.gq = Variable('Safety Factor Gradient', label=r'$g_{q}$')
        self.gte = Variable('Electron Temperature Gradient', label=r'$g_{T_\mathrm{e}}$')
        self.gti = Variable('Thermal Ion Temperature Gradient', smooth=0, label=r'$g_{T_\mathrm{i}}$')
        self.gvpar = Variable('Parallel Velocity Gradient', )
        self.gvpol = Variable('Poloidal Velocity Gradient', label=r'$g_{\nu_\theta}$')
        self.gvtor = Variable('Toroidal Velocity Gradient', label=r'$g_{\nu_\phi}$')

        # Test Variables
        self.test = Variable('Test Variable')
        self.test2 = Variable('Test Variable 2')
        self.gtest = Variable('Test Variable Gradient')

    def get_cdf_variables(self):
        vars = self.get_variables()
        return [var for var in vars if getattr(self, var).cdfvar is not None]

    def get_nboundaries(self):
        return self.xb.values.shape[0] if self.xb.values is not None and self.xb.values.ndim > 0 else 0

    def get_ntimes(self):
        return self.x.values.shape[1] if self.xb.values is not None and self.xb.values.ndim > 1 else 0

    def use_temperature_profiles(self):
        if self.tepro.values is not None:
            self.te = deepcopy(self.tepro)
        else:
            raise ValueError('Failed to set TEPRO since TEPRO is None')

        if self.tipro.values is not None:
            self.ti = deepcopy(self.tipro)
        else:
            raise ValueError('Failed to set TIPRO since TIPRO is None')

# Variables obtained from MMM output
class OutputVariables(Variables):
    def __init__(self):
        self.rho = Variable('rho', label=r'$\rho$')
        self.rmin = Variable('rmin', label=r'$r_\mathrm{min}$')
        self.xti = Variable('xti', label='xti', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xdi = Variable('xdi', label='xdi', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xte = Variable('xte', label='xte', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xdz = Variable('xdz', label='xdz', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xvt = Variable('xvt', label='xvt', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xvp = Variable('xvp', label='xvp', units=r'$\left(\mathrm{m}^2/\mathrm{s}\right)$')
        self.xtiW20 = Variable('xtiW20', label='xtiW20')
        self.xdiW20 = Variable('xdiW20', label='xdiW20')
        self.xteW20 = Variable('xteW20', label='xteW20')
        self.xtiDBM = Variable('xtiDBM', label='xtiDBM')
        self.xdiDBM = Variable('xdiDBM', label='xdiDBM')
        self.xteDBM = Variable('xteDBM', label='xteDBM')
        self.xteETG = Variable('xteETG', label='xteETG')
        self.xteMTM = Variable('xteMTM', label='xteMTM')
        self.xteETGM = Variable('xteETGM', label='xteETGM')
        self.xdiETGM = Variable('xdiETGM', label='xdiETGM')
        self.gmaW20ii = Variable('gmaW20ii', label='gmaW20ii', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.omgW20ii = Variable('omgW20ii', label='omgW20ii', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.gmaW20ie = Variable('gmaW20ie', label='gmaW20ie', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.omgW20ie = Variable('omgW20ie', label='omgW20ie', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.gmaW20ei = Variable('gmaW20ei', label='gmaW20ei', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.omgW20ei = Variable('omgW20ei', label='omgW20ei', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.gmaW20ee = Variable('gmaW20ee', label='gmaW20ee', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.omgW20ee = Variable('omgW20ee', label='omgW20ee', units=r'$\left(\mathrm{s}^{-1}\right)$')
        self.gmaDBM = Variable('gmaDBM', label='gmaDBM')
        self.omgDBM = Variable('omgDBM', label='omgDBM')
        self.gmaMTM = Variable('gmaMTM', label='gmaMTM')
        self.omgMTM = Variable('omgMTM', label='omgMTM')
        self.gmaETGM = Variable('gmaETGM', label='gmaETGM')
        self.omgETGM = Variable('omgETGM', label='omgETGM')
        self.dbsqprf = Variable('dbsqprf', label='dbsqprf')

class Variable:
    def __init__(self, name, cdfvar=None, smooth=None, label=None, desc=None, units=None, dimensions=None, values=None):
        # Public
        self.name = name
        self.cdfvar = cdfvar # Name of variable as used in CDF's
        self.smooth = smooth # None to disable smoothing, or n = 1, 2, 3, ...  
        self.label = label if label is not None else '' # Plot label in LaTeX Format
        self.desc = desc if desc is not None else ''
        # Private
        self._units = units if units is not None else ''
        self._dimensions = dimensions if dimensions is not None else ['','']
        self._values = values

    def __str__(self):
        return str(self.name)

    def get_xdim(self):
        return self.dimensions[0] if self.dimensions is not None and len(self.dimensions) > 0 else None

    def set_xdim(self, xdim):
        if self.dimensions is not None and len(self.dimensions) > 0:
            self.dimensions[0] = xdim
        else:
            raise ValueError(f'Failed to set xdim on variable {self.name}')

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        if type(dimensions) == list:
            self._dimensions = dimensions
        else:
            raise ValueError(f'Variable dimensions must be {list} and not {type(dimensions)}')
    
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        if type(values) == np.ndarray:
            self._values = values
        else:
            raise ValueError(f'Variable values must be {np.ndarray} and not {type(values)}')
    
    @dispatch(np.ndarray)
    def set_variable(self, values):
        self.set_variable(values, self.units, self.dimensions)

    @dispatch(np.ndarray, str)
    def set_variable(self, values, units):
        self.set_variable(values, units, self.dimensions)

    # Set variable values, units, dimensions
    @dispatch(np.ndarray, str, list)
    def set_variable(self, values, units, dimensions):
        self.values = values
        self.units = units
        self.dimensions = dimensions

    # Variable smoothing using a Gaussian filter
    def apply_smoothing(self):
        if self.smooth is not None and settings.APPLY_SMOOTHING:
            self.values = scipy.ndimage.gaussian_filter(self.values, sigma=(self.smooth, 0))

    # Clamps values between -value and value, and sets origin value to apprximately 0
    def clamp_gradient(self, value):
        self.values[0, :] = 1e-6
        self.values[self.values > value] = value
        self.values[self.values < -value] = -value

    # Removes values outside of m standard deviations
    # TODO: Currently not ideal since removed values are replaced with None,
    # which turns everything into nan after smoothing or intepolating again
    def reject_outliers(self, m=4):
        if settings.REMOVE_OUTLIERS:
            self.values[(np.abs(self.values - np.mean(self.values)) > m * np.std(self.values))] = None

    def remove_nan(self):
        if np.isnan(self.values).any():
            print('nan values found for var ' + self.name)
            self.values[np.isnan(self.values)] = 0

class InputOptions:
    def __init__(self, cdf_name, shot_type=None, input_time=None, input_points=None):
        # Public
        self.cdf_name = cdf_name
        self.shot_type = shot_type
        self.input_time = input_time
        self.input_points = input_points
        # Private
        self._runid = None
        self._interp_points = None
        self._time = None
        self._time_idx = None
        self._var_to_scan = None
        self._scan_range = None
        self._scan_factor_str = None

    @property
    def runid(self):
        return self._runid

    @runid.setter
    def runid(self, runid):
        self._runid = runid.strip()
        if self._runid != self.cdf_name:
            print(f'*** WARNING: runid {self.runid} does not match cdf_name {self.cdf_name}')

    @property
    def interp_points(self):
        return self._interp_points if self._interp_points is not None else self.input_points

    @interp_points.setter
    def interp_points(self, points):
        self._interp_points = points
        if self._interp_points < self.input_points:
            print(f'*** WARNING: Interpolation points ({self.interp_points}) is less than specified input points ({self.input_points})')

    @property
    def time_idx(self):
        return self._time_idx

    @property
    def time(self):
        return self._time

    # Find the index of the measurement time closest to the input_time and index and the value
    def set_measurement_time(self, tvar):
        self._time_idx = np.argmin(np.abs(tvar.values - self.input_time))
        self._time = "{:.3f}".format(tvar.values[self.time_idx])

    @property
    def var_to_scan(self):
        return self._var_to_scan

    @property
    def scan_range(self):
        return self._scan_range

    # Sets values needed for conducting a variable scan
    def set_scan_values(self, var_to_scan, scan_range):
        # Condition to skip variable scan
        if var_to_scan is None:
            return
        # Error checking
        elif not hasattr(InputVariables(), var_to_scan):
            raise ValueError(f'Variable {var_to_scan} is not an InputVariable.  Please use a variable defined under InputVariable.')
        elif type(scan_range) is not np.ndarray:
            raise ValueError('Specified scan range must be a Numpy array (type np.ndarray)')
        # Set scan inputs
        else:
            self._var_to_scan = var_to_scan
            self._scan_range = scan_range

    @property
    def scan_factor_str(self):
        return self._scan_factor_str

    @scan_factor_str.setter
    def scan_factor_str(self, scan_factor_str):
        self._scan_factor_str = '{:.3f}'.format(scan_factor_str)
