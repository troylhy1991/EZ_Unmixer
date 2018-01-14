# EZ_Unmixer

1. EZ_Unmixer is a tool for quick spectal unmixing of two channel images.

      Master channel: the dominant channel (Left Image Panel)
 
      Leakage channel: the corrupted channel (Right Image Panel)

2. By sampling several leaked area, a spectral leakage ratio will be calculated;

3. leaked signal component will be subtracted from the Leakge channel.

## Installation

1. Install [Acaconda Python 2.7](https://www.anaconda.com/download/);

2. create a conda virtual env "conda create -n EZ_Unmixer", and "activate EZ_Unmixer";

3. conda install -c conda-forge pims;

4. conda install -c anaconda pyqt=4.11.4.

## Usage Tips

1. Start the tool by typing "python unmixer.py";

2. Toggle on/off draw/sample mode by press key D;

3. Follow the demo video.


