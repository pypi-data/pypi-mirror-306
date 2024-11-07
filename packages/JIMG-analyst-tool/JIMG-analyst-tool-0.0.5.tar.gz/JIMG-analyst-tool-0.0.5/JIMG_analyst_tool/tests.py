'''
Download test data 
'''

from features_selection import test_data

test_data()


'''
Test for microscope image of nuclei
'''

from features_selection import NucleiFinder


# initiate class
nf = NucleiFinder()


image = nf.load_image('test_data/microscope_nuclei/r01c02f90p20-ch1sk1fk1fl1.tiff')


nf.input_image(image)


# Check the basic parameters
nf.current_parameters_nuclei


# Test nms & prob parmeters for nuclei segmentation
nf.nuclei_finder_test()

nf.browser_test()


# If required, change parameters
nf.set_nms(nms = 0.9)

nf.set_prob(prob = 0.5)


# Analysis

# 1. First step on nuclei analysis
nf.find_nuclei()


# Parameters for micrsocope image adjustment 
nf.current_parameters_img_adj


# If image required changes, change parameters and run again (nf.find_nuclei())
nf.set_adj_image_brightness(brightness = 1000)

nf.set_adj_image_gamma(gamma = 1.2)

nf.set_adj_image_contrast(contrast = 2)


# Check if parameters has changed
nf.current_parameters_nuclei


# Second execution with new parameters for image adjustment
nf.find_nuclei()


# Return results
nuclei_results, analysed_img = nf.get_results_nuclei()


# 2. Second step of analysis (selection)
nf.select_nuclei()


# Parameters for selecting nuclei; adjust if analysis results do not meet 
# requirements, and re-run the analysis as needed.
nf.current_parameters_nuclei

nf.set_nuclei_circularity(circ = 0.5)

nf.set_nuclei_yx_len_min_ratio(ratio = 0.2)

nf.set_nuclei_size(size = (100,800))

nf.set_nuclei_min_mean_intensity(intensity = 2000)


# Check if parameters has changed
nf.current_parameters_nuclei


# Second execution with adjusted parameters of second step of analysis (selection)
nf.select_nuclei()


# Return results
nuclei_selected_results, analysed_selected_img = nf.get_results_nuclei_selected()


# 3. third step (chromatinization alaysis)
nf.nuclei_chromatinization()


# Parameters for nuclei chromatinization; adjust if analysis results do not meet 
# requirements, and re-run the analysis as needed.


# Chromatinization parameters

nf.current_parameters_chromatinization

nf.set_chromatinization_size(size = (2,400))

nf.set_chromatinization_ratio(ratio = .05)

nf.set_chromatinization_cut_point(cut_point = .95)

nf.current_parameters_chromatinization

# Chromatinization image parameters

nf.current_parameters_img_adj_chro

nf.set_adj_chrom_gamma(gamma = 0.25)

nf.set_adj_chrom_contrast(contrast = 3)

nf.set_adj_chrom_brightness(brightness = 950)

nf.current_parameters_img_adj_chro


# Second execution of the third step (chromatinization analysis)
nf.nuclei_chromatinization()


# Return results
chromatinization_results, analysed_chromatinization_img = nf.get_results_nuclei_chromatinization()



# If your parameters are correct for your data, you can run series analysis on more images

# Nuclei 

series_results_nuclei = nf.series_analysis_nuclei(path_to_images = 'test_data/microscope_nuclei', 
                                                  file_extension = 'tiff', 
                                                  selected_id = [], 
                                                  fille_name_part = 'ch1',
                                                  selection_opt = True, 
                                                  include_img = False, 
                                                  test_series = 0)

# save results

import os
from features_selection import NucleiDataManagement
# initiate class
ndm = NucleiDataManagement()

ndm.save_nuclei_results(path = os.getcwd(), data = series_results_nuclei, id_name = 'example_nuclei')


# Chromatinization 

series_results_chromatinization = nf.series_analysis_chromatinization(path_to_images = 'test_data/microscope_nuclei', 
                                                  file_extension = 'tiff', 
                                                  selected_id = [], 
                                                  fille_name_part = 'ch1',
                                                  selection_opt = True, 
                                                  include_img = True, 
                                                  test_series = 0)

# save results
ndm = NucleiDataManagement()

ndm.save_nuclei_results(path = os.getcwd(), data = series_results_chromatinization, id_name = 'example_chromatinization')



###############################################################################

# Nuclei data selection, experiments concatenation and DataFrame creation


ndm = NucleiDataManagement()

ndm.select_nuclei_data(path_to_results = os.getcwd(), 
                       data_sets = ['example_chromatinization'])



data = ndm.get_mutual_data()


###############################################################################


'''
Test for Flow Cytometry images of nuclei
'''


from features_selection import NucleiFinder


# initiate class
nf = NucleiFinder()


image = nf.load_image('test_data/flow_cytometry/ctrl/3087_Ch7.ome.tif')


nf.input_image(image)


# Check the basic parameters
nf.current_parameters_nuclei


# Test nms & prob parmeters for nuclei segmentation
nf.nuclei_finder_test()

nf.browser_test()


# If required, change parameters
nf.set_nms(nms = 0.6)

nf.set_prob(prob = 0.3)


# Analysis

# 1. First step on nuclei analysis
nf.find_nuclei()


# Parameters for micrsocope image adjustment 
nf.current_parameters_img_adj


# If image required changes, change parameters and run again (nf.find_nuclei())
nf.set_adj_image_brightness(brightness = 1000)

nf.set_adj_image_gamma(gamma = 1.2)

nf.set_adj_image_contrast(contrast = 2)


# Check if parameters has changed
nf.current_parameters_nuclei


# Second execution with new parameters for image adjustment
nf.find_nuclei()


# Return results
nuclei_results, analysed_img = nf.get_results_nuclei()


# 2. Second step of analysis (selection)
nf.select_nuclei()


# Parameters for selecting nuclei; adjust if analysis results do not meet 
# requirements, and re-run the analysis as needed.
nf.current_parameters_nuclei

nf.set_nuclei_circularity(circ = 0.5)

nf.set_nuclei_yx_len_min_ratio(ratio = 0.2)

nf.set_nuclei_size(size = (100,800))

nf.set_nuclei_min_mean_intensity(intensity = 2000)


# Check if parameters has changed
nf.current_parameters_nuclei


# Second execution with adjusted parameters of second step of analysis (selection)
nf.select_nuclei()


# Return results
nuclei_selected_results, analysed_selected_img = nf.get_results_nuclei_selected()


# 3. third step (chromatinization alaysis)
nf.nuclei_chromatinization()


# Parameters for nuclei chromatinization; adjust if analysis results do not meet 
# requirements, and re-run the analysis as needed.


# Chromatinization parameters
nf.current_parameters_chromatinization

nf.set_chromatinization_size(size = (2,1000))

nf.set_chromatinization_ratio(ratio = 0.005)

nf.set_chromatinization_cut_point(cut_point = 1.05)

nf.current_parameters_chromatinization


# Chromatinization image parameters
nf.current_parameters_img_adj_chro

nf.set_adj_chrom_gamma(gamma = 0.25)

nf.set_adj_chrom_contrast(contrast = 4)

nf.set_adj_chrom_brightness(brightness = 950)

nf.current_parameters_img_adj_chro


# Second execution of the third step (chromatinization analysis)
nf.nuclei_chromatinization()


# Return results
chromatinization_results, analysed_chromatinization_img = nf.get_results_nuclei_chromatinization()


# If your parameters are correct for your data, you can run series analysis on more images


# Chromatinization CTRL CELLS
series_results_chromatinization = nf.series_analysis_chromatinization(path_to_images = 'test_data/flow_cytometry/ctrl', 
                                                  file_extension = 'tif', 
                                                  selected_id = [], 
                                                  selection_opt = True, 
                                                  include_img = False, 
                                                  test_series = 0)




import os
from features_selection import NucleiDataManagement

# initiate class
ndm = NucleiDataManagement()

ndm.save_nuclei_results(path = os.getcwd(), data = series_results_chromatinization, id_name = 'ctrl_chromatinization')



# Chromatinization DISEASE CELLS

series_results_chromatinization = nf.series_analysis_chromatinization(path_to_images = 'test_data/flow_cytometry/dis', 
                                                  file_extension = 'tif', 
                                                  selected_id = [], 
                                                  selection_opt = True, 
                                                  include_img = False, 
                                                  test_series = 0)

# save results
ndm = NucleiDataManagement()

ndm.save_nuclei_results(path = os.getcwd(), data = series_results_chromatinization, id_name = 'disease_chromatinization')



###############################################################################

# Nuclei data selection, experiments concatenation and DataFrame creation


ndm = NucleiDataManagement()

ndm.select_nuclei_data(path_to_results = os.getcwd(), 
                       data_sets = ['ctrl_chromatinization', 'disease_chromatinization'])



nuclei_data = ndm.get_mutual_data()

import pandas as pd

features_list = pd.read_csv('test_data/flow_cytometry/ctrl.txt', sep='\t', header=1, nrows=0).columns.tolist()

# reduce features - to exclude

to_reduce = ['Object Number.1', 'Camera Timer', 'Camera Line Number', 
             'Raw Centroid X', 'Raw Centroid Y', 'Time']

reduced_features_list = [col for col in features_list if col not in to_reduce]

ndm.concat_IS_results(nuclei_data, 
                      data_sets = ['ctrl', 'dis'], 
                      IS_data_path = 'test_data/flow_cytometry', 
                      IS_features = reduced_features_list)


data = ndm.get_mutual_IS_data()


# save to csv

data.to_csv('dis_vs_ctrl_nuclei.csv', index = False)




###############################################################################


'''
Test for DFA analysis of nuclei
'''


from features_selection import GroupAnalysis

# initiate class
ga = GroupAnalysis()



# load data from csv file
ga.load_data(path = 'test_data/DFA/dis_vs_ctrl_nuclei.csv',
          ids_col = 'id_name', 
          set_col = 'set')


# check available groups for selection of differential features
ga.groups

# run DFA analysis on example sets
group_diff_features = ga.DFA(meta_group_by = 'sets',
    sets = {'disease':['disease_chromatinization'],
            'ctrl':['ctrl_chromatinization']}, 
    n_proc = 5)


# select differential features

diff_features = list(group_diff_features['feature'][group_diff_features['p_val'] <= 0.05])

ga.select_data(features_list = diff_features)


# scale data
ga.data_scale()


# run PCA dimensionality reduction
ga.PCA()


# get PCA data, if required
pca_data = ga.get_PCA()


# run PC variance analysis
ga.var_plot()


# get var_data, if required
var_data = ga.get_var_data()


# get knee_plot, if required
knee_plot = ga.get_knee_plot(show = True)


# save knee_plot, if required
ga.save_knee_plot(path = os.getcwd(),
               name = '', 
               extension = 'svg')


# run UMAP dimensionality reduction
ga.UMAP(PC_num = 15,
     factorize_with_metadata = True, 
     n_neighbors = 25,
     min_dist = 0.01,
     n_components =2)


# get UMAP_data, if required
UMAP_data = ga.get_UMAP_data()


# get UMAP_plots, if required
UMAP_plots = ga.get_UMAP_plots(show = True)


# save UMAP_plots, if required
ga.save_UMAP_plots(path = os.getcwd(),
                name = '', 
                extension = 'svg')


# run db_scan on UMAP components
ga.db_scan(eps = 0.5,
        min_samples = 10)


# run UMAP_on_clusters
ga.UMAP_on_clusters(min_entities = 10)


# get UMAP_plots, if required
UMAP_plots = ga.get_UMAP_plots(show = True)


# save UMAP_plots, if required
ga.save_UMAP_plots(path = os.getcwd(),
                name = '', 
                extension = 'svg')


# get full_data [data + metadata], if required
full_data = ga.full_info()



# check available groups for selection of differential features
ga.groups


# run DFA analysis on finl clusters
dfa_clusters = ga.DFA(meta_group_by = 'full_name',
    sets = {}, 
    n_proc = 5)



###############################################################################


'''
Test for intensity area selection and analysis
'''


from features_selection import FeatureIntensity


# Select intenity are data for 1st Image - healthy

# initiate class
fi = FeatureIntensity()

# check current metadata
fi.current_metadata

# if required, change parameters
fi.set_projection(projection = 'avg')

fi.set_correction_factorn(factor = 0.2)

# fi.set_scale(scale = 0.5)
# fi.set_selection_list(rm_list = [2,5,6,7])
# OR
# load JIMG project where scale and rm_lis is set in project metadata
# fi.load_JIMG_project_(path = '')
# for more information go to: https://github.com/jkubis96/JIMG
# rm_list and scale can be omitted

# load image
fi.load_image_3D(path = 'test_data/intensity/ctrl/image.tiff')

# or 1D image after projection, be sure that image was not adjusted, for analysis should be use !RAW! image
# fi.load_image_(path)


fi.load_mask_(path = 'test_data/intensity/ctrl/mask_1.png')

fi.load_normalization_mask_(path = 'test_data/intensity/ctrl/background_1.png')


fi.run_calculations()


results = fi.get_results()


fi.save_results(path = os.getcwd(), 
             mask_region = 'brain', 
             feature_name = 'Feature1', 
             individual_number = 1, 
             individual_name = 'CTRL')


###############################################################################


# Select intenity are data for 2st Image - disease

# initiate class
fi = FeatureIntensity()

fi.set_projection(projection = 'avg')

fi.set_correction_factorn(factor = 0.2)

fi.load_image_3D(path = 'test_data/intensity/dise/image.tiff')

fi.load_mask_(path = 'test_data/intensity/dise/mask_1.png')

fi.load_normalization_mask_(path = 'test_data/intensity/dise/background_1.png')

fi.run_calculations()


results = fi.get_results()


fi.save_results(path = os.getcwd(), 
             mask_region = 'brain', 
             feature_name = 'Feature1', 
             individual_number = 1, 
             individual_name = 'DISEASE')



# concatenate data of experiment 1 & 2


fi.concatenate_intensity_data(directory = os.getcwd(), name = 'example_data')


###############################################################################


# Intensity analysis


from features_selection import IntensityAnalysis
import pandas as pd


# initiate class
ia = IntensityAnalysis()



input_data = pd.read_csv('example_data_Feature1_brain.csv')

# check columns
input_data.head()

data = ia.df_to_percentiles(data = input_data,
                                       group_col = 'individual_name',
                                       values_col = 'norm_intensity', sep_perc = 1)


results = ia.hist_compare_plot(data = data,
                               queue = ['CTRL', 'DISEASE'],
                               tested_value = 'avg', p_adj = True, txt_size = 20)




results.savefig('example_results.svg', format='svg', dpi=300, bbox_inches='tight')



