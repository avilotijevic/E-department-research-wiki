---
layout: default
title: Eye-tracking
parent: Methods
nav_order: 1
---

# Eye tracking

Eye tracking is a method for measuring eye-related events—such as eye movements, gaze position, and pupil size—during an experiment. It is widely used to study visual attention, perception, decision-making, and cognitive processing.

In addition to gaze behavior, eye trackers can also measure **pupil size** (pupillometry), which is commonly used as an index of arousal, and sensory processing.

## Eye-tracking facilities

Eye-tracking systems are available in the following labs:

- **M226** – Munting Building, 2nd floor  
- **H-184** – Heymans Building, basement

Both labs are equipped with the **EyeLink 1000** eye-tracking system.

## What is eye tracking used for?

Eye tracking can be used to measure:

- gaze position and fixation patterns  
- saccades and eye movements  
- pupil size changes (pupillometry)

In this department, eye tracking is commonly combined with:

- behavioral experiments  
- EEG recordings  
- stimulation techniques  
- other psychophysiological measures

Please note that **not all labs support all combinations of eye tracking with other measurement techniques**.

## Typical workflow for an eye-tracking study

The recommended order of steps when running an eye-tracking experiment is:

1. Build the experiment using the **OpenSesame eye-tracking template**.
2. Test the experiment locally without the eye tracker to verify logic and timing.
3. Run and test the experiment in the lab with the **EyeLink system connected**.
4. Verify that behavioral output files (.csv) and eye-tracking files (.edf) are generated correctly.
5. If everything works as expected, start data collection.
6. Perform calibration and validation for each participant.
7. Collect data and verify output files after each session.

## Starting an eye-tracking experiment

Typical setup procedure:

- Turn on the stimulus computer and the EyeLink system.
- Start the experiment computer and open the experiment in OpenSesame.
- Check the camera and participant position.
- Perform eye-tracker calibration/ validation procedure.
- Verify that gaze tracking is stable before starting the experiment.

If calibration quality is poor, adjust:

- participant head position
- camera alignment

## After the session

After completing the experiment:

- Stop the recording.
- Save the EDF data file.
- Back up behavioral and eye-tracking data.
- Turn off all computers.
- Unplug the eye tracker.

## Data handling

EyeLink experiments typically produce:

- **.edf files** containing eye-tracking data
- **.csv files** containing behavioral data

After each session:

- Verify that both files were saved correctly.
- Copy data to the appropriate project folder.
- Back up the data to secure storage.

## Important notes

- Always test experiments in the lab before running participants.
- Ensure calibration quality before starting recordings.
- Keep environmental conditions consistent during the experiment.
