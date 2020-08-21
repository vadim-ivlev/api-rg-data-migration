#!/bin/bash

echo "deploying via https://git.rgwork.ru/"

git push origin master:production

echo "Watch pipeline -> https://git.rgwork.ru/masterback/log-monitor/pipelines"

