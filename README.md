## Citation
This work was published in ------. If you use this code for your research, please consider citing:
```
-----@BIBTEX JOURNAL REFERENCE ------
```
Download the paper [add link to paper](https://github.com/EllieBowler/optimising-sample-designs/name-of-the.pdf)

<a name="optimising-sample-designs"></a>
# Optimising sampling designs for habitat fragmentation studies
  
The motivation of this project is to develop a standardised computational approach to designing sample layouts for habitat fragmentations studies. 
Importantly we propose taking widely used fragmentation metric maps as inputs to the methods, which will **output designs optimised to cover the metrics of interest.**

Habitat fragmentation can be assessed with a wide range of different metrics, for example distance to habitat edges, fragment area, shape and configuration. While many studies aim to record impacts in relation to these metrics, in practice designing sample schemes which capture reponses to these measures can be challenging for three main reasons:
1. Fragmented landscapes present a complex mosaic which can be challenging to assess, making it difficult to optimally sample ranges of fragmentation metrics

2. Sample points are often placed in close proximity in the landscape leading to issues with spatial autocorrelation

3. Field researchers face challenges with inaccessible regions such as areas of private land, distance to research stations and unexpected obstacles such as landslides.

While it is common practice to use satellite dervied maps to quantify fragmentation metrics for a study landscape, to our knowledge these metric maps are predominantly used to extract metric values after sampling is completed. The novel approach we take in this study is to use these metric maps directly in the sampling design stage, allowing the configuration of metric values in the landscape to be quantitatively assessed. The methods are presented as open-source python code, and include features for masking innaccessible locations, suggesting optimal number of sample sites, and adapting partially completed designs given unforseen field-work imposed constraints.
  
In the topics below you can find an overview of the methods described in the paper, as well as samples showing how to use our code.

## Table of contents

- [Motivation](#optimising-sample-designs)
- [Inputs](#inputs)
  - [Map inputs](#map-inputs)
  - [Other inputs](#other-inputs)
- [**Running jupyter demo files**](#running-demo-files)
- [Package list](#package-list)
- [Stratified Design Algorithm](#stratified-design-algorithm)
- [Uniform Design Algorithm](#uniform-design-algorithm)
- [Adapted Designs](#adapted-designs)
  - [Option 1](#option-1)
  - [Option 2](#option-2)
- [**How to use this project**](#how-to-use-this-project)

## Inputs

### Map Inputs
Spatial inputs fall into three main categories, as below. Example metric maps are provided in the ```input``` folder, and can also be downloaded directly [here](https://github.com/EllieBowler/optimising-sample-designs/raw/master/test_files.zip). All map should be in **georeferenced tif format**. 

- **Habitat Map**: A categorical map classifying the landscape into land-cover types, which should be the one used to produce the metric maps. In the example we have:
  - HabitatMap.tif: A two-category grassland/forest map
- **Invalid Areas Mask**: Map showing areas to exclude (with 0=invalid / 1=valid). The example files include:
  - InvalidAreasMask.tif: masks out all non-focal grassland habitat
  - InvalidAreasMask_updated.tif: adds additional excluded regions which can be used to test the adapted design options
- **Fragmentation Metric Maps**: Maps showing some feature of fragmentation. The example files include:
  - DistanceToEdgeLog2.tif: Log 2 transformed distance to edge (m, up to a maximum of 1024m)
  - FragmentAreaLog10.tif: Log 10 transformed fragment area (ha)
  
### Other Inputs
Extra inputs which can be specified by the user include:
- **Number of sample sites**: ```nsp``` should be an integer value specifying the desired number of sites
- **Number of bins**: ```n_bins``` an integer value specifying the number of intervals the range of a metric should be broken into


## Running demo files

The .ipynb files in this repository provide code demonstrations using the example files listed above, and can be run remotely via Google Colaboratory. This allows users to explore the code, load their own files, and generate designs without the need to download or install python or any extra libraries. To run these demo files please first [download the test files here](https://github.com/EllieBowler/optimising-sample-designs/raw/master/test_files.zip) and then follow [these instructions](https://github.com/EllieBowler/optimising-sample-designs/raw/master/jupyter-colab-instructions.pdf) to get set up. 


### Package list

The following packages are required to run the code:

- conda 4.5.9
- numpy 1.15.0
- pandas 0.20.3
- click 6.7
- gdal 2.3.1
- matplotlib 2.1.0
- scipy 1.0.0


## Stratified Design Algorithm

The stratified design focuses only on spreading sites evenly geographically, given the layout of invalid areas. Invalid areas could include towns, roads, bodies of water, habitat types which are not of interest, areas in high elevation etc. The design is the building block for the uniform design alogorithm. 

The image below illustrates an example input and output of the stratified design.

<!--- Stratified Design --->
<p align="center">
<img src="https://github.com/EllieBowler/optimising-sample-designs/aux_images/filename.png" align="center"/></p>

### Uniform Design Algorithm 

The image below illustrates an example input and output of the uniform design.

<!--- Stratified Design --->
<p align="center">
<img src="https://github.com/EllieBowler/optimising-sample-designs/aux_images/filename.png" align="center"/></p>

### Adapted Designs

Sometimes unforseen circumstances make it impossible to access certain locations. In this instance designs can be updated, keep all sites which have been successfully accessed in place.
There are two options for adapting designs based on user preference:

#### Option 1

The invalid areas mask can be manually upadste in software such as arcmap. Instructions can be found here. 

#### Option 2

The csv file can be tagged with a 2 in 'sampled column'. A user defined radiaus can then be masked around this point. 




#### An ilustrated example 

## How to use this project

[Sample_1](https://github.com/rafaelpadilla/Object-Detection-Metrics/tree/master/samples/sample_1) and [sample_2](https://github.com/rafaelpadilla/Object-Detection-Metrics/tree/master/samples/sample_2) 
are practical examples demonstrating how to access directly the core functions of this project, providing more flexibility on the usage of the metrics. But if you don't want to spend your time understanding our code, see the instructions below to easily evaluate your detections:  

Follow the steps below to start evaluating your detections:

1. [Copy input files into raw data folder](#copy-input-files-into-raw-data-folder)
2. For **uniform design**, run the command: `python uda.py`  
   If you want to reproduce the example above, run the command: `python uda.py --nsp 30`
3. (Optional) [You can use arguments to control the optimal number of sample sites, save file name etc](#optional-arguments)

### Copy input files into raw data folder

The files you need will depend on the design you wish to generate. For demonstration we have put example files in the raw folder. These include:
- Log 10 etc
- mask.tif
- etc

### Optional arguments

Optional arguments:

| Argument &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description | Example | Default |
|:-------------:|:-----------:|:-----------:|:-----------:|
| `-h`,<br>`--help ` |	show help message | `python uda.py -h` | |  
|  `-v`,<br>`--version` | check version | `python uda.py -v` | |  
| `-gt`,<br>`--gtfolder` | folder that contains the input files | `python uda.py -gt /home/whatever/my_raw_files/` | `/optimising-sample-designs/raw`|  
| `-sp`,<br>`--savepath` | folder where the results are saved | `python uda.py -sp /home/whatever/my_results/` | `optimising-sample-designs/results/` |  

