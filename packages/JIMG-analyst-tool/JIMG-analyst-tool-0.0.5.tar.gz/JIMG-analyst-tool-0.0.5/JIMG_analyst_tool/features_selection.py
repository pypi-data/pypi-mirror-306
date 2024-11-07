from JIMG.functions import jimg as jg
import cv2
from stardist.plot import render_label
from csbdeep.utils import normalize
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from stardist.models import StarDist2D
import copy
from tqdm import tqdm
import skimage
from skimage import measure
from collections import Counter
from IPython.display import display, HTML
import mpld3
import tempfile
import webbrowser
import os
import glob
import pickle
import json
import re
import tkinter as tk  
import random
from scipy.stats import chi2_contingency
import scipy.stats as stats
from itertools import combinations
import pingouin as pg
from joblib import Parallel, delayed
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import umap
import plotly.express as px





random.seed(42)


def test_data(path = os.getcwd()):
    
    try:
        import gdown
        import tarfile
    
        file_name  = 'test_data.tar.gz'
        
        file_name = os.path.join(path, file_name)
        
        url = 'https://drive.google.com/uc?id=1MhzhleMP7iTzlBVW8eP5sFaonJdg1a3T'
        
        gdown.download(url, file_name, quiet=False)
        
        # Unzip 
    
        with tarfile.open(file_name, 'r:gz') as tar:
            tar.extractall(path=path)
            
        print(f"\nTest data downloaded succesfully -> {os.path.join(path, 'test_data')}")
            
    except:
        
        print("\nTest data could not be downloaded. Please check your connection and try again!")

    
    
class ImageTools:
    
    def get_screan(self):
        
        """
         This method returns current screen size.
         
         Returns:
             screen_width (int)
             screen_height (int)
            
         """
    
    
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        root.destroy()
    
        return screen_width, screen_height
    
    def resize_to_screen_img(self, img_file, factor = 0.5):
        
         
        """
        This method resizes input image to screen size refactored by user-defined factor value.
        
        Args:
           img_file (np.ndarray) - input image
           factor (int) - value 
          
        Returns: 
            resized_image (np.ndarray) - resized image
           
           
        """
    
        screen_width, screen_height = self.get_screan()
        
    
        screen_width = int(screen_width*factor)
        screen_height = int(screen_height*factor)
        
    
        h = int(img_file.shape[0])
        w = int(img_file.shape[1])
        
        
        if screen_width < w or screen_width*0.3 > w:
            h = img_file.shape[0]
            w = img_file.shape[1]
            
            ww = int((screen_width/w) * w)
            hh = int((screen_width/w) * h)
            
    
            img_file = cv2.resize(img_file, (ww, hh))
            
            h = img_file.shape[0]
            w = img_file.shape[1]
                
            
            
        if screen_height < h or screen_height*0.3 > h:
            h = img_file.shape[0]
            w = img_file.shape[1]
            
            ww = int((screen_height/h) * w)
            hh = int((screen_height/h) * h)
    
        
        
            img_file = cv2.resize(img_file, (ww, hh))
            
    
        return img_file
    
    def load_JIMG_project(self, project_path):
        
           
        """
        This method loads a JIMG project. The project file must have the *.pjm extension.
        
        Args:
            file_path (str) - path to the project file.
    
        Returns:
            project (class) - loaded project object
    
        Raises:
            ValueError: If the file does not have a *.pjm extension.
        
        """
            
        if '.pjm' in project_path:
            with open(project_path, 'rb') as file:
                app_metadata_tmp = pickle.load(file)
                
            return app_metadata_tmp
        
        else:
            print('\nProvide path to the project metadata file with *.pjm extension!!!')
            
    def ajd_mask_size(self, image, mask):
        try:
            mask = cv2.resize(mask, (image.shape[2], image.shape[1]))
        except:
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        
        return mask
    
    def load_image(self, path_to_image):
        
             
        """
        This method loads an image.
        
        Args:
            path_to_image (str) - the path to the image
    
        Returns:
            image (np.ndarray) - loaded image
    
        
        """
        
        image = jg.load_image(path_to_image)
        return image
    
    def load_3D_tiff(self, path_to_image):
        
        """
        This method loads a 3D-image.
        
        Args:
            path_to_image (str) - the path to the 3D-image. Extension *.tiff
    
        Returns:
            image (np.ndarray) - loaded 3D-image
    
        
        """
        image = jg.load_tiff(path_to_image)
        
        return image
    
    def load_mask(self, path_to_mask):
        
        """
        This method loads a mask-image.
        
        Args:
            path_to_mask (str) - the path to the mask-image
    
        Returns:
            mask (np.ndarray) - loaded mask-image
    
        
        """
        
        mask = cv2.imread(path_to_mask, cv2.IMREAD_GRAYSCALE)
        return mask
    
    def save(self, image, file_name):
        
        """
        This method saves image.
        
        Args:
            image (np.ndarray) - the image to save
            file_name (str) - the file name, including extension [.png, .jpeg, ...], and the path to save the file
    
        """
        
        cv2.imwrite(filename = file_name, img = image)
        
    # calculation methods
    
    def drop_dict(self, dictionary, key, var, action = None):
    
        dictionary = copy.deepcopy(dictionary)
        indices_to_drop = []
        for i, dr in enumerate(dictionary[key]):
    
            if isinstance(dr, np.ndarray):
                dr = np.mean(dr)
                
            if action == '<=':
                if var <= dr:
                    indices_to_drop.append(i)
            elif action == '>=':
                if var >= dr:
                    indices_to_drop.append(i)
            elif action == '==':
                if var == dr:
                    indices_to_drop.append(i)
            elif action == '<':
                if var < dr:
                    indices_to_drop.append(i)
            elif action == '>':
                if var > dr:
                    indices_to_drop.append(i)
            else:
                print('\nWrong action!')
                return None
                
    
        for key, value in dictionary.items():
            dictionary[key] = [v for i, v in enumerate(value) if i not in indices_to_drop]
    
        return dictionary
    
    
    def create_mask(self, dictionary, image):
        image_mask = np.zeros(image.shape)
        
        arrays_list = copy.deepcopy(dictionary['coords'])
    
        for arr in tqdm(arrays_list):
            image_mask[arr[:,0], arr[:,1]] = 2**16-1
            
            
        return image_mask.astype('uint16')
    
    
    
    def min_max_histograme(self, image):
        q = []
        val = []
        perc = []
        
        max_val = image.shape[0] * image.shape[1]
        
        for n in range(0, 100, 5):
            q.append(n)
            val.append(np.quantile(image,n/100))
            sum_val = np.sum(image < np.quantile(image,n/100))
            pr = sum_val/max_val
            perc.append(pr)
                
        
        df = pd.DataFrame({'q':q, 'val':val, 'perc':perc})
        
        
        min_val = 0
        for i in df.index:
            if df['val'][i] != 0 and min_val == 0:
                min_val = df['perc'][i]
                
                
        max_val = 0
        df = df[df['perc'] > 0]
        df = df.sort_values('q',ascending=False).reset_index(drop=True)
    
        for i in df.index:       
            if i > 1 and df['val'][i]*1.5 > df['val'][i-1]:
                max_val = df['perc'][i]
                break
            elif i == len(df.index)-1:
                max_val = df['perc'][i]
                
        return min_val, max_val, df
    
        
    

class NucleiFinder(ImageTools):
    
    
    def __init__(self, image=None, test_results=None, 
                 hyperparameter_nuclei=None, 
                 hyperparameter_chromatinization=None, 
                 img_adj_par_chrom=None, 
                 img_adj_par=None, 
                 show_plots=None, 
                 nuclei_results=None, 
                 images=None):
        
        
        # Use default values if parameters are None
        self.image = image or None
        self.test_results = test_results or None
        self.hyperparameter_nuclei = hyperparameter_nuclei or {'nms': 0.8, 'prob': 0.4, 'max_size': 1000, 'min_size': 200, 'circularity': .3, 'ratio': .1, 'intensity_mean': (2**16-1) / 5}
        self.hyperparameter_chromatinization = hyperparameter_chromatinization or {'max_size': 200, 'min_size': 2, 'ratio': .1, 'cut_point': .95}
        self.img_adj_par_chrom = img_adj_par_chrom or {'gamma': .25, 'contrast': 4, 'brightness': 950}
        self.img_adj_par = img_adj_par or {'gamma': 1, 'contrast': 1, 'brightness': 1000}
        self.show_plots = show_plots or True
        self.nuclei_results = nuclei_results or {'nuclei': None, 'nuclei_reduced': None, 'nuclei_chromatinization': None}
        self.images = images or {'nuclei': None, 'nuclei_reduced': None, 'nuclei_chromatinization': None}

       
       
       
    def set_nms(self, nms:float):
        
        """
        This method sets 'nms' parameter. The nms threshold is set to a small number to reduce the probability of nuclei overlap.
        
        Args:
            nms (float) - the nms value

        """
        
        self.hyperparameter_nuclei['nms'] = nms
    
    
    def set_prob(self, prob:float):
        
        """
        This method sets 'prob' parameter. The prob is a parameter used in image segmentation to determine the level of confidence required for an object (such as a nucleus) to be classified as a segmented entity.

        Effect of Larger prob_thresh Values: When you increase the value of prob_thresh, you will typically observe fewer segmented objects in the resulting images. This is because a higher threshold means that only those objects with a greater degree of certainty will be included in the segmentation, potentially leading to the omission of weaker or less distinct objects.

        Determining Optimal Values: The ideal settings for prob_thresh and other related parameters, such as nm_thresh, can vary significantly based on the specific characteristics of the images being analyzed. It is crucial to visually assess the nuclei segmentation masks produced with different thresholds to find the values that best suit your particular dataset.

        Args:
            prob (float) - the prob value

        """
        
        self.hyperparameter_nuclei['prob'] = prob
        
        
    def set_nuclei_circularity(self, circ:float):
        
        """
        This method sets 'circ' parameter. The circ is a parameter used for adjust minimal nucleus circularity.
        
        Args:
            circ (float) - the nuclei circularity value

        """
        
        self.hyperparameter_nuclei['circularity'] = circ      
        
    
         
    def set_nuclei_yx_len_min_ratio(self, ratio:float):
        
        """
        This method sets the 'ratio' parameter. In this case, the 'ratio' parameter is similar to 'circularity' as it describes the ratio between the maximum lengths in the x and y dimensions of the nucleus.
        
        Args:
            ratio (float) - the prob value

        """
        
        self.hyperparameter_nuclei['ratio'] = ratio        
        
        
        
    def set_nuclei_size(self, size:tuple):
        
        """
        This method sets 'size' parameter. The size is a parameter used for adjust minimal and maximal nucleus area (px).
        
        Args:
            size (tuple) - (min_value, max_value)

        """
        
        self.hyperparameter_nuclei['min_size'] = size[0]
        self.hyperparameter_nuclei['max_size'] = size[1]
        
             
    def set_nuclei_min_mean_intensity(self, intensity:int):
        
        """
        This method sets 'intensity' parameter. The 'intensity' parameter is used to adjust the minimum mean intensity of all pixel intensities within the nucleus.        
        
        Args:
            intensity (int) - the intensity value

        """
        
        self.hyperparameter_nuclei['intensity_mean'] = intensity
        
        
    def set_chromatinization_size(self, size:tuple):
        
        """
        This method sets 'size' parameter. The size is a parameter used for adjust minimal and maximal chromanitization spot area (px) within the nucleus.
        
        Args:
            size (tuple) - (min_value, max_value)

        """
        
        self.hyperparameter_chromatinization['min_size'] = size[0]
        self.hyperparameter_chromatinization['max_size'] = size[1]
   
    
    def set_chromatinization_ratio(self, ratio:int):
        
        """
        This method sets the 'ratio' parameter. In this case, the 'ratio' parameter is similar to 'circularity' as it describes the ratio between the maximum lengths in the x and y dimensions of the nucleus chromatinization.
        
        Args:
            ratio (float) - the ratio value

        """
        
        self.hyperparameter_chromatinization['ratio'] = ratio
             
        
    def set_chromatinization_cut_point(self, cut_point:int):
        
        """
        This method sets the 'cut_point' parameter. The 'cut_point' parameter is a factor used to adjust the threshold for separating the background from chromatin spots.        
        
        Args:
            cut_point (int) - the cut_point value

        """
        
        self.hyperparameter_chromatinization['cut_point'] = cut_point

    
    #
    
    def set_adj_image_gamma(self, gamma:float):
        
        """
        This method sets 'gamma' parameter. The gamma is a parameter used for adjust gamma of the nucleus image.
        
        Args:
            gamma (float) - the gamma value

        """
        
        self.img_adj_par['gamma'] = gamma
        
    def set_adj_image_contrast(self, contrast:float):
        
        """
        This method sets 'contrast' parameter. The contrast is a parameter used for adjust contrast of the nucleus image.
        
        Args:
            contrast (float) - the contrast value

        """
        
        self.img_adj_par['contrast'] = contrast
        
    def set_adj_image_brightness(self, brightness:float):
        
        """
        This method sets 'brightness' parameter. The brightness is a parameter used for adjust brightness of the nucleus image.
        
        Args:
            brightness (float) - the brightness value

        """
        
        self.img_adj_par['brightness'] = brightness
        
    #
    
    def set_adj_chrom_gamma(self, gamma:float):
        
        """
        This method sets 'gamma' parameter. The gamma is a parameter used for adjust gamma of the nucleus chromatinization image.
        
        Args:
            gamma (float) - the gamma value

        """
        
        self.img_adj_par_chrom['gamma'] = gamma
        
    def set_adj_chrom_contrast(self, contrast:float):
        
        """
        This method sets 'contrast' parameter. The contrast is a parameter used for adjust contrast of the nucleus chromatinization image.
        
        Args:
            contrast (float) - the contrast value

        """
        
        self.img_adj_par_chrom['contrast'] = contrast
        
    def set_adj_chrom_brightness(self, brightness:float):
        
        """
        This method sets 'brightness' parameter. The brightness is a parameter used for adjust brightness of the nucleus chromatinization image.
        
        Args:
            brightness (float) - the brightness value
 
        """
        
        self.img_adj_par_chrom['brightness'] = brightness
             
         
    
    @property
    def current_parameters_nuclei(self):
        
        """
        This method returns current nuclei analysis parameters.
        
    
        Returns:
            nuclei (dict) - nuclei analysis parameters
    
        
        """
        print(self.hyperparameter_nuclei)
        return self.hyperparameter_nuclei
    
    
    @property
    def current_parameters_chromatinization(self):
        
        """
        This method returns current nuclei chromatinization analysis parameters.
        
        Returns:
            nuclei_chromatinization (dict) - nuclei chromatinization analysis parameters
    
        
        """
        
        print(self.hyperparameter_chromatinization)
        return self.hyperparameter_chromatinization
    
    @property
    def current_parameters_img_adj(self):
        
        """
        This method returns current nuclei image setup.
        
        Returns:
            neuclei_image_setup (dict) - nuclei image setup
    
        
        """
        
        print(self.img_adj_par)
        return self.img_adj_par
    
    
    @property
    def current_parameters_img_adj_chro(self):
        
        """
        This method returns current nuclei chromatinization image setup.
        
    
        Returns:
            neuclei_chromatinization_setup (dict) - nuclei chromatinization image setup
    
        
        """
        
        print(self.img_adj_par_chrom)
        return self.img_adj_par_chrom


    def get_results_nuclei(self):
        
        """
        This function returns nuclei analysis results.
        
    
        Returns:
            neuclei_results (dict) - neuclei results in the dictionary format 
    
        
        """
        
        if self.images['nuclei'] is None:
            print('No results to return!')
            return None
        else:
            if self.show_plots == True:
                jg.display_preview(self.images['nuclei'])   
            return self.nuclei_results['nuclei'], self.images['nuclei']
    
    
    def get_results_nuclei_selected(self):
        
        """
        This function returns the results of the nuclei analysis following adjustments to the data selection thresholds.
        
    
        Returns:
            neuclei_results (dict) - neuclei results in the dictionary format 
    
        
        """
        
        if self.images['nuclei_reduced'] is None:
            print('No results to return!')
            return None
        else:
            if self.show_plots == True:
                jg.display_preview(self.images['nuclei_reduced'])   
            return self.nuclei_results['nuclei_reduced'], self.images['nuclei_reduced']
        

    def get_results_nuclei_chromatinization(self):
        
        """
        This function returns the results of the nuclei chromatinization analysis.
        
    
        Returns:
            nuclei_chromatinization_results (dict) - nuclei chromatinization results in the dictionary format 
    
        
        """
        
        if self.images['nuclei_chromatinization'] is None:
            print('No results to return!')
            return None
        else:
            if self.show_plots == True:
                jg.display_preview(self.images['nuclei_chromatinization'])   
            return self.nuclei_results['nuclei_chromatinization'], self.images['nuclei_chromatinization']


        
    def add_test(self, plots):
        self.test_results = plots
       
        
    def input_image(self, img):
        
        """
        This method adds the image to the class for nuclei and/or chromatinization analysis.
    
        Args:
            img (np.ndarray) - input image
    
        
        """
        
        self.image = img
        self.add_test(None)
        
        
        
    def get_features(self, model_out, image):

        features = {'label':[],
                    'area':[],
                    'area_bbox':[],
                    'area_convex':[],
                    'area_filled':[],
                    'axis_major_length':[],
                    'axis_minor_length':[],
                    'eccentricity':[],
                    'equivalent_diameter_area':[],
                    'feret_diameter_max':[],
                    'solidity':[],
                    'orientation':[],
                    'perimeter':[],
                    'perimeter_crofton':[],
                    'circularity':[],
                    'intensity_max':[],
                    'intensity_mean':[],
                    'intensity_min':[],
                    'ratio':[],
                    'coords':[]

                    }
                   
        
        
        for region in skimage.measure.regionprops(model_out, intensity_image=image):
            # Compute circularity
            circularity = 4 * np.pi * region.area / (region.perimeter ** 2)
            
            
            features['area'].append(region.area)
            features['area_bbox'].append(region.area_bbox)
            features['area_convex'].append(region.area_convex)
            features['area_filled'].append(region.area_filled)
            features['axis_major_length'].append(region.axis_major_length)
            features['axis_minor_length'].append(region.axis_minor_length)
            features['eccentricity'].append(region.eccentricity)
            features['equivalent_diameter_area'].append(region.equivalent_diameter_area)
            features['feret_diameter_max'].append(region.feret_diameter_max)
            features['solidity'].append(region.solidity)
            features['orientation'].append(region.orientation)
            features['perimeter'].append(region.perimeter)
            features['perimeter_crofton'].append(region.perimeter_crofton)
            features['label'].append(region.label)
            features['coords'].append(region.coords)
            features['circularity'].append(circularity)
            features['intensity_max'].append(np.max(region.intensity_max))
            features['intensity_min'].append(np.max(region.intensity_min))
            features['intensity_mean'].append(np.max(region.intensity_mean))


           
            
        ratios = []  

        # Calculate the ratio for each pair of values
        for min_len, max_len in zip(features['axis_minor_length'], features['axis_major_length']):
            if max_len != 0:
                ratio = min_len / max_len
                ratios.append(ratio)
            else:
                ratios.append(float(0.0))  
                
        features['ratio'] = ratios


            
        return features
     
     
     
     
    def nuclei_finder_test(self):
        
        """
        This method performs testing analysis on the image provided by the input_image() method 
        using the specified 'nms' and 'prob' parameters.

        To display the test results, run the browser_test() method.

        """
        
        StarDist2D.from_pretrained()
        model = StarDist2D.from_pretrained('2D_versatile_fluo')
        
        nmst = [0,.2,.4,.6,.8]
        probt = [.1,.3,.5,.7]
        
        try:
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        except:
            img = self.image
    
        plot = []
        
        fig = plt.figure(dpi=300)
        plt.imshow(img)
        plt.axis("off")
        plt.title("Original", fontsize = 25)
        
        if self.show_plots == True:
            plt.show()
    
        
        plot.append(fig)
        
        for n in tqdm(nmst):
            for t in probt:
                
                img = jg.adjust_img_16bit(img, brightness = self.img_adj_par['brightness'], contrast = self.img_adj_par['contrast'], gamma = self.img_adj_par['gamma'])
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                labels, _ = model.predict_instances(normalize(img), nms_thresh=n, prob_thresh=t)
                
                tmp = self.get_features(model_out = labels, image = img)
                
                
                fig = plt.figure(dpi=300)
                plt.imshow(render_label(labels, img=img))
                plt.axis("off")
                plt.title(f"nms {n} & prob {t} \n detected nuc: {len(tmp['area'])} \n var: {int(np.array(tmp['area']).var())}", fontsize=25)
                
                if self.show_plots == True:
                    plt.show()
            
                
                plot.append(fig)
                
                
        self.add_test(plot)
      
    
     

    
    def find_nuclei(self):
        
        """
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

        """
        
        if isinstance(self.image, np.ndarray):
            StarDist2D.from_pretrained()
            model = StarDist2D.from_pretrained('2D_versatile_fluo')
            
            try:
                img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            except:
                img = self.image    
            
            img = jg.adjust_img_16bit(img, brightness = self.img_adj_par['brightness'], contrast = self.img_adj_par['contrast'], gamma = self.img_adj_par['gamma'])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            labels, _ = model.predict_instances(normalize(img), nms_thresh=self.hyperparameter_nuclei['nms'], prob_thresh=self.hyperparameter_nuclei['prob'])
             
            
            self.nuclei_results['nuclei'] = self.get_features(model_out = labels, image = img)     
            
            if len(self.nuclei_results['nuclei']['coords']) > 0:
                
                nuclei_mask = jg.adjust_img_16bit(cv2.cvtColor(self.create_mask(self.nuclei_results['nuclei'] , self.image), cv2.COLOR_BGR2GRAY), color='blue')
                
                nuclei_mask = self.resize_to_screen_img(nuclei_mask)
    
                
                oryginal = jg.adjust_img_16bit(img, color='gray')
                oryginal = self.resize_to_screen_img(oryginal)
    
                concatenated_image = cv2.hconcat([oryginal, nuclei_mask])
                
                     
                self.images['nuclei'] = concatenated_image
    
                
                if self.show_plots == True:
                    jg.display_preview(self.images['nuclei'])   
                    
            else:
                
                self.nuclei_results['nuclei'] = None
                print('Nuclei not detected!')
                    
                
                
        
        else:
            print('\nAdd image firstly!')
        
        
       
    
    
    def select_nuclei(self):
        
        """
        This method selects data obtained from find_nuclei() based on the set threshold parameters.
        
        To show current parameters run:
            - current_parameters_nuclei
        
        To set new parameters run:
            
            - set_nuclei_circularity()
            - set_nuclei_yx_len_min_ratio()
            - set_nuclei_size()
            - set_nuclei_min_mean_intensity()
      


        To get analysis results run get_results_nuclei_selected() method.

        """
        
        if self.nuclei_results['nuclei'] is not None:
            input_in = copy.deepcopy(self.nuclei_results['nuclei'])
            
            nuclei_dictionary = self.drop_dict(input_in, key = 'area', var = self.hyperparameter_nuclei['min_size'], action = '>')
            nuclei_dictionary = self.drop_dict(nuclei_dictionary, key = 'area', var =  self.hyperparameter_nuclei['max_size'], action = '<')
            nuclei_dictionary = self.drop_dict(nuclei_dictionary, key = 'circularity', var = self.hyperparameter_nuclei['circularity'], action = '>')
            nuclei_dictionary = self.drop_dict(nuclei_dictionary, key = 'ratio', var =  self.hyperparameter_nuclei['ratio'], action = '>')
            nuclei_dictionary = self.drop_dict(nuclei_dictionary, key = 'intensity_mean', var =  self.hyperparameter_nuclei['intensity_mean'], action = '>')
        
            if len(nuclei_dictionary['coords']) > 0:
                
                self.nuclei_results['nuclei_reduced'] = nuclei_dictionary
                
                nuclei_mask = jg.adjust_img_16bit(cv2.cvtColor(self.create_mask(self.nuclei_results['nuclei_reduced'] , self.image), cv2.COLOR_BGR2GRAY), color='blue')
        
                try:
                    img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                except:
                    img = self.image    
                     
                     
             
                
                nuclei_mask = self.resize_to_screen_img(nuclei_mask)
        
                oryginal = jg.adjust_img_16bit(img, color='gray')
                
                oryginal = self.resize_to_screen_img(oryginal)
        
        
                concatenated_image = cv2.hconcat([oryginal, nuclei_mask])
                concatenated_image = self.resize_to_screen_img(concatenated_image)
                
                
                self.images['nuclei_reduced'] = concatenated_image
                
                
                
                if self.show_plots == True:
                    jg.display_preview(self.images['nuclei_reduced'])   
                    
            else:
                self.nuclei_results['nuclei'] = None
                self.nuclei_results['nuclei_reduced'] = None
                self.nuclei_results['nuclei_chromatinization'] = None
                
                print('Selected zero nuclei! Analysis stop!')
                
                
        else:
            print('Lack of nuclei data to select!')
            


          
    
    def nuclei_chromatinization(self):
        
        """
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

        """
        
        def is_list_in_llist(lst, llist):
            return any(sub_lst == lst for sub_lst in llist)
    
        def add_lists(f, g):
            result = []
            max_length = max(len(f), len(g))
           
            for i in range(max_length):
                f_elem = f[i] if i < len(f) else ""
                g_elem = g[i] if i < len(g) else ""
                result.append(f_elem + g_elem)
           
            return result
        
            
        def reverse_coords(image, x, y):
            
            
            zero = np.zeros(image.shape)
            
            zero[x, y] = 2**16
    
            zero_indices = np.where(zero == 0)
            
            return zero_indices[0], zero_indices[1]
            
        
        
        
         
        if isinstance(self.nuclei_results['nuclei_reduced'], dict):
            nuclei_dictionary = self.nuclei_results['nuclei_reduced']
        else:
            nuclei_dictionary = self.nuclei_results['nuclei']

         
        if nuclei_dictionary is not None:
            arrays_list = copy.deepcopy(nuclei_dictionary['coords'])
        
            chromatione_info = {
               
                        'area':[],
                        'area_bbox':[],
                        'area_convex':[],
                        'area_filled':[],
                        'axis_major_length':[],
                        'axis_minor_length':[],
                        'eccentricity':[],
                        'equivalent_diameter_area':[],
                        'feret_diameter_max':[],
                        'solidity':[],
                        'orientation':[],
                        'perimeter':[],
                        'perimeter_crofton':[],
                        'coords':[]

                        }
            
            full_im = np.zeros(self.image.shape[0:2], dtype=np.uint16)
            full_im = jg.adjust_img_16bit(full_im)
            
            
            for arr in arrays_list:
                x = list(arr[:,0])
                y = list(arr[:,1])
                
            
                x1, y1 = reverse_coords(self.image, x, y)
                       
                   
                regions_chro2 = self.image.copy()
                   
                   
                regions_chro2[x1, y1] = 0
                     
                    
                regions_chro2 = regions_chro2.astype('uint16')
                  
                try:
                    regions_chro2 = cv2.cvtColor(regions_chro2, cv2.COLOR_BGR2GRAY)
                except:
                    pass
                  
               
                regions_chro2 = jg.adjust_img_16bit(regions_chro2, 
                                                    brightness=self.img_adj_par_chrom['brightness'],
                                                    contrast=self.img_adj_par_chrom['contrast'],
                                                    gamma=self.img_adj_par_chrom['gamma'])
                
                full_im = jg.merge_images(image_list = [full_im, regions_chro2], intensity_factors = [1,1])
                
                    
                ret, thresh = cv2.threshold(regions_chro2[x,y], 0, 2**16-1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
               
                regions_chro2[regions_chro2 <= ret*self.hyperparameter_chromatinization['cut_point']] = 0
                

              
                    
                regions_chro2 = cv2.cvtColor(regions_chro2, cv2.COLOR_BGR2GRAY)
                    
                
                chromatione = regions_chro2 > 0
              
              
                labeled_cells = measure.label(chromatione)
                regions = measure.regionprops(labeled_cells)
                regions = measure.regionprops(labeled_cells, intensity_image=regions_chro2)
               
                    
                for region in regions:
                      
                    chromatione_info['area'].append(region.area)
                    chromatione_info['area_bbox'].append(region.area_bbox)
                    chromatione_info['area_convex'].append(region.area_convex)
                    chromatione_info['area_filled'].append(region.area_filled)
                    chromatione_info['axis_major_length'].append(region.axis_major_length)
                    chromatione_info['axis_minor_length'].append(region.axis_minor_length)
                    chromatione_info['eccentricity'].append(region.eccentricity)
                    chromatione_info['equivalent_diameter_area'].append(region.equivalent_diameter_area)
                    chromatione_info['feret_diameter_max'].append(region.feret_diameter_max)
                    chromatione_info['solidity'].append(region.solidity)
                    chromatione_info['orientation'].append(region.orientation)
                    chromatione_info['perimeter'].append(region.perimeter)
                    chromatione_info['perimeter_crofton'].append(region.perimeter_crofton)
                    chromatione_info['coords'].append(region.coords)
                
            
                
            ratios = []  
              
              
            for min_len, max_len in zip(chromatione_info['axis_minor_length'], chromatione_info['axis_major_length']):
                if max_len != 0:
                    ratio = min_len / max_len
                    ratios.append(ratio)
                else:
                    ratios.append(float(0.0))  
                      
                      
            chromatione_info['ratio'] = ratios
                    
                
            chromation_dic = self.drop_dict(chromatione_info, key = 'area', var = self.hyperparameter_chromatinization['min_size'], action = '>')
            chromation_dic = self.drop_dict(chromation_dic, key = 'area', var = self.hyperparameter_chromatinization['max_size'], action = '<')
            chromation_dic = self.drop_dict(chromation_dic, key = 'ratio', var = self.hyperparameter_chromatinization['ratio'], action = '>')
               
              
            arrays_list2 = copy.deepcopy(chromation_dic['coords'])
              
            nuclei_dictionary['spot_size_area'] = []
            nuclei_dictionary['spot_size_area_bbox'] = []
            nuclei_dictionary['spot_size_area_convex'] = []
            nuclei_dictionary['spot_size_area_filled'] = []
            nuclei_dictionary['spot_axis_major_length'] = []
            nuclei_dictionary['spot_axis_minor_length'] = []
            nuclei_dictionary['spot_eccentricity'] = []
            nuclei_dictionary['spot_size_equivalent_diameter_area'] = []
            nuclei_dictionary['spot_feret_diameter_max'] = []
            nuclei_dictionary['spot_orientation'] = []
            nuclei_dictionary['spot_perimeter'] = []
            nuclei_dictionary['spot_perimeter_crofton'] = []
            
            
            
              
            for i, arr in enumerate(tqdm(arrays_list)):
                  
                spot_size_area = []
                spot_size_area_bbox = []
                spot_size_area_convex = []
                spot_size_area_convex = []
                spot_size_area_filled = []
                spot_axis_major_length = []
                spot_axis_minor_length = []
                spot_eccentricity = []
                spot_size_equivalent_diameter_area = []
                spot_feret_diameter_max = []
                spot_orientation = []
                spot_perimeter = []
                spot_perimeter_crofton = []
            
            
                # Flatten the array,
                df_tmp = pd.DataFrame(arr)
                df_tmp['duplicates'] = add_lists([str(x) for x in df_tmp[0]], [str(y) for y in df_tmp[1]])
                  
                counter_tmp = Counter(df_tmp['duplicates'])
                  
               
                for j, arr2 in enumerate(arrays_list2):
                    df_tmp2 = pd.DataFrame(arr2)
                    df_tmp2['duplicates'] = add_lists([str(x) for x in df_tmp2[0]], [str(y) for y in df_tmp2[1]])
                      
                    counter_tmp2 = Counter(df_tmp2['duplicates'])
                    intersection_length = len(counter_tmp.keys() & counter_tmp2.keys())
                    min_length = min(len(counter_tmp), len(counter_tmp2))
                      
                    if intersection_length >= 0.8 * min_length:
                          
               
                        if (len(list(df_tmp2['duplicates']))/len(list(df_tmp['duplicates']))) >= 0.025 and (len(list(df_tmp2['duplicates']))/len(list(df_tmp['duplicates']))) <= 0.5:
                            spot_size_area.append(chromation_dic['area'][j])
                            spot_size_area_bbox.append(chromation_dic['area_bbox'][j])
                            spot_size_area_convex.append(chromation_dic['area_convex'][j])
                            spot_size_area_filled.append(chromation_dic['area_filled'][j])
                            spot_axis_major_length.append(chromation_dic['axis_major_length'][j])
                            spot_axis_minor_length.append(chromation_dic['axis_minor_length'][j])
                            spot_eccentricity.append(chromation_dic['eccentricity'][j])
                            spot_size_equivalent_diameter_area.append(chromation_dic['equivalent_diameter_area'][j])
                            spot_feret_diameter_max.append(chromation_dic['feret_diameter_max'][j])
                            spot_orientation.append(chromation_dic['orientation'][j])
                            spot_perimeter.append(chromation_dic['perimeter'][j])
                            spot_perimeter_crofton.append(chromation_dic['perimeter_crofton'][j])
                              
                              
                              
                              
                nuclei_dictionary['spot_size_area'].append(spot_size_area)
                nuclei_dictionary['spot_size_area_bbox'].append(spot_size_area_bbox)
                nuclei_dictionary['spot_size_area_convex'].append(spot_size_area_convex)
                nuclei_dictionary['spot_size_area_filled'].append(spot_size_area_filled)
                nuclei_dictionary['spot_axis_major_length'].append(spot_axis_major_length)
                nuclei_dictionary['spot_axis_minor_length'].append(spot_axis_minor_length)
                nuclei_dictionary['spot_eccentricity'].append(spot_eccentricity)
                nuclei_dictionary['spot_size_equivalent_diameter_area'].append(spot_size_equivalent_diameter_area)
                nuclei_dictionary['spot_feret_diameter_max'].append(spot_feret_diameter_max)
                nuclei_dictionary['spot_orientation'].append(spot_orientation)
                nuclei_dictionary['spot_perimeter'].append(spot_perimeter)
                nuclei_dictionary['spot_perimeter_crofton'].append(spot_perimeter_crofton)
                        
                    
                
            self.nuclei_results['chromatinization'] = chromation_dic
            self.nuclei_results['nuclei_chromatinization'] = nuclei_dictionary
             
            self.images['nuclei_chromatinization'] = self.create_mask(chromation_dic, self.image)
             
            img_chrom = jg.adjust_img_16bit(cv2.cvtColor(self.create_mask(self.nuclei_results['chromatinization'] , self.image), cv2.COLOR_BGR2GRAY), color='yellow')        
              
              
            if isinstance(self.nuclei_results['nuclei_reduced'], dict):
                nuclei_mask = jg.adjust_img_16bit(cv2.cvtColor(self.create_mask(self.nuclei_results['nuclei_reduced'] , self.image), cv2.COLOR_BGR2GRAY), color='blue')
            else:
                nuclei_mask = jg.adjust_img_16bit(cv2.cvtColor(self.create_mask(self.nuclei_results['nuclei'] , self.image), cv2.COLOR_BGR2GRAY), color='blue')
             
             
            nuclei_mask = jg.merge_images([nuclei_mask, img_chrom], [1, 1])

                 
       
            try:
                img = cv2.cvtColor(full_im, cv2.COLOR_BGR2GRAY)
            except:
                img = full_im 
                 
    
             
            oryginal = jg.adjust_img_16bit(img, color='gray')
            
            
             
            concatenated_image = cv2.hconcat([oryginal, nuclei_mask])
            concatenated_image = self.resize_to_screen_img(concatenated_image)
              
             
            self.images['nuclei_chromatinization'] = concatenated_image
              
              
            if self.show_plots == True:
                jg.display_preview(self.images['nuclei_chromatinization'])   
                
        else:
            print('Lack of nuclei data to select!')
            
            


    def browser_test(self):
        
        """
        This method performs test results provided by the `nuclei_finder_test()` method in the default browser.

        """
        
        html_content = ""

        # Iterate through the test results and concatenate HTML representations
        for f in self.test_results:
            html_content += mpld3.fig_to_html(f)

        # Write the HTML content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as tmp_file:
            tmp_file.write(html_content)
            tmp_filename = tmp_file.name

        # Open the temporary HTML file in a web browser
        webbrowser.open_new_tab(tmp_filename)



    def series_analysis_chromatinization(self, path_to_images:str, file_extension:str = 'tiff', selected_id:list = [], fille_name_part:str = '',  selection_opt:bool = True, include_img:bool = True, test_series:int = 0):
        
        """
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
               
        """
        
        results_dict = {}

        files = glob.glob(os.path.join(path_to_images, "*." + file_extension))
        
        if len(fille_name_part) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if fille_name_part.lower() in x.lower()]
        
        if len(selected_id) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if any(selected in x for selected in selected_id)]

        if test_series > 0:
            
            files = random.sample(files,  test_series)
            
        for file in tqdm(files):
            
            print(file)
            
            self.show_plots = False
            
            image = self.load_image(file)
    
            self.input_image(image)
            
            self.find_nuclei()
            
            if self.nuclei_results['nuclei'] is not None:
            
                if selection_opt == True:
                    self.select_nuclei()
        
                self.nuclei_chromatinization()
                
                tmp = self.get_results_nuclei_chromatinization()
                
                if tmp[0] != None:
                    tmp[0].pop('coords')
                    
                    if include_img == True:
                        results_dict[str(os.path.basename(file))] = {'stats':tmp[0], 'img':tmp[1]}
                        del tmp
                    else:
                        results_dict[str(os.path.basename(file))] = tmp[0]
                        del tmp
                        
                else:
                    print(f'Unable to obtain results for {print(file)}')

                
            else:
                
                print(f'Unable to obtain results for {print(file)}')
                
            self.show_plots = True


        return results_dict
    
    
    def series_analysis_nuclei(self, path_to_images:str, file_extension:str = 'tiff', selected_id:list = [], fille_name_part:str = '',  selection_opt:bool = True, include_img:bool = True, test_series:int = 0):
        
        """
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
        
            results_dict (dict) - dictionary containing results for each image in the directory. The dictionary keys are the image names
               
        """
        
        results_dict = {}

        files = glob.glob(os.path.join(path_to_images, "*." + file_extension))
        
        if len(fille_name_part) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if fille_name_part.lower() in x.lower()]
        
        if len(selected_id) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if any(selected in x for selected in selected_id)]
        
        if test_series > 0:
            
            files = random.sample(files,  test_series)

        for file in tqdm(files):
            
            print(file)
            
            self.show_plots = False
            
            image = self.load_image(file)
    
            self.input_image(image)
            
            self.find_nuclei()
            
            if self.nuclei_results['nuclei'] is not None:
            
                if selection_opt == True:
                    self.select_nuclei()
                    
                tmp = self.get_results_nuclei_selected()
                if tmp is None:
                    tmp = self.get_results_nuclei()
                    
                tmp[0].pop('coords')
                
                if include_img == True:
                    results_dict[str(os.path.basename(file))] = {'stats':tmp[0], 'img':tmp[1]}
                    del tmp
                else:
                    results_dict[str(os.path.basename(file))] = tmp[0]
                    del tmp
                    
                
            else:
                
                print(f'Unable to obtain results for {print(file)}')
                
                
            self.show_plots = True

        
        return results_dict

            



class NucleiDataManagement:
    
    def __init__(self, mutual_data = None,
                 mutual_IS_data = None,
                 images = None):
        

       self.mutual_IS_data = mutual_IS_data or None
       self.mutual_data = mutual_data or None
       self.images = images or None
   
       

    
    def get_mutual_data(self):
        
        """
        Retrieves the mutual data (returned from select_nuclei_data() method) stored in the object.
       
        Returns:
            mutual_data (DataFrame) - the mutual data
           
       """
        
        return self.mutual_data
        
    
    def get_mutual_IS_data(self):
        
        """
        Retrieves the mutual nuclei and IS data (returned from concat_IS_results() method) stored in the object.
        
        Returns:
            mutual_IS_data (DataFrame) - the mutual nuclei and IS data
            
        """
        
        return self.mutual_IS_data
    
    
    def get_prepared_images(self):
        
        """
        Retrieves the prepared images (returned from preapre_selected_img() method) stored in the object.
        
        Returns:
            images (dict) - a dictionary of prepared images
            
        """
        
        return self.images
    
    
    def save_prepared_images(self, path_to_save = os.getcwd()):
        
        
        """
        Saves prepared images (returned from preapre_selected_img() method) to the specified directory.
        
        Args:
            path_to_save (str) - the directory path where the images will be saved. Default is the current working directory
            
        """
      
        
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save, exist_ok=True)
        
        
        for i in tqdm(self.images.keys()):
            cv2.imwrite(os.path.join(path_to_save.  i + '.png'), self.images[i])
        
        
        
      
        
    def save_nuclei_results(self, path:str = os.getcwd(), data:dict = {}, id_name:str = 'name'):
        
        """
        Saves nuclei results as images and JSON data with *.nuc extension.
        Results to save must be obtained from NucleiFinder class series_analysis_nuclei() or series_analysis_chromatinization() methods.
        
        Args:
            path (str) - the directory where results will be saved. Default is the current working directory
            data (dict) - the dictionary containing nuclei data or nuclei data and images
            id_name (str) - w string used for naming the result folder. Default is 'name'
        
        """
        
        if len(data.keys()) > 0:
            full_path = os.path.join(path, id_name)
    
            if data[list(data.keys())[0]].get('img') is not None:
                
                isExist = os.path.exists(full_path)
                if not isExist:
                   os.makedirs(full_path, exist_ok=True)
            
                for i in tqdm(data.keys()):
                    cv2.imwrite(filename = os.path.join(full_path, i + '.png'), img = data[i]['img'])
                    data[i] = data[i]['stats']
    
    
            with open(full_path + '.nuc', 'w') as json_file:
                json.dump(data, json_file, indent=4) 
        else:
            print('\nData not provided!')

    
    
    def select_nuclei_data(self, path_to_results:str = os.getcwd(), data_sets:list = []):
        
        """
        Loads and selects nuclei (nuclei parameters and / or chromatinization parameters) data from results files for each data set, processes it, and stores it in mutual_data.
        
        Args:
            path_to_results (str) - directory containing the results files. Default is the current working directory
            data_sets (list) - list of data set names to be selected. Default is an empty list
        
        """
      
      
        final_df = pd.DataFrame()
        
        file_list = os.listdir(path_to_results)
        
        for o in tqdm(data_sets):
            print(o)
            for f in file_list:
                if o in f and '.nuc' in f:
                    with open(os.path.join(path_to_results,f), 'r') as file:
                        nuclei_data = json.load(file)
                   
                    id_name = []
                    nuclei_area = []
                    nuclei_area_bbox = []
                    nuclei_equivalent_diameter_area = []
                    nuclei_feret_diameter_max = []
                    nuclei_orientation = []
                    nuclei_axis_major_length = []
                    nuclei_axis_minor_length = []
                    nuclei_circularity = []
                    nuclei_eccentricity = []
                    nuclei_perimeter = []
                    nuclei_ratio = []
                    nuclei_solidity = []
                   
                    
                    spot_amount = []
                    avg_spot_axis_major_length = []
                    avg_spot_axis_minor_length = []
                    avg_spot_eccentricity = []
                    avg_spot_size_equivalent_diameter_area = []
                    
                    avg_spot_area = []
                    avg_spot_size_area_bbox = []
                    avg_spot_perimeter = []
                    sum_spot_area = []
                    sum_spot_size_area_bbox = []
                    sum_spot_perimeter = []
                    sum_spot_size_equivalent_diameter_area = []

            
                    
            
            
                    for i in tqdm(nuclei_data.keys()):
                        
                        for n, _ in enumerate(nuclei_data[i]['area']):
                            id_name.append(re.sub('_.*', '', i))
                            nuclei_area.append(nuclei_data[i]['area'][n])
                            nuclei_area_bbox.append(nuclei_data[i]['area_bbox'][n])
                            nuclei_equivalent_diameter_area.append(nuclei_data[i]['equivalent_diameter_area'][n])
                            nuclei_feret_diameter_max.append(nuclei_data[i]['feret_diameter_max'][n])
                            nuclei_orientation.append(nuclei_data[i]['orientation'][n])
                            nuclei_axis_major_length.append(nuclei_data[i]['axis_major_length'][n])
                            nuclei_axis_minor_length.append(nuclei_data[i]['axis_minor_length'][n])
                            nuclei_circularity.append(nuclei_data[i]['circularity'][n])
                            nuclei_eccentricity.append(nuclei_data[i]['eccentricity'][n])
                            nuclei_perimeter.append(nuclei_data[i]['perimeter'][n])
                            nuclei_ratio.append(nuclei_data[i]['ratio'][n])
                            nuclei_solidity.append(nuclei_data[i]['solidity'][n])
                            
                            if 'spot_size_area' in nuclei_data[i].keys() :
                                if len(nuclei_data[i]['spot_size_area'][n]) > 0:
                                    spot_amount.append(len(nuclei_data[i]['spot_size_area'][n]))
                                    avg_spot_area.append(np.mean(nuclei_data[i]['spot_size_area'][n]))
                                    avg_spot_size_area_bbox.append(np.mean(nuclei_data[i]['spot_size_area_bbox'][n]))
                                    avg_spot_perimeter.append(np.mean(nuclei_data[i]['spot_perimeter'][n]))
                                    sum_spot_area.append(np.sum(nuclei_data[i]['spot_size_area'][n]))
                                    sum_spot_size_area_bbox.append(np.sum(nuclei_data[i]['spot_size_area_bbox'][n]))
                                    sum_spot_perimeter.append(np.sum(nuclei_data[i]['spot_perimeter'][n]))
                                    avg_spot_axis_major_length.append(np.mean(nuclei_data[i]['spot_axis_major_length'][n]))
                                    avg_spot_axis_minor_length.append(np.mean(nuclei_data[i]['spot_axis_minor_length'][n]))
                                    avg_spot_eccentricity.append(np.mean(nuclei_data[i]['spot_eccentricity'][n]))
                                    avg_spot_size_equivalent_diameter_area.append(np.mean(nuclei_data[i]['spot_size_equivalent_diameter_area'][n]))
                                    sum_spot_size_equivalent_diameter_area.append(np.sum(nuclei_data[i]['spot_size_equivalent_diameter_area'][n]))


                                else:
                                    spot_amount.append(0)
                                    avg_spot_area.append(0)
                                    avg_spot_size_area_bbox.append(0)
                                    avg_spot_perimeter.append(0)
                                    avg_spot_axis_major_length.append(0)
                                    avg_spot_axis_minor_length.append(0)
                                    avg_spot_eccentricity.append(0)
                                    avg_spot_size_equivalent_diameter_area.append(0)
                                    sum_spot_size_equivalent_diameter_area.append(0)
                                    sum_spot_area.append(0)
                                    sum_spot_size_area_bbox.append(0)
                                    sum_spot_perimeter.append(0)
                            
                        
                        if 'spot_size_area' in nuclei_data[i].keys() :
                            nuclei_df = pd.DataFrame({
                                
                                'id_name': id_name,
                                'nuclei_area': nuclei_area,
                                'nuclei_area_bbox': nuclei_area_bbox,
                                'nuclei_equivalent_diameter_area': nuclei_equivalent_diameter_area,
                                'nuclei_feret_diameter_max': nuclei_feret_diameter_max,
                                'nuclei_orientation': nuclei_orientation,
                                'nuclei_axis_major_length': nuclei_axis_major_length,
                                'nuclei_axis_minor_length': nuclei_axis_minor_length,
                                'nuclei_circularity': nuclei_circularity,
                                'nuclei_eccentricity': nuclei_eccentricity,
                                'nuclei_perimeter': nuclei_perimeter,
                                'nuclei_ratio': nuclei_ratio,
                                'nuclei_solidity': nuclei_solidity,
                                'spot_amount': spot_amount,
                                'avg_spot_area': avg_spot_area,
                                'avg_spot_area_bbox': avg_spot_size_area_bbox,
                                'avg_spot_perimeter': avg_spot_perimeter,
                                'sum_spot_area': sum_spot_area,
                                'sum_spot_area_bbox': sum_spot_size_area_bbox,
                                'sum_spot_perimeter': sum_spot_perimeter,
                                'avg_spot_axis_major_length': avg_spot_axis_major_length,
                                'avg_spot_axis_minor_length': avg_spot_axis_minor_length,
                                'avg_spot_eccentricity': avg_spot_eccentricity,
                                'avg_spot_size_equivalent_diameter_area': avg_spot_size_equivalent_diameter_area,
                                'sum_spot_size_equivalent_diameter_area': sum_spot_size_equivalent_diameter_area

                            })
                        
                        else:
                            nuclei_df = pd.DataFrame({
                                
                                'id_name': id_name,
                                'nuclei_area': nuclei_area,
                                'nuclei_area_bbox': nuclei_area_bbox,
                                'nuclei_equivalent_diameter_area': nuclei_equivalent_diameter_area,
                                'nuclei_feret_diameter_max': nuclei_feret_diameter_max,
                                'nuclei_orientation': nuclei_orientation,
                                'nuclei_axis_major_length': nuclei_axis_major_length,
                                'nuclei_axis_minor_length': nuclei_axis_minor_length,
                                'nuclei_circularity': nuclei_circularity,
                                'nuclei_eccentricity': nuclei_eccentricity,
                                'nuclei_perimeter': nuclei_perimeter,
                                'nuclei_ratio': nuclei_ratio,
                                'nuclei_solidity': nuclei_solidity
                                
                            })
                        
                        
                    nuclei_df['set'] = o
                
            
            final_df = pd.concat([final_df, nuclei_df])        
                    
                    
        self.mutual_data = final_df
        # self.mutual_metadata = self.create_metadata(final_df)
                



    def concat_IS_results(self, nuclei_data, data_sets:list = [], IS_data_path:str = os.getcwd(), IS_features:list = []):

        """
        Concatenates IS (Image Stream [https://cytekbio.com/pages/imagestream]) data with nuclei data and merges them based on object IDs.
        
        Args:
            nuclei_data (DataFrame) - the DataFrame containing nuclei data
            data_sets (list) - list of data sets to be used
            IS_data_path (str) - directory containing IS data files. Default is the current working directory
            IS_features (list) - list of features to be extracted from IS data. Default is an empty list
        
        """
       
        is_df = pd.DataFrame()
        
        
        file_list = os.listdir(IS_data_path)
        
        for o in tqdm(data_sets):
            print(o)
            for f in file_list:
                        
                if o in f and '.txt' in f:
                    isdata = pd.read_csv(os.path.join(IS_data_path,f), sep = '\t', header=1)
                    ot = [x for x in set(nuclei_data['set']) if o in x][0]
                    isdata['set'] = ot
                    is_df = pd.concat([is_df, isdata])
        
        if len(IS_features) > 0:
            IS_features = list(set(IS_features + ['Object Number', 'set']))
            is_df = is_df[IS_features]
                    
        nuclei_data['id'] = nuclei_data['id_name'].astype(str) + '_' + nuclei_data['set']
        is_df['id'] = is_df['Object Number'].astype(str) + '_' + is_df['set']
        
        merged_data = pd.merge(nuclei_data, is_df, on='id', how='left')
        merged_data.pop('set_x')
        merged_data = merged_data.rename(columns={
        'set_y': 'set'
        })
        
        
        self.mutual_IS_data = merged_data
        # self.mutual_IS_metadata = self.create_metadata(merged_data)

    
    
    
    

    def preapre_selected_img(self, path_to_images:str, 
                             file_extension:str = 'tiff', 
                             eq:bool = True, 
                             clahe:bool = True, 
                             kernal:tuple = (50,50), 
                             fille_name_part:str = '', 
                             selected_id:list = [], 
                             color = 'gray', 
                             max_intensity:int = 65535, 
                             min_intenisty:int = 0, 
                             brightness:int = 1000, 
                             contrast = 1.0, 
                             gamma = 1.0, 
                             img_n:int = 0):
          
         
        """
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


        """
       
        results_dict = {}
        
        files = glob.glob(os.path.join(path_to_images, "*." + file_extension))
        
        if len(selected_id) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if any(selected in x for selected in selected_id)]
            
        if len(fille_name_part) > 0:
            selected_id = [str(x) for x in selected_id]
            files = [x for x in files if fille_name_part.lower() in x.lower()]
        
        if img_n > 0:
            
            files = random.sample(files,  img_n)
        
        for file in tqdm(files):
            
            print(file)
                      
            image = jg.load_image(file)
            
            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            except:
                pass  
            
            if eq == True:
                image =  jg.equalizeHist_16bit(image)
        
            if clahe == True:
                image = jg.clahe_16bit(image, kernal = kernal)
             
             
         
         
            image = jg.adjust_img_16bit(img = image, color = color, max_intensity = max_intensity, min_intenisty = min_intenisty, brightness = brightness, contrast = contrast, gamma = gamma)
        
           
            results_dict[os.path.basename(file)] = image
            
              
        self.images = results_dict
        
    
   

        


        
        
        
class FeatureIntensity(ImageTools):
    
    def __init__(self, input_image = None, 
                image=None,   
                normalized_image_values = None,
                mask = None,
                background_mask = None,
                typ = None,
                size_info = None,
                correction_factor = None,
                show_plots = None,
                img_type = None,
                scale = None,
                stack_selection = None):
        

       self.input_image = input_image or None
       self.image = image or None
       self.normalized_image_values = normalized_image_values or None
       self.mask = mask or None
       self.background_mask = background_mask or None
       self.typ = typ or 'avg'
       self.size_info = size_info or None
       self.correction_factor = correction_factor or .1
       self.show_plots = show_plots or True
       self.scale = scale or None
       self.stack_selection = stack_selection or []




    @property
    def current_metadata(self):
        
        """
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
        
        """
        
        print(f'Projection type: {self.typ}') 
        print(f'Correction factor: {self.correction_factor}')
        print(f'Scale (unit/px): {self.scale}')
        print(f'Selected stac to remove: {self.stack_selection}')
        
        return self.typ, self.correction_factor, self.scale, self.stack_selection
    
        
    def set_projection(self, projection:str):
        
        """
        This method sets 'projection' parameter. The projection is a parameter used for 3D-image projection to 1D-image.
       
        Args:
           projection (str) - the projection value ['avg', 'median', 'std', 'var', 'max', 'min']. Default: 'avg'
 
        """
       
        t = ['avg', 'median', 'std', 'var', 'max', 'min']
        if projection in t:
            self.typ = projection
        else:
            print(f'\nProvided parameter is incorrect. Avaiable projection types: {t}')
            
    def set_correction_factorn(self, factor:float):
        
        """
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
 
        """
       
        if factor < 1 and factor > 0:
            self.correction_factor = factor
        else:
            print('\nProvided parameter is incorrect. The factor should be a floating-point value within the range of 0 to 1.')
            
    def set_scale(self, scale):
        
        """
        This method sets the 'scale' parameter. The scale is used to calculate the actual size of the tissue or organ.
        
        The scale is also loaded using the load_JIMG_project_() method.
        
        Args:
           scale (float) - the scale value [um/px]
 
        """
        
        self.scale = scale
       
    def set_selection_list(self, rm_list:list):
        
        """
        This method sets the 'rm_list' parameter. The 'rm_list' is used to exclude partial z-axis images from the full 3D image in the projection.

        Args:
           rm_list (list) - list of images to remove.
 
        """
        
        
        self.stack_selection = rm_list
       
        
    def load_JIMG_project_(self, path):
        
        
        """
        This method loads a JIMG project. The project file must have the *.pjm extension.
        
        Args:
            file_path (str) - path to the project file.
    
        Returns:
            project (class) - loaded project object
    
        Raises:
            ValueError: If the file does not have a *.pjm extension.
        
        """
       
        
        if '.pjm' in path:
            metadata = self.load_JIMG_project(path)
    
            try:
                self.scale = metadata.metadata['X_resolution[um/px]']
            except:
                
                try:
                    self.scale = metadata.images_dict['metadata'][0]['X_resolution[um/px]']
                
                except: 
                    print('\nUnable to set scale on this project! Set scale using "set_scale()"')
                
            self.stack_selection = metadata.removal_list

            
        else:
            print('\nWrong path. The provided path does not point to a JIMG project (*.pjm).')
        
        
       
    def stack_selection_(self):
        if len(self.input_image.shape) == 3:
            if len(self.stack_selection) > 0:
                self.input_image = self.input_image[[x for x in range(self.input_image.shape[0]) if x not in self.stack_selection]]
            else:
                print('\nImages to remove from the stack were not selected!')
       

    def projection(self):
        
        if self.typ == 'avg':
            img = np.mean(self.input_image, axis=0)

        elif self.typ == 'std':
            img = np.std(self.input_image, axis=0)

        elif self.typ == 'median':
            img = np.median(self.input_image, axis=0)

        elif self.typ == 'var':
            img = np.var(self.input_image, axis=0)

        elif self.typ == 'max':
            img = np.max(self.input_image, axis=0)

        elif self.typ == 'min':
            img = np.min(self.input_image, axis=0)
            
        self.image = img
            
     
    def detect_img(self):
        check = len(self.input_image.shape)
        
        if check == 3:
            print('\n3D image detected! Starting processing for 3D image...')
            print(f'Projection - {self.typ}...')
            
            self.stack_selection_()
            self.projection()
            
        elif check == 2:
            print('\n2D image detected! Starting processing for 2D image...')
            
        else:
            print('\nData does not match any image type!')
            
            
    def load_image_3D(self, path):
        
        """
        This method loads an 3D-image (*.tiff) into the class.

        Args:
            path (str) - path to the *.tiff image.
        
        """
        
        self.input_image = self.load_3D_tiff(path)


    def load_image_(self, path):
        
        """
        This method loads an image into the class.

        Args:
            path (str) - path to the image.
        
        """
        
        self.input_image = self.load_image(path)

        
    def load_mask_(self, path):
        
             
        """
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
        
        """
        
        self.mask = self.load_mask(path)
        
        print("\nThis mask was also set as the reverse background mask. If you want a different background mask for normalization, use 'load_normalization_mask()'.")
        self.background_mask = self.load_mask(path)


    def load_normalization_mask_(self, path):
        
        """
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
        
        """
        
        self.background_mask = self.load_mask(path)

    
    def intensity_calculations(self):
        tmp_mask = self.ajd_mask_size(image = self.image, mask = self.mask)
        tmp_bmask = self.ajd_mask_size(image = self.image, mask = self.background_mask)
        
        
        selected_values = self.image[tmp_mask == np.max(tmp_mask)]

        threshold = np.mean(self.image[tmp_bmask == np.min(tmp_bmask)])
        
        # normalization
        final_val = selected_values - (threshold+(threshold*self.correction_factor))

        final_val[final_val < 0] = 0
        

        tmp_dict = {'norm_min':np.min(final_val), 
                    'norm_max':np.max(final_val), 
                    'norm_mean':np.mean(final_val),
                    'norm_median':np.median(final_val),
                    'norm_std':np.std(final_val),
                    'norm_var':np.var(final_val),
                    'norm_values':final_val.tolist(),
                    'min':np.min(selected_values), 
                    'max':np.max(selected_values), 
                    'mean':np.mean(selected_values),
                    'median':np.median(selected_values),
                    'std':np.std(selected_values),
                    'var':np.var(selected_values)}
        
        self.normalized_image_values = tmp_dict
    
    
    
    def size_calculations(self):
        
        tmp_mask = self.ajd_mask_size(image = self.image, mask = self.mask)
        
        size_px = int(len(tmp_mask[tmp_mask > np.min(tmp_mask)]))
        
        
        if self.scale is not None:
            size = float(size_px*self.scale)
        else:
            size = None
            print('\nUnable to calculate real size, scale (unit/px) not provided, use "set_scale()" or load JIMG project .pjm metadata "load_pjm()" to set scale for calculations!')
            
        non_zero_indices = np.where(tmp_mask == np.max(tmp_mask))

        min_y, max_y = np.min(non_zero_indices[0]), np.max(non_zero_indices[0])
        min_x, max_x = np.min(non_zero_indices[1]), np.max(non_zero_indices[1])
        
        max_length_x_axis = int(max_x - min_x + 1)
        max_length_y_axis = int(max_y - min_y + 1)
        


        tmp_val = {'size':size, 
                   'px_size':size_px,
                   'max_length_x_axis':max_length_x_axis,
                   'max_length_y_axis':max_length_y_axis}

        self.size_info = tmp_val


    def run_calculations(self):
        
        """
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

               
        """
        
        if self.input_image is not None:
            
            if self.mask is not None:
                
                print('\nStart...')
                self.detect_img()
                self.intensity_calculations()
                self.size_calculations()
                print('\nCompleted!')
                
                
    def get_results(self):
        
        """
        This method returns the results from the `run_calculations()` method in dictionary format.

        
        Returns:
        
            results_dict (dict) - dictionary containing results from run_calculations()
               
        """
        
        
        if self.normalized_image_values is not None and self.size_info is not None:
        
            results = {'intensity':self.normalized_image_values,
                     'size':self.size_info}
        
            return results
        
        else:
            print('\nAnalysis were not conducted. Run analysis "run_calculations()"')
                
            
    def save_results(self, path = os.getcwd(), 
                     mask_region:str = '', 
                     feature_name:str = '', 
                     individual_number:int = 0, 
                     individual_name:str = ''):
        
        """
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
      
            
        """
  
        if len(mask_region) > 1 and len(feature_name) > 1 and individual_number != 0 and len(individual_name) > 1: 
        
            if self.normalized_image_values is not None and self.size_info is not None:
            
                results = {'intensity':self.normalized_image_values,
                         'size':self.size_info}
                
                mask_region = re.sub(r'[_\s]+', '.', mask_region)
                feature_name = re.sub(r'[_\s]+', '.', feature_name)
                individual_number = re.sub(r'[_\s]+', '.', str(individual_number))
                individual_name = re.sub(r'[_\s]+', '.', individual_name)
            
                full_name = f'{individual_name}_{individual_number}_{mask_region}_{feature_name}'  

                   
                isExist = os.path.exists(path)
                if not isExist:
                   os.makedirs(path, exist_ok=True)
                
                
                full_path = os.path.join(path, re.sub('\\.json', '', full_name) + '.int')
                
                with open(full_path, 'w') as file:
                    json.dump(results, file, indent=4)
            
            else:
                print('\nAnalysis were not conducted. Run analysis "run_calculations()"')
        
        else:
            print("\nAny of 'mask_region', 'feature_name', 'individual_number', 'individual_name' parameters were provided wrong!")
                     
            
            
            
            
    def concatenate_intensity_data(self,  directory:str = os.getcwd(), name:str = ''):
        
        """
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
            
        """
   
       
        files_list = [f for f in os.listdir(directory) if f.endswith('.int')]
        
                
        genes_set = set([re.sub('\\.int', '', x.split('_')[3]) for x in files_list])
        regions_set = set([re.sub('\\.int', '', x.split('_')[2]) for x in files_list])
    
    
        for g in genes_set:
            for r in regions_set:
                json_to_save = {'individual_name':[], 'individual_number':[], 'norm_intensity':[], 'size':[]}
    
                for f in tqdm(files_list):
                    if g in f and r in f:
                        with open(os.path.join(directory, f), 'r') as file:
                            data = json.load(file)
                            
                            json_to_save['norm_intensity'] = json_to_save['norm_intensity'] + data['intensity']['norm_values']
                            json_to_save['individual_name'] = json_to_save['individual_name'] + [f.split('_')[0]] * len(data['intensity']['norm_values'])
                            json_to_save['individual_number'] = json_to_save['individual_number'] + [f.split('_')[1]] * len(data['intensity']['norm_values'])
                            json_to_save['size'] = json_to_save['size'] + [data['size']['px_size']] * len(data['intensity']['norm_values'])
                        
                      
        
        pd.DataFrame(json_to_save).to_csv(f'{name}_{g}_{r}.csv', index=False)
    


   

class IntensityAnalysis:
    
    
    def drop_up_df(self, data:pd.DataFrame, group_col:str, values_col:str):
        
        """
        Removes upper outliers from the DataFrame based on the specified value column and grouping column.
        Outliers are calculated and removed separately for each group defined by the grouping column.
   
        Args:
            data (pd.DataFrame) - the input DataFrame
            group_col (str) - the name of the column used for grouping
            values_col (str) - the column containing the values from which upper outliers will be removed
     
        Returns:
            filtered_data (pd.DataFrame) - a filtered DataFrame with the upper outliers removed
            
       """
        
        def iqr_filter(group):
            q75 = np.quantile(group[values_col], 0.75)
            q25 = np.quantile(group[values_col], 0.25)
            itq = q75 - q25
            return group[group[values_col] <= (q75 + 1.5 * itq)]

        filtered_data = data.groupby(group_col).apply(iqr_filter).reset_index(drop=True)
        
        return filtered_data
        
        
            
            
    
    def percentiles_calculation(self, values, sep_perc:int = 1):
        
        """
        Calculates percentiles for a given set of values with a specified separation interval. 

        This function computes percentiles from 0 to 100, at intervals defined by the `sep_perc` parameter.
        Additionally, it creates a loopable list of percentile ranges, useful for further data analysis or binning.
     
        Args:
            values (array-like) - the input data values for which the percentiles are calculated
            sep_perc (int) - the separation between percentiles (default is 1, meaning percentiles are calculated at every 1%)
     
        Returns:
            percentiles (np.ndarray) - nn array of calculated percentile values
            percentiles_loop (list of tuples) - a list of tuples representing consecutive percentile ranges (e.g., [(0, 1), (1, 2), ...])
        
        """
        
        per_vector = values.copy()
        
        percentiles = np.percentile(per_vector, np.arange(0, 101, sep_perc))
        percentiles[0] = 0
        
        percentiles_loop = [(i, i+1) for i in range(int(100/sep_perc))]
        
        return percentiles, percentiles_loop

        
    
    def to_percentil(self, values, percentiles, percentiles_loop):
        
            
        """
        Aggregates statistics for a given set of values based on calculated percentile ranges.
 
        This function calculates summary statistics (e.g., count, average, median, standard deviation, and variance) for each percentile range 
        in `percentiles_loop`. The results are based on the percentiles calculated in the `percentiles_calculation()` method.
     
        Parameters:
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
        
        """
        
        per_vector = values.copy()
        
    
        data = {'n':[], 'n_standarized':[], 'avg':[], 'median':[], 'std':[], 'var':[]}
        
        amount = len(per_vector)

        
        for x in percentiles_loop:
            if len(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]) > 0:
                data['n'].append(len(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]))
                data['n_standarized'].append(len(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])])/amount)
                data['avg'].append(np.mean(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]))
                data['std'].append(np.std(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]))
                data['median'].append(np.median(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]))
                data['var'].append(np.var(per_vector[(per_vector > percentiles[x[0]]) & (per_vector <= percentiles[x[1]])]))
            else:
                data['n'].append(1)
                data['n_standarized'].append(0)
                data['avg'].append(0)
                data['std'].append(0)
                data['median'].append(0)
                data['var'].append(0)
            
        return data
        
        
        
        
    def df_to_percentiles(self, data:pd.DataFrame, group_col:str, values_col:str, sep_perc:int = 1, drop_outlires:bool = True):
        
        """
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
                
        """
        
        full_data = {}
        
        if drop_outlires == True:
            data = self.drop_up_df(data = data, group_col = group_col, values_col = values_col)
            
        groups = set(data[group_col])
        
        percentiles, percentiles_loop = self.percentiles_calculation(data[values_col], sep_perc = sep_perc)
        
        for g in groups:
            
            print(f'Group: {g} ...')
            
            tmp_values = data[values_col][data[group_col] == g]
            
            per_dat = self.to_percentil(tmp_values,  percentiles, percentiles_loop)

            full_data[g] = per_dat
        
        return full_data


    def round_to_scientific_notation(self, num):
        if num == 0:
            return "0.0"
        
        if abs(num) < 0.0001:
            rounded_num = np.format_float_scientific(num, precision=1, exp_digits=1)
            return rounded_num
        else:
            return f"{num:.1f}"


    def aov_percentiles(self, data, testes_col, comb:str = '*'):
        
        """
        Performs a Welch's ANOVA on percentile-based group data.
        
        This method calculates group values by combining the columns specified in `testes_col` according to the operation defined in `comb`. 
        It then performs a Welch's ANOVA to test for differences in means between the groups. Welch's ANOVA is suitable when the groups have 
        unequal variances.
        
        Parameters:
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
            
            
        """
        
        groups = []
   
        for d in data.keys():
            
            if isinstance(testes_col, str):
                g = data[d][testes_col]
            elif isinstance(testes_col, list):
                g = [1]*len(data[d][testes_col[0]])
                for t in testes_col:
                    if comb == '*':
                        g = [a * b for a, b in zip(g, data[d][t])]
                    elif comb == '+':
                        g = [a + b for a, b in zip(g, data[d][t])]
                    elif comb == '**':
                        g = [a ** b for a, b in zip(g, data[d][t])]
                    elif comb == '-':
                        g = [a - b for a, b in zip(g, data[d][t])]
                    elif comb == '/':
                        g = [a / b for a, b in zip(g, data[d][t])]
            
            groups.append(g)
        
        df = pd.DataFrame({f'group_{i}': group for i, group in enumerate(groups)})
        
        df_melted = df.melt(var_name='group', value_name='value')
        

        welch_results = pg.welch_anova(data=df_melted, dv='value', between='group')
        
        return welch_results['F'].values[0], welch_results['p-unc'].values[0]



    def post_aov_percentiles(self, data, testes_col, comb:str = '*'):
        
        """
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
                
        """
    
        
        p_val = self.aov_percentiles(data = data, testes_col = testes_col, comb = comb)[1]
        
            
        pairs = list(combinations(data, 2))
        final_results = {'group1':[], 'group2':[], 'stat':[], 'p_val':[], 'adj_p_val':[]}

        for (group1, group2) in pairs:
            if isinstance(testes_col, str):
                g1 = data[group1][testes_col]
            elif  isinstance(testes_col, list):
                g1 = [1]*len(data[group1][testes_col[0]])
                for t in testes_col:
                    if comb == '*':
                        g1 = [a * b for a, b in zip(g1, data[group1][t])]
                    elif comb == '+':
                        g1 = [a + b for a, b in zip(g1, data[group1][t])]
                    elif comb == '**':
                        g1 = [a ** b for a, b in zip(g1, data[group1][t])]
                    elif comb == '-':
                        g1 = [a - b for a, b in zip(g1, data[group1][t])]
                    elif comb == '/':
                        g1 = [a / b for a, b in zip(g1, data[group1][t])]
            
            if isinstance(testes_col, str):
                g2 = data[group2][testes_col]
            elif isinstance(testes_col, list):
                g2 = [1]*len(data[group2][testes_col[0]])
                for t in testes_col:
                    if comb == '*':
                        g2 = [a * b for a, b in zip(g2, data[group2][t])]
                    elif comb == '+':
                        g2 = [a + b for a, b in zip(g2, data[group2][t])]
                    elif comb == '**':
                        g2 = [a ** b for a, b in zip(g2, data[group2][t])]
                    elif comb == '-':
                        g2 = [a - b for a, b in zip(g2, data[group2][t])]
                    elif comb == '/':
                        g2 = [a / b for a, b in zip(g2, data[group2][t])]
                        
            stat, p_val = stats.ttest_ind(g1, g2, alternative='two-sided', equal_var = False)
            g = sorted([group1, group2])
            final_results['group1'].append(g[0])
            final_results['group2'].append(g[1])
            final_results['stat'].append(stat)
            final_results['p_val'].append(p_val)
            adj = p_val*len(pairs)
            if adj > 1:
                final_results['adj_p_val'].append(1)
            else:
                final_results['adj_p_val'].append(adj) 
            
            
        return p_val, final_results

          


    def chi2_percentiles(self, input_hist):
        
        """
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
            
        """
        
        chi_data = {}
        
        for d in input_hist.keys():
            tmp_dic = {}
            
        
            for n, c in enumerate(input_hist[d]['n']):
                tmp_dic[f'p{n+1}'] = c
                
            chi_data[d] = tmp_dic
            
            
        chi2_statistic, p_value, dof, expected = chi2_contingency(pd.DataFrame(chi_data).T, correction=True)
        
        return chi2_statistic, p_value, dof, expected, chi_data



            
        
    def post_ch2_percentiles(self, input_hist):
        
        
        """
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
        
        """
        
        res = self.chi2_percentiles(input_hist)
        
        pairs = list(combinations(res[4], 2))
        results = []
      
        for (group1, group2) in pairs:
            table_pair = pd.DataFrame(res[4])[[group1, group2]]
            chi2_stat, p_val, _, _ = chi2_contingency(table_pair, correction=True)
            results.append((group1, group2, chi2_stat, p_val))
      
      
        
        final_results = {'group1':[], 'group2':[], 'chi2':[], 'p_val':[], 'adj_p_val':[]}
        
        for group1, group2, chi2_stat, p_val in results:
            g = sorted([group1, group2])
            final_results['group1'].append(g[0])
            final_results['group2'].append(g[1])
            final_results['chi2'].append(chi2_stat)
            final_results['p_val'].append(p_val)
            adj = p_val*len(results)
            if adj > 1:
                final_results['adj_p_val'].append(1)
            else:
                final_results['adj_p_val'].append(adj)

                

        return res[1], final_results
        
    
    def hist_compare_plot(self, data, queue, tested_value, p_adj:bool = True, txt_size:int = 20):
        
        """
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
        
        """
        
        from scipy import stats

        for i in data.keys():
            values = np.array(data[i][tested_value])  
            values += 1 
            transformed_values, fitted_lambda = stats.boxcox(values)
            data[i][tested_value] = transformed_values.tolist()
            
        
        
        
        if sorted(queue) != sorted(data.keys()):
            print('\n Wrong queue provided! The queue will be sorted with default settings!')
            queue = sorted(data.keys())
                
        # parametric selected value
        pk, dfk = self.post_aov_percentiles(data, testes_col = tested_value)
      
        dfk = pd.DataFrame(dfk)
        
        dfk = dfk.sort_values(
            by=['group1', 'group2'],
            key=lambda col: [queue.index(val) if val in queue else -1 for val in col]
        ).reset_index(drop = True)   
        
        
        # parametric standarized selected value
        pkc, dfkc = self.post_aov_percentiles(data, testes_col = [tested_value, 'n_standarized'], comb = '*')
      
        dfkc = pd.DataFrame(dfkc)
        
        dfkc = dfkc.sort_values(
            by=['group1', 'group2'],
            key=lambda col: [queue.index(val) if val in queue else -1 for val in col]
        ).reset_index(drop = True)    
    
    
        # chi2
        pchi, dfchi = self.post_ch2_percentiles(data)
        
        
        dfchi = pd.DataFrame(dfchi)
        
        dfchi = dfchi.sort_values(
            by=['group1', 'group2'],
            key=lambda col: [queue.index(val) if val in queue else -1 for val in col]
        ).reset_index(drop = True)   
        
        
        ##############################################################################
    
        standarized_max, standarized_min, value_max, value_min = [], [], [], []
        for d in queue:
            standarized_max.append(max(data[d]['n_standarized']))
            standarized_min.append(min(data[d]['n_standarized']))
            value_max.append(max(data[d][tested_value]))
            value_min.append(min(data[d][tested_value]))
        
        num_columns = len(queue) + 1
        
        fig, axs = plt.subplots(3, num_columns, figsize=(8 * num_columns, 10),
                                gridspec_kw={'width_ratios': [1] * len(queue) + [0.5], 'wspace': 0.05}) 
            
        for i, d in enumerate(queue):
            tmp_data = data[d]
        
            axs[0, i].bar([str(n) for n in range(len(tmp_data['n_standarized']))], tmp_data['n_standarized'], 
                          width=0.95, color='gold')
            axs[0, i].set_ylim(min(standarized_min) * 0.9995, max(standarized_max) * 1.0005)
            
            if i == 0:
                axs[0, i].set_ylabel('Standarized\nfrequency', fontsize = txt_size)
            else:
                axs[0, i].set_yticks([])
        
            axs[0, i].set_xticks([])
            axs[0, i].tick_params(axis='y', labelsize=txt_size*.7)
        
            axs[1, i].bar([str(n) for n in range(len(tmp_data[tested_value]))], tmp_data[tested_value], 
                          width=0.95, color='orange')
            
            mean_value = np.mean(tmp_data[tested_value])
            axs[1, i].axhline(y=mean_value, color='red', linestyle='--')
            
            # axs[1, i].set_ylim(min(value_min) - 1, max(value_max) + 1)
            axs[1, i].set_ylim(min(value_min) * 0.9995, max(value_max) * 1.0005)
            
            if i == 0:
                axs[1, i].set_ylabel(f'Normalized\n{tested_value}', fontsize = txt_size)
            else:
                axs[1, i].set_yticks([])
        
            axs[1, i].set_xticks([])
            axs[1, i].tick_params(axis='y', labelsize=txt_size*.7)
            
            
            
            axs[2, i].bar([str(n) for n in range(len(tmp_data['n_standarized']))], [a * b for a, b in zip(tmp_data[tested_value],  tmp_data['n_standarized'])], 
                          width=0.95, color='goldenrod')
            
            mean_value = np.mean([a * b for a, b in zip(tmp_data[tested_value],  tmp_data['n_standarized'])])
            axs[2, i].axhline(y=mean_value, color='red', linestyle='--')
            
            
            axs[2, i].set_ylim((min(standarized_min)*min(value_min)) * 0.9995, (max(standarized_max)*max(value_max) * 1.0005))
            axs[2, i].set_xlabel(d, fontsize = txt_size)

            if i == 0:
                axs[2, i].set_ylabel(f'Standarized\nnorm_{tested_value}', fontsize = txt_size)
            else:
                axs[2, i].set_yticks([])
        
            axs[2, i].set_xticks([])
            axs[2, i].tick_params(axis='y', labelsize=txt_size*.7)
    
        
        sign = 'ns'
        if float(self.round_to_scientific_notation(pk)) < 0.001:
            sign = '***'
        elif float(self.round_to_scientific_notation(pk)) < 0.01:
            sign = '**'
        elif float(self.round_to_scientific_notation(pk)) < 0.05:
            sign = '*'
        
        text = f"Test Welch's ANOVA\np-value: {self.round_to_scientific_notation(pk)} - {sign}\n"
        
        if p_adj == True:
            for i in range(len(dfk['group1'])):
                sign = 'ns'
                if dfk['adj_p_val'][i] < 0.001:
                    sign = '***'
                elif dfk['adj_p_val'][i] < 0.01:
                    sign = '**'
                elif dfk['adj_p_val'][i] < 0.05:
                    sign = '*'
                
                text += f"{dfk['group1'][i]} vs. {dfk['group2'][i]}\np-value: {self.round_to_scientific_notation(dfk['adj_p_val'][i])} - {sign}\n"
        else:
            for i in range(len(dfk['group1'])):
                sign = 'ns'
                if dfk['p_val'][i] < 0.001:
                    sign = '***'
                elif dfk['p_val'][i] < 0.01:
                    sign = '**'
                elif dfk['p_val'][i] < 0.05:
                    sign = '*'
                    
                text += f"{dfk['group1'][i]} vs. {dfk['group2'][i]}\np-value: {self.round_to_scientific_notation(dfk['p_val'][i])} - {sign}\n"
                
        axs[1, -1].text(0.5, 0.5, text, ha='center', va='center', fontsize=txt_size*.7, wrap=True)
        axs[1, -1].set_axis_off()
        
        sign = 'ns'
        if float(self.round_to_scientific_notation(pkc)) < 0.001:
            sign = '***'
        elif float(self.round_to_scientific_notation(pkc)) < 0.01:
            sign = '**'
        elif float(self.round_to_scientific_notation(pkc)) < 0.05:
            sign = '*'
            
        text = f"Test Welch's ANOVA\np-value: {self.round_to_scientific_notation(pkc)} - {sign}\n"
        
        if p_adj == True:
            for i in range(len(dfkc['group1'])):
                sign = 'ns'
                if dfkc['adj_p_val'][i] < 0.001:
                    sign = '***'
                elif dfkc['adj_p_val'][i] < 0.01:
                    sign = '**'
                elif dfkc['adj_p_val'][i] < 0.05:
                    sign = '*'
                    
                text += f"{dfkc['group1'][i]} vs. {dfkc['group2'][i]}\np-value: {self.round_to_scientific_notation(dfkc['adj_p_val'][i])} - {sign}\n"
        else:
            for i in range(len(dfkc['group1'])):
                sign = 'ns'
                if dfkc['p_val'][i] < 0.001:
                    sign = '***'
                elif dfkc['p_val'][i] < 0.01:
                    sign = '**'
                elif dfkc['p_val'][i] < 0.05:
                    sign = '*'
                    
                text += f"{dfkc['group1'][i]} vs. {dfkc['group2'][i]}\np-value: {self.round_to_scientific_notation(dfkc['p_val'][i])} - {sign}\n"
                
        axs[2, -1].text(0.5, 0.5, text, ha='center', va='center', fontsize=txt_size*.7, wrap=True)
        axs[2, -1].set_axis_off()
        
        sign = 'ns'
        if float(self.round_to_scientific_notation(pchi)) < 0.001:
            sign = '***'
        elif float(self.round_to_scientific_notation(pchi)) < 0.01:
            sign = '**'
        elif float(self.round_to_scientific_notation(pchi)) < 0.05:
            sign = '*'
            
        text = f"Test Chi-squared\np-value: {self.round_to_scientific_notation(pchi)} - {sign}\n"
        
        if p_adj == True:
            for i in range(len(dfchi['group1'])):
                sign = 'ns'
                if dfchi['adj_p_val'][i] < 0.001:
                    sign = '***'
                elif dfchi['adj_p_val'][i] < 0.01:
                    sign = '**'
                elif dfchi['adj_p_val'][i] < 0.05:
                    sign = '*'
                    
                text += f"{dfchi['group1'][i]} vs. {dfchi['group2'][i]}\np-value: {self.round_to_scientific_notation(dfchi['adj_p_val'][i])} - {sign}\n"
        else:
            for i in range(len(dfchi['group1'])):
                sign = 'ns'
                if dfchi['p_val'][i] < 0.001:
                    sign = '***'
                elif dfchi['p_val'][i] < 0.01:
                    sign = '**'
                elif dfchi['p_val'][i] < 0.05:
                    sign = '*'
                    
                text += f"{dfchi['group1'][i]} vs. {dfchi['group2'][i]}\np-value: {self.round_to_scientific_notation(dfchi['p_val'][i])} - {sign}\n"
            
        axs[0, -1].text(0.5, 0.5, text, ha='center', va='center', fontsize=txt_size*.7, wrap=True)
        axs[0, -1].set_axis_off()
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    
    
    
class GroupAnalysis:
    
    # basic method
    
    
    def statistic(self, input_df, sets = None, metadata = None, n_proc = 10):
        
        try:
        
            offset = 1e-100
            
            #Fun
            final_dict = None
            
            def stat_calc(choose, i):
                
                test = []
                perc_traget = []
                perc_rest = []
                feature = []
                avg_valid = []
                avg_ctrl = []
                
                
                table = {'p_val':test, 'pct_valid':perc_traget, 'pct_ctrl':perc_rest, 'avg_valid':avg_valid, 'avg_ctrl':avg_ctrl,  'feature':feature}
        
        
                table['pct_valid'].append(len(choose[i][(choose['DEG'] == 'target') & (choose[i][(choose['DEG'] == 'target')] > 0)]) / len(choose[i][(choose['DEG'] == 'target')]))
                table['pct_ctrl'].append(len(choose[i][(choose['DEG'] == 'rest') & (choose[i][(choose['DEG'] == 'rest')] > 0)]) / len(choose[i][(choose['DEG'] == 'rest')]))
                table['feature'].append(i)
                table['avg_valid'].append(np.mean(choose[i][choose['DEG'] == 'target']))
                table['avg_ctrl'].append(np.mean(choose[i][choose['DEG'] == 'rest']))
        
                if np.sum(choose[i][choose['DEG'] == 'target']) == np.sum(choose[i][choose['DEG'] == 'rest']):
                    table['p_val'].append(1)
                else:
                    f,p = stats.mannwhitneyu(choose[i][choose['DEG'] == 'target'], choose[i][choose['DEG'] == 'rest'])
                    table['p_val'].append(p)
                        
                return table
         
        
            #cells:
            choose = input_df.copy().transpose()
               
            
            
            if  sets == None:
                      
                print('\nAnalysis started...')
                print('\nComparing each type of cell to others...')
                
                final_dict = pd.DataFrame()

                if len(set(metadata['sets'])) > 1:
                    choose.index = metadata['sets']
                    
        
                indexes = list(choose.index)
        
                for c in set(indexes):
                    print('Calculating statistics for ' + str(c))
                    indexes_tmp = []
                    choose.index = indexes
                    for i, n in enumerate(indexes):
                        if n == c:
                            indexes_tmp.append('target')
                        else:
                            indexes_tmp.append('rest')
                            
                    choose['DEG'] = indexes_tmp
                
                
                    valid = ','.join(list(set(choose.index[choose['DEG'] == 'target'])))
                
                    choose = choose.reset_index(drop=True)
                    choose = choose.loc[:,list((choose!=0).any(axis=0))]
                    
                    
                    table = Parallel(n_jobs=n_proc)(delayed(stat_calc)(choose, i) for i in tqdm(choose.columns[choose.columns != 'DEG']))
                    
            
                    combined_dict = {}
                    for d in tqdm(table):
                        for key, value in d.items():
                            if key not in combined_dict:
                                combined_dict[key] = []
                            combined_dict[key] = combined_dict[key] + value
                        
                            
                    combined_dict = pd.DataFrame(combined_dict) 
                    combined_dict['valid_group'] = valid
                    combined_dict = combined_dict.sort_values(by = 'p_val', ascending = True)
                    combined_dict['adj_pval'] = (combined_dict['p_val'] * int(len(combined_dict['p_val']))) / np.arange(1, int(len(combined_dict['p_val']))+1)
                    combined_dict['adj_pval'][combined_dict['adj_pval'] >= 1] = 1
                    combined_dict['-log(p_val)'] = -np.log10(offset + combined_dict['p_val'])
                    low_factor = min(i for i in (np.array(combined_dict['avg_valid']) + np.array(combined_dict['avg_ctrl'])) if i > 0) * 0.95
                    combined_dict['FC'] = ((np.array(combined_dict['avg_valid'])) + low_factor) / ((np.array(combined_dict['avg_ctrl'])) + low_factor) 
                    combined_dict['log(FC)'] = np.log2(combined_dict['FC'])
                    combined_dict['norm_diff'] = ((np.array(combined_dict['avg_valid'])) + low_factor) - ((np.array(combined_dict['avg_ctrl'])))
                    combined_dict = combined_dict.sort_values(by = ['p_val'], ascending = True)
           
                
                
            
                    final_dict = pd.concat([final_dict, combined_dict])
                    
                print('\nAnalysis has finished!')
                        
          
                
            elif sets and isinstance(sets, dict):
                
                print('\nAnalysis started...')
                print('\nComparing groups...')
                
                final_dict = pd.DataFrame()
                
                group_list = list(sets.keys())
        
                choose.index = metadata['sets']
                
                inx = []
                for x in sets.values(): 
                    inx = inx + x
                  
                inx.sort()
                choose = choose.loc[list(inx),:]
                

                print('Calculating statistics for ' + str(group_list[0]))
                
                indexes_tmp = []
                tmp_inx = list(metadata['sets'][metadata['sets'].isin(inx)])
                tmp_inx.sort()
                choose.index = tmp_inx
                for i, n in enumerate(choose.index):
                    if n in list(metadata['sets'][metadata['sets'].isin(sets[group_list[0]])]):
                        indexes_tmp.append('target')
                    elif n in list(metadata['sets'][metadata['sets'].isin(sets[group_list[1]])]):
                        indexes_tmp.append('rest')
                    else:
                        indexes_tmp.append('drop')
                        
                        
                choose['DEG'] = indexes_tmp
                choose = choose[choose['DEG'] != 'drop']
                
                valid = group_list[0]
            
                choose = choose.reset_index(drop=True)
                choose = choose.loc[:,list((choose!=0).any(axis=0))]
                
                
                table = Parallel(n_jobs=n_proc)(delayed(stat_calc)(choose, i) for i in tqdm(choose.columns[choose.columns != 'DEG']))
                
        
                combined_dict = {}
                for d in tqdm(table):
                    for key, value in d.items():
                        if key not in combined_dict:
                            combined_dict[key] = []
                        combined_dict[key] = combined_dict[key] + value
                    
                        
                combined_dict = pd.DataFrame(combined_dict) 
                combined_dict['valid_group'] = valid
                combined_dict = combined_dict.sort_values(by = 'p_val', ascending = True)
                combined_dict['adj_pval'] = (combined_dict['p_val'] * int(len(combined_dict['p_val']))) / np.arange(1, int(len(combined_dict['p_val']))+1)
                combined_dict['adj_pval'][combined_dict['adj_pval'] >= 1] = 1
                combined_dict['-log(p_val)'] = -np.log10(offset + combined_dict['p_val'])
                low_factor = min(i for i in (np.array(combined_dict['avg_valid']) + np.array(combined_dict['avg_ctrl'])) if i > 0) * 0.95
                combined_dict['FC'] = ((np.array(combined_dict['avg_valid'])) + low_factor) / ((np.array(combined_dict['avg_ctrl'])) + low_factor) 
                combined_dict['log(FC)'] = np.log2(combined_dict['FC'])
                combined_dict['norm_diff'] = ((np.array(combined_dict['avg_valid'])) + low_factor) - ((np.array(combined_dict['avg_ctrl'])))
                combined_dict = combined_dict.sort_values(by = ['p_val'], ascending = True)
       

                final_dict = pd.concat([final_dict, combined_dict])
                
                
                print('\nAnalysis has finished!')
                
            else:
                print('\nNo suitable parameters found. Check the parameters entered into the function or refer to the documentation') 
                    
            return final_dict
        
        except:
            print("Something went wrong. Check the function input data and try again!")
    
    
    


    
    def __init__(self, input_data = None,
                 input_metadata = None,
                 tmp_metadata = None,
                 tmp_data = None,
                 scaled_data = None,
                 PCA_results = None,
                 var_data = None,
                 knee_plot = None,
                 UMAP_data = None,
                 UMAP_plot = None,
                 dblabels = None,
                 explained_variance_ratio = None):
        
        self.input_data = input_data or None
        self.input_metadata = input_metadata or None
        self.tmp_metadata = tmp_metadata or None
        self.tmp_data = tmp_data or None
        self.scaled_data = scaled_data or None
        self.PCA_results = PCA_results or None
        self.var_data = var_data or None
        self.knee_plot = knee_plot or None
        self.UMAP_data = UMAP_data or None
        self.UMAP_plot = UMAP_plot or {}
        self.dblabels = dblabels or None
        self.explained_variance_ratio = explained_variance_ratio or None


    @property
    def groups(self):
        
        """
        Returns information about available groups in the metadata for self.DFA.

           Returns:
               dict: A dictionary where each key is a column name, and each value is a list of available groups
                     in that column.

        """
        
        try:
            return {'sets':set(self.tmp_metadata['sets']), 'full_name':set(self.tmp_metadata['full_name'])}
        except:
            return {'sets':set(self.tmp_metadata['sets'])}



    def get_PCA(self):
        
        """
        Retrieve the PCA results from the PCA() method.
      
        Returns:
            PCA_results (np.ndarray) - the PCA results stored in `self.PCA_results`
      
      
        """
        
        if None in self.PCA_results:
            print('\nNo results to return! Please run the PCA() method first.')        
        else:
            return self.PCA_results
    
    
    def get_knee_plot(self, show:bool = True):
        
        """
        Retrieve the knee plot of cumulative explained variance from the var_plot() method.
     
        Args:
            show (bool) - whether to display the knee plot. Default: True
     
        Returns:
            fig (matplotlib.figure.Figure) - the knee plot figure.
     
      
        """
   
        if self.knee_plot is None:
            print('\nNo results to return! Please run the var_plot() method first.')      
        else:
            if show == True:
                self.knee_plot
                try:
                    display(self.knee_plot)
                except:
                    None
                
            return self.knee_plot

    def get_var_data(self):
        
        """
        Retrieve the explained variance data of PCA from var_plot() method.
     
        Returns:
            var_data (np.ndarray) - the explained variance data stored in `self.var_data`
     
        
        """
        
        if None in self.var_data:
            print('\nNo results to return! Please run the var_plot() method first.')      
        else:
            return self.var_data
    
    def get_scaled_data(self):
        
        """
       Retrieve the scaled data from data_scale() method.
    
       Returns
           scaled_data (np.ndarray) - the scaled data stored in `self.scaled_data`.
    

       """
        
        if None in self.scaled_data:
            print('\nNo results to return! Please run the data_scale() method first.')      
        else:
            return self.scaled_data
    
    def get_UMAP_data(self):
        
        """
        Retrieve the UMAP-transformed data from UMAP() method.

        Returns:
            UMAP_data (np.ndarray) - the UMAP data stored in `self.UMAP_data`
         
        """
        
        if None in self.UMAP_data:
            print('\nNo results to return! Please run the UMAP() method first.')      
        else:
            return self.UMAP_data
    
    def get_UMAP_plots(self, show:bool = True):
        
        """
        Retrieve the UMAP plots from UMAP() and/or UMAP_on_clusters() methods.
     
        Args:
            show (bool) - whether to display the UMAP plots. Default: True
     
        Returns:
            figs (dict of matplotlib.figure.Figure) - a dictionary of UMAP plots
     
        """
        
        if len(self.UMAP_plot.keys()) == 0:
            print('\nNo results to return! Please run the UMAP() and / or UMAP_on_clusters() methods first.')      
        else:
        
            if show == True: 
                for k in  self.UMAP_plot.keys():
                    self.UMAP_plot[k]
                    try:
                        display(self.UMAP_plot[k])
                    except:
                        None
                
        
        return self.UMAP_plot
    
    def save_UMAP_plots(self, path = os.getcwd(), name = '', extension = 'svg'):
        
        """
        Save the UMAP plots to a specified directory from UMAP() and / or UMAP_on_clusters() methods.
     
        Args:
            path (str) - the directory path where plots will be saved. Default: current working directory
            name (str) - the base name for the saved plot files. Default: ''
            extension (str) - the file extension for the saved plots. Default: 'svg'
     
        Returns:
        
            Saves UMAP plots to the specified path with the given name and extension.
     
        """
        
        if len(self.UMAP_plot.keys()) == 0:
            print('\nNo results to return! Please run the UMAP() and / or UMAP_on_clusters() methods first.')      
        else:
        
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            
            for k in  self.UMAP_plot.keys():
                full_path = os.path.join(path, f'{name}_{k}.{extension}')
                self.UMAP_plot[k].write_image(full_path)
            
    
    def save_knee_plot(self, path = os.getcwd(), name = '', extension = 'svg'):
        
        """
        Save the knee plot to a specified directory from var_plot() method.

        Parameters:
            path (str) - the directory path where plots will be saved. Default: current working directory
            name (str) - the base name for the saved plot files. Default: ''
            extension (str) - the file extension for the saved plots. Default: 'svg'
     
        Returns:
        
            Saves the knee plot to the specified path with the given name and extension.
     
        """
        
        if self.knee_plot is None:
            print('\nNo results to return! Please run the var_plot() method first.')      
        else:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
         
            full_path = os.path.join(path, f'{name}_knee_plot.{extension}')
            self.knee_plot.savefig(full_path)
 
    
    

    def load_data(self, path:str, ids_col:str = 'id_name', set_col:str = 'set'):
        
        """
        Load and preprocess data from a CSV file, storing both the data and metadata in the instance attributes.
     
        Args:
            path (str) - the file path to the CSV file containing the data to be loaded
            ids_col (str) - the name of the column in the CSV file that contains the unique identifiers for the objects. Ddefault: 'id_name'
            set_col (str) - the name of the column in the CSV file that specifies the set or group each object belongs to.  Default: 'set'
         
        Returns:
            This method modifies the instance by loading data into the following attributes:
            - `self.input_data`: A pandas DataFrame containing the loaded and cleaned data, with the index set to the values in the `ids_col` column.
            - `self.tmp_data`: A copy of the input data, which can be used for temporary operations or further manipulation.
            - `self.input_metadata`: A pandas DataFrame containing the metadata, specifically the object IDs and set assignments, as defined by `ids_col` and `set_col`.
            - `self.tmp_metadata`: A copy of the metadata for temporary operations or further manipulation.
     
        
        """
   

        data = pd.read_csv(path)
        data = data.dropna()
    
        metadata = pd.DataFrame()
        metadata['id'] = data[ids_col]
        metadata['sets'] = data[set_col]
    
        data.index = data[ids_col]
        
        
        try:
            data.pop('id_name')
        except:
            None
            
            
        try:
            data.pop('Object Number')
        except:
            None

        
        self.input_data = data
        self.tmp_data = data
        self.input_metadata = metadata
        self.tmp_metadata = metadata




    def select_data(self, features_list:list = []):
        
        """
        Select specific features (columns) from the dataset and store them for further use.
      
        Args:
            features_list (list) - a list of feature names (column names) to select from the dataset. Default: [].
          
        Returns:
            
            This method modifies the `self.tmp_data` attribute to contain only the selected features from `self.input_data`.
      
        
        """
  
  
        
        dat = self.input_data.copy()
        
        not_in_columns = [name for name in features_list if name not in dat.columns]
        
        if not_in_columns:
            print("These names are not in data", not_in_columns)
        else:
            print("All names are present in data.")
            
        in_columns = [name for name in features_list if name in dat.columns]

        dat = dat[in_columns]
        
        self.tmp_data = dat
        
        
        
    def data_scale(self):
        
        """
        Scale the data using standardization (z-score normalization).
    
        This method applies the `StandardScaler` from scikit-learn to the current temporary data (`self.tmp_data`) and stores the scaled data.
    
        Returns:

            This method modifies the `self.scaled_data` attribute to contain the scaled version of the temporary dataset (`self.tmp_data`).
    

        """

        if None not in self.tmp_data:
            scaler = StandardScaler()
            self.scaled_data = scaler.fit_transform(self.tmp_data)
        else:
            print("\nNo data to scale. Please use the load_data() method first, and optionally the select_data() method.")
        
        

    def PCA(self):
        
        """
        Perform Principal Component Analysis (PCA) on the scaled data.
    
        This method applies PCA to reduce the dimensionality of the `self.scaled_data` while retaining the maximum variance possible.
    
        Returns:

            This method modifies the `self.PCA_results` attribute to contain the transformed data after applying PCA.
    
        
        """
        
        if None not in self.scaled_data:
            pca = PCA(n_components=len(self.tmp_data.columns))  
            self.PCA_results = pca.fit_transform(self.scaled_data)
            self.explained_variance_ratio = pca.explained_variance_ratio_
        else:
            print("\nNo data for PCA. Please use the data_scale() method first.")


        
        
          
            
    def var_plot(self):
        
        """
        Plot the cumulative explained variance of the principal components from PCA.
    
        This method generates a plot showing the cumulative explained variance as a function of the number of principal components. The plot helps visualize how much variance is captured by each component and can assist in determining the optimal number of components.
    
        Returns:

            This method stores:
            - `self.var_data`: The explained variance ratio for each principal component
            - `self.knee_plot`: A matplotlib figure object representing the plot of cumulative explained variance
    
       
        """

        if None not in self.PCA_results:

            fig, ax = plt.subplots(figsize=(15, 7))
            explained_var = self.explained_variance_ratio
        
            cumulative_var = np.cumsum(explained_var)
        
            # Plot the cumulative explained variance as a function of the number of components
            plt.plot(cumulative_var)
            plt.xlabel('Number of Components')
            plt.ylabel('Cumulative Explained Variance')
            plt.title('Explained variance of PCs')
        
            self.var_data = explained_var
            self.knee_plot = fig
        
        else:

            print("\nNo data for variance explanation analysis. Please use the PCA() method first.")



            



    def UMAP(self, PC_num:int = 5, factorize_with_metadata:bool = True, n_neighbors:int = 25, min_dist:float=0.01, n_components:int=2):
        
        """
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
    
      
        """
    
        if None not in self.PCA_results:

            reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components)
        
            if factorize_with_metadata == True:
                numeric_labels = pd.Categorical(self.tmp_metadata['sets']).codes
            
                umap_result = reducer.fit_transform(self.PCA_results[:,:PC_num+1], y = numeric_labels)
                
            else:
                umap_result = reducer.fit_transform(self.PCA_results[:,:PC_num+1])
                
        
            fig = px.scatter(
                x=umap_result[:, 0], y=umap_result[:, 1],
                color=self.tmp_metadata['sets'], labels={'color': 'Cells'},
                template='simple_white',
                width=800, height=600,
                render_mode='svg',
                color_discrete_sequence=px.colors.qualitative.Dark24 + px.colors.qualitative.Light24
        
            )
        
            fig.update_xaxes(title_text='UMAP_1')
            fig.update_yaxes(title_text='UMAP_2')

            self.UMAP_data = umap_result
            self.UMAP_plot['PrimaryUMAP'] = fig

        else:

            print("\nNo data for UMAP. Please use the PCA() method first.")




    def db_scan(self, eps = 0.5, min_samples:int = 10):
        
        """
        Perform DBSCAN clustering on the UMAP-transformed data.
     
        This method applies DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to identify clusters in the UMAP embedding.
     
        Args:
            eps (float/int) - the maximum distance between two points for one to be considered as in the neighborhood of the other. Default: 0.5
            min_samples (int) - the minimum number of points required to form a dense region. Default: 10
         
        Returns:
  
            This method stores the cluster labels:
            - `self.dblabels`: A list of cluster labels assigned by DBSCAN, with each label converted to a string.
     
     
       """

        from sklearn.cluster import DBSCAN
        
        if None not in self.UMAP_data:

            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            dbscan_labels = dbscan.fit_predict(self.UMAP_data)
            self.dblabels  = [str(x) for x in dbscan_labels]

        else:

            print("\nNo data for DBSCAN. Please use the UMAP() method first.")


        
    def UMAP_on_clusters(self, min_entities:int = 50):
        
        """
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
    
        
        """
        
        if None not in self.UMAP_data:


            umap_result = pd.DataFrame(self.UMAP_data.copy())
            umap_result['id'] = self.tmp_metadata.index
            umap_result['clusters'] = self.dblabels
            tmp_metadata = self.tmp_metadata.copy()
            tmp_metadata['clusters'] = self.dblabels
            label_counts_dict = Counter(self.dblabels)
            
            label_counts = pd.DataFrame.from_dict(label_counts_dict, orient='index', columns=['count'])
            
            filtered_counts = label_counts[label_counts['count'] > min_entities]
            
            tmp_metadata['full_id'] = list(tmp_metadata['id'].astype(str) + ' # ' +  tmp_metadata['sets'])
            tmp_data = self.tmp_data.copy()
            tmp_data.index = tmp_metadata['full_id']
            umap_result['full_id'] = list(tmp_metadata['full_id'])
            
            umap_result = umap_result[umap_result['clusters'].isin(np.array(filtered_counts.index))]
            tmp_metadata = tmp_metadata[tmp_metadata['clusters'].isin(np.array(filtered_counts.index))]
            
            tmp_data = tmp_data[tmp_data.index.isin(np.array(tmp_metadata['full_id']))]
        
        
        
            fig = px.scatter(
                x=umap_result[0], y=umap_result[1],
                color=umap_result['clusters'], labels={'color': 'Cells'},
                template='simple_white',
                width=800, height=600,
                render_mode='svg',
                color_discrete_sequence=px.colors.qualitative.Dark24 + px.colors.qualitative.Light24
        
            )
        
            fig.update_xaxes(title_text='UMAP_1')
            fig.update_yaxes(title_text='UMAP_2')
        
            self.UMAP_plot['ClusterUMAP'] = fig


            tmp_metadata['full_name'] = list(tmp_metadata['clusters'] + ' # ' + tmp_metadata['sets'])
        
            label_counts_dict = Counter(list(tmp_metadata['full_name']))
        
            label_counts = pd.DataFrame.from_dict(label_counts_dict, orient='index', columns=['count'])
        
            filtered_counts = label_counts[label_counts['count'] > min_entities]
        
            tmp_data.index = tmp_metadata['full_name']
            umap_result['full_name'] = list(tmp_metadata['full_name'])
        
            umap_result = umap_result[umap_result['full_name'].isin(np.array(filtered_counts.index))]
            tmp_metadata = tmp_metadata[tmp_metadata['full_name'].isin(np.array(umap_result['full_name']))]
        
            tmp_data = tmp_data[tmp_data.index.isin(np.array(tmp_metadata['full_name']))]
            
            
            fig = px.scatter(
                x=umap_result[0], y=umap_result[1],
                color= umap_result['full_name'], labels={'color': 'Cells'},
                template='simple_white',
                width=800, height=600,
                render_mode='svg',
                color_discrete_sequence=px.colors.qualitative.Dark24 + px.colors.qualitative.Light24
        
            )
        
            fig.update_xaxes(title_text='UMAP_1')
            fig.update_yaxes(title_text='UMAP_2')
        
            self.UMAP_plot['ClusterXSetsUMAP'] = fig

            self.tmp_data = tmp_data
            self.tmp_metadata = tmp_metadata

        else:
            print("\nNo data for visualization. Please use the UMAP() and db_scan() methods first.")


        
    ## save data
    def full_info(self):
        
        """
        Merge data with metadata if metadata contains a 'full_id' column.
      
        This method combines `tmp_data` and `tmp_metadata` into a single DataFrame for comprehensive information if the metadata includes the 'full_id' column. If 'full_id' is not found, the method suggests completing the necessary preprocessing pipeline.
      
        Returns:
            merged_df (pd.DataFrame) - returns a merged DataFrame with both data and metadata
      
       
        """
        
        tmp_data = self.tmp_data.copy() 
        tmp_metadata = self.tmp_metadata.copy()
        
        if 'full_id' in tmp_metadata.columns:
            tmp_data.index = tmp_metadata['full_id']
            
            merged_df = tmp_data.merge(tmp_metadata, left_index = True, right_on='full_id', how = 'left')
            
            return merged_df
        
        else:
            
            print('\nMetadata is not completed!')
    
    
        #################################################################################
    
    
    
   
    
    def DFA(self, meta_group_by:str = 'sets', sets:dict = {}, n_proc = 5):
        
        """
        Perform Differential Feature Analysis (DFA) on specified data groups.
      
        This method conducts DFA using a grouping factor from metadata and a dictionary of sets for comparison. It allows for the identification of significant differences across defined sets.
      
        Parameters:
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
      
        
        """
        
      
        tmp_data = self.tmp_data.copy()
        
        
        
        tmp_data = tmp_data.select_dtypes(include='number')

        tmp_metadata = self.tmp_metadata.copy()
        
        
        if len(sets.keys()) >= 2:
            print('\nAnalysis strated on provided sets dictionary and meta_group_by...')
            tmp_data.index = list(tmp_metadata[meta_group_by])
            tmp_metadata['sets'] =  tmp_metadata[meta_group_by]
            results = self.statistic(tmp_data.transpose(), sets = sets, metadata = tmp_metadata, n_proc = n_proc)
        
        else:
            print('\nAnalysis strated on for all groups to each other in meta_group_by...')
            tmp_data.index = list(tmp_metadata[meta_group_by])
            tmp_metadata['sets'] =  tmp_metadata[meta_group_by]
            results = self.statistic(tmp_data.transpose(), sets = None, metadata = tmp_metadata, n_proc = n_proc)
            
        return results

            
            



    