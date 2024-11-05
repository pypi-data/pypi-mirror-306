Miniquant -- Python Wrapper for PicoQuant's Harp API
====================================================

This is a modern, convenient Python interface for PicoQuant's HydraHarp
photon counter and similar devices. It connects to [PicoQuant's properietary
C library](https://github.com/PicoQuant/HH400-v3.x-Demos/tree/master/Linux/64bit/library).

Obligatory disclaimer: this is not an officially supported product of PicoQuant,
or in any other way affiliated, endorsed or sponsored by PicoQuant. Use at your
own risk. If you break it, you get to keep both pieces. If it breaks your hardware
(though it shouldn't), it's on you.

Supported Devices
-----------------

To this point, Miniquant has been only developed for and tested with PicoQuant's
HydraHarp 400. Other devices (e.g. the PicoHarp) may be easy to support, but
no work has been done on that.

Installation
------------

Miniquant has only been tested on Linux. This installation guide focuses
on getting it up and running there.

1. **Obtain the Miniquant package.** There are several ways to do that:
   - Via PIP: `pip install miniquant` to run the latest official release
   - From [git repository](https://gitlab.com/codedump2/miniquant):
     ```
	 $ git clone https://gitlab.com/codedump2/miniquant
	 $ cd miniquant
	 $ pip install -e .
	 ```

2. **Obtaining
   [`hhlib.so` ](https://github.com/PicoQuant/HH400-v3.x-Demos/raw/master/Linux/64bit/library/hhlib.so)**
   Miniquant uses the [official manufacturer's API library](https://github.com/PicoQuant/HH400-v3.x-Demos),
   `hhlib.so`. This has to be obtained manually, as it cannot be distributed
   with the Miniquant
   package for licensing reasons.
   Place it somewhere on your system were it's easily accessible
   (e.g. `~/.local/share/miniquant/hhlib.so`, or, quite generically, into `/path/to/hhlib.so`)
   and point the environment variable `MINIQUANT_HHLIB` to the full path of the library.
   ```
   $ mkdir -p ~/.local/share/miniquant
   $ export MINIQUANT_LIB=~/.local/share/miniquant/hhlib.so
   $ curl -O $MINIQUANT_LIB https://github.com/PicoQuant/HH400-v3.x-Demos/raw/master/Linux/64bit/library/hhlib.so
   ```
   For downloading `hhlib.so`, you can alternatively use the supplied script
   `helpers/download-hhlib`, which is located either in the Miniquant source tree,
   or in the distribution folder of the installed package.

3. **Seting up the proper USB device permissions.** The device ID is `0e0d:0004`
   for the PicoHarp,
   and `0e0d:0009` for the HydraHarp. You can either set permissions to allow
   read-write for everyone (`0666`), or allow read-write for a specific group
   (e.g. dialout). The example file `helpers/miniharp.rules` shows udev rules for
   the first option, i.e. allowing access for everyone:
   ```
   $ sudo cp helpers/miniquant.rules /etc/udev/rules.d/99-miniquant.rules
   $ sudo udevadm control --reload
   $ sudo udevadm trigger
   ```
   
4. **Dealing with the quirky USB controller.**
   At least the PicoQuant PicoHarp device, possibly others, have buggy USB
   controllers. You may have to enable USB core device quirks. To do this
   temporarily, execute this as a privileged user (e.g. `root`):
   ```
   $ echo 0e0d:0009:k >> /sys/module/usbcore/parameters/quirks
   ```
   To make the changes permanent, append `usbcore.quirks=0e0d:0009:k` to the
   linux kernel boot command line (e.g. by editing `/etc/default/grub` or
   `/boot/grub2/grub.cfg`, depending on the customs of the Linux distribution
   you're using).
   
   Failing to do this will result in the HydraHarp 400 not responding
   to connection attempts, and a corresponding disconnection entry
   in `dmesg`.

5. **Checking your installation.** For a start,
   `dmesg` should tell you whether you the device is properly reconized:
   ```
   $ dmesg
   ...
   usb 2-2: new SuperSpeed USB device number 4 using xhci_hcd
   usb 2-2: New USB device found, idVendor=0e0d, idProduct=0009, bcdDevice= 0.01
   usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
   usb 2-2: Product: HydraHarp 400
   usb 2-2: Manufacturer: PicoQuant
   usb 2-2: SerialNumber: 1041490
   ```
   Trying a simple Python script will also show you whether the connection
   can be established:
   ```
   $ python
   >>> from miniquant.harp import Monster
   >>> h = Monster().find('any')
   >>> h.serial
   1041490
   ```
   
Unit testing
------------

Miniquant comes with a set of unit tests which require a Harp device
attached to the computer. As such, they cannot be executed automatically
e.g. in a CI/CD enviroment, but can, and should, be executed by developers
working on Miniquant, or on users wanting to check the compatibility
of their device with the software.

The unit tests are in the `miniquant.tests_hw` module, and they are divided
in two groups:
 
  - `harp_test_quirked` contains tests that check proper failure
    reporting on a system that does *not* have the USB quirks enabled
	(see [Installation](#installation) above. Essentially, the tests succeed
	when connection *fails*.
	
  - `harp_test` contains function tests on the hardware itself, i.e.
    correct connection and data processing.
	
The tests can be started using Pytest and will use the first device
available.


Usage Principles
----------------

There are two main classes the end user will directly interact with:

  - `miniquant.harp.Monster` represents a connection to the `hhlib.so`
    library. Essentially, requests of finding and opening an attached
	device are directed to that class:
	```
	>>> from miniquant.harp import Monster
	>>> h = Monster().find()
	```
	`Monster.find()` takes several types of parameters to specify
	the identity of the device to be opened. Check the
	[class documentation](src/miniquant/harp.py) for details.
	The function returns a Harp device object.

  - `miniquant.harp.MonsterHarp` is the Harp device object of
    an "open" device. It offers a number of Python properties,
	mostly named after getter and setter
	[functions in the manufacturer's library.](https://github.com/PicoQuant/HH400-v3.x-Demos/raw/master/Linux/manual_HHLibLinuxv3.0.0.2.pdf)
	Reading or setting those properties will trigger calls to
	those specific functions.
	
Specific properties `miniquant.harp.MonsterHarp` object will return
sub-objects with properties of subsystems of the Harp ("portals").
For instance:

  - `miniquant.harp.InputChannel` and `miniquant.harp.InputChannelPortal`
    for access to channel-specific API elements
	
  - `miniquant.harp.ModuleInfoPortal` for access to API elements specific
    to Harp extension modules
	
  - `miniquant.harp.ErrorStringPortal` for easier handling of error
    messages / strings from the Harp API.
	
In general, effort has been made to make access to the Harp device as
"Python-esque" as possible. But ultimately, the capabilities of Miniquant
are limited by the underlying API.

See also the [examples section below](#examples) for more elaborate
usage scenarii.

Examples
--------

### Reading device information

This is how to open a device and view general information
like hardware details, warnings, features and flags. Note
that some data (e.g. flags) may not necessarily contain useful
data unless measurement work has been started. Consult PicoQuant
documentation for that.

```
#!/usr/bin/python3

import miniquant.harp as harp

hdev = harp.Monster().find()
hdev.initialize (harp.MeasurementMode.Histogramming, harp.ReferenceClock.Internal)

print ("Serial number:", hdev.serialNumber)
print ("Hardware info:", hdev.hardwareInfo)
print ("Base Resolution:", hdev.baseResolution)

print ("Features:", [ f for f in hdev.features ])
print ("Modules:", [ m.info for m in hdev.modules])
print ("Input count rates:", [ c.countRate for c in hdev.channels])
print ("Flags:", [ f for f in hdev.flags])
print ("Warnings:", [ w for w in hdev.warnings])
```

### Reading and plotting histogram

Here's how to initialize and read a data histogram with
minimal settings to the HydraHarp:

```
#!/usr/bin/python3

import miniquant.harp as harp
import matplotlib.pyplot as plt

hdev = harp.Monster().find()
hdev.initialize(harp.MeasurementMode.Histogramming,  harp.ReferenceClock.Internal)
hdev.calibrate()
hdev.syncCfd = { "level": 0.200, "zerox": 0.01 }
hdev.channels[0].cfd = { "level": 0.300, "zerox": 0.01 }

hdev.clearHistogram()
hdev.acquire(1.0)          ## acquire data for 1 second
while hdev.acquiring:
	pass

data = hdev.channels[0].histogram

plt.plot(data)

```

Copying
-------

Note that Miniquant is *only* available under the
[GNU GPL license](./LICENSE). You are not allowed
to base commercial products on Miniquant. You are also not allowed
to redistribute this, or any products derived from it, unless you
place said products under the same license.
