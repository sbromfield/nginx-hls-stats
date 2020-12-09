# nginx-hls-stats

This is an easy way to see how many viewers are watching your HLS streams if you are using the Nginx RTMP module. 

USAGE 

From the server running the Nginx RTMP module, run python3 stats.py. The scrit will read your access.log and count the number of HLS requests being served by Nginx. You have two optional parameters: --path and --timeout. 

--path allows you dictate the location of the Nginx access.log. The default is /var/log/nginx/access.log.

--timeout take an integer as input. This is the number of mintues a HLS playlist should be consider live before removing the request from the counted section. The default is 3 minutes.
