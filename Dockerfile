FROM openresty/openresty:latest

# Install required packages
RUN apt-get update && \
    apt-get install -y \
        luarocks \
        libssl-dev \
        build-essential \
        git && \
    rm -rf /var/lib/apt/lists/*

# Install pgmoon
RUN luarocks install pgmoon

# Install luaossl (Required for SCRAM authentication)
RUN luarocks install luaossl

# Install redis-lua
RUN luarocks install lua-resty-redis

# Install lua-resty-hmac FIRST (required by lua-resty-jwt)
RUN git clone https://github.com/jkeys089/lua-resty-hmac.git /tmp/lua-resty-hmac && \
    cp /tmp/lua-resty-hmac/lib/resty/hmac.lua /usr/local/openresty/lualib/resty/ && \
    rm -rf /tmp/lua-resty-hmac

# Install lua-resty-jwt
RUN git clone https://github.com/SkyLothar/lua-resty-jwt.git /tmp/lua-resty-jwt && \
    cp -r /tmp/lua-resty-jwt/lib/resty/* /usr/local/openresty/lualib/resty/ && \
    rm -rf /tmp/lua-resty-jwt

# Copy Nginx config
COPY nginx/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf

# Copy Lua files
COPY lua /usr/local/openresty/nginx/lua

EXPOSE 80

CMD ["openresty", "-g", "daemon off;"]