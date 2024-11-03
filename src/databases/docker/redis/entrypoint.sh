#!/bin/sh

mkdir -p /usr/local/etc/redis

echo "bind 0.0.0.0" > /usr/local/etc/redis/redis.conf
echo "requirepass $REDIS_PASSWORD" >> /usr/local/etc/redis/redis.conf

exec redis-server /usr/local/etc/redis/redis.conf