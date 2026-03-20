local uri = ngx.var.uri

local tenant = require "tenant_validation"
local jwt = require "jwt_validation"

local public_routes = {
    ["/tenants/login/"] = true
}

if public_routes[uri] then
    tenant.run()
else
    jwt.run()
end