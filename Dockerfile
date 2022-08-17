#FROM python:3.9-slim
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

#Install ubuntu libraires and packages
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update -y
Run apt-get install git curl -y

#Initial GrandChallenge Docker Setting 
RUN groupadd -r algorithm && useradd -m --no-log-init -r -g algorithm algorithm
RUN mkdir -p /opt/algorithm /input /output \
    && chown algorithm:algorithm /opt/algorithm /input /output
USER algorithm
WORKDIR /opt/algorithm
ENV PATH="/home/algorithm/.local/bin:${PATH}"

#Install packages
RUN python -m pip install --user -U pip
RUN pip install --upgrade pip
COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
RUN python -m pip install --user -r requirements.txt

#Update Original Files
COPY --chown=algorithm:algorithm process.py /opt/algorithm/
COPY --chown=algorithm:algorithm settings.py /opt/algorithm/
COPY --chown=algorithm:algorithm grandchallenges/ /opt/algorithm/grandchallenges

#Update Edited Files
COPY utils.py /home/algorithm/.local/lib/python3.8/site-packages/HD_BET/utils.py
COPY bet_params /home/algorithm/.local/lib/python3.8/site-packages/HD_BET/bet_params
COPY nnUNet_model /opt/algorithm/nnUNet_model
COPY inference/predict.py /home/algorithm/.local/lib/python3.8/site-packages/nnunet/inference/predict.py
COPY inference/segmentation_export.py /home/algorithm/.local/lib/python3.8/site-packages/nnunet/inference/segmentation_export.py
COPY inference/ensemble_predictions.py /home/algorithm/.local/lib/python3.8/site-packages/nnunet/inference/ensemble_predictions.py

# COPY --chown=algorithm:algorithm isles/ /opt/algorithm/isles
ENTRYPOINT python -m process $0 $@
