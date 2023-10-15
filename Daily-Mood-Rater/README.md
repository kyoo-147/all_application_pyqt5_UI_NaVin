# Daily Mood Rater

 This is a simple app where you can rate your mood daily from 1 to 10 and keep track of your mood history by month.

The app features a graph function, where all the mood ratings within a specific month will be visualized. If an *optional* description was added for any specific day, the description can be viewed by hovering over the bar that represents that day.



## Requirements

The current required libraries for this app to work are:

- `PyQt5`
- `matplotlib`
- `mplcursors`

these libraries also have their own dependencies, so using the included `requirements.txt` is recommended.



#### Installing with `requirements.txt`

1. Activate your virtual environment

2. ```shell
   pip install -r requirements.txt
   ```



## Features to be added

#### Export Mood Data to CSV or Excel

I am planning on adding options to export mood data to a `CSV` or `Excel` file.


#### Custom Color Palettes

Currently, the app has only 1 set of colors to visualize the mood scale. There will be more palettes in the upcoming updates.



#### Graph Background Color

Currently, the app has a dark mode only for the main window. The graph window is actually a `matplotlib` figure embedded into a `Qt` window, so changing the theme of the Qt application does not affect the graph colors. In the future, updates the dark mode will also affect the `matplotlib` graph.



## Known Bugs

- Clicking anywhere other than the slider pointer makes the slider go to either 1 or 10
- Visual bug: Although the slider is scrollable with mousewheel, the changes to the values do not actually reflect on the display text
  - This issue **does not** affect the actual value entered into the database. 
    - e.g. If the slider is scrolled to **2**, but the display text shows **5**, the rating in the database will still be **2**.



## Credits

"[faces](https://thenounproject.com/term/faces/4127357/)" icon created by Vector Valley, PK from [the Noun Project](http://thenounproject.com/).

