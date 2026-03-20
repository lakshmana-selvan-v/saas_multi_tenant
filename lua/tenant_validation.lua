local _M = {}

function _M.run()
    local redis = require "resty.redis"
    local pgmoon = require "pgmoon"

    if ngx.var.uri == "/tenants/onboard/" then
        return
    end

    local headers = ngx.req.get_headers()

    local header_tenant = headers["X-Tenant-Name"]
    local host = ngx.var.host:gsub(":%d+", "")

    local tenant = nil
    local subdomain = nil
    local domain = nil

    -- Extract subdomain
    subdomain = host:match("^([^.]+)%.")

    -- Detect custom domain (no subdomain)
    if not subdomain or subdomain == "www" then
        domain = host
    end

    -- Rule 1: Subdomain
    if subdomain and subdomain ~= "www" and subdomain ~= "localhost" then
        tenant = subdomain
    end

    -- Rule 2: Custom Domain
    if not tenant and domain and domain ~= "localhost" then
        tenant = domain
    end

    -- Rule 3: Header fallback (only if host is localhost)
    if not tenant and host == "localhost" then
        tenant = header_tenant
    end

    -- Validate mismatch cases
    if tenant and header_tenant and tenant ~= header_tenant then
        ngx.status = 400
        ngx.say('{"error":"Tenant mismatch between host and header"}')
        return ngx.exit(400)
    end

    if not tenant then
        ngx.status = 400
        ngx.say('{"error":"Tenant not identified"}')
        return ngx.exit(400)
    end


    -- Redis Connection
    local red = redis:new()
    red:set_timeout(1000)

    local ok, err = red:connect(
        os.getenv("REDIS_HOST") or "redis",
        tonumber(os.getenv("REDIS_PORT")) or 6379
    )

    if ok then
        local cached = red:get("tenant:" .. tenant)

        if cached and cached ~= ngx.null then
            ngx.req.set_header("X-Tenant-Name", tenant)
            red:set_keepalive(10000, 100)
            return
        end
    end


    -- PostgreSQL Validation
    local pg = pgmoon.new({
        host     = os.getenv("POSTGRES_HOST") or "postgres",
        port     = tonumber(os.getenv("POSTGRES_PORT")) or 5432,
        database = os.getenv("POSTGRES_DB") or "saas_product",
        user     = os.getenv("POSTGRES_USER") or "app_user",
        password = os.getenv("POSTGRES_PASSWORD") or "admin@123!",
    })

    pg:settimeout(1000)

    local ok, err = pg:connect()
    if not ok then
        ngx.status = 503
        ngx.say('{"error":"Database unavailable"}')
        return ngx.exit(503)
    end

    local res = pg:query(
        "SELECT sub_domain FROM tenants " ..
        "WHERE sub_domain = " .. pg:escape_literal(tenant) ..
        " AND is_active = true LIMIT 1"
    )

    if not res then
        pg:keepalive()
        ngx.status = 503
        ngx.say('{"error":"Database query failed"}')
        return ngx.exit(503)
    end

    if #res == 0 then
        pg:keepalive()
        ngx.status = 403
        ngx.say('{"error":"Tenant not registered"}')
        return ngx.exit(403)
    end

    pg:keepalive()

    -- Cache result
    if red then
        red:set("tenant:" .. tenant, "valid")
        red:expire("tenant:" .. tenant, 3600)
        red:set_keepalive(10000, 100)
    end

    ngx.req.set_header("X-Tenant-Name", tenant)
end

return _M