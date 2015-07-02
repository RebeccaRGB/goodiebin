#!/bin/sh
chmod -R a-w "$@"
chflags -R uchg "$@"
