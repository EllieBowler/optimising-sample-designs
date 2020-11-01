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

Habitat fragmentation can be assessed with a wide range of different metrics, for example distance to habitat edges, areas of fragments, their compactness and configuration. 
Commonly these metrics are calculated by using satellite maps of study sites, and using programs such as fragstats to output maps representing these metrics. 
Despite this, metrics are commonly used at the assessment stage, and negelcted at teh design stage. In order to properly assess a landscape, we should optimise the placement of
sites along gradients of the metric quantities. This leads to little standardisation between studies, and sub-optimal coverage of the metrics of interest. 

**This project provides functions which output sampling designs based on user input fragmentation metric maps**. 
Our implementation can be used on any map which can be represented as a georeferenced tiff file, and can optimise along multiple metrics in tandem. 
Invalid areas masks can also be used to remove known innaccessible locations. The outputs are in csv format, showing the long lat coordinated of sample locations. 
The methods are implented in python, however we also provide demonstation jupyter notebooks which can be loaded and run in google colabotory. This allows users to run the methods
without the need to install python or any packages.   

In the topics below you can find an overview of the methods described in the paper, as well as samples showing how to use our code.

## Table of contents

- [Motivation](#optimising-sample-designs)
- [Important definitions](#important-definitions)
  - [Stratified Design Algorithm](#stratified-design-algorithm)
  - [Uniform Design Algorithm](#uniform-design-algorithm)
  - [Adapted Designs](#adapted-designs)
    - [Option 1](#option-1)
    - [Option 2](#option-2)
- [Inputs](#inputs)
- [**How to use this project**](#how-to-use-this-project)
- [**Running jupyter demo files**](#running-demo-files)

## Important definitions  

### Stratified Design Algorithm

The stratified design focusus only on spreading sites evenly given the layout of inbvalid areas. Invalid areas can include towns, roads, locations which are known to be inaccessible, or habitat
types which are not of interest. The design is the building block for the uniform design alogorithm. 

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


## Inputs

* **Invalid Areas Mask**: A georeferenced tif file with 0=valid / 1=invalid  
* **Metric Map**: Map showing some feature of fragmentation 
* **Number of sample sites (nsp)**: Integer number of samples sites  

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

## Running demo files

The .ipynb files in this repository can be loaded into Google Colaboratory an run remotely. This allows users to explore the code and load their own files without the need to download or install python or any extra libraries. To run these files please follow the set up instructions [here](https://github.com/EllieBowler/optimising-sample-designs/raw/master/jupyter-colab-instructions.pdf).

Test the example files [here](https://github.com/EllieBowler/optimising-sample-designs/raw/master/results/)
