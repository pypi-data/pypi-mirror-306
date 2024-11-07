# JIMG_analyst_tool - python library

#### JIMG_analyst_tool is a Python library for analyzing high-resolution confocal microscope and flow cytometry images

</br>

<p align="right">
    <img src="https://github.com/jkubis96/Logos/blob/main/logos/jbs_current.png?raw=true" alt="drawing" width="250" />
    <img src="https://github.com/jkubis96/Logos/blob/main/logos/jbi_current.png?raw=true" alt="drawing" width="250" />
</p>

</br>

### Author: Jakub Kubiś 

<div align="left">
 Institute of Bioorganic Chemistry<br />
 Polish Academy of Sciences<br />
</div>


## Description


<div align="justify">

 The JIMG_analyst_tool is a Python library that extends the JIMG image processing tool, specifically tailored for analyzing high-resolution confocal microscope images [Opera-Phoenix](https://www.revvity.com/product/opera-phenix-plus-system-hh14001000?srsltid=AfmBOoohz1LiEemNbG4SJnaEtScwr16MyFL8Ulf9NyDDEAffV2NLJXoe) and other technologies. This library enables detailed examination of nuclei and their chromatin organization, supporting high-resolution analysis of nuclear morphology and chromatin structure.

It also provides algorithms for measuring the intensity of specific protein markers using customizable image masks on high-resolution microscope images. These measurements are normalized using a background mask for consistent data comparison. The collected intensity data can be statistically analyzed to detect differences in marker localization, occurrence, and intensity.

In addition to microscopy, flow cytometry [Amnis-ImageStream](https://cytekbio.com/pages/imagestream) analysis capabilities are integrated into the tool. It can analyze flow cytometry images, applying nuclear and chromatin analysis methods similar to those used for confocal microscopy. Furthermore, the tool enables advanced analysis of cell populations from cytometric data, offering options to select distinguishing cell characteristics, perform clustering of cell sets based on these features, and analyze clusters using statistical methods to identify unique attributes.

With these combined functionalities, the JIMG_analyst_tool is a versatile resource for researchers requiring in-depth quantitative analysis of nuclear and chromatin features in both confocal microscopy and flow cytometry datasets.

</div>

</br>



<br />

## Table of contents

[Installation](#installation) \
[Usage](#usage)
1. [ImageTools](#ImageTools) \
1.1. [Get screen size](#get-screen) \
1.2. [Adjust image to screen size](#adjim) \
1.3. [JIMG project loading](#jimg) \
1.4. [Image loading](#il) \
1.5. [3D-image loading](#3d) \
1.6. [Binary mask loading](#bl) \
1.7. [Image saving](#is) 
2. [NucleiFinder](#nf) \
2.1. [Check metadata](#meta) \
2.1.1. [Parameters for nuclei analysis](#pfna) \
2.1.2. [Parameters for nuclei chromatinization analysis](#pfca) \
2.1.3. [Parameters for nuclei image adjustment](#pfnia) \
2.1.4. [Parameters for nuclei chromatinization image adjustment](#pfcia) \
2.2. [Nuclei analysis parameters adjustment](#napa) \
2.2.1. [Set 'nms' parameter](#nms) \
2.2.2. [Set 'prob' parameter](#prob) \
2.2.3. [Set 'circularity' parameter](#circ) \
2.2.4. [Set 'ratio' parameter](#ratio) \
2.2.5. [Set 'size' parameter](#size) \
2.2.6. [Set 'intensity' parameter](#intensity) \
2.3. [Nuclei chromatinization analysis parameters adjustment](#ncapa) \
2.3.1. [Set chromatinization 'size' parameter](#chsize) \
2.3.2. [Set chromatinization 'ratio' parameter](#chratio) \
2.3.3. [Set chromatinization 'cut_point' parameter](#chcut) \
2.4. [Nuclei image parameters adjustment](#nipa) \
2.4.1. [Set 'brightness' parameter](#brightness) \
2.4.2. [Set 'gamma' parameter](#gamma) \
2.4.3. [Set 'contrast' parameter](#contrast) \
2.5. [Set 'contrast' parameter](#ncipa) \
2.5.1. [Set chromatinization 'gamma' parameter](#cgamma) \
2.5.2. [Set chromatinization 'contrast' parameter](#ccontrast) \
2.5.3. [Set chromatinization 'brightness' parameter](#cbrightness) \
2.6. [Analysis methods](#am) \
2.6.1. [Input single image to analysis](#is) \
2.6.2. [Primary parameters testing](#ppt) \
2.6.3. [Find nuclei on image](#fni) \
2.6.4. [Select 'True' nuclei on image](#st) \
2.6.5. [Find nuclei chromatinization on image](#fnc) \
2.7. [Series analysis methods](#sam) \
2.7.1. [Find nuclei on image series](#fnis) \
2.7.2. [Find nuclei chromatinization on image series](#fncis) 
3. [NucleiDataManagement](#ndm) \
3.1. [Save experiment nuclei data](#send) \
3.2. [Concatenating different sets of experimental data](#cds) \
3.3. [Adding information to the nuclei data](#aitn) \
3.4. [Preparing images for results visualization](#pif) 
4. [GroupAnalysis](#ga) \
4.1. [Loading data from *.csv file](#ldf) \
4.2. [Select features (columns) from data table for analysis](#sffg) \
4.3. [Data scale](#ds) \
4.4. [Principal Component Analysis (PCA)](#pca) \
4.5. [Variance analysis of principal components](#var) \
4.6. [Uniform Manifold Approximation and Projection (UMAP)](#umap) \
4.7. [Clustering of dimensionality reduced data (dbscan)](#dbscan) \
4.8. [Clusters / UMAP visualization](#cu) \
4.9. [Return complete metadata](#rcm) \
4.10. [Differential Feature Analysis (DFA)](#dfa) 
5. [FeatureIntensity](#fi) \
5.1. [Check and adjust primary metadata](#caap) \
5.1.1. [Parameters for intensity analysis](#pfia) \
5.1.2. [Set projection type. If input image is *.tiff file (3D-image)](#3dl) \
5.1.3. [Set correction factor](#scf) \
5.1.4. [Set image scale](#sis) \
5.1.5. [Select images along the z-axis for analysis](#zas) \
5.2. [Input data loading](#idl) \
5.2.1. [Loading JIMG project](#ljp) \
5.2.2. [Loading image](#li) \
5.2.3. [Loading mask(s) for input image](#lmii) \
5.3. [Intensity features selection](#ifs) \
5.3.1. [Run analysis](#raa) \
5.3.2. [Get analysis results](#gaa) \
5.3.3. [Save analysis results](#saa) \
5.3.4. [Concatenation particular analysis results](#cpar) 
6. [IntensityAnalysis](#iaa) \
6.1. [Data preparing](#dp) \
6.1.1. [Drop outlires](#do) \
6.1.2. [Percentiles ranges calculations](#[prc]) \
6.1.3. [Percentiles calculations](#[pcc]) \
6.2. [Statistics](#sta) \
6.2.1. [ANOVA](#staa) \
6.2.2. [ANOVA + posthoc](#anpo) \
6.2.3. [Chi²](#chi) \
6.2.4. [Chi² + posthoc](#chipo) \
6.3. [Visualization](#vis) 
7. [Example pipelines](#epip) \
7.1. [Nuclei analysis - confocal microscopy](#nacm) \
7.2. [Nuclei analysis - flow cytometry](#nafc) \
7.3. [Clustering and DFA - nuclei data](#cdnd) \
7.4. [Marker intensity analysis - confocal microscopy](#miacm) \
7.4.1. [Data collection](#miacmdc) \
7.4.2. [Data analysis](#miacmda) 

<br />

<br />

# Installation <a id="installation"></a>

#### In command line write:

```
pip install JIMG-analyst-tool>=0.0.5
```



<br />


# Usage <a id="usage"></a>

<br />

### 1. ImageTools<a id="ImageTools"></a>

```
from JIMG_analyst_tool.features_selection import ImageTools

# initiate class
it = ImageTools()
```

#### 1.1 Get screen size <a id="get-screen"></a>


```
it.get_screan()
```
    This method returns current screen size.
        
        Returns:
            screen_width (int) - screen width in pixels
            screen_height (int) - Screen height in pixels
                

<br />

#### 1.2 Adjust image to screen size<a id="adjim"></a>

```
resized_image = it.resize_to_screen_img(img_file, factor = 0.5)
```

    This function resizes input image to screen size refactored by user-defined factor value.
        
        Args:
           img_file (np.ndarray) - input image
           factor (int) - value 
          
        Returns:
            
            resized_image (np.ndarray) - resized image
           

<br />

#### 1.3 JIMG project loading <a id="jimg"></a>

```
project = it.load_JIMG_project(project_path)
```

    This method loads a JIMG project. The project file must have the *.pjm extension.
        
        Args:
            file_path (str) - path to the project file.
    
        Returns:
            project (class) - loaded project object
    
        Raises:
            ValueError: If the file does not have a *.pjm extension.
        
<br />

#### 1.4 Image loading<a id="il"></a>

```
image = it.load_image(path_to_image)
```

    This method loads an image.
        
        Args:
            path_to_image (str) - the path to the image
    
        Returns:
            image (np.ndarray) - loaded image
    

<br />

#### 1.5 3D-image loading <a id="3d"></a>

```
image = it.load_3D_tiff(path_to_image)
```

    This method loads a 3D-image.
        
        Args:
            path_to_image (str) - the path to the 3D-image. Extension *.tiff
    
        Returns:
            image (np.ndarray) - loaded 3D-image

<br />

#### 1.6 Binary mask loading<a id="bl"></a>

```
mask = it.load_mask(path_to_mask)
```

    This method loads a mask-image.
        
        Args:
            path_to_mask (str) - the path to the mask-image
    
        Returns:
            mask (np.ndarray) - loaded mask-image
    

<br />

#### 1.7 Image saving <a id="is"></a>

```
it.save(image, file_name)
```

    This method saves image.
        
        Args:
            image (np.ndarray) - the image to save
            file_name (str) - the file name, including extension [.png, .jpeg, ...], and the path to save the file
    

<br />

<br />

### 2. NucleiFinder <a id="nf"></a>

The NucleiFinder class contains all methods from the ImageTools class, as it inherits from ImageTools.

```
from JIMG_analyst_tool.features_selection import NucleiFinder

# initiate class
nf = NucleiFinder()
```

<br />


#### 2.1 Check metadata <a id="meta"></a>

##### 2.1.1 Parameters for nuclei analysis <a id="pfna"></a>

<br />

```
nf.current_parameters_nuclei
```
    @ property
    This method returns current nuclei analysis parameters.
    
        Returns:
            nuclei (dict) - nuclei analysis parameters

<br />


##### 2.1.2 Parameters for nuclei chromatinization analysis <a id="pfca"></a>

<br />

```
nf.current_parameters_chromatinization
```
    @ property
    This method return current nuclei chromatinization analysis parameters.

        Returns:
            nuclei_chromatinization (dict) - nuclei chromatinization analysis parameters
    

<br />



##### 2.1.3 Parameters for nuclei image adjustment <a id="pfnia"></a>

<br />

```
nf.current_parameters_img_adj
```
    @ property
    This method returns current nuclei image setup.
    
        Returns:
            neuclei_image_setup (dict) - nuclei image setup


<br />


##### 2.1.4 Parameters for nuclei chromatinization image adjustment <a id="pfcia"></a>

<br />

```
nf.current_parameters_img_adj_chro
```
    @ property
    This method returns current nuclei chromatinization image setup.
    
        Returns:
            neuclei_chromatinization_setup (dict) - nuclei chromatinization image setup
        

<br />

#### 2.2 Nuclei analysis parameters adjustment <a id="napa"></a>

##### 2.2.1 Set 'nms' parameter <a id="nms"></a>

<br />

```
nf.set_nms(nms)
```
    This method sets 'nms' parameter. The nms threshold is set to a small number to reduce the probability of nuclei overlap.
        
        Args:
            nms (float) - the nms value

<br />

##### 2.2.2 Set 'prob' parameter <a id="prob"></a>

<br />

```
nf.set_prob(prob)
```

    This method sets 'prob' parameter. The prob is a parameter used in image segmentation to determine the level of confidence required for an object (such as a nucleus) to be classified as a segmented entity.

    Effect of Larger prob_thresh Values: When you increase the value of prob_thresh, you will typically observe fewer segmented objects in the resulting images. This is because a higher threshold means that only those objects with a greater degree of certainty will be included in the segmentation, potentially leading to the omission of weaker or less distinct objects.

    Determining Optimal Values: The ideal settings for prob_thresh and other related parameters, such as nm_thresh, can vary significantly based on the specific characteristics of the images being analyzed. It is crucial to visually assess the nuclei segmentation masks produced with different thresholds to find the values that best suit your particular dataset.

        Args:
            prob (float) - the prob value


<br />


##### 2.2.3 Set 'circularity' parameter <a id="circ"></a>

```
nf.set_nuclei_circularity(circ)
```

    This method sets 'circ' parameter. The circ is a parameter used for adjust minimal nucleus circularity.
        
        Args:
            circ (float) - the nuclei circularity value

<br />



##### 2.2.4 Set 'ratio' parameter <a id="ratio"></a>

```
nf.set_nuclei_yx_len_min_ratio(ratio)
```

    This method sets the 'ratio' parameter. In this case, the 'ratio' parameter is similar to 'circularity' as it describes the ratio between the maximum lengths in the x and y dimensions of the nucleus.
        
        Args:
            ratio (float) - the prob value


<br />

##### 2.2.5 Set 'size' parameter <a id="size"></a>

```
nf.set_nuclei_size(size)
```

    This method sets 'size' parameter. The size is a parameter used for adjust minimal and maximal nucleus area (px).
        
        Args:
            size (tuple) - (min_value, max_value)



<br />


##### 2.2.6 Set 'intensity' parameter <a id="intensity"></a>

```
nf.set_nuclei_min_mean_intensity(intensity)
```

    This method sets 'intensity' parameter. The 'intensity' parameter is used to adjust the minimum mean intensity of all pixel intensities within the nucleus.        
        
        Args:
            intensity (int) - the intensity value


<br />

#### 2.3 Nuclei chromatinization analysis parameters adjustment <a id="ncapa"></a>

##### 2.3.1 Set chromatinization 'size' parameter <a id="chsize"></a>

```
nf.set_chromatinization_size(size)
```

    This method sets 'size' parameter. The size is a parameter used for adjust minimal and maximal chromanitization spot area (px) within the nucleus.
        
        Args:
            size (tuple) - (min_value, max_value)

<br />


##### 2.3.2 Set chromatinization 'ratio' parameter <a id="chratio"></a>

```
nf.set_chromatinization_ratio(ratio)
```
    This method sets the 'ratio' parameter. In this case, the 'ratio' parameter is similar to 'circularity' as it describes the ratio between the maximum lengths in the x and y dimensions of the nucleus chromatinization.
        
        Args:
            ratio (float) - the ratio value

<br />

##### 2.3.3 Set chromatinization 'cut_point' parameter <a id="chcut"></a>

```
nf.set_chromatinization_cut_point(cut_point)
```

    This method sets the 'cut_point' parameter. The 'cut_point' parameter is a factor used to adjust the threshold for separating the background from chromatin spots.        
        
        Args:
            cut_point (int) - the cut_point value

<br />


#### 2.4 Nuclei image parameters adjustment <a id="nipa"></a>

##### 2.4.1 Set 'brightness' parameter <a id="brightness"></a>

```
nf.set_adj_image_brightness(brightness)
```

    This method sets 'brightness' parameter. The brightness is a parameter used for adjust brightness of the nucleus image.
        
        Args:
            brightness (float) - the brightness value

<br />


##### 2.4.2 Set 'gamma' parameter <a id="gamma"></a>

```
nf.set_adj_image_gamma(gamma)
```

    This method sets 'gamma' parameter. The gamma is a parameter used for adjust gamma of the nucleus image.
        
        Args:
            gamma (float) - the gamma value


<br />




##### 2.4.3 Set 'contrast' parameter <a id="contrast"></a>

```
nf.set_adj_image_contrast(contrast)
```

    This method sets 'contrast' parameter. The contrast is a parameter used for adjust contrast of the nucleus image.
        
        Args:
            contrast (float) - the contrast value


<br />

#### 2.5 Nuclei chromatinization image parameters adjustment <a id="ncipa"></a>


##### 2.5.1 Set chromatinization 'gamma' parameter <a id="cgamma"></a>

```
nf.set_adj_chrom_gamma(gamma)
```

    This method sets 'gamma' parameter. The gamma is a parameter used for adjust gamma of the nucleus chromatinization image.
        
        Args:
            gamma (float) - the gamma value


<br />



##### 2.5.2 Set chromatinization 'contrast' parameter <a id="ccontrast"></a>

```
nf.set_adj_chrom_contrast(contrast)
```


    This method sets 'contrast' parameter. The contrast is a parameter used for adjust contrast of the nucleus chromatinization image.
    
        Args:
            contrast (float) - the contrast value



<br />


##### 2.5.3 Set chromatinization 'brightness' parameter <a id="cbrightness"></a>

```
nf.set_adj_chrom_brightness(brightness)
```


     This method sets 'brightness' parameter. The brightness is a parameter used for adjust brightness of the nucleus chromatinization image.
        
        Args:
            brightness (float) - the brightness value
 


<br />



#### 2.6 Analysis methods <a id="am"></a>


##### 2.6.1 Input single image to analysis <a id="is"></a>

```
nf.input_image(img)
```


    This method adds the image to the class for nuclei and/or chromatinization analysis.
    
        Args:
            img (np.ndarray) - input image
    

<br />


##### 2.6.2 Primary parameters testing <a id="ppt"></a>

```
nf.nuclei_finder_test()
```

    This method performs testing analysis on the image provided by the input_image() method using the specified 'nms' and 'prob' parameters.

    To display the test results, run the browser_test() method.


```
nf.browser_test()
```

    This method performs test results provided by the `nuclei_finder_test()` method in the default browser.


    
    

<br />


##### 2.6.3 Find nuclei on image <a id="fni"></a>

```
nf.find_nuclei()
```

     This method performs analysis on the image provided by the input_image() method on default or set bu user parameters.
        
        To show current parameters run:
            - current_parameters_nuclei
            - current_parameters_img_adj
        
        To set new parameters run:
            
            - set_nms()
            - set_prob()
            - set_adj_image_gamma()
            - set_adj_image_contrast()
            - set_adj_image_brightness()


        To get analysis results run get_results_nuclei() method.


To return data use:


```
nf.get_results_nuclei()
```


    This function returns nuclei analysis results.
        
    
        Returns:
            neuclei_results (dict) - neuclei results in the dictionary format 
    
        
    

<br />


##### 2.6.4 Select 'True' nuclei on image <a id="st"></a>

```
nf.select_nuclei()
```

    This method selects data obtained from find_nuclei() based on the set threshold parameters.
    
        To show current parameters run:
            - current_parameters_nuclei
        
        To set new parameters run:
            
            - set_nuclei_circularity()
            - set_nuclei_yx_len_min_ratio()
            - set_nuclei_size()
            - set_nuclei_min_mean_intensity()
        


        To get analysis results run get_results_nuclei_selected() method.


To return data use:


```
nf.get_results_nuclei_selected()
```

    This function returns the results of the nuclei analysis following adjustments to the data selection thresholds.
        
    
        Returns:
            neuclei_results (dict) - neuclei results in the dictionary format 
    
    


<br />


##### 2.6.5 Find nuclei chromatinization on image <a id="fnc"></a>

```
nf.nuclei_chromatinization()
```

    This method performs finding chromatinization of nuclei on data obtained from find_nuclei() and/or select_nuclei()          
            
        To show current parameters run:
            - current_parameters_chromatinization
            - current_parameters_img_adj_chro 
        
        To set new parameters run:
            
            - set_chromatinization_size()
            - set_chromatinization_ratio()
            - set_chromatinization_cut_point()
            - set_adj_chrom_gamma()
            - set_adj_chrom_contrast()
            - set_adj_chrom_brightness()
      


        To get analysis results run get_results_nuclei_chromatinization() method.


To return data use:


```
nf.get_results_nuclei_chromatinization()
```

    This function returns the results of the nuclei chromatinization analysis.
        
    
        Returns:
            nuclei_chromatinization_results (dict) - nuclei chromatinization results in the dictionary format 
    

<br />

<br />





#### 2.7 Series analysis methods <a id="sam"></a>

##### 2.7.1 Find nuclei on image series <a id="fnis"></a>

```
nf.series_analysis_nuclei(path_to_images, 
                          file_extension = 'tiff', 
                          selected_id = [], 
                          fille_name_part = '', 
                          selection_opt = True, 
                          include_img = True, 
                          test_series = 0)
```

    This method performs analysis on the image provided by the input_image() method on default or set bu user parameters.
        
        To show current parameters run:
            - current_parameters_nuclei
            - current_parameters_img_adj
           
        
        To set new parameters run:
            
            - set_nms()
            - set_prob()
            - set_adj_image_gamma()
            - set_adj_image_contrast()
            - set_adj_image_brightness()
            - set_nuclei_circularity()
            - set_nuclei_yx_len_min_ratio()
            - set_nuclei_size()
            - set_nuclei_min_mean_intensity()
            
      
       Args:

            path_to_images (str) - path to the directory containing images for analysis
            file_extension (str) - extension of the image files. Default: 'tiff'
            selected_id (list) - list of IDs that must be part of the image name to distinguish them from others. Default: []
                If the list is empty, all images in the directory will be processed
            fille_name_part (str) - part of the file name to filter images. Default is an empty string
            selection_opt (bool) - decides if the select_nuclei() method with the defined parameters should be run. Default: True
            include_img (bool) - determines whether the images should be included in the result dictionary. Default: True
            test_series (int) - number of images to test the parameters and return results. Default: 0
                If set to 0, all images in the directory will be processed
        
        Returns:
        
            results_dict (dict) - dictionary containing results for each image in the directory. The dictionary keys are the image names.
               

<br />



##### 2.7.2 Find nuclei chromatinization on image series <a id="fncis"></a>

```
nf.series_analysis_chromatinization(path_to_images, 
                                    file_extension = 'tiff', 
                                    selected_id = [], 
                                    fille_name_part = '', 
                                    selection_opt = True, 
                                    include_img = True, 
                                    test_series = 0)
```

    This method performs analysis on the image provided by the input_image() method on default or set bu user parameters.
        
        To show current parameters run:
            - current_parameters_nuclei
            - current_parameters_img_adj
            - current_parameters_chromatinization
            - current_parameters_img_adj_chro 
        
        To set new parameters run:
            
            - set_nms()
            - set_prob()
            - set_adj_image_gamma()
            - set_adj_image_contrast()
            - set_adj_image_brightness()
            - set_nuclei_circularity()
            - set_nuclei_yx_len_min_ratio()
            - set_nuclei_size()
            - set_nuclei_min_mean_intensity()
            
            - set_chromatinization_size()
            - set_chromatinization_ratio()
            - set_chromatinization_cut_point()
            - set_adj_chrom_gamma()
            - set_adj_chrom_contrast()
            - set_adj_chrom_brightness()
      
       Parameters:

            path_to_images (str) - path to the directory containing images for analysis
            file_extension (str) - extension of the image files. Default: 'tiff'
            selected_id (list) - list of IDs that must be part of the image name to distinguish them from others. Default: []
                If the list is empty, all images in the directory will be processed
            fille_name_part (str) - part of the file name to filter images. Default is an empty string
            selection_opt (bool) - decides if the select_nuclei() method with the defined parameters should be run. Default: True
            include_img (bool) - determines whether the images should be included in the result dictionary. Default: True
            test_series (int) - number of images to test the parameters and return results. Default: 0
                If set to 0, all images in the directory will be processed
        
        Returns:
        
            results_dict (dict) - dictionary containing results for each image in the directory. The dictionary keys are the image names
               

<br />

### 3. NucleiDataManagement <a id="ndm"></a>

The NucleiDataManagement class dealing with data from NucleiFinder class.

```
from JIMG_analyst_tool.features_selection import NucleiDataManagement

# initiate class
ndm = NucleiDataManagement()
```

#### 3.1 Save experiment nuclei data  <a id="send"></a>


```
ndm.save_nuclei_results(path = os.getcwd(), data = {}, id_name = 'name')
```

    Saves nuclei results as images and JSON data with *.nuc extension.
    Results to save must be obtained from NucleiFinder class series_analysis_nuclei() or series_analysis_chromatinization() methods.
        
        Args:
            path (str) - the directory where results will be saved. Default is the current working directory
            data (dict) - the dictionary containing nuclei data or nuclei data and images
            id_name (str) - w string used for naming the result folder. Default is 'name'
        

<br />



#### 3.2 Concatenating different sets of experimental data <a id="cds"></a>


```
ndm.select_nuclei_data(path_to_results = os.getcwd(), data_sets = [])
```

    Loads and selects nuclei (nuclei parameters and / or chromatinization parameters) data from results files for each data set, processes it, and stores it in mutual_data.
        
        Args:
            path_to_results (str) - directory containing the results files. Default is the current working directory
            data_sets (list) - list of data set names to be selected. Default is an empty list


To return data use:
  

```
ndm.get_mutual_data()
```

    Retrieves the mutual data (returned from select_nuclei_data() method) stored in the object.
       
        Returns:
            mutual_data (DataFrame) - the mutual data

     

<br />




#### 3.3 Adding information to the nuclei data  <a id="aitn"></a>


```
ndm.concat_IS_results(nuclei_data, 
                      data_sets = [], 
                      IS_data_path = os.getcwd(), 
                      IS_features = [])
```

    Concatenates IS (Image Stream [https://cytekbio.com/pages/imagestream]) data with nuclei data and merges them based on object IDs.
        
        Args:
            nuclei_data (DataFrame) - the DataFrame containing nuclei data
            data_sets (list) - list of data sets to be used
            IS_data_path (str) - directory containing IS data files. Default is the current working directory
            IS_features (list) - list of features to be extracted from IS data. Default is an empty list
        

To return data use:
  

```
ndm.get_mutual_IS_data()
```

    Retrieves the mutual nuclei and IS data (returned from concat_IS_results() method) stored in the object.
        
        Returns:
            mutual_IS_data (DataFrame) - the mutual nuclei and IS data
            
     

<br />




#### 3.4 Preparing images for results visualization  <a id="pif"></a>


```
ndm.preapre_selected_img(path_to_images, 
                     file_extension = 'tiff', 
                     eq = True, 
                     clahe = True, 
                     kernal = (50,50), 
                     fille_name_part = '', 
                     selected_id = [], 
                     color = 'gray', 
                     max_intensity = 65535, 
                     min_intenisty = 0, 
                     brightness = 1000, 
                     contrast = 1.0, 
                     gamma = 1.0, 
                     img_n = 0)
```


    Prepares selected images for processing, applying histogram equalization and CLAHE, if required.
        
        Args:
            path_to_images (str) - path to the directory containing images
            file_extension (str) - the image file extension. Default is 'tiff'
            eq (bool) - whether to apply histogram equalization. Default is True
            clahe (bool) - whether to apply CLAHE. Default is True
            kernal (tuple) - kernel size for CLAHE. Default is (50, 50)
            fille_name_part (str) - part of the file name to filter images. Default is an empty string
            selected_id (list) - list of selected image IDs. Default is an empty list
            color (str) - color space to use. Default is 'gray'
            max_intensity (int) - maximum intensity for image adjustment. Default is 65535
            min_intenisty (int) - minimum intensity for image adjustment. Default is 0
            brightness (int) - brightness adjustment value. Default is 1000
            contrast (float) - contrast adjustment factor. Default is 1.0
            gamma (float) - gamma correction factor. Default is 1.0
            img_n (int) - number of images to process. Default is 0, which means all images
        
        Returns:
            self.images (dict) - a dictionary of processed
            
            To get the images use:
                - get_prepared_images() method
            
            To save the images use:
                - save_prepared_images() method


        

To return images use:
  

```
ndm.get_prepared_images()
```

    Retrieves the prepared images (returned from preapre_selected_img() method) stored in the object.
        
        Returns:
            images (dict) - a dictionary of prepared images
            
     


To save images use:
  

```
ndm.save_prepared_images(path_to_save = os.getcwd())
```

    Saves prepared images (returned from preapre_selected_img() method) to the specified directory.
        
        Args:
            path_to_save (str) - the directory path where the images will be saved. Default is the current working directory
            
     

<br />


### 4. GroupAnalysis <a id="ga"></a>

The GroupAnalysis class dealing with data from NucleiDataManagement class.

```
from JIMG_analyst_tool.features_selection import GroupAnalysis

# initiate class
ga = GroupAnalysis()
```

#### 4.1 Loading data from *.csv file  <a id="ldf"></a>


```
ga.load_data(path, ids_col = 'id_name', set_col = 'set')
```

    Load and preprocess data from a CSV file, storing both the data and metadata in the instance attributes.
     
        Args:
            path (str) - the file path to the CSV file containing the data to be loaded
            ids_col (str) - the name of the column in the CSV file that contains the unique identifiers for the objects. Ddefault: 'Object Number'
            set_col (str) - the name of the column in the CSV file that specifies the set or group each object belongs to.  Default: 'set'
         
        Returns:
            This method modifies the instance by loading data into the following attributes:
            - `self.input_data`: A pandas DataFrame containing the loaded and cleaned data, with the index set to the values in the `ids_col` column.
            - `self.tmp_data`: A copy of the input data, which can be used for temporary operations or further manipulation.
            - `self.input_metadata`: A pandas DataFrame containing the metadata, specifically the object IDs and set assignments, as defined by `ids_col` and `set_col`.
            - `self.tmp_metadata`: A copy of the metadata for temporary operations or further manipulation.
     
        

<br />



#### 4.2 Select features (columns) from data table for analysis  <a id="sffg"></a>


```
ga.select_data(features_list = [])
```

    Select specific features (columns) from the dataset and store them for further use.
      
        Args:
            features_list (list) - a list of feature names (column names) to select from the dataset. Default: [].
          
        Returns:
            
            This method modifies the `self.tmp_data` attribute to contain only the selected features from `self.input_data`.
      
        

<br />



#### 4.3 Data scale  <a id="ds"></a>


```
ga.data_scale(self)
```

    Select specific features (columns) from the dataset and store them for further use.
      
        Args:
            features_list (list) - a list of feature names (column names) to select from the dataset. Default: [].
          
        Returns:
            
            This method modifies the `self.tmp_data` attribute to contain only the selected features from `self.input_data`.
      
        

<br />


#### 4.4 Principal Component Analysis (PCA) <a id="nf"></a>


```
ga.PCA()
```

    Perform Principal Component Analysis (PCA) on the scaled data.
    
    This method applies PCA to reduce the dimensionality of the `self.scaled_data` while retaining the maximum variance possible.

        Returns:

            This method modifies the `self.PCA_results` attribute to contain the transformed data after applying PCA.
    

To return results:

```
ga.get_PCA()
```

    Retrieve the PCA results from the PCA() method.
      
        Returns:
            PCA_results (np.ndarray) - the PCA results stored in `self.PCA_results`
      
      

<br />


#### 4.5 Variance analysis of principal components  <a id="var"></a>


```
ga.var_plot()
```

    Plot the cumulative explained variance of the principal components from PCA.
    
    This method generates a plot showing the cumulative explained variance as a function of the number of principal components. The plot helps visualize how much variance is captured by each component and can assist in determining the optimal number of components.
    
        Returns:

            This method stores:
            - `self.var_data`: The explained variance ratio for each principal component
            - `self.knee_plot`: A matplotlib figure object representing the plot of cumulative explained variance
    

<br />

To return results:

```
ga.get_var_data()
```

    Retrieve the explained variance data of PCA from var_plot() method.
     
        Returns:
            var_data (np.ndarray) - the explained variance data stored in `self.var_data`
     
<br />


```
ga.get_knee_plot()
```

    Retrieve the knee plot of cumulative explained variance from the var_plot() method.
     
        Args:
            show (bool) - whether to display the knee plot. Default: True
     
        Returns:
            fig (matplotlib.figure.Figure) - the knee plot figure.
     

<br />


```
ga.save_knee_plot(path = os.getcwd(), name = '', extension = 'svg')
```

    Retrieve the knee plot of cumulative explained variance from the var_plot() method.
     
        Args:
            show (bool) - whether to display the knee plot. Default: True
     
        Returns:
            fig (matplotlib.figure.Figure) - the knee plot figure.
     
        
        
<br />






#### 4.6 Uniform Manifold Approximation and Projection (UMAP)  <a id="umap"></a>


```
ga.UMAP(PC_num = 5,
        factorize_with_metadata = True, 
        n_neighbors = 25,
        min_dist = 0.01,
        n_components = 2)
```

    Perform UMAP (Uniform Manifold Approximation and Projection) dimensionality reduction on the PCA results.
    
    This method applies UMAP to the top principal components from PCA and generates a 2D or 3D scatter plot for visualization. Optionally, UMAP can use metadata labels to influence the layout of the projection.
    
        Args:
            PC_num (int) - the number of top principal components from the PCA results to use in the UMAP embedding. Default: 5
            factorize_with_metadata (bool) - whether to use metadata (such as 'sets') to factorize the UMAP embedding. Default: True
                If True, the 'sets' column from the metadata is factorized and used as labels during the UMAP transformation.
            n_neighbors (int) - the number of neighbors used in UMAP to compute the local structure. Default: 25
            min_dist (float)  - the minimum distance between points in the low-dimensional space. Default: 0.01
            n_components (int) - the number of dimensions for the UMAP embedding. Typically set to 2 for visualization. Default: 2
        
        Returns:
       
            This method stores:
            - `self.UMAP_data`: The UMAP-transformed data (embedding).
            - `self.UMAP_plot['PrimaryUMAP']`: A Plotly scatter plot showing the UMAP embedding, colored by metadata 'sets'.
    
        
<br />


To return results:

```
ga.get_UMAP_data()
```

    Retrieve the UMAP-transformed data from UMAP() method.

        Returns:
            UMAP_data (np.ndarray) - the UMAP data stored in `self.UMAP_data`
         
     
<br />


```
ga.get_UMAP_plots(show = True)
```

    Retrieve the UMAP plots from UMAP() and/or UMAP_on_clusters() methods.
     
        Args:
            show (bool) - whether to display the UMAP plots. Default: True
     
        Returns:
            figs (dict of matplotlib.figure.Figure) - a dictionary of UMAP plots
     

<br />


```
ga.save_UMAP_plots(path = os.getcwd(), name = '', extension = 'svg')
```

     Save the UMAP plots to a specified directory from UMAP() and / or UMAP_on_clusters() methods.
     
        Args:
            path (str) - the directory path where plots will be saved. Default: current working directory
            name (str) - the base name for the saved plot files. Default: ''
            extension (str) - the file extension for the saved plots. Default: 'svg'
     
        Returns:
        
            Saves UMAP plots to the specified path with the given name and extension.
     
        
<br />





#### 4.7 Clustering of dimensionality reduced data (dbscan)  <a id="dbscan"></a>


```
ga.db_scan(eps = 0.5, min_samples = 10)
```

    Perform DBSCAN clustering on the UMAP-transformed data.
     
    This method applies DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to identify clusters in the UMAP embedding.
     
        Args:
            eps (float/int) - the maximum distance between two points for one to be considered as in the neighborhood of the other. Default: 0.5
            min_samples (int) - the minimum number of points required to form a dense region. Default: 10
         
        Returns:
  
            This method stores the cluster labels:
            - `self.dblabels`: A list of cluster labels assigned by DBSCAN, with each label converted to a string.
     
     
        
<br />



#### 4.8 Clusters / UMAP visualization  <a id="cu"></a>


```
ga.UMAP_on_clusters(min_entities = 50)
```

    Generate UMAP visualizations based on clusters with a minimum entity threshold.

    This method refines UMAP visualizations by filtering clusters based on the minimum number of entities and applies additional metadata. Two UMAP plots are created: one with clusters only and another combining clusters with set identifiers.
    
        Args:
            min_entities (int) - the minimum number of entities required for a cluster to be included in the visualization. Default: 50
        
        Returns
    
            This method modifies:
            - `self.UMAP_plot['ClusterUMAP']`: A Plotly scatter plot of UMAP embedding with clusters (dbscan) that meet the minimum entity threshold.
            - `self.UMAP_plot['ClusterXSetsUMAP']`: A Plotly scatter plot of UMAP embedding with clusters and set identifiers.
            - `self.tmp_data`: The filtered data based on the selected clusters and sets.
            - `self.tmp_metadata`: The metadata associated with the filtered data.
    

To return results:


```
ga.get_UMAP_plots(show = True)
```

    Retrieve the UMAP plots from UMAP() and/or UMAP_on_clusters() methods.
     
        Args:
            show (bool) - whether to display the UMAP plots. Default: True
     
        Returns:
            figs (dict of matplotlib.figure.Figure) - a dictionary of UMAP plots
     

<br />


```
ga.save_UMAP_plots(path = os.getcwd(), name = '', extension = 'svg')
```

     Save the UMAP plots to a specified directory from UMAP() and / or UMAP_on_clusters() methods.
     
        Args:
            path (str) - the directory path where plots will be saved. Default: current working directory
            name (str) - the base name for the saved plot files. Default: ''
            extension (str) - the file extension for the saved plots. Default: 'svg'
     
        Returns:
        
            Saves UMAP plots to the specified path with the given name and extension.
     
        
<br />





#### 4.9 Return complete metadata  <a id="rcm"></a>


```
ga.full_info()
```

    Merge data with metadata if metadata contains a 'full_id' column.
    
    This method combines `tmp_data` and `tmp_metadata` into a single DataFrame for comprehensive information if the metadata includes the 'full_id' column. If 'full_id' is not found, the method suggests completing the necessary preprocessing pipeline.
      
        Returns:
            merged_df (pd.DataFrame) - returns a merged DataFrame with both data and metadata
      
       
    
     
        
<br />


#### 4.10 Differential Feature Analysis (DFA) <a id="dfa"></a>


```
ga.groups
```

    Returns information about available groups in the metadata for self DFA.

           Returns:
               dict: A dictionary where each key is a column name, and each value is a list of available groups in that column.
        


```
ga.DFA(meta_group_by = 'sets', sets = {}, n_proc = 5)
```

    Perform Differential Feature Analysis (DFA) on specified data groups.
      
    This method conducts DFA using a grouping factor from metadata and a dictionary of sets for comparison. It allows for the identification of significant differences across defined sets.
    
        Args:
            meta_group_by (str) - the metadata column to use for grouping in the analysis. Default: 'sets'
                    To check the available analysis groups in metadata, use 'self.groups'  

            sets (dict) - a dictionary specifying the sets for comparison, where keys are group names, and values are lists of associated labels.
                Example:
                    `sets = {'healthy': ['21q'], 'disease': ['71q', '77q', '109q']}`
                
                    In this case, the healthy group is compared to the disease groups.

            n_proc : int, optional
                The number of processing cores to use for parallel computation (default is 5).
      
        Returns:

            results (pd.DataFrame) - the result of the analysis containing:
                - p_val: p-value calculated using the Mann-Whitney U test to assess statistical difference between the target and control groups.
                 
                - adj_pval: adjusted p-value to correct for multiple comparisons using the Bonferroni correction, capped at a maximum value of 1.
        
                - -log(p_val): negative base-10 logarithm of the p-value, providing a clearer visualization for small p-values.
               
                - pct_valid: percentage of cases in the target group where the given feature value is greater than zero.
               
                - pct_ctrl: percentage of cases in the control group where the given feature value is greater than zero.
               
                - avg_valid: mean value of the feature within the target group.
               
                - avg_ctrl: mean value of the feature within the control group.
               
                - feature: name of the feature being analyzed in each iteration.
               
                - FC: Fold Change calculated as the ratio of the mean feature value in the target group to the mean feature value in the control group, with a small adjustment factor (low_factor) to avoid division by zero.
               
                - log(FC): base-2 logarithm of the Fold Change, aiding interpretation of changes between groups.
               
                - norm_diff: normalized difference between the mean feature values of the target and control groups.
               
                - valid_group: name of the group assigned as 'target' in the analysis (e.g., healthy or disease group depending on input data).
      
        
    
     
        
<br />

<br />


### 5. FeatureIntensity <a id="fi"></a>

The FeaureIntensity class contains all methods from the ImageTools class, as it inherits from ImageTools.

```
from JIMG_analyst_tool.features_selection import FeaureIntensity

# initiate class
fi = FeaureIntensity()
```

<br />

#### 5.1 Check and adjust primary metadata <a id="caap"></a>

##### 5.1.1 Parameters for intensity analysis <a id="pfia"></a>

<br />

```
fi.current_metadata
```
    @ property
     This property returns current metadata parameters.
        
    
        Returns:
            projection_type (str) - type of data projection, if 3D-image
            correction_factor (str) - correction factor for backgroud separation during pixels intensity normalization
                The formula applied for each target_mask_pixel is:
                
                    Result_{i,j} = T_{i,j} - (mean(B) * (1 + c))
                
                Where:
                * Result_{i,j} – the result value for each pixel (i,j) in the target mask
                * T_{i,j} – intensity value of pixel (i,j) in the target mask
                * mean(B) – the mean intensity of the pixels in the normalization_mask
                * c – correction factor

            scale (str) - scale loaded using the load_JIMG_project_() method or set by the set_scale() method
            stack_selection (list) - list of partial z-axis images from the full 3D-image to exclude from the projection
        

<br />

##### 5.1.2 Set projection type. If input image is *.tiff file (3D-image) <a id="3dl"></a>

<br />

```
fi.set_projection(projection)
```
    This method sets 'projection' parameter. The projection is a parameter used for 3D-image projection to 1D-image.
       
        Args:
           projection (str) - the projection value ['avg', 'median', 'std', 'var', 'max', 'min']. Default: 'avg'
 

<br />


##### 5.1.3 Set correction factor <a id="scf"></a>

<br />

```
fi.set_correction_factorn(factor)
```

    This method sets 'correction_factor' parameter. 
    The correction_factor is a parameter used for backgroud separation during pixels intensity normalization
    
    The formula applied for each target_mask_pixel is:
    
        Result_{i,j} = T_{i,j} - (mean(B) * (1 + c))
        
        Where:
        * Result_{i,j} – the result value for each pixel (i,j) in the target mask
        * T_{i,j} – intensity value of pixel (i,j) in the target mask
        * mean(B) – the mean intensity of the pixels in the normalization_mask
        * c – correction factor

       
        Args:
           factor (float) - the correction_factor value [factor < 1 and factor > 0]. Default: 0.1
 
 


<br />


##### 5.1.4 Set image scale <a id="sis"></a>

<br />

```
fi.set_scale(scale)
```

    This method sets the 'scale' parameter. The scale is used to calculate the actual size of the tissue or organ.
    
    The scale is also loaded using the load_JIMG_project_() method.
        
        
        Args:
           scale (float) - the scale value [um/px]
 
 
<br />


##### 5.1.5 Select images along the z-axis for analysis <a id="zas"></a>

<br />

```
fi.set_selection_list(rm_list)
```

    This method sets the 'rm_list' parameter. The 'rm_list' is used to exclude partial z-axis images from the full 3D image in the projection.

        Args:
           rm_list (list) - list of images to remove.
 

<br />

<br />


#### 5.2 Input data loading <a id="idl"></a>

##### 5.2.1 Loading JIMG project <a id="ljp"></a>

If required or exist.
[JIMG](https://github.com/jkubis96/JIMG) - source and description


```
fi.load_JIMG_project_(path)
```

    This method loads a JIMG project. The project file must have the *.pjm extension.
        
        Args:
            file_path (str) - path to the project file.
    
        Returns:
            project (class) - loaded project object
    
        Raises:
            ValueError: If the file does not have a *.pjm extension.
        
 

<br />


##### 5.2.2 Loading image <a id="li"></a>


```
fi.load_image_3D(path)
```

    This method loads an 3D-image (*.tiff) into the class.

        Args:
            path (str) - path to the *.tiff image.
        
 
 <br />

OR

<br />

```
fi.load_image_(path)
```

    This method loads an image into the class.

        Args:
            path (str) - path to the image.
        
 
<br />


##### 5.2.3 Loading mask(s) for input image <a id="lmii"></a>


```
fi.load_mask_(path)
```

    This method loads an image mask into the class. The mask can be in different formats, such as 16-bit or 8-bit, with extensions like *.png and *.jpeg, but it must be in binary format (e.g., 0/2**16-1, 0/255, 0/1, etc.). 
    
    If the `load_normalization_mask_()` method is not used, the mask from the `load_mask_()` method is set as the normalization mask. 
    The mean pixel intensity from the area of the reversed normalization mask (where reversed binary == 0 becomes 1 and values greater than 0 become 0) is used for normalization.
        
        The formula applied for each target_mask_pixel is:
        
            Result_{i,j} = T_{i,j} - (mean(B) * (1 + c))
        
            Where:
            * Result_{i,j} – the result value for each pixel (i,j) in the target mask
            * T_{i,j} – intensity value of pixel (i,j) in the target mask
            * mean(B) – the mean intensity of the pixels in the normalization_mask
            * c – correction factor

        Args:
            path (str) - path to the mask image



<br />

```
fi.load_normalization_mask_(path)
```

    This method loads an image mask for normalization into the class. The mask can be in different formats, such as 16-bit or 8-bit, with extensions like *.png and *.jpeg, but it must be in binary format (e.g., 0/2**16-1, 0/255, 0/1, etc.). 
    
    The mean pixel intensity from the area of the reversed normalization mask (where reversed binary == 0 becomes 1 and values greater than 0 become 0) is used for normalization.
    The user defines the mask by drawing the area of interest (tisse, part of tissue, organ, ...), and normalization will be applied to the area that is the inverse of the defined area.
        
        The formula applied for each target_mask_pixel is:
        
            Result_{i,j} = T_{i,j} - (mean(B) * (1 + c))
        
            Where:
            * Result_{i,j} – the result value for each pixel (i,j) in the target mask
            * T_{i,j} – intensity value of pixel (i,j) in the target mask
            * mean(B) – the mean intensity of the pixels in the normalization_mask
            * c – correction factor

        Args:
            path (str) - path to the mask image
 

<br />



#### 5.3 Intensity features selection <a id="ifs"></a>

##### 5.3.1 Run analysis <a id="raa"></a>


```
fi.run_calculations()
```

    This method performs analysis on the image provided by the `load_image_()` method, using either default parameters or parameters set by the user, along with masks loaded by the `load_mask_()` and/or `load_normalization_mask_()` methods.

        To display the current parameters, run:
        - current_metadata
        
        To set new parameters, run:
        - set_projection()
        - set_correction_factor()
        - set_scale() - cannot be defined
        - set_selection_list() - cannot be defined
        - load_JIMG_project_() - cannot be defined
        
        Returns:
            
            For results, use the `get_results()` method.
 

<br />


##### 5.3.2 Get analysis results <a id="gaa"></a>


```
fi.get_results()
```

    This method returns the results from the `run_calculations()` method in dictionary format.

        Returns:
        
            results_dict (dict) - dictionary containing results from run_calculations()
               

<br />


##### 5.3.3 Save analysis results <a id="saa"></a>


```
fi.save_results(path = os.getcwd(), 
                mask_region = '', 
                feature_name = '', 
                individual_number = 0, 
                individual_name = '')
```

    This method saves the results from the `run_calculations()` method in dictionary format to a *.json file.
      
        Args:
        
            path (str) - path to the directory for saving the file. If not provided, the current working directory is used
            mask_region (str) - name or identifier of the mask region (e.g., tissue, part of tissue, etc.)
            feature_name (str) - name of the feature being analyzed. It is also processed to replace any underscores or spaces with periods
            individual_number (int) - unique number or identifier for the individual in the analysis (e.g., 1, 2, 3)
            individual_name (str) - name of the individual (e.g., species name, tissue, organoid, etc.) 

      
        The method checks if valid values for `mask_region`, `feature_name`, `individual_number`, and `individual_name` are provided. 
        If so, and the results (`normalized_image_values` and `size_info`) from `run_calculations()` exist, it saves them as a dictionary 
        in a `.int` file (JSON format) in the specified directory. If the directory does not exist, it is created.
      
        If the analysis has not been conducted or the provided parameters are incorrect, an error message is printed.
      
        File name format:
            '<individual_name>_<individual_number>_<mask_region>_<feature_name>.int'
      
        Raises:
            FileNotFoundError: If the path cannot be created or accessed.
            ValueError: If any of 'mask_region', 'feature_name', 'individual_number', or 'individual_name' is missing or invalid.
      
               

<br />


##### 5.3.4 Concatenation particular analysis results <a id="cpar"></a>


```
fi.concatenate_intensity_data( directory = os.getcwd(), name = '')
```

    This method processes and concatenates intensity data from multiple `.int` files in a specified directory. 
    It groups the data by gene (feature) and mask region, and then saves the concatenated results as CSV files.
     
        Args:
        
            directory (str) - path to the directory containing the `.int` files. If not provided, the current working directory is used
            name (str): Prefix for the output CSV file names. The final CSV files will be saved in the format '<name>_<gene>_<region>.csv'
        
     
        
        Raises:
            FileNotFoundError: If the directory cannot be accessed or no `.int` files are found.
            ValueError: If the `.int` file format is incorrect or missing expected data.
     
        Output:
            One CSV file per unique gene-region combination, saved in the specified directory.
            
               

<br />




### 6. IntensityAnalysis <a id="iaa"></a>

The IntensityAnalysis class dealing with data from FeatureIntensity class.


```
from JIMG_analyst_tool.features_selection import IntensityAnalysis

# initiate class
ia = IntensityAnalysis()
```

<br />

#### 6.1 Data preparing <a id="dp"></a>

##### 6.1.1 Drop outlires <a id="do"></a>

<br />

```
ia.drop_up_df(data, group_col, values_col)
```

    Removes upper outliers from the DataFrame based on the specified value column and grouping column.
    
    Outliers are calculated and removed separately for each group defined by the grouping column.
   
        Args:
            data (pd.DataFrame) - the input DataFrame
            group_col (str) - the name of the column used for grouping
            values_col (str) - the column containing the values from which upper outliers will be removed
     
        Returns:
            filtered_data (pd.DataFrame) - a filtered DataFrame with the upper outliers removed
            

<br />


##### 6.1.2 Percentiles ranges calculations <a id="prc"></a>

<br />

```
ia.percentiles_calculation(values, sep_perc = 1)
```

    Calculates percentiles for a given set of values with a specified separation interval. 

    This function computes percentiles from 0 to 100, at intervals defined by the `sep_perc` parameter.
    Additionally, it creates a loopable list of percentile ranges, useful for further data analysis or binning.
     
        Args:
            values (array-like) - the input data values for which the percentiles are calculated
            sep_perc (int) - the separation between percentiles (default is 1, meaning percentiles are calculated at every 1%)
     
        Returns:
            percentiles (np.ndarray) - nn array of calculated percentile values
            percentiles_loop (list of tuples) - a list of tuples representing consecutive percentile ranges (e.g., [(0, 1), (1, 2), ...])
        
            

<br />



##### 6.1.3 Percentiles calculations <a id="raa"></a>

<br />

```
ia.to_percentil(values, percentiles, percentiles_loop)
```

    Aggregates statistics for a given set of values based on calculated percentile ranges.
 
    This function calculates summary statistics (e.g., count, average, median, standard deviation, and variance) for each percentile range 
    in `percentiles_loop`. The results are based on the percentiles calculated in the `percentiles_calculation()` method.
     
        Args:
            values [array-like] - the input data values for which the statistics are calculated
            percentiles [np.ndarray] - the array of percentile values used to define the ranges
            percentiles_loop [list of tuples] - a list of tuples representing consecutive percentile ranges (e.g., [(0, 1), (1, 2), ...])
     
        Returns:
            data (dict) - a dictionary containing the following keys:
                - 'n' (list): The number of elements in each percentile range
                - 'n_standarized' (list): The proportion of elements in each percentile range relative to the total number of elements
                - 'avg' (list): The average value of elements within each percentile range
                - 'median' (list): The median value of elements within each percentile range
                - 'std' (list): The standard deviation of elements within each percentile range
                - 'var' (list): The variance of elements within each percentile range
        
    
<br />

```
ia.df_to_percentiles(data, group_col, values_col, sep_perc = 1, drop_outlires = True)
```

    Calculates summary statistics based on percentile ranges for each group in a DataFrame.
     
    This method groups the data by the specified `group_col`, calculates percentile ranges for each group's values in the `values_col`, and
    computes summary statistics (e.g., count, average, median, standard deviation, and variance) for each percentile range.
    Optionally, it can drop upper outliers from the data before performing the calculations.
     
        Args:
            data (pd.DataFrame) - the input DataFrame containing the data
            group_col (str) - the name of the column used for grouping the data
            values_col (str) - the name of the column containing the values for which percentiles are calculated.
            sep_perc (int) - the separation interval for percentiles (default is 1, meaning percentiles are calculated at every 1%)
            drop_outlires (bool) - whether to remove upper outliers from the data before performing calculations (default is True)
     
        Returns:
            full_data (dict) - a dictionary where each key is a group name (from `group_col`), and the value is another dictionary containing:
                - 'n' (list): The number of elements in each percentile range
                - 'n_standarized' (list): The proportion of elements in each percentile range relative to the total number of elements
                - 'avg' (list): The average value of elements within each percentile range
                - 'median' (list): The median value of elements within each percentile range
                - 'std' (list): The standard deviation of elements within each percentile range
                - 'var' (list): The variance of elements within each percentile range
                
            
            

<br />


#### 6.2 Statistics <a id="sta"></a>

##### 6.2.1 ANOVA <a id="staa"></a>

<br />

```
ia.aov_percentiles(data, testes_col, comb = '*')
```

    Performs a Welch's ANOVA on percentile-based group data.
        
    This method calculates group values by combining the columns specified in `testes_col` according to the operation defined in `comb`. 
    It then performs a Welch's ANOVA to test for differences in means between the groups. Welch's ANOVA is suitable when the groups have 
    unequal variances.
    
        Args:
            data (dict of pd.DataFrame) - a dictionary where keys are group names and values are DataFrames containing the data.
            testes_col (str or list of str) - column name(s) from which the group values are derived. If a list is provided, columns will be 
            combined based on the `comb` operation.
            comb (str) - the operation used to combine multiple columns if `testes_col` is a list. Options include:
                '*' (multiplication), 
                '+' (addition), 
                '**' (exponentiation), 
                '-' (subtraction),
                '/' (division),
                Default is '*'
        
        Returns:
            F (float) - the F-statistic from Welch's ANOVA.
            p-val (float) - the uncorrected p-value from Welch's ANOVA, testing for significant differences between groups.
        
        Notes:
            - If `testes_col` is a single string, no combination is performed, and the group values are taken directly from that column.
            - Welch's ANOVA is used as it accounts for unequal variances between groups.
            - The `df.melt()` method is used to reshape the data, allowing the ANOVA to be applied to all groups.
        
        Example Usage:
            welch_F, welch_p = self.aov_percentiles(data, testes_col=['col1', 'col2'], comb='+')
            print(f"Welch's ANOVA F-statistic: {welch_F}, p-value: {welch_p}")
            
            

<br />


##### 6.2.2 ANOVA + posthoc <a id="anpo"></a>

<br />

```
ia.post_aov_percentiles(data, testes_col, comb = '*')
```

     Performs a Welch's ANOVA on percentile-based group data and pairwise comparisons Welch's T-test.
        
        Args:
            data (dict of pd.DataFrame) - dictionary where keys are group names and values are DataFrames containing the data
            testes_col (str or list of str) - column name(s) from which the group values are derived
                If a list is provided, columns will be combined based on the `comb` operation
            comb (str) - operation used to combine multiple columns if `testes_col` is a list. Options include:
                '*' (multiplication), 
                '+' (addition), 
                '**' (exponentiation), 
                '-' (subtraction), 
                '/' (division).
                Default is '*'
        
        Returns:
            p_val (float) - the uncorrected p-value from Welch's ANOVA
            final_results (dict) - results of pairwise t-tests with keys:
                'group1', 'group2', 'stat', 'p_val', 'adj_p_val'
            
            

<br />


##### 6.2.3 Chi² <a id="chi"></a>

<br />

```
ia.chi2_percentiles(input_hist)
```

     Performs a Chi-squared test on percentile-based group data.
    
        This method takes input histogram data, reformats it into a contingency table, 
        and then performs a Chi-squared test to evaluate whether there is a significant 
        association between the groups.
    
        Args:
            input_hist (dict of pd.DataFrame) - a dictionary where keys are group names and 
                values are DataFrames containing histogram data. 
                The histogram data should include a column 'n' that contains counts 
                for each percentile/bin.
    
        Returns:
            chi2_statistic (float) - the test statistic from the Chi-squared test
            p_value (float) - the p-value from the Chi-squared test
            dof (int) - degrees of freedom for the test
            expected (np.ndarray) - the expected frequencies for each group/bin under the null hypothesis
            chi_data (dict) - the formatted data used in the Chi-squared test
    
        Example Usage:
            chi2_stat, p_val, dof, expected, chi_data = self.chi2_percentiles(input_hist)
            print(f"Chi-squared statistic: {chi2_stat}, p-value: {p_val}")
            
            

<br />


##### 6.2.4 Chi² + posthoc <a id="chipo"></a>

<br />

```
ia.post_ch2_percentiles(input_hist)
```

    Performs a Chi-squared test on percentile-based group data, including pairwise comparisons.
      
    This method first performs a Chi-squared test on the input histogram data across all groups to 
    check for a significant association. Then, it performs pairwise Chi-squared tests between 
    groups to identify specific group differences. Multiple comparisons are corrected using 
    the Bonferroni method.
      
        Args:
            input_hist (dict of pd.DataFrame) - a dictionary where keys are group names and 
                values are DataFrames containing histogram data. The histogram data should include 
                a column 'n' that contains counts for each percentile/bin
      
        Returns:
            p_val (float) - the overall p-value from the initial Chi-squared test across all groups
            final_results (dict) - a dictionary containing the results of pairwise Chi-squared tests with keys:
                - 'group1' (list): The name of the first group in each comparison
                - 'group2' (list): The name of the second group in each comparison
                - 'chi2' (list): The Chi-squared statistic for each pairwise comparison
                - 'p_val' (list): The p-value for each pairwise comparison
                - 'adj_p_val' (list): The adjusted p-value (Bonferroni correction) for multiple comparisons
      
        Example Usage:
            p_val, final_results = self.post_ch2_percentiles(input_hist)
            print(f"Overall Chi-squared p-value: {p_val}")
            for i in range(len(final_results['group1'])):
                print(f"Comparison: {final_results['group1'][i]} vs {final_results['group2'][i]}")
                print(f"Chi2 stat: {final_results['chi2'][i]}, p-value: {final_results['p_val'][i]}, adj. p-value: {final_results['adj_p_val'][i]}")
        

<br />


#### 6.3 Visualization <a id="vis"></a>

<br />


```
ia.hist_compare_plot(data, queue, tested_value, p_adj = True, txt_size = 20)
```

    Generates comparative histograms and displays results of statistical tests (ANOVA and Chi-squared).
    
    This method performs transformations on the input data, generates comparative histograms for
    each group, and displays statistical test results, including Welch's ANOVA and Chi-squared tests. 
    It includes options for multiple comparison corrections using the Bonferroni method.
        
        Args:
            data (dict of pd.DataFrame) - a dictionary where keys are group names and values are DataFrames 
                containing histogram data. The data should include the column for the tested variable
            queue (list) - a list defining the order of groups to be plotted
            tested_value (str) - the column name in `data` representing the variable to test and visualize
            p_adj (bool) - if True, applies Bonferroni correction for multiple comparisons. Default: True
            txt_size (int) - font size for text annotations in the plot. Default: 20
        
        Returns:
            fig (matplotlib.figure.Figure) - a Matplotlib figure object containing the generated histograms 
                and statistical test results
        
        Example Usage:
            fig = self.hist_compare_plot(data, queue=['group1', 'group2', 'group3'], tested_value='n', p_adj=True, txt_size=18)
            plt.show()
        
        

<br />




### 7. Example pipelines <a id="epip"></a>

If you want to run the examples, you must download the test data. To do this, use:

```
from JIMG_analyst_tool.features_selection import test_data

test_data()
```


<br />

#### 7.1 Nuclei analysis - confocal microscopy <a id="nacm"></a>

```
from JIMG_analyst_tool.features_selection import NucleiFinder


# initiate class
nf = NucleiFinder()


image = nf.load_image('test_data/microscope_nuclei/r01c02f90p20-ch1sk1fk1fl1.tiff')


nf.input_image(image)


# Check the basic parameters
nf.current_parameters_nuclei


# Test nms & prob parmeters for nuclei segmentation
nf.nuclei_finder_test()

nf.browser_test()
```

<br/>

[Browse Raport](https://htmlpreview.github.io/?https://raw.githubusercontent.com/jkubis96/JIMG-analyst-tool/refs/heads/main/examples/Microscope_nuclei/nms_prob_test.html)

<br/>

```
# If required, change parameters
nf.set_nms(nms = 0.9)

nf.set_prob(prob = 0.5)


# Analysis

# 1. First step on nuclei analysis
nf.find_nuclei()


# Parameters for micrsocope image adjustment 
nf.current_parameters_img_adj
```

<br/>

##### Image with 'Default' parameters:
<p align="center">
<img  src="examples/Microscope_nuclei/find_nuclei_before.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# If image required changes, change parameters and run again (nf.find_nuclei())
nf.set_adj_image_brightness(brightness = 1000)

nf.set_adj_image_gamma(gamma = 1.2)

nf.set_adj_image_contrast(contrast = 2)


# Check if parameters has changed
nf.current_parameters_nuclei


# Second execution with new parameters for image adjustment
nf.find_nuclei()
```
<br/>

##### Image with adjusted parameters:

<p align="center">
<img  src="examples/Microscope_nuclei/find_nuclei_after.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# Return results
nuclei_results, analysed_img = nf.get_results_nuclei()
```
<br/>

##### Dictionary with nuclei results:

<p align="center">
<img  src="examples/Microscope_nuclei/dict_nuclei.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# 2. Second step of analysis (selection)
nf.select_nuclei()
```
<br/>

##### Image with 'Default' selection parameters:

<p align="center">
<img  src="examples/Microscope_nuclei/select_nuclei_before.bmp" alt="drawing" width="600" />
</p>

<br/>

```
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
```
<br/>

##### Image with adjusted selection parameters:

<p align="center">
<img  src="examples/Microscope_nuclei/select_nuclei_after.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# Return results
nuclei_selected_results, analysed_selected_img = nf.get_results_nuclei_selected()
```
<br/>

##### Dictionary with nuclei results:

<p align="center">
<img  src="examples/Microscope_nuclei/dict_nuclei.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# 3. third step (chromatinization alaysis)
nf.nuclei_chromatinization()
```
<br/>

##### Image with 'Default' chromatinization parameters:

<p align="center">
<img  src="examples/Microscope_nuclei/nuclei_chromatinization_before.bmp" alt="drawing" width="600" />
</p>

<br/>

```
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
```
<br/>

##### Image with adjusted chromatinization parameters:

<p align="center">
<img  src="examples/Microscope_nuclei/nuclei_chromatinization_after.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# Return results
chromatinization_results, analysed_chromatinization_img = nf.get_results_nuclei_chromatinization()
```
<br/>

##### Dictionary with nuclei chromatinization results:

<p align="center">
<img  src="examples/Microscope_nuclei/dict_chrom.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# If your parameters are correct for your data, you can run series analysis on more images

# Nuclei 

series_results_nuclei = nf.series_analysis_nuclei(path_to_images = 'test_data/microscope_nuclei', 
                                                  file_extension = 'tiff', 
                                                  selected_id = [], 
                                                  fille_name_part = 'ch1',
                                                  selection_opt = True, 
                                                  include_img = False, 
                                                  test_series = 0)

```
<br/>

##### Dictionary with series nuclei results:

<p align="center">
<img  src="examples/Microscope_nuclei/series.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# save results

import os
from JIMG_analyst_tool.features_selection import NucleiDataManagement

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

```
<br/>

##### Dictionary with series nuclei chromatinization results:

<p align="center">
<img  src="examples/Microscope_nuclei/series_chrom.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# save results
ndm = NucleiDataManagement()

ndm.save_nuclei_results(path = os.getcwd(), data = series_results_chromatinization, id_name = 'example_chromatinization')



###############################################################################

# Nuclei data selection, experiments concatenation and DataFrame creation


ndm = NucleiDataManagement()

ndm.select_nuclei_data(path_to_results = os.getcwd(), 
                       data_sets = ['example_chromatinization'])



data = ndm.get_mutual_data()

```
<br/>

##### Data table with series nuclei chromatinization results:

<p align="center">
<img  src="examples/Microscope_nuclei/data_table_results.bmp" alt="drawing" width="700" />
</p>




<br />

<br />

#### 7.2 Nuclei analysis - flow cytometry <a id="nafc"></a>

```

from JIMG_analyst_tool.features_selection import NucleiFinder


# initiate class
nf = NucleiFinder()


image = nf.load_image('test_data/flow_cytometry/ctrl/3087_Ch7.ome.tif')


nf.input_image(image)


# Check the basic parameters
nf.current_parameters_nuclei


# Test nms & prob parmeters for nuclei segmentation
nf.nuclei_finder_test()

nf.browser_test()
```

<br/>

[Browse Raport](https://htmlpreview.github.io/?https://raw.githubusercontent.com/jkubis96/JIMG-analyst-tool/refs/heads/main/examples/FlowCytometry_nuclei/nms_prob_test.html)

<br/>

```
# If required, change parameters
nf.set_nms(nms = 0.6)

nf.set_prob(prob = 0.3)


# Analysis

# 1. First step on nuclei analysis
nf.find_nuclei()
```

<br/>

##### Image with 'Default' parameters:
<p align="center">
<img  src="examples/FlowCytometry_nuclei/find_nuclei_before.bmp" alt="drawing" width="500" />
</p>

<br/>

```
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
```
<br/>

##### Image with adjusted parameters:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/find_nuclei_after.bmp" alt="drawing" width="500" />
</p>

<br/>

```
# Return results
nuclei_results, analysed_img = nf.get_results_nuclei()
```
<br/>

##### Dictionary with nuclei results:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/dict_nuclei.bmp" alt="drawing" width="400" />
</p>

<br/>

```
# 2. Second step of analysis (selection)
nf.select_nuclei()
```
<br/>

##### Image with 'Default' selection parameters:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/select_nuclei_before.bmp" alt="drawing" width="500" />
</p>

<br/>

```
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
```
<br/>

##### Image with adjusted selection parameters:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/select_nuclei_after.bmp" alt="drawing" width="500" />
</p>

<br/>

```
# Return results
nuclei_selected_results, analysed_selected_img = nf.get_results_nuclei_selected()
```
<br/>

##### Dictionary with nuclei results:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/dict_nuclei.bmp" alt="drawing" width="400" />
</p>

<br/>

```
# 3. third step (chromatinization alaysis)
nf.nuclei_chromatinization()
```
<br/>

##### Image with 'Default' chromatinization parameters:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/nuclei_chromatinization_before.bmp" alt="drawing" width="500" />
</p>

<br/>

```
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
```
<br/>

##### Image with adjusted chromatinization parameters:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/nuclei_chromatinization_after.bmp" alt="drawing" width="500" />
</p>

<br/>

```
# Return results
chromatinization_results, analysed_chromatinization_img = nf.get_results_nuclei_chromatinization()
```
<br/>

##### Dictionary with nuclei chromatinization results:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/dict_chrom.bmp" alt="drawing" width="400" />
</p>

<br/>

```
# If your parameters are correct for your data, you can run series analysis on more images


# Chromatinization CTRL CELLS
series_results_chromatinization = nf.series_analysis_chromatinization(path_to_images = 'test_data/flow_cytometry/ctrl', 
                                                  file_extension = 'tif', 
                                                  selected_id = [], 
                                                  selection_opt = True, 
                                                  include_img = False, 
                                                  test_series = 0)


```
<br/>

##### Dictionary with series nuclei chromatinization results:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/series_chrom.bmp" alt="drawing" width="600" />
</p>

<br/>

```
import os
from JIMG_analyst_tool.features_selection import NucleiDataManagement

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

```
<br/>

##### Dictionary with series nuclei chromatinization results:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/series_chrom.bmp" alt="drawing" width="600" />
</p>

<br/>

```
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
```
<br/>

##### Data table showing chromatinization results for nuclear series across both concatenated experiments:

<p align="center">
<img  src="examples/FlowCytometry_nuclei/data_table_results.bmp" alt="drawing" width="700" />
</p>

<br/>

```
# save to csv

data.to_csv('dis_vs_ctrl_nuclei.csv', index = False)
```



<br />
<br />


#### 7.3 Clustering and DFA - nuclei data <a id="cdnd"></a>

```
from JIMG_analyst_tool.features_selection import GroupAnalysis

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

```
<br/>

##### Data table presenting statistical analysis of differential features:

<p align="center">
<img  src="examples/DFA_analysis_nuclei/primary_stat.bmp" alt="drawing" width="600" />
</p>

<br/>

```
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
```
<br/>

##### Knee plot - cumulative explanation of variance:

<p align="center">
<img  src="examples/DFA_analysis_nuclei/variance.bmp" alt="drawing" width="500" />
</p>

<br/>

```
# save knee_plot, if required
ga.save_knee_plot(path = os.getcwd(),
               name = '', 
               extension = 'svg')


# run UMAP dimensionality reduction
ga.UMAP(PC_num = 15,
     factorize_with_metadata = True, 
     n_neighbors = 25,
     min_dist = 0.01,
     n_components = 2)


# get UMAP_data, if required
UMAP_data = ga.get_UMAP_data()


# get UMAP_plots, if required
UMAP_plots = ga.get_UMAP_plots(show = True)
```
<br/>

##### UMAP plot - primary clusters description (sets):

<p align="center">
<img  src="examples/DFA_analysis_nuclei/umap_1.bmp" alt="drawing" width="500" />
</p>

<br/>

```
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
```
<br/>

##### UMAP plot - db_scan clusters:

<p align="center">
<img  src="examples/DFA_analysis_nuclei/umap_2.bmp" alt="drawing" width="500" />
</p>

<br/>


##### UMAP plot -  set / cluster combination:

<p align="center">
<img  src="examples/DFA_analysis_nuclei/umap_3.bmp" alt="drawing" width="500" />
</p>

<br/>

```
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

```
<br/>

##### Data table presenting statistical analysis of differential features for final clusters:

<p align="center">
<img  src="examples/DFA_analysis_nuclei/primary_stat.bmp" alt="drawing" width="600" />
</p>





<br />
<br />



#### 7.4 Marker intensity analysis - confocal microscopy <a id="miacm"></a>

##### 7.4.1 Data collection <a id="miacmdc"></a>


```
from JIMG_analyst_tool.features_selection import FeatureIntensity

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
```
<br/>

##### Analysed image projection (after projection with JIMG)

* input image in this case is raw 3D-image in *.tiff format

<p align="center">
<img  src="examples/Intensity/ctrl.bmp" alt="drawing" width="600" />
</p>

<br/>

```
fi.load_mask_(path = 'test_data/intensity/ctrl/mask_1.png')
```
<br/>

##### Analysed image region mask


<p align="center">
<img  src="examples/Intensity/ctrl_mask.bmp" alt="drawing" width="600" />
</p>

<br/>

```
fi.load_normalization_mask_(path = 'test_data/intensity/ctrl/background_1.png')
```
<br/>

##### Normalization region mask (reversed)


<p align="center">
<img  src="examples/Intensity/ctrl_back.bmp" alt="drawing" width="600" />
</p>

<br/>

```
# strat calculations
fi.run_calculations()


# get results
results = fi.get_results()


# save results for further analysis, ensuring each feature 
# is stored in a separate directory (single directory 
# should contain data with the same 'feature_name'),
# this setup allows running fi.concatenate_intensity_data() 
# in the specific directory of each feature
# while preventing errors from incorrect feature concatenation

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
```
<br/>

##### Analysed image projection (after projection with JIMG)

* input image in this case is raw 3D-image in *.tiff format

<p align="center">
<img  src="examples/Intensity/dis.bmp" alt="drawing" width="600" />
</p>

<br/>

```
fi.load_mask_(path = 'test_data/intensity/dise/mask_1.png')
```
<br/>

##### Analysed image region mask


<p align="center">
<img  src="examples/Intensity/dis_mask.bmp" alt="drawing" width="600" />
</p>

<br/>

```
fi.load_normalization_mask_(path = 'test_data/intensity/dise/background_1.png')
```
<br/>

##### Normalization region mask (reversed)


<p align="center">
<img  src="examples/Intensity/dis_back.bmp" alt="drawing" width="600" />
</p>

<br/>

```
fi.run_calculations()

results = fi.get_results()

fi.save_results(path = os.getcwd(), 
             mask_region = 'brain', 
             feature_name = 'Feature1', 
             individual_number = 1, 
             individual_name = 'DISEASE')



# concatenate data of experiment 1 & 2
fi.concatenate_intensity_data(directory = os.getcwd(), name = 'example_data')
```

<br />

##### 7.4.2 Data analysis <a id="miacmda"></a>

```
from JIMG_analyst_tool.features_selection import IntensityAnalysis
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


```
<br/>

##### Results of intensity comparison analysis (region under the mask)

<p align="center">
<img  src="examples/Intensity/compare_result.bmp" alt="drawing" width="600" />
</p>

<br/>

```
results.savefig('example_results.svg', format = 'svg', dpi = 300, bbox_inches = 'tight')
```

<br />
<br />

### Have fun JBS