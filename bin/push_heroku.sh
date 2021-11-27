#!/usr/bin/env bash
# PROD
heroku container:push web -a ubademy-subscriptions-api
heroku container:release web -a ubademy-subscriptions-api