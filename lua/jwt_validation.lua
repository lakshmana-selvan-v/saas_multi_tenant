local _M = {}

local jwt = require "resty.jwt"
local redis = require "resty.redis"
local pgmoon = require "pgmoon"

function _M.run()

    --------------------------------------------------
    -- GET AUTH HEADER
    --------------------------------------------------

    local headers = ngx.req.get_headers()
    local auth_header = headers["Authorization"]

    if not auth_header then
        ngx.status = 401
        ngx.say('{"error":"Authorization header missing"}')
        return ngx.exit(401)
    end

    local token = auth_header:match("Bearer%s+(.+)")

    if not token then
        ngx.status = 401
        ngx.say('{"error":"Invalid Authorization format"}')
        return ngx.exit(401)
    end


    --------------------------------------------------
    -- VERIFY JWT
    --------------------------------------------------

    local jwt_obj = jwt:verify(
        os.getenv("JWT_SECRET") or "django-insecure-p1h%_vn7lt=_oppovhf)$zj^(h2(%f@x+rr!)1bvlhqg#=^w*9",
        token
    )

    if not jwt_obj.verified then
        ngx.status = 401
        ngx.say('{"error":"Invalid JWT token"}')
        return ngx.exit(401)
    end


    --------------------------------------------------
    -- GET TENANT FROM TOKEN
    --------------------------------------------------

    local payload = jwt_obj.payload
    local tenant_id = payload.tenant_id

    if not tenant_id then
        ngx.status = 401
        ngx.say('{"error":"Tenant ID missing in token"}')
        return ngx.exit(401)
    end

    --------------------------------------------------
    -- DETECT TENANT NAME
    --------------------------------------------------

    local host = ngx.var.host:gsub(":%d+", "")
    local tenant_name = nil

    -- Case 1: Subdomain
    local subdomain = host:match("^([^.]+)%.localhost")

    if subdomain then
        tenant_name = subdomain
    end

    -- Case 2: Custom domain
    if not tenant_name and host ~= "localhost" then
        tenant_name = host
    end

    -- Case 3: Header tenant
    if not tenant_name then
        tenant_name = headers["X-Tenant-Name"]
    end

    if not tenant_name then
        ngx.status = 400
        ngx.say('{"error":"Tenant cannot be determined"}')
        return ngx.exit(400)
    end

    --------------------------------------------------
    -- REDIS CACHE CHECK
    --------------------------------------------------

    local red = redis:new()
    red:set_timeout(1000)

    local redis_ok, redis_err = red:connect("redis", 6379)

    if redis_ok then

        local cached_domain = red:get("tenant_domain:" .. tenant_id)

        if cached_domain and cached_domain ~= ngx.null then

            if cached_domain ~= host then
                ngx.status = 403
                ngx.say('{"error":"Tenant domain mismatch"}')
                return ngx.exit(403)
            end

            ngx.req.set_header("X-Tenant-ID", tenant_id)

            red:set_keepalive(10000, 100)
            return
        end
    end


    --------------------------------------------------
    -- POSTGRES VALIDATION
    --------------------------------------------------

    local pg = pgmoon.new({
        host = "postgres",
        port = 5432,
        database = "saas_product",
        user = "app_user",
        password = "admin@123!"
    })

    pg:settimeout(1000)

    local ok, err = pg:connect()

    if not ok then
        ngx.status = 503
        ngx.say('{"error":"Database unavailable"}')
        return ngx.exit(503)
    end


    local query = "SELECT id, sub_domain FROM tenants WHERE id = " ..
        pg:escape_literal(tenant_id) ..
        " AND sub_domain = " ..
        pg:escape_literal(tenant_name) ..
        " AND is_active = true LIMIT 1"


    local res, err = pg:query(query)

    if not res then
        pg:keepalive()

        ngx.status = 503
        ngx.say('{"error":"Database query failed"}')
        return ngx.exit(503)
    end


    if #res == 0 then
        pg:keepalive()

        ngx.status = 403
        ngx.say('{"error":"Tenant invalid for this domain"}')
        return ngx.exit(403)
    end


    pg:keepalive()


    --------------------------------------------------
    -- CACHE TENANT DOMAIN
    --------------------------------------------------

    if redis_ok then

        red:set("tenant_domain:" .. tenant_id, host)
        red:expire("tenant_domain:" .. tenant_id, 3600)

        red:set_keepalive(10000, 100)
    end


    --------------------------------------------------
    -- PASS TENANT TO BACKEND
    --------------------------------------------------

    ngx.req.set_header("X-Tenant-ID", tenant_id)

end

return _M