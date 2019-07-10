import astropy as ap
import astropy.io.fits as ap_fits
import astropy.modeling as ap_mod
import copy
import gc
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import scipy as sp
import scipy.optimize as sp_opt
import scipy.stats as sp_stat

import IfA_Smeargle as ifa


# Finding the data files
fits_file_list = glob.glob('./**/Mk20_M12145-40/**/set4/*first16avg.fits',recursive=True)
print(len(fits_file_list))
names = fits_file_list[0].split('\\')[-1]
print(names[:-5] + '.pdf')

print(fits_file_list[0][:-5] + '.pdf')


counter = 0
# List of figures.\n",
for filedex in fits_file_list[counter:]:
    counter += 1

    # Extract.\n",
    fits,header,data = ifa.meta.smeargle_open_fits_file(filedex)

    # Applying hard filter.
    masks = ifa.echo.echo120_subarray_mask(data, [33,288],[0,256], return_mask=False)
    col_mask = np.array([2, 34, 66,98, 130, 162,194, 226, 258, 290]) - 1
    masks = ifa.echo.echo382_column_mask(data, col_mask, previous_mask=masks, return_mask=False)

    # Cold filtering
    masks = ifa.echo.echo_270_minimum_cut(data, 43000, previous_mask=masks, return_mask=False)
    
    final_data = ifa.echo.numpy_masked_array(data,None,masking_dictionary=masks)

    print(ifa.meta.smeargle_masked_array_min_max(final_data))
    
    # Histogram parameters, desires 1 ADU wide bins.
    bin_list = np.arange(np_ma.min(final_data) - 1,np_ma.max(final_data) + 1,100)
    hist_range = [np_ma.min(final_data),np_ma.max(final_data)]
    histogram_parameters = {'histogram_plot_paramters':{'bins':bin_list, 'range':hist_range},'fit_gaussian':False}
    
    figure = ifa.hotel.plot_single_heatmap_and_histogram(final_data,
                                      figure_subplot_parameters={'figsize':(9,3.5), 'dpi':100},
                                      plot_heatmap_parameters={},
                                      plot_histogram_parameters=histogram_parameters)

    ifa.meta.smeargle_save_figure_file(figure,filedex[:-5],filedex[:-5].split('\\')[-1])

    print(" A figure has been saved. Count {cnt}".format(cnt=counter))
    
    
