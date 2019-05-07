#!/bin/bash

until [[ $(pgrep restart.sh) ]]; do
	echo "The tip-bot is not running, starting.."
	/home/helix/discord-bot/restart.sh
	sleep 15
done
