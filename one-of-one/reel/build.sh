set -e
V="-c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -r 30 -an"
seg(){ # name clip start dur overlay
  if [ -n "$5" ]; then
    ffmpeg -v error -y -ss $3 -t $4 -i $2 -loop 1 -t $4 -i $5 -filter_complex "[0:v]fps=30,scale=1080:1920,setsar=1[v];[1:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[o];[v][o]overlay=0:0:shortest=1[out]" -map "[out]" -t $4 $V seg_$1.mp4
  else
    ffmpeg -v error -y -ss $3 -t $4 -i $2 -vf "fps=30,scale=1080:1920,setsar=1" -t $4 $V seg_$1.mp4
  fi; }
seg 1 k1-rail.mp4 0.5 4 o1.png
seg 2 k2-top.mp4 0.0 4 o2.png
seg 3 k3-snap.mp4 1.0 4 o3.png
ffmpeg -v error -y -framerate 30 -i s4/%04d.jpg -vf "scale=1080:1920,setsar=1" $V seg_4.mp4
seg 5 k5-noa.mp4 0.6 3 o5.png
seg 6 k6-dalia.mp4 0.6 3 o6.png
seg 7 k7-bag.mp4 0.8 3 ""
ffmpeg -v error -y -framerate 30 -i s8/%04d.jpg -vf "scale=1080:1920,setsar=1" $V seg_8.mp4
for i in 1 2 3 4 5 6 7 8; do echo "file 'seg_$i.mp4'"; done > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -vf tpad=stop_mode=clone:stop_duration=1 -t 30 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -r 30 -an -movflags +faststart one-of-one-1080.mp4
ffmpeg -v error -y -i one-of-one-1080.mp4 -vf scale=720:1280 -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p -r 30 -an -movflags +faststart one-of-one.mp4
ffmpeg -v error -y -ss 1.2 -i one-of-one-1080.mp4 -frames:v 1 -vf scale=720:1280 -q:v 3 one-of-one.jpg
