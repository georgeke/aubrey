#!/bin/bash

# NOTE: NOT a good idea to run this script with all URLs, you WILL get your IP blocked by *
urls=()

for url in ${urls[@]}; do
    curl -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2593.0 Safari/537.36" */$url >> out
done
