from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'JIMG-analyst-tool'
LONG_DESCRIPTION = '''

The JIMG_analyst_tool is a Python library that extends the JIMG image processing tool, specifically tailored for analyzing high-resolution confocal microscope images [Opera-Phoenix](https://www.revvity.com/product/opera-phenix-plus-system-hh14001000?srsltid=AfmBOoohz1LiEemNbG4SJnaEtScwr16MyFL8Ulf9NyDDEAffV2NLJXoe) and other technologies. This library enables detailed examination of nuclei and their chromatin organization, supporting high-resolution analysis of nuclear morphology and chromatin structure.

It also provides algorithms for measuring the intensity of specific protein markers using customizable image masks on high-resolution microscope images. These measurements are normalized using a background mask for consistent data comparison. The collected intensity data can be statistically analyzed to detect differences in marker localization, occurrence, and intensity.

In addition to microscopy, flow cytometry [Amnis-ImageStream](https://cytekbio.com/pages/imagestream) analysis capabilities are integrated into the tool. It can analyze flow cytometry images, applying nuclear and chromatin analysis methods similar to those used for confocal microscopy. Furthermore, the tool enables advanced analysis of cell populations from cytometric data, offering options to select distinguishing cell characteristics, perform clustering of cell sets based on these features, and analyze clusters using statistical methods to identify unique attributes.

With these combined functionalities, the JIMG_analyst_tool is a versatile resource for researchers requiring in-depth quantitative analysis of nuclear and chromatin features in both confocal microscopy and flow cytometry datasets.

Detailed description available at: https://github.com/jkubis96/JIMG-analyst-tool/

'''


# Setting up
setup(
        name="JIMG-analyst-tool", 
        version=VERSION,
        author="Jakub Kubis",
        author_email="jbiosystem@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['JIMG_analyst_tool'],
        include_package_data=True, 
        install_requires=[
                "csbdeep",
                "JIMG",
                "matplotlib",
                "pandas",
                "numpy",
                "opencv-python", 
                "stardist",
                "tqdm",
                "scikit-image",
                "IPython",
                "mpld3",
                "plotly",
                "scipy",
                "pingouin",
                "joblib",
                "scikit-learn",
            ], 
        keywords=['python', 'nuclei', 'intenisty', 'image', 'high-resolution', 'comparison'],
        license = 'MIT',
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires='>=3.6',
)


