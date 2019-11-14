#!/bin/dash

# $1: url or Youtube video id
# $2: starting time, in seconds, or in hh:mm:ss[.xxx] form
# $3: duration, in seconds, or in hh:mm:ss[.xxx] form
# $4: format, as accepted by youtube-dl (default: best)
# other args are passed directly to youtube-dl; eg, -r 40K
local fmt=${4:-best}
local url="$(youtube-dl --get-url "$1" -f $fmt ${@:5})" 
local filename="$(youtube-dl --get-filename "$1" ${@:5})"
ffmpeg -loglevel warning -hide_banner \
-ss $2 -i "$url" -c copy -t $3 "$filename"
printf "Saved to: %s\n" "$filename"
# based on Reino17's and teocci's comments in https://github.com/rg3/youtube-dl/issues/4821