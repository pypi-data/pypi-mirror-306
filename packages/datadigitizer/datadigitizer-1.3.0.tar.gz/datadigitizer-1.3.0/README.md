# Introduction

DataDigitizer is a simple graphical tool for digitizing data from images.

In terminal enter the following command:

```bash
python -m datadigitizer
```


The cursor is used to point a specific position in the graph
whereas all operations are done through keyboard combinations or through the main menu.

Legend:

* Red crosses are data points
* Blue crosses are Xmin and Xmax
* Green crosses are Ymin and Ymax

Commands:

* <Ctrl-o> for loading image.
* <Ctrl-a> add data point.
* <Hold a+Left Click> add data point.
* <Left Click> select a data point.
* <Hold Ctrl+Left Click> multiple data point selection.

* <Ctrl-g> set Xmin from last data point or from selected data point.
* <Ctrl-h> set Xmax from last data point or from selected data point.

* <Ctrl-j> set Ymin from last data point or from selected data point.
* <Ctrl-k> set Ymax from last data point or from selected data point

* <Ctrl-l> set all limits from last 4 data points or from last 4 selected data points.
* <Ctrl-n> remove all limits.

* <Ctrl-z> remove last data point.
* <Ctrl-d> remove selected data point.
* <Ctrl-D> remove all data points.

* <Ctrl-m> compute the data points.
* <Ctrl-t> view data table.
* <Ctrl-s> save data points.
* <Ctrl-w> clear all.



# Dependencies

numpy>=1.21, <2 
matplotlib>=3.4.0 
Pillow>=9.0.0


# Installation

```
pip install datadigitizer
```

# License

MIT License

