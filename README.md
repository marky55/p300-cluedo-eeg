\# P300 Cluedo EEG Analysis



This project analyzes EEG data recorded during a \*\*P300-based Cluedo task\*\*, following the instructions from the course assignment :contentReference\[oaicite:2]{index=2}.  

The goal is to determine \*\*which suspect, weapon, and location\*\* the subject was focusing on by detecting the \*\*P300 event-related potential (ERP)\*\*.



---



\## Task Summary



During the experiment, the subject was shown:

\- 9 \*\*suspects\*\* (markers 11–19)

\- 9 \*\*weapons\*\* (markers 21–29)

\- 9 \*\*locations\*\* (markers 31–39)



At each stimulus onset, a marker was sent to the EEG recording system (see page 2 of the assignment :contentReference\[oaicite:3]{index=3} for the visual interface).



The P300 response should appear:

\- ~300 ms after the target stimulus  

\- As a \*\*positive peak\*\*, strongest in centro-parietal electrodes



---



\## What the Script Does



The included Python script (`main.py`) :contentReference\[oaicite:4]{index=4} performs:



\### 1. EEG Preprocessing

\- Loads `.mat` files (`Cluedo1.mat`, `Cluedo2.mat`)

\- Selects channels (e.g., Fz)

\- Extracts stimulus \*\*timestamps\*\* using markers

\- Cuts EEG into \*\*epochs\*\* from:

&nbsp; - \*\*−100 ms to +1000 ms\*\* relative to onset (as required in assignment)

\- Performs \*\*baseline correction\*\* (subtracts pre-stimulus mean)



\### 2. ERP Computation

For each marker:

\- Averages all epochs  

\- Produces ERP curves for:

&nbsp; - All suspects  

&nbsp; - All weapons  

&nbsp; - All locations



Plots (per assignment instructions):

\- Mean ERP curves per suspect  

\- Mean ERP curves per weapon  

\- Mean ERP curves per location  



These allow \*\*visual detection of the P300 target\*\*, as described on page 3 of the assignment :contentReference\[oaicite:5]{index=5}.



\### 3. Automatic Detection

Two peak-based methods are implemented:



\#### A) Mean peak amplitude

The suspect/weapon/location with the largest mean positive peak is selected.



\#### B) Electrode voting

Each electrode votes for its top peak → majority vote selects the item.




