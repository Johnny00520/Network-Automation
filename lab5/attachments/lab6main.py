#!/bin/env python3
import sshInfo, validateIP, connectivity, bgp

def main():
    sshInfo.main()
    print("\n")
    validateIP.main()
    print("\n")
    connectivity.main()
    print("\n")
    bgp.main()


if __name__ == '__main__':
    main()
