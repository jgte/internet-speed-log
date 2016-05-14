# Internet Speed Log

This program will test your internet speed and append it to a file specified in the first input argument.
You can schedule it to run however often you want using `crontab`. Also if you have
a laptop like me, it may be more suitable to run this on a Raspberry Pi or something
that is always connected to the internet.

## Getting Started

This program uses the fabulous `speedtest-cli` tool:

    sudo pip install speedtest-cli

Then download this repo and setup a cron job:

    git clone https://github.com/jgte/internet-speed-log.git

### Crontab

Setting up a cron job on a unix system (I use my Raspberry Pi) is pretty easy. There is simple [documentation](http://www.raspberrypi.org/documentation/linux/usage/cron.md) for
how to do it as well.

Run `crontab -e` to open up the cron job list. Append the following line:

```
# Speedtest
0 * * * * python /home/pi/programs/internet-speed-log/speedtest.py /home/pi/programs/internet-speed-log/speedLog.txt
```

This will run `speedtest.py` every hour on the hour.

### Input files

Should you require to parse input files containing the output of `speedtest-cli`, use the second input argument for that:

```
speedtest-cli --share > /tmp/speedtest-cli.log
python /home/pi/programs/internet-speed-log/speedtest.py /home/pi/programs/internet-speed-log/speedLog.txt /tmp/speedtest-cli.log
```

### Debug

To check if the parsing of the a test string is working as expected, set the variable `debug` to True (line 16).


### Plotting

I've including a `plot-data.py` script that is incomplete right now will plot your
download and upload speed as a function of a time span. This is coming soon.

### Disclaimer

I kept this log file as much unchanged as possible relative to the [original](https://github.com/ccorcos/internet-speed-log).