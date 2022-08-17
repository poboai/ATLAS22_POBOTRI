# # For Test
# loader_settings = {"InputPath": "/workspace/7_ATLAS_Docker/POBOTRI/input/images/t1-brain-mri/",
#                     "OutputPath": "/workspace/7_ATLAS_Docker/POBOTRI/output/images/stroke-lesion-segmentation/",
#                     "GroundTruthRoot": "/opt/evaluatlion/mha_masks/",
#                     "JSONPath": "/workspace/7_ATLAS_Docker/POBOTRI/input/predictions.json",
#                     "BatchSize": 2,
#                     "InputSlugs": ["t1-brain-mri"],
#                     "OutputSlugs": ["stroke-lesion-segmentation"]}
# Original
loader_settings = {"InputPath": "/input/images/t1-brain-mri/",
                    "OutputPath": "/output/images/stroke-lesion-segmentation/",
                    "GroundTruthRoot": "/opt/evaluation/mha_masks/",
                    "JSONPath": "/input/predictions.json",
                    "BatchSize": 2,
                    "InputSlugs": ["t1-brain-mri"],
                    "OutputSlugs": ["stroke-lesion-segmentation"]}