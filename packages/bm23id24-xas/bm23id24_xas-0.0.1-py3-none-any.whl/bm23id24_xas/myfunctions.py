import h5py
import os 
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from itertools import cycle


import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter


import statistics
import numpy as np
import pandas as pd
import larch
from larch import Group
from larch.xafs import *
from datetime import datetime
from scipy.signal import savgol_filter as savgol
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()


def load_params(file_path):
    spec = importlib.util.spec_from_file_location("params", file_path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    
    # Load all variables from the module directly into the global scope
    globals().update({key: value for key, value in params.__dict__.items() if not key.startswith("__")})

def xas(n_first = 1, n_last = None, skiplist = [], path = None, calibrate = False, align = False, interpolate = False, exafs = False, merge = 1):
    ### Choosing the file
    if path == None:
        path = filedialog.askopenfilename(title="Select a file", filetypes=(("h5 files", "*.h5"), ("All files", "*.*")))       # full path containing filename
            
    ### Saving directory 
    directory=str(os.path.dirname(path))  # that will save to the directory of the .h5 file
    print(f'Directory set to: {directory}')        
    
    ### Setting filename   
    filename = str(os.path.basename(path)) 
    print(f'Working with file: {filename}\n')        
    
    if merge !=1:
        print(f'Merging every {merge} scans\n')
        if not interpolate:
            print(f'Merging without interpolation may lead to wrong results. Forcing interpolation anyway (interpolate = True)\n')
            interpolate = True
    
    filename = filename[:-3]  #keep the name of the h5 file removing .h5 in the end
    
    ### Opening the file 
    dataset = h5py.File(path,mode ='r')
                
    if n_last == None:
        n_last = len(dataset)    
    
    data={}    #initialize the dictionary

    first_scan=True    # To discriminate between the first and the consequent scans for alignment

    for scan_number in range (n_first, n_last + 1):
        
        if scan_number in skiplist:
            continue
        
        scan_label = '/'+str(scan_number)+'.1'
        scan_data=dataset[scan_label]
              
        
        if "scans.exafs_" in str(scan_data['title'][()]) or "contscan.motor" in str(scan_data['title'][()]) or "trigscan" in str(scan_data['title'][()]):
            
            try:
                repeats = scan_data['instrument']['fscan_parameters']['nscans'][()]
                npoints_theor = scan_data['instrument']['fscan_parameters']['npoints'][()] + 1 # value defined in the beginning of the scan
            except:
                repeats = 1
            
            if repeats != 1:
                print(f'Scan {scan_number} contains {repeats} repeats\n')

            for rep in range (1,repeats+1):
            
                scan_address = f'{scan_number}.{rep}'
                
                print(f'Extracting scan {scan_address}')
                
                try:
                    energy = scan_data['measurement'][energy_counter][()]           
                    if np.max(energy)<100:
                        energy=energy*1000                                  
                except:
                    print(f'Scan {scan_number} cannot be read, skipping it')
                    continue
                
                if max(energy) < e0 + norm2:
                    print(f'Scan {scan_address}: WARNING, data range smaller than normalization range')
                if min(energy) > e0 + pre1:
                    print(f'Scan {scan_address}: WARNING, data range smaller than pre-edge range')

                npoints_total = len(energy)
                
                
                try:
                    if repeats != 1:                        
                        energy = energy[int((rep-1)*npoints_theor + 2) : int(rep*npoints_theor) - 2] #skipping the first and last two points of every scan
                    else:                        
                        energy = energy[2:-2]
                
                    if energy[-1] < energy[0]: # Invert for "back" scans in back'n'forth mode
                        energy= energy[::-1]
                        need_to_invert = True
                        print('It is a "back" scan: inverting the energy scale')
                    else:
                        need_to_invert = False
                    
                except:
                    print(f'Scan {scan_address} does not exist, skipping it')
                    continue
                
                
                
                
                mu = scan_data['measurement'][mu_counter][()]              
                
                if repeats != 1:                    
                    mu = mu[int((rep-1)*npoints_theor + 2) : int(rep*npoints_theor) - 2]
                else:
                    mu = mu[2:-2]                
                if need_to_invert:
                    mu = mu[::-1]
                    
                mu[np.isnan(mu)] = 0.0  # Replaces NaNs by 0
                mu[np.isinf(mu)] = 0.0  # Replaces infs by 0
                
                
                ref = scan_data['measurement'][ref_counter][()]            
                
                if repeats != 1:                    
                    ref = ref[int((rep-1)*npoints_theor + 2) : int(rep*npoints_theor) - 2]
                else:
                    ref=ref[2:-2]
                if need_to_invert:
                    ref = ref[::-1]
                
                
                
                ref[np.isnan(ref)] = 0.0  # Replaces NaNs by 0
                ref[np.isinf(ref)] = 0.0  # Replaces infs by 0
                
                
                mu_prime = np.gradient(mu)/np.gradient(energy)
                ref_prime = np.gradient(ref)/np.gradient(energy)
                ref_prime_smoothed = savgol(ref_prime,7,2)
                
                try:                
                    comment = scan_data['instrument']['comment'][()]
                except:
                    comment = ''
                                
                start_time = scan_data['start_time'][()]
                end_time = scan_data['end_time'][()]
                
                if isinstance(start_time, bytes):                        # This is to be compatible with different versions of (?) h5py 
                    start_time = start_time.decode('ascii', 'replace')
                    end_time = end_time.decode('ascii', 'replace')
                start_time = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S.%f%z')
                end_time = datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%S.%f%z')
                
                if repeats != 1:
                    start_time = start_time + (rep-1)* (end_time-start_time)/repeats * npoints_theor * repeats/npoints_total    # Only approximate estimation for the scans that are not finished
                        
                if first_scan:
                    zero_time = start_time
                    number = 0
                rel_time = (start_time - zero_time).total_seconds()
                number = number + 1 # Order number of the scan
                print(f'Number of the scan in the series: {number}')
                
                
                #################################################################
                ############## Calibration of the spectra #######################
                #################################################################
                
                
                
                if calibrate: # Main issue here: determination of the edge energy of the reference                                                 
                    
                    radius_calib = 5 # Energy radius to be taken into account for calibration (in eV)                    
                    ref_prime_max_energy = energy[np.argmax(ref_prime_smoothed)]                    
                    
                    grid = np.linspace(ref_prime_max_energy - radius_calib, ref_prime_max_energy + radius_calib, 1000) 
                    ref_prime_smoothed_fine = interp1d(energy, ref_prime_smoothed, kind= 'quadratic')(grid)
                    
                    
                    
                    ref_prime_max_energy = grid[np.argmax(ref_prime_smoothed_fine)]
                    
                    
                    calibration_error = ref_prime_max_energy - Eref
                    
                    acceptable_error = 10 # eV. Can be changed depending on how wrong the beamline energy offset is
                    
                    if abs(calibration_error) < acceptable_error:
                        calibration_shift = - calibration_error
                        print(f'Scan {scan_address}: reference E0 found at {ref_prime_max_energy:.3f} eV. The scan shifted by {calibration_shift:.3f} eV to match Eref = {Eref}')
                    else:
                        print(f'Scan {scan_address}: reference E0 found at {ref_prime_max_energy:.3f} eV, which is more than {acceptable_error: .1f} eV away from reference value of Eref = {Eref}. Apply calibration shift of {calibration_shift:.3f} eV from the previous scan.')
                                                          
                    energy = energy + calibration_shift                                                            
                else:
                    calibration_shift = 0
                    
                      
                        
                #################################################################
                ################### Alignment of the spectra ####################
                #################################################################
                alignment_shift = 0
                if align:                               
                    if align == 'load':
                        std_energy = np.loadtxt("align_ref_prime.txt")[:,0]
                        std_ref_prime = np.loadtxt("align_ref_prime.txt")[:,1]
                    
                    else:
                        if first_scan:
                            std_energy = energy
                            std_ref_prime = ref_prime_smoothed
                            if align == 'save':
                                saved = np.column_stack((energy, std_ref_prime))
                                np.savetxt("align_ref_prime.txt", saved)
                    
                                        
                    radius_align = 50 # Energy radius to be taken into account for alignment (in eV)
                    
                    grid = np.linspace(Ealign - radius_align, Ealign + radius_align, 1000) 
                    standard = interp1d(std_energy, std_ref_prime, kind= 'quadratic') 
                    spectrum = interp1d(energy, ref_prime_smoothed, kind= 'quadratic') 
                    
                    def alignment_function(x, E):
                        return spectrum(x - E)                
                    
                    best_vals, covar = curve_fit(alignment_function, grid, standard(grid), p0=0)                
                    alignment_shift = best_vals[0]                
                    
                    
                    if first_scan:
                        print(f'Scan {scan_address} was used as reference for alignment of the next scans.')
                        first_scan_address = scan_address 
                    else:                    
                        print(f'Scan {scan_address} shifted by {alignment_shift :.3f} eV to match the scan {first_scan_address}.')
                    
                    energy = energy + alignment_shift
                    
                
               
                
                #################################################################
                ################ Interpolation of the energy axis #########
                #################################################################
                if interpolate:                
                    if first_scan:
                        if align == 'load':
                            interp_grid = np.linspace(std_energy[0], std_energy[-1], len(std_energy))    
                        else:    
                            interp_grid = np.linspace(energy[0], energy[-1], len(energy))    
                    mu = interp1d(energy, mu, bounds_error = False, fill_value = 'extrapolate')(interp_grid)
                    mu_prime = interp1d(energy, mu_prime, bounds_error = False, fill_value = 'extrapolate')(interp_grid)
                    ref = interp1d(energy, ref, bounds_error = False, fill_value = 'extrapolate')(interp_grid)
                    ref_prime = interp1d(energy, ref_prime, bounds_error = False, fill_value = 'extrapolate')(interp_grid)
                    
                    if calibrate:
                        ref_prime_smoothed = interp1d(energy, ref_prime_smoothed, bounds_error = False, fill_value = 'extrapolate')(interp_grid)    
                    
                    energy = interp_grid 
                                                
                
                #################################################################
                ############################ Merging ############################
                #################################################################
                if merge !=1:                    
                    if number % merge == 1: # first scan of the merged group
                        start_time_temp = start_time
                        rel_time_temp = rel_time

                        mu_temp = mu
                        ref_temp = ref

                        scan_address_temp = scan_address                        
                        first_scan = False
                        print('')                        
                        continue                       
                    
                    elif number % merge != 1 and number % merge != 0: # other scans of the merged group
                        mu_temp += mu
                        ref_temp += ref                        
                        print('')
                        continue
                    
                    else: # Time to merge
                        start_time = start_time_temp
                        rel_time = rel_time_temp
                        scan_address = scan_address_temp
                        
                        mu = (mu + mu_temp)/merge
                        ref = (ref + ref_temp)/merge
                        
                        mu_prime = np.gradient(mu)/np.gradient(energy)
                        ref_prime = np.gradient(ref)/np.gradient(energy)
                                                                                 
                
                #################################################################
                ####################### Larch processing ########################
                #################################################################
                                    
                larch_group = Group()
                pre_edge(energy, mu, group = larch_group, e0=e0, step=step, pre1=pre1, pre2=pre2, norm1=norm1, norm2=norm2, nnorm=nnorm, nvict=nvict, make_flat=make_flat)
                
                flat = larch_group.flat
                edge_step = larch_group.edge_step
                flat_prime = np.gradient(flat)/np.gradient(energy)
                
                xaq = larch_group.pre_edge[np.argmin(abs(energy-(e0+(pre1+pre2)/2)))] # To check. Also, it may be different with new Larch
                
                            
                #################################################################
                #################### Calculating edge positions #################
                #################################################################
                                         
                flat_prime_max_index = np.argmax(flat_prime)
                flat_prime_max_energy = energy[flat_prime_max_index]
                
                
                if np.isclose(flat_prime_max_energy, e0, atol = 20):
                    edge_estimate = flat_prime_max_energy
                    edge_estimate_index = flat_prime_max_index
                else:
                    edge_estimate = e0
                    edge_estimate_index = np.argmin(abs(energy-e0))
                
                
                init_vals = [0.2, edge_estimate, 2]  # for [amp, cen, wid]
                radius = 5   # Number of points around the center of the range to consider for fitting. For clean data 5 is OK. For noisy ones 10 is better.        
                best_vals, covar = curve_fit(gaussian, energy[edge_estimate_index - radius : edge_estimate_index + radius], flat_prime[edge_estimate_index - radius : edge_estimate_index + radius] , p0=init_vals)
                edge_energy = best_vals[1]                        
                
                
                
                
                #################################################################
                ######################## Calculating noise ######################
                #################################################################
                
                # Calculates noise as a difference between the raw data and sg-smoothed raw data in the range between norm1 and norm2
                
                width_savgol = 5   # Seems to be OK, but probably to be checked better 
                smoothed=savgol(mu,width_savgol,2)                       
                noise = abs(mu - smoothed)
                noise_start_index = np.argmin(abs(energy - (e0 + norm1))) 
                noise_end_index = np.argmin(abs(energy - (e0 + norm2)))            
                noise_mean = np.sqrt(np.mean((noise[noise_start_index : noise_end_index])**2))
                noise_mean_norm = noise_mean/edge_step
                
                
                #################################################################
                ############################# EXAFS #############################
                #################################################################
                
                if exafs:
                    rebin_xafs(energy, mu, group = larch_group, e0=e0, method = 'boxcar') 
                    
                    for i in range (len (larch_group.rebinned.mu)): # because rebinned data sometimes have NaN in the beginning of the EXAFS region
                        if np.isnan(larch_group.rebinned.mu[i]):
                            larch_group.rebinned.mu[i] = 0.5 * (larch_group.rebinned.mu[i-1] + larch_group.rebinned.mu[i+1])
                    
                    
                    autobk(larch_group.rebinned.energy,larch_group.rebinned.mu, larch_group, rbkg=rbkg, 
                                    e0=e0, nknots=nknots, kmin=splinekmin, 
                                    kmax=splinekmax, kweight=splinekweight, 
                                    clamp_lo=clamp_lo, clamp_hi=clamp_hi)
                    k = larch_group.k
                    chik = larch_group.chi*k**ftkweight
    
                    
                    xftf(larch_group.k, larch_group.chi, larch_group, kmin = ftkmin, kmax = ftkmax, 
                                     kweight = ftkweight, dk1 = ftdk, dk2 = ftdk, window = 'hanning')
                    r = larch_group.r
                    chir_mag = larch_group.chir_mag
                    chir_im = larch_group.chir_im
                
                
                
                first_scan = False # To discriminate between the first and the consequent scans.  
                
               
                
                #################################################################
                ########################## Temperature ##########################
                #################################################################
                
                Temperature = scan_data['instrument']['EurothermNanodac']['measure'][()]
                
                #################################################################
                ################### Filling the final dictionary ################
                #################################################################
                
                data[scan_address] = {}
                data[scan_address]['filename'] = filename
                data[scan_address]['directory'] = directory            
                data[scan_address]['energy'] = energy
                data[scan_address]['mu'] = mu
                data[scan_address]['ref'] = ref
                data[scan_address]['mu_prime'] = mu_prime
                data[scan_address]['ref_prime'] = ref_prime
                data[scan_address]['comment'] = comment
                data[scan_address]['start_time'] = start_time
                data[scan_address]['rel_time'] = rel_time
                data[scan_address]['number'] = number
                data[scan_address]['merge'] = merge                               
                
                data[scan_address]['calibration_shift'] = calibration_shift
                data[scan_address]['alignment_shift'] = alignment_shift
                data[scan_address]['total_shift'] = calibration_shift + alignment_shift
                data[scan_address]['ref_prime_smoothed'] = ref_prime_smoothed
                
                data[scan_address]['flat'] = flat
                data[scan_address]['edge_step'] = edge_step
                data[scan_address]['flat_prime'] = flat_prime
                data[scan_address]['edge_energy'] = edge_energy
                data[scan_address]['xaq'] = xaq

                
                data[scan_address]['smoothed'] = smoothed
                data[scan_address]['noise'] = noise
                data[scan_address]['noise_mean'] = noise_mean
                data[scan_address]['noise_mean_norm'] = noise_mean_norm
                
                data[scan_address]['Temperature'] = Temperature
                
                if exafs: 
                    data[scan_address]['k'] = k
                    data[scan_address]['chik'] = chik
    
                    
                    data[scan_address]['r'] = r
                    data[scan_address]['chir_mag'] = chir_mag    
                    data[scan_address]['chir_im'] = chir_im 
                
                print('')
        
  
    


        
    return data
        

def gaussian(x, amp, cen, wid):
            return amp * np.exp(-(x-cen)**2 / wid)

import numpy as np
from sklearn.decomposition import PCA as PCAskl
import matplotlib.pyplot as plt
from pyfitit.factor_analysis import *


# +
###########################################################################
###################### CREATES .dat FILE FOR PCA ##########################
###########################################################################

def pca_file(dataset=None, skiplist =[],file_path = None , xanes_start = None, xanes_end = None, plot_xanesrange = True):
    """
    This function creates a .dat file with the energy and flat values of the scans in the XANES range.
    This .dat file is needed for the PCA functions. 
    

    Parameters:
    - dataset: dictionary
        XAS dictionary.
    - skiplist: list
        Scan numbers to skip.
    - file_path: str
        Path to the .dat file with the XANES data. 
    - xanes_start: int, optional
        Start energy value for XANES range.
    - xanes_end: int, optional
        End energy value for XANES range.
    - plot_xanesrange: bool, optional
        Whether to plot XANES range. Default is True.
    
    Returns:
    
    """
    if dataset == None:
        print("Select the corresponding dataset")
   
    interp_grid = np.linspace(xanes_start, xanes_end, 2000)
    pca_array = interp_grid

    first_key = list(dataset.keys())[0]

        
    for scan_key in dataset.keys():
                
        if scan_key in skiplist:
            continue
        flat = interp1d(dataset[scan_key]["energy"], dataset[scan_key]["flat"])(interp_grid)
        pca_array = np.c_[pca_array,flat]
   
    np.savetxt(file_path,pca_array)
    print(f"Selected data saved to {file_path}")
    
    if plot_xanesrange:
        fig, axs = plt.subplots(1,2, figsize=(8,8),dpi=300) 
        fig.tight_layout()
    
        
        axs[0].plot(dataset[first_key]["energy"], dataset[first_key]["flat"])
        axs[0].set_title('XAS')
        axs[0].set_xlabel('Energy')
        axs[0].set_ylabel('Normalized $\mu$')

        
        axs[1].plot(pca_array.T[0],pca_array.T[1])
        axs[1].set_title('XANES Range')
        # axs[1].set_xlim(xanes_start,xanes_end)
        axs[1].set_xlabel('Energy')
        axs[1].set_ylabel('Normalized $\mu$')


    
        plt.show()
    
    
   
        
        
        
        
    
    


# +
def noise(dataset=None, skiplist=[]):
    """
    This function appends the noise, average noise and average normalized noise values for every scan of the dataset.
    
    Parameters:
    - dataset: dictionary
        XAS dictionary.
    - skiplist: list
        Scan numbers to skip.
        

    Returns:
    - x: list
        Array of the scan keys of the XAS dictionary.
    - noise_array_norm: list
        Array of the average noise.
    - noise_array_v: list
        Array of the normalized average noise.
    """
    noise_array_av= []
    noise_array_norm= []
    
    x = []

    for scan_key in dataset.keys():
                
        if scan_key in skiplist:
            continue

        #print(dataset[n]["noise_mean_norm"])
        noise_array_av.append(dataset[scan_key]["noise_mean"])
        noise_array_norm.append(dataset[scan_key]["noise_mean_norm"])
        x.append(scan_key)
        
    return x, noise_array_norm, noise_array_av

def set_y_limits(data, lower_percentile=5, upper_percentile=95):
    """
    Set the y-axis limits based on the specified percentiles to exclude outliers.
    
    Parameters:
    - data: The data array or pandas Series.
    - lower_percentile: The lower percentile for the y-axis minimum limit.
    - upper_percentile: The upper percentile for the y-axis maximum limit.
    
    Returns:
    - A tuple of (y_min, y_max) for the y-axis limits.
    """
    y_min = np.percentile(data, lower_percentile)
    y_max = np.percentile(data, upper_percentile)
    return y_min, y_max
# -



# +
###########################################################################
##################### PCA STATISTICAL ESTIMATORS ##########################
###########################################################################

        
class Dataset:
    """
    A class to represent a dataset.

    Attributes:
    - original_energy: numpy.ndarray
        The original energy data.
    - original_intensity: numpy.ndarray
        The original intensity data.
    - energy: numpy.ndarray
        The energy data.
    - intensity: numpy.ndarray
        The intensity data.
    - references: None
        References associated with the dataset.
    - manipulated_energy: numpy.ndarray
        Energy data to be used for interpolation and normalization.
    - manipulated_intensity: numpy.ndarray
        Intensity data to be used for interpolation and normalization.
    """
    
    def __init__(self,xanes):
        self.original_energy=xanes[:,0] #original energy
        self.original_intensity=xanes[:,1:] #original xanes coefficients
        self.energy=self.original_energy
        self.intensity=self.original_intensity
        self.references=None
        self.manipulated_energy=self.energy #to be used for the interpolation and normalization
        self.manipulated_intensity=self.intensity #to be used for the interpolation and normalization
        cwd=os.getcwd()
    
class PCAest: 
    """
    A class to perform Principal Component Analysis (PCA) estimation.
    Adapated from https://github.com/gudasergey/pyFitIt/blob/master/pyfitit/factor_analysis.py#L190

    Methods:
    - PCA_Statistic(intensity, pc=None)
        Calculates various statistics related to PCA.
    - Rfactor(intensity, pc=None, plot_noise=False, dataset=None)
        Calculates R-factor and optionally plots noise.
    - NSS(intensity, pc=None, dataset=None, skiplist=[])
        Calculates and plots NSS values.
    """
    
    def __init__(self):
        self.components=None
        self.e_pca=None
        self.s_pca=None
        self.c_pca=None
        cwd=os.getcwd()
        
            
    def PCA_Statistic(intensity, pc = None):
        """
        Calculates and plots various statistics related to PCA.

        Parameters:
        - intensity: numpy.ndarray
            The XANES intensity data.
        - pc: int, optional
            The number of principal components. Default is None and will take the value of total number of scans.

        Returns:
        - s: numpy.ndarray
            Singular values from SVD, values for Scre plot.
        - ind: numpy.ndarray
            IND values.
        - ie: numpy.ndarray
            IE values.
        - fisher: numpy.ndarray
            F-test values.
        """
        u,s,v=makeSVD(intensity)
        if np.shape(intensity)[0]<np.shape(intensity)[1]: intensity=np.transpose(intensity)
        nrow,ncol=np.shape(intensity)
        l=(s**2)/(nrow-1)
        ind,ie=malinowsky(l,nrow,ncol)
        fisher=fisherFunction(l,nrow,ncol)
        
        
        if pc == None:
            pc = ncol
            
        fig, axs = plt.subplots(2, 2, figsize=(8, 6),dpi=300)

        axs[0, 0].plot(range(1,ncol+1), s, marker='o', color="red")
        axs[0, 0].set_title('Scree')
        axs[0, 0].set_yscale('log')
        axs[0, 0].set_xlim(0,pc)
        axs[0, 0].set_xlabel('Number of pc')


        axs[0, 1].plot(range(1,ncol),ind, marker='o', color="purple")
        axs[0, 1].set_title('IND')
        axs[0, 1].set_yscale('log')
        axs[0, 1].set_xlim(0,pc)
        axs[0, 1].set_xlabel('Number of pc')


        axs[1, 0].plot(range(1,ncol),fisher, marker='o')
        axs[1, 0].set_title("F test")
        axs[1, 0].plot([0, ncol], [5,5], 'k-', lw=1,dashes=[2, 2])
        axs[1, 0].set_xlim(0,pc)
        axs[1, 0].set_xlabel('Number of pc')



        axs[1, 1].plot(range(1,ncol),ie, marker='o', color="pink")
        axs[1, 1].set_title('IE plot')
        axs[1, 1].set_yscale('log')
        axs[1, 1].set_xlim(0,pc)
        axs[1, 1].set_xlabel('Number of pc')


        fig.tight_layout()
        plt.show()
        
        return s, ind, ie, fisher
    
########################################################################################
###################################### Rfactor #########################################
########################################################################################      

    def Rfactor(intensity, pc = None, plot_noise = False,dataset=None):
        """
        Calculates and plots R-factor and optionally plots noise.

        Parameters:
        - intensity: numpy.ndarray
            The intensity data.
        - pc: int, optional
            The number of principal components. Default is None and will take the value of total number of scans.
        - plot_noise: bool, optional
            Whether to plot noise. Default is False.
        - dataset: dict, optional
            Dataset dictionary. 

        Returns:
        - resvalue: numpy.ndarray
            R-factor values.
        """
        u,s,v=makeSVD(intensity)
        ncol=np.shape(intensity)[1]
        
        if pc == None:
            pc = ncol

        if plot_noise == True:
            x,noise_array_norm,noise_array_av = noise(dataset=dataset,skiplist=[])


            for n in range(1,pc+1):
                pcfit_initial=np.dot(u[:,0:n],np.dot(np.diag(s[0:n]),v[0:n,:]))
                resvalue=xanesRfactor(intensity, pcfit_initial)

                fig, axs = plt.subplots(2,1, figsize=(8,6),dpi=300) 


                axs[0].bar(np.arange(ncol),resvalue, label=f"PC = {n}")
                axs[0].legend()
                axs[0].set_title('R factor')
                axs[0].set_xlabel('Scan')


                axs[1].plot(np.arange(ncol),noise_array_norm)
                # axs[1].plot(x,noise_array_norm)
                axs[1].set_title('Average noise')
                axs[1].set_xlabel('Scan')
                fig.tight_layout()  

                plt.show()
                

        if plot_noise == False:
            for n in range(1,pc+1):
                pcfit_initial=np.dot(u[:,0:n],np.dot(np.diag(s[0:n]),v[0:n,:]))
                resvalue=xanesRfactor(intensity, pcfit_initial)

                plt.figure(figsize=(8, 3),dpi=300)

                plt.bar(np.arange(ncol),resvalue, label=f"PC = {n}")
                plt.xlabel('Scan')
                plt.title('R factor')
                plt.legend()
                plt.show()
                plt.tight_layout()
                
        
        return resvalue
            
            
########################################################################################
################################ NSS Estimator #########################################
########################################################################################
    def NSS(intensity, pc = None, dataset=None,skiplist =[]):
        """
        Calculates and plots NSS values.

        Parameters:
        - intensity: numpy.ndarray
            The intensity data.
        - pc: int, optional
            The number of principal components. Default is None and will take the value of total number of scans.
        - dataset: dict, optional
            Dataset dictionary. 
        - skiplist: list, optional
            List of scans to skip. Default is an empty list.

        Returns:
        - nss_values: dict
            NSS values for each scan.
        - nss_val: dict
            NSS values for each scan for each PC.
        """
        ...

        if dataset == None:
            raise ValueError("The dataset parameter is required")
        # Extraction of data from dictionary
        original_data = {scan: data['mu'] for scan, data in dataset.items() if scan not in skiplist}
        smoothed_data = {scan: data['smoothed'] for scan, data in dataset.items() if scan not in skiplist}
        flat_data = {scan: data['flat'] for scan, data in dataset.items() if scan not in skiplist}
        
        u,s,v=makeSVD(intensity)
        ncol=np.shape(intensity)[1]
        if pc == None:
            pc = ncol
        
        for scan_number in dataset.keys():
        
            if scan_number in skiplist:
                continue
            
            # NORMALIZED DATA
            width_savgol = 21   
            dataset[scan_number]["flat_smoothed"] = savgol(dataset[scan_number]["flat"], width_savgol, 2)
            #plt.plot(dataset[scan_number]["flat_smoothed"])

        # Calculate noise levels
        noise_levels = {scan: np.std(original - smoothed) for scan, (original, smoothed) in
                zip(original_data.keys(), zip(original_data.values(), smoothed_data.values()))}

        # Convert smoothed data to a single array for PCA
        flat_smoothed_data = {scan: data['flat_smoothed'] for scan, data in dataset.items() if scan not in skiplist}
        
        XAS_data_smoothed = np.array(list(smoothed_data.values()))
        XAS_data_flat_smoothed = np.array(list(flat_smoothed_data.values()))
       

        PCA_fits = []
        average_nss_values = []
        std_nss_values =[]
        fig, axs = plt.subplots(1, 2, figsize=(10, 4), sharex=True,dpi=300) 
        nss_val = {}
        for n in range(1, pc+1 ):

            pca = PCAskl(n_components = n)
            XAS_data_pca = pca.fit_transform(XAS_data_flat_smoothed)
    
            # Reconstruct the spectra from the PCA components
            XAS_data_reconstructed = pca.inverse_transform(XAS_data_pca)
            PCA_fits.append(XAS_data_reconstructed)
            

            #NSS for each scan
            nss_val[n]={} #Fillin final dictionary
            nss_values={}
            nss_values_list = []
            nss_values_listlog = []
            for i, scan in enumerate(flat_smoothed_data.keys()):
                original = original_data[scan]
                reconstructed = XAS_data_reconstructed[i]
                smoothed =  flat_smoothed_data[scan]
                noise = noise_levels[scan]
                nss_den = np.sum((smoothed - reconstructed) ** 2) / np.sum(smoothed ** 2)
                nss_data = np.sum((original - smoothed) ** 2) / np.sum(original ** 2)
                nss=(nss_den / nss_data)
                nss_values[scan] = nss
                nss_val[n][scan] = nss
                nss_values_list.append(nss)
                nss_values_listlog.append(np.log(nss))
    
    
            # Output the NSS values
            average_nss = np.mean(nss_values_list)
            std_nss = np.std(nss_values_list)
            average_nss_values.append(average_nss)
            std_nss_values.append(std_nss)
    

            # Plot NSS values for each scan against PCA components
            
            sc=axs[0].scatter([n] * len(nss_values), list(nss_values.keys()), c =nss_values_listlog, cmap='viridis',
                marker='o')
            y_min,y_max=set_y_limits(nss_values_listlog, lower_percentile=25, upper_percentile=75)
            sc.set_clim(vmin=y_min, vmax=y_max)
            


        cbar = plt.colorbar(sc, ax=axs[0], label='log(NSS Value)')
        axs[0].set_xlabel("PCA Components")
        axs[0].set_ylabel("Scans")
        axs[0].set_title("NSS-Estimator")
        
        log_std_nss_values = np.log(std_nss_values)
        
        first_diff = np.diff(log_std_nss_values)

        axs[1].set_xlabel('PCA Components')
        axs[1].set_ylabel('Log $\sigma$ (NSS Values)', color='tab:blue')
        axs[1].plot(range(1, pc+1), log_std_nss_values, marker='o', color='tab:blue')
        axs[1].tick_params(axis='y', labelcolor='tab:blue')
        axs[1].set_xlim(0,pc+1)
        axs_twin = axs[1].twinx()  # Create a twin axis for the second plot
        axs_twin.set_ylabel('Log of First Differences of $\sigma$ (NSS Values)', color='tab:red')

        
        y_min,y_max=set_y_limits(log_std_nss_values, lower_percentile=10, upper_percentile=100)
        axs[1].set_ylim(y_min, y_max)
        
        y_min,y_max=set_y_limits(first_diff,lower_percentile=5, upper_percentile=100)
        axs_twin.set_ylim(y_min, y_max)

        axs_twin.plot(range(2, pc + 1), first_diff, color='tab:red')
        axs_twin.tick_params(axis='y', labelcolor='tab:red')
      
        fig.tight_layout()  
        plt.show()
        return nss_values, nss_val
    
########################################################################################
#################################### PCA fit ###########################################
########################################################################################

    def make_PCAfit(energy,intensity):
        """
        Perform PCA fits for a given scan and number of principal components.

       

        Returns:
        - pcfitdic: dict
            Dictionary containing spectra PCA fits and residuals
        """
        u,s,v=makeSVD(intensity)
        ncol = np.shape(intensity)[1]
        pcfitdic={}
        
        while True:
            scan_input = input("Please select a scan number for the PCA fit (or 'q' to quit): ")
            if scan_input.lower() == 'q':
                break

            scan_input = int(scan_input)
            pc_input = input("Please select the number of principal components for the PCA fit: ")
            if pc_input.lower() == 'q':
                break

            pc_input = int(pc_input)
            
           
            fig = plt.figure(figsize=(8, 7),dpi=300)
            gs = GridSpec(2, 1, height_ratios=[5, 1])
            ax1 = fig.add_subplot(gs[0])
            ax2 = fig.add_subplot(gs[1])
            ax2.set_xlabel('Energy', size=12)
            ax1.set_ylabel('Intensity', size=12)
            ax2.set_ylabel('Residuals', size=12)
            ax1.set_title('PCA Fit', size=15)

            pcfit = np.dot(u[:, 0:pc_input], np.dot(np.diag(s[0:pc_input]), v[0:pc_input, :]))
            
            title = f"PCs: {pc_input}, Scan: {scan_input}"
            
            
            
            line, = ax1.plot(energy, intensity[:, scan_input], color='black', label='Spectrum: '+str(scan_input))
            line1, = ax1.plot(energy, pcfit[:, scan_input], color='blue', label='PCs: '+str(pc_input))
            residuals = intensity[:, scan_input] - pcfit[:, scan_input]
            line2, = ax2.plot(energy, residuals)
            ax1.legend()
            
            if title not in pcfitdic:
                pcfitdic[title] = {}  # Initialize the dictionary for this title
                pcfitdic[title]["fit"]= pcfit[:, scan_input]
                pcfitdic[title]["residuals"]= residuals
                
                
            plt.show()
            
        return pcfitdic
        
        

    


########################################################################################
########################## INCLUDES EVERYTHING #########################################
########################################################################################

def pca_estimator(dataset=None, skiplist=[], file_path = None , xanes_start = None, xanes_end = None, plot_xanesrange = True, pc = None,
                  statistic = True, r_factor = True, plot_noise = True, PCA_fit= False, NSS = True):
    """
    Perform PCA estimation.

    Parameters:
    - dataset: dict, optional
        Dataset dictionary. 
    - skiplist: list, optional
        List of scans to skip. Default is an empty list.
    - file_path: str, optional
        Path to the .dat file with the XANES data. 
    - xanes_start: int, optional
        Start energy value for XANES range.
    - xanes_end: int, optional
        End energy value for XANES range.
    - plot_xanesrange: bool, optional
        Whether to plot XANES range. Default is True.
    - pc: int, optional
        The number of principal components. Default is None and will take the value of total number of scans.
    - statistic: bool, optional
        Whether to compute PCA statistics. 
    - r_factor: bool, optional
        Whether to compute R-factor.
    - plot_noise: bool, optional
        Whether to plot noise. 
    - PCA_fit: bool, optional
        Wheter to compute de PCA fit for a given scan and number of principal components.
    - NSS: bool, optional
        Whether to compute NSS values. 

    Returns:
    - pca_datadic: dict
        Dictionary containing PCA statistics, R-factor, and NSS values.
    """
    # Fillin dictionary
    pca_datadic = {}
    
    pca_file(dataset=dataset,skiplist=skiplist,file_path = file_path , xanes_start = xanes_start, xanes_end = xanes_end, plot_xanesrange = plot_xanesrange)
    xanes=Dataset(np.loadtxt(file_path))
    
     
    
    if statistic == True:
        s, ind, fisher, ie = PCAest.PCA_Statistic(xanes.intensity, pc=pc)
        pca_datadic["Scree-plot"] = s
        pca_datadic["IND"] = ind
        pca_datadic["Fisher"] = fisher
        pca_datadic["IE"] = ie
             
    if r_factor == True:
        resvalue = PCAest.Rfactor(xanes.intensity,  pc=pc, plot_noise = plot_noise,dataset=dataset)
        pca_datadic["R-factor"] = resvalue
    if PCA_fit == True:
        pcfitdic= PCAest.make_PCAfit(xanes.energy,xanes.intensity)
        pca_datadic["PCA-Fits"] = pcfitdic
    if NSS == True:
        nss_values, nss_val = PCAest.NSS(xanes.intensity, pc=pc,dataset=dataset,skiplist=skiplist)
        pca_datadic["NSS-Values"] = nss_val
    
    
    return pca_datadic
        
import numpy as np
import matplotlib.gridspec as gs

import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.rcParams['savefig.dpi'] = 100

import pymcr
from pymcr.mcr import McrAR
from pymcr.regressors import OLS, NNLS
from pymcr.constraints import ConstraintNonneg, ConstraintNorm

from sklearn.linear_model import Ridge
from scipy.interpolate import interp1d
import numpy as np


def create_file(datasets=[], skiplist =[],file_path = None , xanes_start = None, xanes_end = None):
    """
    This function creates a .dat file with the energy and flat values of the scans in the XANES range.
    This .dat file is needed for the PCA functions. 
    

    Parameters:
    - dataset: dictionary
        XAS dictionary.
    - skiplist: list
        Scan numbers to skip.
    - file_path: str
        Path to the .dat file with the XANES data. 
    - xanes_start: int, optional
        Start energy value for XANES range.
    - xanes_end: int, optional
        End energy value for XANES range.
    - plot_xanesrange: bool, optional
        Whether to plot XANES range. Default is True.
    
    Returns:
    
    """
    if datasets == None:
        print("Select the corresponding datasets")
   
   
    x=np.linspace(xanes_start,xanes_end,2000)
    refs = x
    
    scans_list=[]
    for dataset in datasets:
        # print(dataset)
                
        for scan_key in dataset.keys():  # Ensuring sorted order for consistency
            scans_list.append(scan_key)
            if scan_key in skiplist:
                continue
                
            f = interp1d(dataset[scan_key]["energy"],dataset[scan_key]["flat"])
               
            refs=np.c_[refs,f(x)]

           
        np.savetxt(file_path,refs)
        print(refs.shape)
            


    print(f"Selected data saved to {file_path}")
    
    # Count the keys in each dictionary
    key_counts = [len(data) for data in datasets]

    # Print the key counts for each dictionary
    for index, count in enumerate(key_counts):
        print(f"Dataset {index + 1} has {count} scans")

    #print(key_counts)

    total_scans = sum(key_counts)
    print(f"Total scans: {total_scans}")

    div_vals = []
    div=0
    for index, count in enumerate(key_counts):
        print(f"Dataset {index + 1} starts in {div} scan")
        div += count
        div_vals.append(div)

    return div_vals, scans_list

def simplisma(d, nr , error=5):
    #Taken from github
    energy=d[:,0]
    d=np.delete(d,0,1)
    
    def wmat(c,imp,irank,jvar):
        dm=np.zeros((irank+1, irank+1))
        dm[0,0]=c[jvar,jvar]
		
        for k in range(irank):
            kvar=int(imp[k])
			
            dm[0,k+1]=c[jvar,kvar]
            dm[k+1,0]=c[kvar,jvar]
			
            for kk in range(irank):
                kkvar=int(imp[kk])
                dm[k+1,kk+1]=c[kvar,kkvar]
		
        return dm

    nrow,ncol=d.shape
	
    dl = np.zeros((nrow, ncol))
    imp = np.zeros(nr)
    mp = np.zeros(nr)
	
    w = np.zeros((nr, ncol))
    p = np.zeros((nr, ncol))
    s = np.zeros((nr, ncol))
	
    error=error/100
    mean=np.mean(d, axis=0)
    error=np.max(mean)*error
	
    s[0,:]=np.std(d, axis=0)
    w[0,:]=(s[0,:]**2)+(mean**2)
    p[0,:]=s[0,:]/(mean+error)

    imp[0] = int(np.argmax(p[0,:]))
    mp[0] = p[0,:][int(imp[0])]
	
    l=np.sqrt((s[0,:]**2)+((mean+error)**2))

    for j in range(ncol):
        dl[:,j]=d[:,j]/l[j]
		
    c=np.dot(dl.T,dl)/nrow
	
    w[0,:]=w[0,:]/(l**2)
    p[0,:]=w[0,:]*p[0,:]
    s[0,:]=w[0,:]*s[0,:]
	
    print('purest variable 1: ', int(imp[0]+1), mp[0])

    for i in range(nr-1):
        for j in range(ncol):
            dm=wmat(c,imp,i+1,j)
            w[i+1,j]=np.linalg.det(dm)
            p[i+1,j]=w[i+1,j]*p[0,j]
            s[i+1,j]=w[i+1,j]*s[0,j]
			
        imp[i+1] = int(np.argmax(p[i+1,:]))
        mp[i+1] = p[i+1,int(imp[i+1])]
		
        print('purest variable '+str(i+2)+': ', int(imp[i+1]+1), mp[i+1])
		
    sp=np.zeros((nrow, nr))
			
    for i in range(nr):
        sp[0:nrow,i]=d[0:nrow,int(imp[i])]
		
    # plt.figure(figsize = (10,6),dpi=300)
    plt.figure().set_figheight(10)
    for i in range(nr):
        plt.plot(energy,sp[:,i]+0.8*i, label = str(i+1))
    plt.title('SIMPLISMA: Initial guess')
    plt.ylabel(r'Normalized $\mu$')
    plt.xlabel('Energy')
    plt.legend()
    # plt.show()
    concs = np.dot(np.linalg.pinv(sp), d)
	
    
    return energy, d, sp, concs    

def mcr(d,nr, ref_spectra=None, fix_spectra=None, div_vals=[], mcr_plot=False, conc_plot=False, MCR_fit=False, Rfactor_plot=False):
    """
    Perform Multivariate Curve Resolution (MCR) analysis on spectral data.

    Parameters:
    d (array): Data matrix
    nr (int): Number of components to be provided by the user.
    ref_spectra (array, optional): Reference spectra to be used as initial guesses.
    fix_spectra (list, optional): Indices of spectra to be fixed during the MCR fitting process.
    div_vals (list, optional): Division values for concentration plot regions (in case of using more that one dataset).
    mcr_plot (bool, optional): If True, plot MCR retrieved spectra. Default is False.
    conc_plot (bool, optional): If True, plot concentration profiles. Default is False.
    MCR_fit (bool, optional): If True, provide detailed MCR fit for individual scans. Default is False.
    Rfactor_plot (bool, optional): If True, plot R-factor. Default is False.

    Returns:
    MCR-AR object and a dictionary containing MCR results.
    """
    energy, d, sp, concs=simplisma(d, nr)
    simp_sp=sp
    print('###### Simplisma shape: ', simp_sp.shape)
    
    if ref_spectra is None:
        adjust_fix_spectra = [x - 1 for x in fix_spectra]
        mcrar = McrAR(max_iter=500, st_regr='NNLS', c_regr=OLS(), 
                    c_constraints=[ConstraintNonneg(), ConstraintNorm()])
        
        mcrar.fit(np.transpose(d),ST=np.transpose(sp), st_fix=adjust_fix_spectra,verbose=True)
        
        
    # If reference spectra are provided, set them as initial estimates
    else:
        energy=ref_spectra[:,0]
        ref_spectra=np.delete(ref_spectra,0,1)
        sp=ref_spectra
        num_ref_spectra = ref_spectra.shape[1]
        
        #Plot references
        plt.figure(figsize = (10,6),dpi=300)
        for i in range(num_ref_spectra):
            plt.plot(energy,sp[:,i], label = str(i+1))
        plt.title('Imported references')
        plt.ylabel(r'Normalized $\mu$')
        plt.xlabel('Energy')
        plt.legend()
        plt.show()
        
        
        # Use a hybrid initial guess combining references and SIMPLISMA solutions
        if num_ref_spectra < nr:
            selected_simplisma_indices = []
            
            
            chosen = False
            while not chosen:
                #Ask the user which solutions from simplisma to take
                print("Enter "+ str(nr-num_ref_spectra)+" indices of the SIMPLISMA spectra you want to add to the initial guess, separated by commas:")
                user_input = input()
            
            
                if user_input:
                    selected_simplisma_indices = list(map(int, user_input.split(',')))
                    if len(selected_simplisma_indices) == nr - num_ref_spectra:
                        chosen = True
            adjusted_simplisma_indices = [x - 1 for x in selected_simplisma_indices]
            sp = np.hstack((ref_spectra, simp_sp[:, adjusted_simplisma_indices]))
            
            
        
        
        adjust_fix_spectra = [x - 1 for x in fix_spectra]
        mcrar = McrAR(max_iter=500, st_regr='NNLS', c_regr=OLS(), 
                    c_constraints=[ConstraintNonneg(), ConstraintNorm()])
        
        mcrar.fit(np.transpose(d),ST=np.transpose(sp), st_fix=adjust_fix_spectra,verbose=True)
        
        plt.figure(figsize = (10,6),dpi=300)
        for i in range(nr):
            
            plt.plot(energy,sp[:,i], label = str(i+1))
            plt.title('Initial guess')
            plt.ylabel(r'Normalized $\mu$')
            plt.xlabel('Energy')
            plt.legend()
        plt.show()
        
        
    
    print('\nFinal MSE: {:.7e}'.format(mcrar.err[-1]))
    mcr_dic={}
    mcr_dic["Initial guess"]={}
    mcr_dic["MCR"]={}
    mcr_dic["Concentration"]={}
    mcr_dic["Energy"]=energy
    for i in range(nr):
        mcr_dic["Initial guess"][i]=sp[:,i]
        mcr_dic["MCR"][i]=mcrar.ST_opt_.T[:,i]
        mcr_dic["Concentration"][i]=mcrar.C_opt_[:,i]
    
    
    if mcr_plot == True:
        
        plt.figure(figsize = (10,6), dpi=300)
        plt.plot(energy, mcrar.ST_opt_.T)
        plt.ylabel(r'Normalized $\mu$')
        plt.xlabel('Energy')
        plt.title('MCR-AR Retrieved')
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize = (6,8),dpi=300)
        for i in range(nr):
            plt.plot(energy,mcrar.ST_opt_.T[:,i]+i*0.8, label = str(i+1)+' component')
            plt.title('MCR-AR Retrieved')
            plt.ylabel(r'Normalized $\mu$')
            plt.xlabel('Energy')
            plt.legend()
        plt.show()
    
    if conc_plot == True:
    
        plt.figure(figsize = (10,4),dpi=300)
        for i in range(nr):
            plt.plot(mcrar.C_opt_[:,i], label = str(i+1)+' component')
        plt.xlabel('Scans')
        plt.ylabel('Concentration')
        
        if div_vals is not None:
            # Get the colormap and the number of colors in it
            colormap = cm.get_cmap('Pastel1')
            num_colors = colormap.N
    
            # Generate a list of colors by cycling through the colormap
            colors = [colormap(i % num_colors) for i in range(len(div_vals))]
            
            for i in range(len(div_vals)):
                if i == 0:
                    plt.axvspan(0, div_vals[i], facecolor=colors[i], alpha=0.5)
                else:
                    plt.axvspan(div_vals[i-1], div_vals[i], facecolor=colors[i], alpha=0.5)
        plt.show()
    
    comp = mcrar.ST_opt_.T
    conc = mcrar.C_opt_
   
    diff = (d - (np.matmul(comp, conc.T)))**2
    diff = diff.sum(axis = 0)/10000
    
    r_factor_top = ((d - (np.matmul(comp, np.transpose(conc)))))**2
    r_factor_top = r_factor_top.sum(axis = 0)
    r_factor_bottom = d**2
    r_factor_bottom = r_factor_bottom.sum(axis=0)
    r_factor = r_factor_top/r_factor_bottom
    
    #R-factor calculation
    if Rfactor_plot == True:
    
        plt.figure(figsize = (10,4),dpi=300)
           
        plt.plot(r_factor, label = str(i+1)+' component')
        plt.xlabel('Scans')
        plt.ylabel('R-factor')
        
        if div_vals is not None:
            # Get the colormap and the number of colors in it
            colormap = cm.get_cmap('Pastel1')
            num_colors = colormap.N

            # Generate a list of colors by cycling through the colormap
            colors = [colormap(i % num_colors) for i in range(len(div_vals))]
        
            for i in range(len(div_vals)):
                if i == 0:
                    plt.axvspan(0, div_vals[i], facecolor=colors[i],alpha=0.5)
                else:
                    plt.axvspan(div_vals[i-1], div_vals[i],facecolor=colors[i], alpha=0.5)
                
        plt.show()
    
    mcr_dic["R-factor"]=r_factor
    
    if MCR_fit == True:
        while True:
            scan_input = input("Please select a scan number for the MCR fit (or 'q' to quit): ")
            
            if scan_input.lower() == 'q':
                break

            scan_input = int(scan_input)
        
            fig = plt.figure(figsize=(8, 7),dpi=300)
            g = gs.GridSpec(2, 1, height_ratios=[5, 1])
            ax1 = fig.add_subplot(g[0])
            ax2 = fig.add_subplot(g[1])
            ax2.set_xlabel('Energy', size=12)
            ax1.set_ylabel('Intensity', size=12)
            ax2.set_ylabel('Residuals', size=12)
            ax1.set_title('MCR Fit', size=15)
            
            
            line, = ax1.plot(energy, d[:,scan_input], color='black', label='Spectrum: '+str(scan_input))
            line1, = ax1.plot(energy, np.matmul(comp, np.transpose(conc))[:,scan_input], color='blue', label="MCR")
            residuals = d[:, scan_input] - np.matmul(comp, np.transpose(conc))[:,scan_input]
            line2, = ax2.plot(energy, residuals)
            ax1.legend()
            plt.show()
            
        
    return mcrar, mcr_dic
    
################################ PROCESS REFERENCES #############################

def process_data_ref_txt(file_paths, xanes_start,xanes_end):
    # Initialize dictionaries
    ref_dicts = {i: {"energy": [], "flat": []} for i in range(len(file_paths))}
    interp_grid = np.linspace(xanes_start, xanes_end, 2000) 

    # General function to read data from a file and populate the dictionary
    def read_data(file_path, ref_dict):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Remove any leading/trailing whitespace
                    line = line.strip()
                    if line:
                        try:
                            # Split line into energy and flat values
                            energy, flat = line.split()#('\t')
                            ref_dict['energy'].append(float(energy.strip()))
                            ref_dict['flat'].append(float(flat.strip()))
                           
                        except ValueError as e:
                            print(f"Error parsing line '{line}': {e}")
        except FileNotFoundError as e:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return ref_dict
   
     
    

    # Read data and create new dictionaries
    selected_refs = {}
    for i, file_path in enumerate(file_paths):
        ref_dict = read_data(file_path, ref_dicts[i])
        selected_refs[i] = {}
        selected_refs[i]['energy'] = interp_grid
        
        
        selected_refs[i]['flat'] = interp1d(ref_dict['energy'],ref_dict['flat'], bounds_error = False, fill_value = 'extrapolate')(interp_grid)
        # f= interp1d(energy,flat)
        
        
    
    return selected_refs


from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit


    # In[2]:
def lc_check(data, components,div_vals):
    
    lcf_dic = {}
    # Extract energy and remove the first column from data and components
    energy = data[:, 0]
    data = np.delete(data, 0, 1)
    components = np.delete(components, 0, 1)
    
    X = components
    Y = data
    
    num_scans = data.shape[1]
    colnum = components.shape[1]
    conc = np.empty((num_scans, colnum))
    
    
    for i in range(num_scans):
        scan = data[:, i]
        reg = LinearRegression(positive=True).fit(components,scan)
        conc[i, :] = reg.coef_
    
    # Plot references
    plt.figure(figsize=(7, 8), dpi=300)
    for i in range(colnum):
        plt.plot(energy, components[:, i], label=str(i + 1))
    plt.title('Imported references')
    plt.ylabel(r'Normalized $\mu$')
    plt.xlabel('Energy')
    plt.legend()
    plt.show()
    
    # plot concentrations
    plt.figure(figsize=(10, 4), dpi=300)
    for i in range(colnum):
        plt.plot(conc[:, i], label=f'Component {i+1}')
    
    if div_vals is not None:
        # Get the colormap and the number of colors in it
        colormap = cm.get_cmap('Pastel1')
        num_colors = colormap.N

        # Generate a list of colors by cycling through the colormap
        colors = [colormap(i % num_colors) for i in range(len(div_vals))]
        
        for i in range(len(div_vals)):
            if i == 0:
                plt.axvspan(0, div_vals[i], facecolor=colors[i], alpha=0.5)
            else:
                plt.axvspan(div_vals[i-1], div_vals[i], facecolor=colors[i], alpha=0.5)
    plt.xlabel('Scans')
    plt.ylabel('Concentration')
    plt.legend()
    plt.show()
    
    diff = (data - (np.matmul(components, conc.T)))**2
    diff = diff.sum(axis = 0)/10000
    
    r_factor_top = ((data - (np.matmul(components, np.transpose(conc)))))**2
    r_factor_top = r_factor_top.sum(axis = 0)
    r_factor_bottom = data**2
    r_factor_bottom = r_factor_bottom.sum(axis=0)
    r_factor = r_factor_top/r_factor_bottom
    
    plt.figure(figsize = (10,4),dpi=300)
       
    plt.plot(r_factor, label = str(i+1)+' component')
    plt.xlabel('Scans')
    plt.ylabel('R-factor')
    
    if div_vals is not None:
        # Get the colormap and the number of colors in it
        colormap = cm.get_cmap('Pastel1')
        num_colors = colormap.N

        # Generate a list of colors by cycling through the colormap
        colors = [colormap(i % num_colors) for i in range(len(div_vals))]
    
        for i in range(len(div_vals)):
            if i == 0:
                plt.axvspan(0, div_vals[i], facecolor=colors[i],alpha=0.5)
            else:
                plt.axvspan(div_vals[i-1], div_vals[i],facecolor=colors[i], alpha=0.5)
            
    plt.show()
    
    lcf_dic['R-factor'] = r_factor
    lcf_dic['Concentration'] = conc
    lcf_dic['Components']= components
    
    return lcf_dic
        