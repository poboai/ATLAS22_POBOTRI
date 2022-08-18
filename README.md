# ATLAS22_POBOTRI
Codes for submission of 2022 Anatomical Tracings of Lesions After Stroke (ATLAS) Challenge with ATLAS R2.0 Dataset.  
The source code for the algorithm container, generated with evalutils version 0.3.1.  

![Figure](./ATLAS_fig_220817.png)
# Inference  
You can run the inference code with docker system.  
please following these instructions:  
  1. Prepare mri image data (mha or nii.gz format) and json data of t1w mri images according to the folder structure below.  
  *or you can use sample data in test folder  
```
ATLAS22_POBOTRI/test/  
├── images  
│   └── t1-brain-mri  
│       └── <t1w_filename>.nii.gz  
```  
  2. Download nnUNet model parameters from [here](https://postechackr-my.sharepoint.com/:f:/g/personal/ych000_postech_ac_kr/EndNDCftgsRDrLGygt8sOkQBgLoW8h3UTej_5M6HuFERlg?e=4qYgjK) and put them in `nnUNet_model` folder.  
  3. Download HD-BET model parameters from [here](https://postechackr-my.sharepoint.com/:f:/g/personal/ych000_postech_ac_kr/Elq1n0enIKxDmg8x94hbjQcB12Gg0GGmhdiJvHsP8d1E0w?e=K7aeUE) and put them in `bet_params` folder.  
  4. Running the test.sh file automatically installs the required package of requirements.txt and allows you to test the code.  
  `./test.sh`  
  *this automatically install all the packages for the ATLAS22_POBOTRI code.  
  *you can modify the test.sh file to change the number of gpu to use, memory limitation, shm size, etc.  

  
