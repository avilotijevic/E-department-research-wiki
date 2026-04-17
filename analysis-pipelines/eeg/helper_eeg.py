"""
This script contains neccessary functions for results_overview.py
"""

"""
Import modules
"""
import itertools
from datamatrix import DataMatrix
from eeg_eyetracking_parser import braindecode_utils as bdu, \
    _eeg_preprocessing as epp
from datamatrix import operations as ops
import numpy as np
from braindecode.visualization import plot_confusion_matrix
from scipy.stats import linregress, ttest_1samp
from statsmodels.formula.api import mixedlm
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import linregress, ttest_rel
from datamatrix import functional as fnc
import mne; mne.set_log_level(False)
from datamatrix import operations as ops, convert as cnv
import eeg_eyetracking_parser as eet
import eeg_eyetracking_parser as eet
from eeg_eyetracking_parser import braindecode_utils as bdu
from datamatrix import convert as cnv, DataMatrix, operations as ops, \
    series as srs, NAN
from eyelinkparser import parse, defaulttraceprocessor, visualize
import time_series_test as tst
import mne
from scipy.stats import linregress, ttest_1samp
import seaborn as sns
from statsmodels.formula.api import mixedlm
from matplotlib import pyplot as plt
from mne.time_frequency import tfr_morlet
import numpy as np
from datamatrix import functional as fnc, series as srs, NAN 
from matplotlib import pyplot as plt
from matplotlib import lines
import matplotlib.lines as mlines
import seaborn as sns
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import itertools as it
import pingouin as pg
import itertools as it
import time_series_test as tst
from scipy.stats import norm
from sklearn.metrics import confusion_matrix


"""
Parameters
"""
TARGET_TRIGGER = 3
CUE_TRIGGER = 1
CHANNELS = 'O1', 'O2', 'Oz', 'POz', 'Pz', 'P3', 'P4', 'P7', 'P8'
N_CHANNELS = 26
SUBJECTS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
25,26,27,28,29,30] 
FULL_FREQS = np.arange(4, 30.5, .5)
ALPHA_FREQS = np.arange(8, 12.5, .5)
THETA_FREQS = np.arange(4, 7.5, .5)
CUE_FACTORS = ['cue_eccentricity', 'inducer']
TGT_FACTORS = ['cue_eccentricity', 'inducer', 'cue']
FACTORS  = 'cue'

CUE_EPOCH_KWARGS = dict(tmin=0, tmax=3.5, picks='eeg',
                        preload=True, reject_by_annotation=True,
                        baseline=None)
TGT_EPOCH_KWARGS = dict(tmin=-.05, tmax=.8, picks='eeg',
                        preload=True, reject_by_annotation=True)

NOTCH_FREQS = np.exp(np.linspace(np.log(4), np.log(30), 15))


"""
Decoding datamatrix 
"""
def memoize_decoding(subject_nr):
    print(f'decoding {subject_nr}')
    read_subject_kwargs = dict(subject_nr=subject_nr) 
    return bdu.decode_subject(read_subject_kwargs=read_subject_kwargs,
                              factors=FACTORS, epochs_kwargs=TGT_EPOCH_KWARGS,
                              trigger=TARGET_TRIGGER, 
                              epochs_query='practice == "no" or target_presence == 0',
                              window_stride=1, window_size=200, n_fold=4, epochs=4)




def visualize_decoding(dm, labels, degree):
    """
    Visualizes decoding results
    ----------
    Parameters
    ----------
    dm:     DataMatrix
            datamatrix on which decoding should be performed
    labels: list of str
            to-be-decoded labels
    degree: int
            value for which labels are rotated
    """
    cm_pred = bdu.build_confusion_matrix(dm.braindecode_label,
                                     dm.braindecode_prediction)
    plot_confusion_matrix(cm_pred, labels, rotate_col_labels=degree,
                      rotate_row_labels=degree, figsize=(6, 6))



def decoding_results_per_factor (dm, factor_nr, factor_name, factor_levels):
    """
    Prints decoding results per factor and statistically tests them
    ----------
    Parameters
    ----------
    dm:             DataMatrix
                    datamatrix on which decoding should be performed
    factor_nr:      int
                    number of factors that are to be decoded
    factor_name:    str/list containing str;
                    name of factors (should be alphabetically listed and as in the dm)
    factor_levels:  int/list
                    number of levels for corresponding factors
    """
    if factor_nr==1:
        factor_decoding = []
        for subject_nr, sdm in ops.split(dm.subject_nr):
            print(f'For subject {subject_nr}, att_br decoding is {sdm.braindecode_correct.mean}')
            factor_decoding.append(sdm.braindecode_correct.mean)
        print('Overall decoding')
        print(f'{factor_name}: {dm.braindecode_correct.mean}')
        print(f'Statistical testing of {factor_name} decoding --> {ttest_1samp(factor_decoding, 1/factor_levels)}')
        return factor_decoding
    elif factor_nr == 2:
        factor1_decoding = []
        factor2_decoding = []
        dm.factor1_correct = 0
        dm.factor1_correct[dm.braindecode_label // 2 == dm.braindecode_prediction // 2] = 1
        dm.factor2_correct = 0
        dm.factor2_correct[dm.braindecode_label % 2 == dm.braindecode_prediction % 2] = 1
        for subject_nr, sdm in ops.split(dm.subject_nr):
            factor1_decoding.append(sdm.factor1_correct.mean)
            factor2_decoding.append(sdm.factor2_correct.mean)
            print(f'For subject {subject_nr}, {factor_name[0]} decoding is {sdm.factor1_correct.mean}')
            print(f'For subject {subject_nr}, {factor_name[1]} decoding is {sdm.factor2_correct.mean}')
        print('Overall decoding')
        print(f'{factor_name[0]}: {dm.factor1_correct.mean}')
        print(f'{factor_name[1]}: {dm.factor2_correct.mean}')
        print(f'Statistical testing of {factor_name[0]} decoding --> {ttest_1samp(factor1_decoding, 1/factor_levels[0])}')
        print(f'Statistical testing of {factor_name[1]} decoding --> {ttest_1samp(factor2_decoding, 1/factor_levels[1])}')



def select_ica(raw, events, metadata, exclude_component=0):
    
    global weights_dict
    print(f'running ica to exclude component {exclude_component}')
    @fnc.memoize(persistent=True)
    def run_ica(raw):
        return epp.run_ica(raw)
    # run_ica.clear()
    raw.info['bads'] = []
    ica = run_ica(raw)
    print('applying ica')
    ica.apply(raw, exclude=[exclude_component])
    weights = np.dot(ica.mixing_matrix_[:, exclude_component].T,
                     ica.pca_components_[:ica.n_components_])
    weights_dict = {ch_name: weight
                    for ch_name, weight in zip(ica.ch_names, weights)}
    print(f'weights: {weights_dict} (len={len(weights_dict)})')
    return raw, events, metadata





@fnc.memoize(persistent=True)
def ica_perturbation_decode(subject_nr):
    read_subject_kwargs = dict(subject_nr=subject_nr)
    fdm = bdu.decode_subject(read_subject_kwargs=read_subject_kwargs,
                             factors=FACTORS, epochs_kwargs=TGT_EPOCH_KWARGS,
                             trigger=TARGET_TRIGGER, window_stride=2, window_size=200,
                             n_fold=4, epochs=4)
    print(f'full-data accuracy: {fdm.braindecode_correct.mean}')
    perturbation_results = {}
    for exclude_component in range(N_CHANNELS):
        bdu.decode_subject.clear()
        dm = bdu.decode_subject(read_subject_kwargs=read_subject_kwargs,
            factors=FACTORS, epochs_kwargs=TGT_EPOCH_KWARGS,
            trigger=TARGET_TRIGGER, window_stride=2, window_size=200,
            n_fold=4, epochs=4,
            patch_data_func=lambda raw, events, metadata: select_ica(
                    raw, events, metadata, exclude_component))
        perturbation_results[exclude_component] = dm, weights_dict
        print(f'perturbation accuracy({exclude_component}): {dm.braindecode_correct.mean}')
    return fdm, perturbation_results



def notch_filter(raw, events, metadata, freq):
    width = np.exp(np.log(freq / 4))
    print(f'notch-filtering frequency band: {freq:.2f} / {width:.2f}')
    raw.notch_filter(freq, notch_widths=width, trans_bandwidth=width)
    return raw, events, metadata


@fnc.memoize(persistent=True)
def freq_perturbation_decode(subject_nr):
    read_subject_kwargs = dict(subject_nr=subject_nr,
                               saccade_annotation='BADS_SACCADE',
                               min_sacc_size=128)
    fdm = bdu.decode_subject(read_subject_kwargs=read_subject_kwargs,
        factors=FACTORS, epochs_kwargs=TGT_EPOCH_KWARGS,
        trigger=TARGET_TRIGGER, window_stride=1, window_size=200,
        n_fold=4, epochs=4)
    print(f'full-data accuracy: {fdm.braindecode_correct.mean}')
    perturbation_results = {}
    for freq in NOTCH_FREQS:
        bdu.decode_subject.clear()
        dm = bdu.decode_subject(read_subject_kwargs=read_subject_kwargs,
            factors=FACTORS, epochs_kwargs=TGT_EPOCH_KWARGS,
            trigger=TARGET_TRIGGER, window_stride=1, window_size=200,
            n_fold=4, epochs=4,
            patch_data_func=lambda raw, events, metadata: notch_filter(raw, events, metadata, freq))
        perturbation_results[freq] = dm
        print(f'perturbation accuracy({freq}): {dm.braindecode_correct.mean}')
    return fdm, perturbation_results
  
    
def erp_plots(iv, dv_left, dv_right, dv_mid, dv_posterior, dm):
    """
    Plots ERPs (target-locked)
    as a function of IV
    ----------
    Parameters
    ----------
    iv:         str
                independent variable
    dv_left:    str
                dependent variable (left channels)
    dv_right:   str
                dependent variable (right channels)
    dv_mid:     str
                dependent variable (mid channels)
    dv_posterior:     str
                dependent variable (all channels)
    dm:         DataMatrix
                datamatrix on which analysis should be performed
    """
    
    fig, axs = plt.subplots(2, 2, 
                            figsize=(10, 5), 
                            constrained_layout=True,
                            sharex=True, 
                            sharey=False
                            )
    fig.supxlabel('Time (ms)', color='black', fontsize=12)
    if iv =='inducer':
        hues = ['blue', 'red']
        fig.suptitle('Inducer effect on ERPs',         fontsize=14)
        red_line = mlines.Line2D([], [], color='red', label='Red')
        blue_line = mlines.Line2D([], [], color='blue', label='Blue')
    elif iv =='cue':
        fig.suptitle('Cue validity effect on ERPs',         fontsize=14)
        hues = ['orange','green']
        valid_line = mlines.Line2D([], [], color='green', label='Valid')
        invalid_line = mlines.Line2D([], [], color='orange', label='Invalid')
    elif iv =='cue_eccentricity':
        fig.suptitle('Cue eccentricity on ERPs',         fontsize=14)
        hues = ['lightseagreen','cadetblue','teal']
        near_line = mlines.Line2D([], [], color='lightseagreen', label='Near')
        medium_line = mlines.Line2D([], [], color='cadetblue', label='Medium')
        far_line = mlines.Line2D([], [], color='teal', label='Far')
    elif iv =='target_eccentricity':
        fig.suptitle('Target eccentricity on ERPs',         fontsize=14)
        hues = ['lightseagreen','cadetblue','teal']
        near_line = mlines.Line2D([], [], color='lightseagreen', label='Near')
        medium_line = mlines.Line2D([], [], color='cadetblue', label='Medium')
        far_line = mlines.Line2D([], [], color='teal', label='Far')
    plt.subplot(221) 
    plt.title(r"$\bf{" + 'a) ' + "}$" +
                ' Left channels', fontsize=12, loc='left')
    tst.plot(dm, dv=dv_left, hue_factor=iv, hues=hues)
    plt.legend([], [], frameon=False)
    if iv == 'inducer':
        plt.legend(handles=[valid_line, invalid_line], title='Inducer color')
    elif iv == 'cue':
        plt.legend(handles=[valid_line, invalid_line], title='Cue validity')
    elif iv == 'target_eccentricity':
        plt.legend(handles=[near_line, medium_line, far_line], title='Target eccentricity')
    elif iv == 'cue_eccentricity':
        plt.legend(handles=[near_line, medium_line, far_line], title='Cue eccentricity')
    plt.axvline(25,color='gray',linestyle=':')
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(222)  
    plt.title(r"$\bf{" + 'b) ' + "}$" +
                ' Right channels', fontsize=12, loc='left')
    tst.plot(dm, dv=dv_right, hue_factor=iv, hues=hues)
    plt.legend([], [], frameon=False)
    plt.axvline(25,color='gray',linestyle=':')
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200))          
    plt.subplot(223)
    plt.title(r"$\bf{" + 'c) ' + "}$" +
                ' Midline channels', fontsize=12, loc='left')
    tst.plot(dm, dv=dv_mid, hue_factor=iv, hues=hues)
    plt.legend([], [], frameon=False)
    plt.axvline(25,color='gray',linestyle=':')
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(224)
    plt.title(r"$\bf{" + 'd) ' + "}$" +
                ' Posterior channels', fontsize=12, loc='left')
    tst.plot(dm, dv=dv_posterior, hue_factor=iv, hues=hues)
    plt.legend([], [], frameon=False)
    plt.axvline(25,color='gray',linestyle=':')
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    #plt.xticks(range(0, 501, 100), range(-500, 1510, 400)) 
    plt.show()
    
    
def difference_waves(dm, dv='tgt_erp_avg'):
    """
    Plots difference ERP waves
    ----------
    Parameters
    ----------
    dm:         DataMatrix
                datamatrix on which analysis should be performed
    """
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), constrained_layout=True,
                        sharex=True, sharey=True)
    fig.supxlabel("Time (ms)", fontsize=14)
    fig.suptitle("Difference waves (valid-invalid) across eccentricities", fontsize=14)
    for eccentricity, edm in ops.split (dm.target_eccentricity):
        dm_valid, dm_invalid =  ops.split(edm.cue, 'valid', 'invalid')
        difference_wave =  dm_valid[dv].mean - dm_invalid[dv].mean
        if eccentricity == 'far':
            color = 'teal'
        elif eccentricity == 'medium':
            color = 'cadetblue'
        elif eccentricity == 'near':
            color = 'lightseagreen'
        plt.plot(difference_wave, color =  color)
        plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
        near_line = mlines.Line2D([], [], color='lightseagreen', label='Near')
        medium_line = mlines.Line2D([], [], color='cadetblue', label='Medium')
        far_line = mlines.Line2D([], [], color='teal', label='Far')
        plt.legend(handles=[near_line, medium_line, far_line], title='Cue eccentricity')
    

def interaction(dm):
    fig, axs = plt.subplots(2, 3, 
                            figsize=(12, 4), 
                            constrained_layout=True,
                            sharex=True, 
                            sharey=True
                            ) 
    fig.supxlabel('Time (ms)', color='black', fontsize=12)
    fig.suptitle('Target eccentricity x Cue validity', color='black', fontsize=14)
    dm_near, dm_medium, dm_far =  ops.split(dm.target_eccentricity, 'near', 'medium', 'far')
    plt.subplot(231)
    plt.title(r"$\bf{" + 'a) ' + "}$" +' Near', color='lightseagreen', fontsize=12)
    plt.ylabel('Posterior channels', fontsize=12)
    plt.axvline(25,color='gray',linestyle=':')
    tst.plot(dm_near, dv='tgt_posterior_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    valid_line = mlines.Line2D([], [], color='green', label='Valid')
    invalid_line = mlines.Line2D([], [], color='orange', label='Invalid')
    plt.legend(handles=[valid_line, invalid_line], title='Cue validity')
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(232)
    plt.title(r"$\bf{" + 'b) ' + "}$" +' Medium', color='cadetblue', fontsize=12)
    plt.axvline(25,color='gray',linestyle=':')
    tst.plot(dm_medium, dv='tgt_posterior_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(233)
    plt.title(r"$\bf{" + 'c) ' + "}$" +' Far', color = 'teal', fontsize=12)
    plt.axvline(25,color='gray',linestyle=':')
    tst.plot(dm_far, dv='tgt_posterior_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(234)
    plt.ylabel('Midline channels', fontsize=12)
    plt.axvline(25,color='gray',linestyle=':')
    tst.plot(dm_near, dv='tgt_mid_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(235)
    plt.axvline(25,color='gray',linestyle=':')
    tst.plot(dm_medium, dv='tgt_mid_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200)) 
    plt.subplot(236)
    plt.axvline(25,color='gray',linestyle=':')
    plt.legend([], [], frameon=False)
    tst.plot(dm_far, dv='tgt_mid_erp_avg', hue_factor='cue', hues = ['orange','green'])
    plt.legend([], [], frameon=False)
    plt.xticks(range(0, 401, 50), range(-100, 1510, 200))
    

"""
TFR related functions
"""

def tfr_target_eccentricity(dm, epoch):
    """
    Plots time-frequency heat maps
    for each Target Eccentricity contrast
    ----------
    Parameters
    ----------
    dm: DataMatrix
        datamatrix in which the data is contained
    epoch: str
        epoch based on which tfr is done ('target' or 'cue')
    """
    if epoch == 'target':
        dm.tfr = dm.tgt_tfr
    elif epoch == 'cue':
        dm.tfr = dm.cue_tfr
    fig, axs = plt.subplots(1, 3, 
                            figsize=(12, 4), 
                            constrained_layout=True,
                            sharex=True, 
                            sharey=True
                            ) 
    fig.supxlabel('Time (ms)', color='black', fontsize=12)
    fig.supylabel('Frequency (Hz)', color='black', fontsize=12)
    fig.suptitle('Target eccentricity', color='black', fontsize=14)
    plt.subplot(141)
    tfr_far = (dm.target_eccentricity == 'far').tfr[...]
    tfr_medium = (dm.target_eccentricity == 'medium').tfr[...]
    tfr_near = (dm.target_eccentricity == 'near').tfr[...]
    plt.title(r"$\bf{" + 'a) ' + "}$" + ' Far - Medium')
    plt.imshow(tfr_far - tfr_medium, aspect='auto',
               interpolation='bicubic', vmin = -.1, vmax =.1)
    plt.xticks(np.arange(0, 61, 15), np.arange(0, 1001, 250))
    plt.yticks(np.arange(0,60, 10), np.arange(4, 36.5, 5.5))
    plt.subplot(142)
    plt.title(r"$\bf{" + 'b) ' + "}$" +' Far - Near')
    plt.imshow(tfr_far - tfr_near, aspect='auto', interpolation='bicubic', vmin = -.1, vmax =.1)
    plt.xticks(np.arange(0, 61, 15), np.arange(0, 1001, 250))
    plt.yticks(np.arange(0,60, 10), np.arange(4, 36.5, 5.5))
    plt.subplot(143)
    plt.title(r"$\bf{" + 'c) ' + "}$" +' Medium - Near')
    plt.imshow(tfr_medium - tfr_near, aspect='auto', interpolation='bicubic', vmin = -.1, vmax =.1)
    plt.xticks(np.arange(0, 61, 15), np.arange(0, 1001, 250))
    plt.yticks(np.arange(0,60, 10), np.arange(4, 36.5, 5.5))
    plt.savefig('svg/tfr-validity-eccentricity.svg')
    plt.show()





def tfr_cue_validity(dm, epoch):
    """
    Plots time-frequency heat maps
    for Cue Validity
    ----------
    Parameters
    ----------
    dm: DataMatrix
        datamatrix in which the data is contained
    epoch: str
        epoch based on which tfr is done ('target' or 'cue')
    """
    if epoch == 'target':
        dm.tfr = dm.tgt_tfr
    elif epoch == 'cue':
        dm.tfr = dm.cue_tfr
    plt.plot()
    tfr_valid = (dm.cue == 'valid').tfr[...]
    tfr_invalid = (dm.cue == 'invalid').tfr[...]
    plt.imshow(tfr_valid - tfr_invalid, aspect='auto',
               interpolation='bicubic')
    plt.xlabel('Time (ms)',color ='black', fontsize=12)
    plt.ylabel('Frequency (Hz)',color ='black', fontsize=12)
    plt.title('Cue validity (valid - invalid)', fontsize=14)
    plt.xticks(np.arange(0, 61, 15), np.arange(0, 1001, 250))
    plt.yticks(np.arange(0,60, 10), np.arange(4, 36.5, 5.5))
    #plt.savefig('svg/tfr-cue-validity.svg')
    plt.show()
