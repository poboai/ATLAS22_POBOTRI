import numpy as np
from settings import loader_settings
import medpy.io
import os, pathlib

# hd-BET
from HD_BET.run import run_hd_bet
from HD_BET.utils import subfiles
import HD_BET
import glob

#nnunet
from nnunet.inference.predict import predict_from_folder
from nnunet.inference.ensemble_predictions import merge
from batchgenerators.utilities.file_and_folder_operations import *

class ATLAS22_POBOTRI():
    def __init__(self):
        return
    def process(self):
        inp_path = loader_settings['InputPath']  # Path for the input
        out_path = loader_settings['OutputPath']  # Path for the output
        #file_list = os.listdir(inp_path)  # List of files in the input
        #file_list = sorted([os.path.join(inp_path, f) for f in file_list])
        file_list = sorted(glob.glob('%s/*'%inp_path))
        print(file_list)
        ## Step0. Save in User Folder
        print('\nStep0. Save in User Folder\n')
        list_dir = []
        list_offset = []
        list_name = []
        sdir = 'usr_folder'
        if not os.path.exists(sdir):os.mkdir(sdir)
        step0_dir = 'usr_folder/step0'
        if not os.path.exists(step0_dir):os.mkdir(step0_dir)
        for idx, fil in enumerate(file_list):
            dat, fc = medpy.io.load(fil)  # dat is a numpy array
            list_dir.append(fc.get_direction())
            list_offset.append(fc.get_offset())
            out_name = os.path.basename(fil)
            list_name.append(out_name)
            print(out_name)
            out_name = os.path.basename(fil)
            medpy.io.save(dat, '%s/%s_0000.nii.gz'%(step0_dir,out_name[:-7]),fc)
        
        ## Step1. HD-BET 3D Skull Strip
        print('\nStep1. HD-BET 3D Skull Strip\n')
        step1_dir = 'usr_folder/step1'
        if not os.path.exists(step1_dir):os.mkdir(step1_dir)
        input_files = subfiles(step0_dir, suffix='.nii.gz', join=False)
        output_files = [os.path.join(step1_dir, i) for i in input_files]
        input_files = [os.path.join(step0_dir, i) for i in input_files]
        config_file = os.path.join(HD_BET.__path__[0], "config.py") 
        run_hd_bet(input_files, output_files, 'accurate', config_file, 0, 1, 1, 0, 1)

        ## Step2. nnUNet
        print('\nStep2. nnUNet\n')
        step2_dir = 'usr_folder/step2'
        if not os.path.exists(step2_dir):os.mkdir(step2_dir)
        step2_2d_dir = 'usr_folder/step2_2d'
        if not os.path.exists(step2_2d_dir):os.mkdir(step2_2d_dir)
        step2_3d_dir = 'usr_folder/step2_3d'
        if not os.path.exists(step2_2d_dir):os.mkdir(step2_2d_dir)
        step2_3d_thres_dir = 'usr_folder/step2_3d_thres'
        if not os.path.exists(step2_3d_thres_dir):os.mkdir(step2_3d_thres_dir)

        # 2d Network Run
        model_folder_name = 'nnUNet_model/2d'
        predict_from_folder(model_folder_name, step1_dir, step2_2d_dir, None, True, 6,
                            2, None, 0, 1, True,overwrite_existing=True, mode="normal", overwrite_all_in_gpu=None,
                            mixed_precision=True,step_size=0.5, checkpoint_name='model_final_checkpoint', thres_postprocessing=False)

        # 3d Network Run --
        model_folder_name = 'nnUNet_model/3d_fullres'
        predict_from_folder(model_folder_name, step1_dir, step2_3d_dir, None, True, 6, #save_npz True
                            2, None, 0, 1, True,overwrite_existing=True, mode="normal", overwrite_all_in_gpu=None,
                            mixed_precision=True,step_size=0.5, checkpoint_name='model_final_checkpoint', thres_postprocessing=False)
        
        # Merge 2d, 3d Network 
        merge([step2_2d_dir, step2_3d_dir],step2_dir,2,True,None)
        
        # 3d thres Network Run
        model_folder_name = 'nnUNet_model/3d_fullres'
        predict_from_folder(model_folder_name, step1_dir, step2_3d_thres_dir, None, True, 6, #save_npz True
                            2, None, 0, 1, True,overwrite_existing=True, mode="normal", overwrite_all_in_gpu=None,
                            mixed_precision=True,step_size=0.5, checkpoint_name='model_final_checkpoint', thres_postprocessing=True)
        
        # Step3. Load Result
        print('\nStep3. Load Result and Union\n')
        file_list_2d3d = sorted(glob.glob('%s/*.nii.gz'%step2_dir))
        file_list_3dthres = sorted(glob.glob('%s/*.nii.gz'%step2_3d_thres_dir))
        for idx in range(len(file_list_2d3d)):
            prediction_2d3d, _ = medpy.io.load(file_list_2d3d[idx])  # dat is a numpy array
            prediction_3dthres, _ = medpy.io.load(file_list_3dthres[idx])  # dat is a numpy array
            
            # Union
            union_2d3d_3dthres = np.logical_or(prediction_2d3d, prediction_3dthres) #union
            union_2d3d_3dthres = union_2d3d_3dthres.astype(np.int8)

            out_name = list_name[idx]
            out_filepath = os.path.join(out_path, out_name)
            fc.set_direction(list_dir[idx])
            fc.set_offset(list_offset[idx])
            medpy.io.save(union_2d3d_3dthres, out_filepath, fc)
        return


if __name__ == "__main__":
    pathlib.Path("/output/images/stroke-lesion-segmentation/").mkdir(parents=True, exist_ok=True)
    ATLAS22_POBOTRI().process()
