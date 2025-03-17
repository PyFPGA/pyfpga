#!/bin/bash

MDIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

export PATH=$MDIR:$PATH
