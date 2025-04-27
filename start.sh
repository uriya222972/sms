#!/bin/bash
mkdir -p data/responses
mkdir -p data/contacts
mkdir -p data/groups
touch data/managers.json
touch data/users.json
exec gunicorn app:app --bind 0.0.0.0:$PORT
