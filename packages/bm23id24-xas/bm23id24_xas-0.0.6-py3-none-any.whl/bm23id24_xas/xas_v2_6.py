import h5py
import os 
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from itertools import cycle


import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter

import importlib.util

import statistics
import numpy as np
import pandas as pd
import larch
from larch import Group
from larch.xafs import *
from datetime import datetime
from scipy.signal import savgol_filter as savgol




def load_params(file_path):
    spec = importlib.util.spec_from_file_location("params", file_path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    
    # Load all variables from the module directly into the global scope
    globals().update({key: value for key, value in params.__dict__.items() if not key.startswith("__")})




def xas(n_first = 1, n_last = None, skiplist = [], path = None, calibrate = False, align = False, interpolate = False, exafs = False, merge = 1):
    """
    xas v2.6
    """
    ### Choosing the file
    if path == None:
        print('Please specify the file path to a .h5 file and restart')
            
    ### Saving directory 
    directory=str(os.path.dirname(path))  # that will save to the directory of the .h5 file
    print(f'Directory set to: {directory}')        
    
    ### Reading params.py file
    load_params(directory+"/params.py")

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




    
    
    