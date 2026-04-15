
---
layout: default
title: Computing servers
parent: Tools & methods
nav_order: 5
---



# Fox — Data analysis server

<div style="text-align: center; margin-bottom: 20px;">
  <img src="../../assets/images/fox.jpeg" width="180">
</div>

Fox is a powerful computer for data analysis. 

## Specifications

    CPU: Core i9
    Memory: 64GB
    Disk space: 2 TB SSD
    GPU: Nvidia RTX A5000 24GB
    Operating system: Ubuntu 22.04

## Getting an account

Ask one of the system administrators:
  Sebastiaan Mathôt (s.mathot@rug.nl)
  Ana Vilotijević (a.vilotijevic@rug.nl)

## Graphical log in

Through **x2go** client. The session type should be **XFCE**. 

When you log in, there are lots of visual artifacts in the interface. To fix this, go to Applications → Settings → Window manager tweaks → Compositor and untick the 'Enable display compositing' option.

## Access from outside the university network

To access Fox from outside the university network, connect to the RUG VPN. Instructions for Linux, Mac OS, and Windows are available from the [CIT help portal](https://www.rug.nl/cit/servicedesk?lang=en).

example (On Ubuntu):
- First install the openconnect VPN client

```
sudo apt install openconnect
```

 - Connect to the RUG VPN. This will ask you to log in with your regular RUG log-in + authenticator.
  - To close the VPN, press Ctrl+C to close the client.

```
sudo openconnect --protocol=gp safenet.vpn.rug.nl
```
example (Mac or Windows):
- Go to safenet.vpn.rug.nl
- Log in
- Download and install "GlobalProtect"
- Log in

for more, please see: [VPN instructions](https://iris.service.rug.nl/tas/public/ssp/content/detail/service?unid=f4c53f8827c54588b267c5f267367505)


## Console log in

Through ```ssh```.

```
ssh 129.125.130.90
```

You can use screen to create persistent sessions that you can reconnect to later.

## Installing software on Fox

Whenever possible, use ```anaconda``` or Python ```venv``` to install the software you need. If you need software that cannot be installed through this route, ask the system administrators.

Matlab is available (open a terminal and run ```matlab```). You do need an account and license key, which you need to arrange yourself through the university. 


## Setting up Anaconda

Start with a clean Anaconda with no channels added (this is important because dependency solving fails if there are too many channels). Then run the following commands in the terminal:

```
conda create -n pydata python=3.10 
conda activate pydata
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
conda install jupyter_client pip datamatrix statsmodels scikit-learn pingouin seaborn mne json_tricks scikit-learn-intelex ipykernel -c conda-forge
pip install eeg_eyetracking_parser moabb braindecode time_series_test biased_memory_toolbox
```

Then check if the GPU is enabled by starting Python and running the following:

```
import torch
torch.cuda.is_available()
```

Finally, you can make the pydata environment available in Rapunzel, Spyder, and similar IPython-aware editors as follows:

```
conda activate pydata
python -m ipykernel install --user --name pydata
```
## What to do when Fox is slow or frozen? 

<div style="text-align: center; margin-bottom: 20px;">
  <img src="../../assets/images/Stoned_Fox.jpg" width="180">
</div>

Ask administrators to check GPU and reboot it.
