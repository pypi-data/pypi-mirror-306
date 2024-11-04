#!/bin/bash
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

if [ "$(whoami)" = "root" ];
then
    echo "please run this script as normal user"
    exit 1
fi

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
SIMPLE_REPO_DIR="$BASE_DIR/test_simple_repo"
BORG_REPO_DIR="$BASE_DIR/test_borg_repo"

if hash trash > /dev/null 2>&1; then
    trash "$BORG_REPO_DIR" > /dev/null 2>&1
else
    rm -rf "$BORG_REPO_DIR" > /dev/null 2>&1
fi

borg init --encryption none --make-parent-dirs --append-only "$BORG_REPO_DIR"

for RUN_DIR in "$SIMPLE_REPO_DIR"/*
do
    if [[ -d "$RUN_DIR" ]]
    then
        BACKUP_NAME=$(basename "$RUN_DIR")
        borg create "$BORG_REPO_DIR::$BACKUP_NAME" "$RUN_DIR"
    fi
done
