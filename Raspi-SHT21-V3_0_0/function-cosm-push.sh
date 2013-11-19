#!/bin/sh
curl --request PUT \
	 --data-binary @sht21-cosm.txt \
	 --header "X-ApiKey: YOUR_KEY" \
	 https://api.cosm.com/v2/feeds/YOUR_FEED.csv

# 	 --verbose \	 
	 
