#!/usr/bin/env python3

import subprocess
import os
import binascii
import sys
import time
import nfc
from nfc.clf import RemoteTarget
from time import sleep

# install nfcpy: sudo  pip3 install nfcpy

# create an instance of the PN532 class.
#pn532 = PN532.PN532("/dev/ttyAMA0",115200)
dir_path = os.path.dirname(os.path.realpath(__file__))
oldcardid = 0
cardid = 0

with nfc.ContactlessFrontend('tty:AMA0') as clf:

    while True:

            sleep(0.1)  # don't burn the CPU

            # reading the card id
            target = clf.sense(RemoteTarget('106A'))

            if target is None:
                #print("No CardID")
                if oldcardid != 0:
                    #comment next line out if removing the card should not stop playback.
                    subprocess.call([dir_path + '/playout_controls.sh -c=playerpauseforce'], shell=True)
                    oldcardid = 0
                    #print("Pause music")

                continue

            elif target.sdd_res.hex() != oldcardid:
                try:
                    # start the player script and pass on the cardid
                    cardid=target.sdd_res.hex()
                    subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + cardid], shell=True)
                    #print("old CardID: " +  oldcardid)
                    oldcardid = cardid
                    #print("new CardID: " +  cardid)
                except OSError as e:
                    print("Execution failed:")
