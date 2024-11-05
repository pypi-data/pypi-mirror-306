
def load_params(file_path):
    spec = importlib.util.spec_from_file_location("params", file_path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    
    # Load all variables from the module directly into the global scope
    globals().update({key: value for key, value in params.__dict__.items() if not key.startswith("__")})





import numpy as np
from sklearn.decomposition import PCA as PCAskl
import matplotlib.pyplot as plt
from pyfitit.factor_analysis import *
from scipy.interpolate import interp1d


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
        
        
    
        
      
# -







#

# +
#help(pca_estimator)
# -




