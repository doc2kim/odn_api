#!/bin/bash

# Wait for Gunicorn
chmod +x /wait-for-it.sh
/wait-for-it.sh localhost:8000 --timeout=0 -- nginx -g 'daemon off;'


