# Citi Bike Visualizations

### This is a school project for learning Bokeh

#### The data used here is Citi Bike Trip History Data which can be found [here](https://s3.amazonaws.com/tripdata/index.html)
##### This project uses only data from one month!

### If you want to run this on your computer, you need to install Anaconda, Bokeh, Pandas and get Google Maps API KEY.

##### For macOS users: 
1. Install Anaconda from homebrew: ``brew cask install anaconda`` (Read more from here: https://medium.com/ayuth/install-anaconda-on-macos-with-homebrew-c94437d63a37)
2. Install Bokeh: ``conda install bokeh`` (Read more from here: https://docs.bokeh.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart-install)
3. Install Pandas: ``pip install pandas`` (Read more from here: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
4. Get Google Maps API KEY
5. To see all visualizations at once, run: ``bokeh serve citi-bike-history.py`` and open http://localhost:5006/citi-bike-history