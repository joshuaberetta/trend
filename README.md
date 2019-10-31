# Trend
> Generating animations from GIS and node data

This program generates animated gifs for a yearly and monthly period for each variable of interest. The output of the programme is both the frames from each year in the series and each month of the year in a png format and gifs that have stitched the individual frames together into a simple animation.

The input vaiables as well as some other minor tweaks can be configured in the `config.yaml` file.

Here's an example output:

![](examples/example_output.gif)

## Installation

>(Note:
All the following lines in this file that
```sh
look like this
```
>must be copy and pasted into your `Anaconda Prompt`, followed by pressing `enter` on your keyboard.)

### First and foremost
If you don't alread have `Anaconda` installed, go to the following [website](https://www.anaconda.com/distribution/) and download the following file for your particular operating system (Windows / macOS / Linux):

![](examples/anaconda.JPG)

Once the download has completed, follow the instructions in this [article](https://problemsolvingwithpython.com/01-Orientation/01.03-Installing-Anaconda-on-Windows/) for installing `Anaconda` on your system.

### Getting the files

Here you have a couple options:
1. 

- Download `Anaconda` from their website: 
- Unzip the `trend.zip` file and place in desired location
- Copy in your variable's folders containing the `*.dat` files into the folder `data/variables`
- On your machine, open up `Anaconda Prompt`
    - Copy the path of your `trend` folder
    - Type `cd <trend-folder-path>` into the command prompt (paste the `trend` path after the `cd`)
    - Copy `conda env create -f environment.yml` into the command prompt and press enter
        - If prompted to type `[y/n]`, type `y` and press enter
        - Wait for the downloads to finish
    - Copy `conda activate trend` into the command prompt and press enter
        - The beggining of your command line should say `(trend)`
- Open up the `config.yaml` in a text editor
    - Follow the instructions in the file
- Copy `python cli.py` into the command prompt and press enter
- DONE

## Environment setup

Run the following command in your `Anaconda Prompt`:
```sh
conda env create -f environment.yml
```

Wait for all the downloads to take place. If prompted to type `[y/n]`, type: 
```sh
y
```

Once all the downloads have completed successfully, run the following command:
```sh
conda activate trend
```

Once you have completed running the program and you have all your outputs, run the following command:
```sh
conda deactivate
```

## Usage example

Open the `config.yaml` file in your text editor of choice and follow the instructions in the file. 
> If you don't have a text editor, download any of the following free programmes: `VS Code`, `Sublime`, `Notepad ++`, etc.

Run the following command from the directory where `cli.py` is placed:
```sh
python cli.py
```

### Notes on Installation

The program should now be running and there should be a progress bar moving along.

The outputs of the script will now be sitting in the output folder specified in the `config.yaml` file.

If you have any issues with any of these steps, please contact me to assist.

## Meta
