www.{$DOMAIN_NAME} {
    redir https://{$DOMAIN_NAME}
}

{$DOMAIN_NAME} {
    proxy / django:5000 {
        header_upstream Host {host}
        header_upstream X-Real-IP {remote}
        header_upstream X-Forwarded-Proto {scheme}
        header_upstream X-CSRFToken {~csrftoken}
    }
    log stdout
    errors stdout
    gzip
}
