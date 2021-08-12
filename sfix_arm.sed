## Common
# 4byte/2byte
s/4byte/word/
s/2byte/short/

# Comment chars
s/@/;/g

# blx instructions are added link-time
/blx (r[0-9]+|sb|sl|fp|ip|sp|lr|pc)/!s/blx/bl/

# swi
s/svc #?/swi /

## Arm-specific
# Conditional byte/half load/store insns
s/(ldr|str)(s?[bh])(\w{2})/\1\3\2/

# ldm/stm
s/(ldm|stm)([id][ab])(\w{2})/\1\3\2/
s/(ldm|stm)(eq|ne|cs|lo|hi|hs|lt|gt|le|ge)?\b/\1\2ia/

# Push/pop
s/push/stmdb sp!,/
s/pop(\w*)/ldm\1ia sp!,/

# Shift instructions
s/(lsl|lsr|asr|ror)(\w* .+,)( \S+)$/mov\2 \1\3/
s/rrx(.+)/mov\1, rrx/

# apsr --> cpsr
s/apsr/cpsr/i
s/cpsr_nzcvq/cpsr_f/i

# mcr/mrc
/(mcr|mrc)/s/#//g

# conditional and/orr/eor/bic
s/(add|sub|and|orr|eor|bic|mul)s(\w{2})/\1\2s/
