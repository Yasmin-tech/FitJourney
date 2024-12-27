#!/bin/bash
openssl aes-256-cbc -d -in credentials.json.enc -out credentials.json -k $1
