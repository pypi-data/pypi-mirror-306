# CCMPlots



## Purpose

CCM plots includes .mplstyle files suitable for plotting scientific data. It uses the same approach as the package SciencePlots.

## Installation

```python
pip install ccmplots
```

As a compromise, the package relies on the MS fonts Arial and Times New Roman. If you are using Linux, these fonts need to be installed on your system. This can be done like this:

```
 sudo apt install ttf-mscorefonts-installer & sudo fc-cache -vr
```

## Usage

The package has to be imported. The style can be selected. The base style is called "ccm". 

```python
import ccmplots

plt.style.use("ccm")

x = np.linspace(0,10,100)
y = np.sin(x)

plt.plot(x,y)
plt.xlabel("my xlabel")
plt.ylabel("my ylabel")
plt.title("my title")
plt.show()
```

The code above produces the following figure which has the default aspect ratio of 6/5. The width of the base style "ccm" is 3.5 inches which corresponds to approx 89 mm. 

![image](examples/simple.svg "Simple figure")

The width of a column in the base style "ccm" can be combined with other styles such as "square" or "sans". Furthermore, the color cycler can be modified. Currently, there is only one additional pre-defined color cycle available which is called "tum4c" and comprises the 4 main TUM colors. The default font size is 8 (this is the font size in Elsevier articles). If the font size should be increase to 11 (to match manuscript text size) "large_font" can be added.

```python
plt.style.use(["ccm", "square", "bw_palette", "large_font"])

```
![image](examples/simple_sans.svg "Simple figure")


Among other things, the examples folder contains the python code to create the following figure:

![image](examples/plot_3square.svg "Panel with 3 diagrams")
