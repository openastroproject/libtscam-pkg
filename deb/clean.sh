#!/bin/bash

version=`cat version`

rm -fr libtscam-$version
rm -fr libtscam_*
rm -fr libtscam-dev_*
rm -f debfiles/compat
rm -f debfiles/patches/*
