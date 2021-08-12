## Common
# 4byte/2byte
s/4byte/word/
s/2byte/short/

# Comment chars
s/@/;/g

# blx instructions are added link-time
/blx (r\d+|sb|sl|fp|ip|sp|lr|pc)/!s/blx/bl/

# swi
s/svc #?/swi /

## Thumb-specific
# Flag-setting instructions
s/(\t\w{3})s\b/\1/

# rsb instructions are not valid in mwasmarm
s/rsb (\w+, \w+), \#0/neg \1/

# ldm/stm must have the "ia" suffix
s/(ldm|stm)\b/\0ia/
s/((ldm|stm)ia \w+),/\1!,/

# mul arg syntax
s/(mul \w+, \w+), \w+/\1/
