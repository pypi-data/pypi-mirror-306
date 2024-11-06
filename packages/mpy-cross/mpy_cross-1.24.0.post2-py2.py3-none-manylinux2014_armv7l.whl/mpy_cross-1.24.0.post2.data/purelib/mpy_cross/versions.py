# https://docs.micropython.org/en/latest/reference/mpyfiles.html
__versions__ = [
    ("v1.23.0", "6.3"),
    ("v1.22.0", "6.2"),
    ("v1.20.0", "6.1"),
    ("v1.19", "6"),
    ("v1.12", "5"),
    ("v1.11", "4"),
    ("v1.9.3", "3"),
    ("v1.9", "2"),
    ("v1.5.1", "0"),
]

__lookup = {v[1]: v[0] for v in __versions__}

def semver(ver: str):
    sem = [
        int(v) for v in 
        ver.strip("v").split(".")
    ] + [0, 0, 0]
    return sem[0:3]

def mpy_version(micropython: str, bytecode: str):
    ret = None
    if micropython:
        sem = semver(micropython)
        prev = None
        for ver, mpy in __versions__:
            ver = semver(ver)
            if sem >= ver:
                ret = __lookup.get(mpy)
    elif bytecode:
        ret =  __lookup.get(bytecode.strip("v"))
    
    if not ret:
        raise SystemExit(f"Error: Couldn't identify {micropython or bytecode} in known versions: \n{__versions__}")
    return ret

if __name__ == "__main__":
    import sys
    if "-b" in sys.argv:
        print(
        " ".join(dict(__versions__).values())
        )
    else:
        print()
        print(
        " ".join(dict(__versions__).keys())
        )