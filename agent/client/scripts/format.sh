#!/bin/bash
echo -e "o\nn\np\n1\n\n\nw" | fdisk $1 \
&&  mkfs.$2	$11	$3
