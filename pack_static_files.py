
import os
from glob import glob

PATH = "./static"
OUTPUT_FILE = "static_packed.py"

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

aFiles = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*'))]
aFiles = [f for f in aFiles if os.path.isfile(f)]

print(aFiles)

sOutputFile = """
dFiles = {
"""

for sFile in aFiles:
    sPacked = ""

    aData = open(sFile, 'rb').read()

    sPacked = '['
    for iB in aData:
        sPacked += str(iB)+','
    sPacked += ']'

    sOutputFile += f""" "{sFile}": {sPacked}, \n"""

sOutputFile += "'end':0"

sOutputFile += """
}
"""

open(OUTPUT_FILE, 'w').write(sOutputFile)
