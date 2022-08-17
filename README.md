# ATLAS22_POBOTRI
Codes for submission of 2022 Anatomical Tracings of Lesions After Stroke (ATLAS) Challenge with ATLAS R2.0 Dataset.  
The source code for the algorithm container, generated with evalutils version 0.3.1.  

![Figure](./ATLAS_fig_220817.png)
# Inference  
You can run the inference code with docker system.  
please following these instructions:  
  1. Prepare mri image data (mha format) and json data of adc, dwi, and flair mri images according to the folder structure below.  
  *or you can use sample data in test folder  
```
POBOTRI/test/  
├── images  
│   └── adc-brain-mri  
│       └── <adc_filename>.mha  
│   └── dwi-brain-mri  
│       └── <dwi_filename>.mha  
│   └── flair-brain-mri  
│       └── <flair_filename>.mha  
├── adc-mri-parametrs.json  
├── dwi-mri-parametrs.json  
├── flair-mri-parametrs.json  
```  
  2. Download models from [here](https://postechackr-my.sharepoint.com/:u:/g/personal/ych000_postech_ac_kr/Eb41Y0SrqSxIoknM10WU7hIB1RcqA7_R1GlTgWiDnU3TKg?e=jyGoog) and put them in `nnUNet_model` folder.  
  3. Running the test.sh file automatically installs the required package of requirements.txt and allows you to test the code.  
  `./test.sh`  
  *this automatically install all the packages for the ISLES22_PAT code.  
  *you can modify the test.sh file to change the number of gpu to use, memory limitation, shm size, etc.  

  
