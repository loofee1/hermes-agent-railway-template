FROM nousresearch/hermes-agent:v2026.9.11@sha256:9469b3e78b9545b6d576eb8887a95352e9a0ea83730eaf31431cf862ca1010e1

# Apply Haloub-specific Dropbox OAuth fix at image build time.
# Dropbox requires token_access_type=offline to issue a refresh_token.
COPY patch-dropbox-oauth.py /tmp/patch-dropbox-oauth.py
RUN python3 /tmp/patch-dropbox-oauth.py && rm -f /tmp/patch-dropbox-oauth.py

COPY --chmod=0755 docker-entrypoint.sh /usr/local/bin/hermes-railway-entrypoint

ENV HERMES_HOME=/data/.hermes \
    HERMES_WRITE_SAFE_ROOT=/data/.hermes \
    HERMES_LAZY_INSTALL_TARGET=/data/.hermes/lazy-packages \
    HERMES_DASHBOARD=1 \
    HERMES_DASHBOARD_HOST=0.0.0.0 \
    HERMES_GATEWAY_BOOTSTRAP_STATE=running

ENTRYPOINT ["/usr/local/bin/hermes-railway-entrypoint"]
CMD ["gateway", "run"]
