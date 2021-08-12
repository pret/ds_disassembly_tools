#!/usr/bin/env bash

(head -c  44 baserom.nds | tail -c 4
head -c  40 baserom.nds | tail -c 4
head -c  48 baserom.nds | tail -c 4
head -c 116 baserom.nds | tail -c 4
sed -r '/^Overlay/!d' main.lsf | sed 's/Overlay //g' | while read ovname; do echo -ne "${ovname}.sbin\0"; done) > main_defs.sbin
