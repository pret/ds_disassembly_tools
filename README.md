These scripts were written to assist with the disassembly of Nintendo DS ROMs. They were previously tracked in [pokeheartgold](/pret/pokeheartgold).

Python scripts require python-3.9 or newer.

Most of these scripts are niche, but a few are more broadly applicable.

## asmdiff.sh
Usage: `asmdiff.sh [-h] [-7] [-m OVERLAY] [-r BASEROM] [-d BUILDDIR] [START [END]]`

When rebuilding the ROM, sometimes a change you make results in an incorrect component being built. This tool will help you investigate the differences. It relies on devkitARM being installed; if you don't have this, it will try to use `arm-none-eabi-objdump` installed on your PATH.

This tool will extract the reference component and, if necessary, uncompress it. \
Pass `-7` to compare the ARM7 binary, otherwise the ARM9 binary will be compared. \
Pass `-m OVERLAY` to compare the overlay with index OVERLAY, otherwise the static module will be compared. \
The default behavior is to use `baserom.nds` as a reference and compare it to the files in `build/heartgold.us` for ARM9 and `sub/build` for ARM7. Use the `-r` flag to use a different reference ROM and the `-d` flag to override the build directory. \
START and END are optional. They indicate the first and last address to be compared. All addresses are with respect to the DS console memory rather than a relative file offset.

## dump_fs.py

Usage: `dump_fs.py [-h] ROM [--no-dump-overlays] [--no-dump-files] [--fsroot FSROOT] [--ovysubdir OVYSUBDIR] [--arm9-root ARM9_ROOT] [--arm7-root ARM7_ROOT]`

Extracts the Nitro file system from a ROM, this includes all overlay modules. \
Control the output directories using --fsroot, --ovysubdir, --arm9-root, and --arm7-root. \
If --no-dump-overlays is passed, no overlay files will be created. Instead, it will print an overlay spec for the linker spec file. \
If --no-dump-files is passed, no files will be created. Instead, it will print a table of file ID, filename, start offset, and file size.

## find_module_params.py
A helper script for asmdiff.sh to help it find the end of the compressed static module. It takes in the (possibly compressed) ARM9 static module and returns the offset to `_start_ModuleParams`.

## get_overlay_load_order.py
Usage: `get_overlay_load_order.py ROM`

It is typical for overlays to be defined with their start addresses after another module. This script helps reverse engineer that spec. It also dumps the overlay table as a flat binary.

## insert_labels.py
Usage: `insert_labels.py BINFILE OFFSETS VMA`

BINFILE: the flat binary from which data should be extracted \
OFFSETS: text file with one data address per line \
VMA: address at the start of the flat binary

Redumps the binary data starting at the first offset and working to the end of the file, inserting labels at each intermediate offset.

## merge_nef.py
Usage: `merge_nef.py SBIN NEF ELF`

SBIN: The static module \
NEF: Debugging symbols for the static module \
ELF: Output file

Creates an ELF file with all the code and data from the static module plus correctly-adjusted VMAs for the autoloads.

## ntruncompbw.c
Compile: `gcc -g -O3 -o ntruncompbw ntruncompbw.c`

Usage: `ntruncompbw FILE VMA END`

FILE: the flat compressed binary \
VMA: the load address of the binary in DS RAM \
END: offset of the compressed binary's footer

Undoes the effects of `ntrcompbw.exe`.
