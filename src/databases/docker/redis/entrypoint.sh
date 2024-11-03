#!/bin/sh

mkdir -p /usr/local/etc/redis

echo "bind $REDIS_HOST" > /usr/local/etc/redis/redis.conf
echo "requirepass $REDIS_PASSWORD" >> /usr/local/etc/redis/redis.conf

exec redis-server /usr/local/etc/redis/redis.conf