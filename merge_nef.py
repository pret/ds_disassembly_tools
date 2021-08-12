#!/usr/bin/env python3

# Creates an ELF from a NEF and corresponding SBIN.

import argparse
import tempfile
import subprocess
import struct
import shlex
import os


class Namespace(argparse.Namespace):
    sbin: str
    nef: str
    elf: str


Elf32_Ehdr = struct.Struct('<16bhhlllllhhhhhh')
Elf32_Phdr = struct.Struct('<llllllll')
Elf32_Shdr = struct.Struct('<llllllllll')
Elf32_Sym = struct.Struct('<lllbbh')


def dump_autoloads(sbin, nef):
    with open(sbin, 'rb') as sbinf:
        binary = sbinf.read()

    with open(nef, 'rb') as neff:
        header = Elf32_Ehdr.unpack(neff.read(Elf32_Ehdr.size))
        entry = header[19]
        shoff = header[21]
        shentsize = header[26]
        shnum = header[27]
        shstrndx = header[28]

        neff.seek(shoff)
        secs = list(Elf32_Shdr.iter_unpack(neff.read(shnum * shentsize)))
        neff.seek(secs[shstrndx][4])
        shstrtab = neff.read(secs[shstrndx][5])
        sec_names = {}
        for i, sec in enumerate(secs):
            if sec[3] != 0:
                sec_names[sec[3]] = shstrtab[sec[0]:].split(b'\0', 1)[0].decode()
            if sec[1] == 2:
                neff.seek(sec[4])
                symtab = list(Elf32_Sym.iter_unpack(neff.read(sec[5])))
            elif sec[1] == 3 and i != shstrndx:
                neff.seek(sec[4])
                strtab = neff.read(sec[5])
            elif sec[1] == 1 and sec[3] != 0 and sec[3] <= entry and (sec[5] == 0 or entry < sec[3] + sec[5]):
                secstart = sec[3]
    for sym in symtab:
        if strtab[sym[0]:].split(b'\0', 1)[0] == b'_start_ModuleParams':
            offset = sym[1] - secstart
            break
    else:
        raise ValueError('No symbol found in NEF named "_start_ModuleParams"')
    atab_start, atab_end, aload, bss_start, bss_end = struct.unpack_from('<lllll', binary, offset)
    aload -= secstart
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(binary[:aload])
    tf.close()
    yield sec_names.get(secstart), tf
    for start, size, bsssize in struct.iter_unpack('<lll', binary[(atab_start - secstart):(atab_end - secstart)]):
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.write(binary[aload:aload + size])
        tf.close()
        yield sec_names.get(start), tf
        aload += size


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sbin')
    parser.add_argument('nef')
    parser.add_argument('elf')
    args = parser.parse_args(namespace=Namespace())
    tfs: list[str, tempfile.NamedTemporaryFile] = list(dump_autoloads(args.sbin, args.nef))
    flags = ' '.join('--update-section {name:s}={file:s} -j {name:s}'.format(name=name, file=tf.name) for name, tf in tfs)
    callstr = f'arm-none-eabi-objcopy {flags} {args.nef} {args.elf}'
    print(callstr)
    subprocess.run(shlex.split(callstr))
    for name, tf in tfs:
        os.remove(tf.name)


if __name__ == '__main__':
    main()
