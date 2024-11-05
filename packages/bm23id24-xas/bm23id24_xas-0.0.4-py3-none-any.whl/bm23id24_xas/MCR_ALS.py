
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

# import importlib.util

# def load_params(file_path):
#     spec = importlib.util.spec_from_file_location("params", file_path)
#     params = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(params)
    
#     # Load all variables from the module directly into the global scope
#     globals().update({key: value for key, value in params.__dict__.items() if not key.startswith("__")})


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


