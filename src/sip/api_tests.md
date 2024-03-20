# API Requests

## SIP proxy status

```bash
# curl -I "http://localhost:8064/status"

HTTP/1.1 200 OK
Sia: SIP/2.0/TCP 127.0.0.1:55960
Content-Type: text/plain
Server: kamailio (5.7.4 (x86_64/linux))
Content-Length: 0
```

## Reload dispatcher

```bash
# curl -X POST "http://localhost:8064/rpc" -d '{"jsonrpc": "2.0", "method": "dispatcher.reload", "id": 1}'

{
        "jsonrpc":      "2.0",
        "result":       "Ok. Dispatcher successfully reloaded.",
        "id":   1
}
```

## Reload dialplan

```bash
# curl -X POST "http://localhost:8064/rpc" -d '{"jsonrpc": "2.0", "method": "dialplan.reload", "id": 1}'

{
        "jsonrpc":      "2.0",
        "result":       {
        },
        "id":   1
}
```

## Reload permissions

```bash
# curl -X POST "http://localhost:8064/rpc" -d '{"jsonrpc": "2.0", "method": "permissions.addressReload", "id": 1}'

{
        "jsonrpc":      "2.0",
        "result":       "Reload OK",
        "id":   1
}
```

## Reload tenant table

```bash
# curl -X POST "http://localhost:8064/rpc" -d '{"jsonrpc": "2.0", "method": "htable.reload", "params": "tenantmap", "id": 1}'

{
        "jsonrpc":      "2.0",
        "result":       {
        },
        "id":   1
}
```
