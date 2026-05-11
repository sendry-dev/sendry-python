# Changelog

All notable changes to `sendry` (Python) are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-11

### Added

- Initial public release.
- Synchronous `Sendry` and asynchronous `AsyncSendry` clients.
- Resource modules: emails, domains, templates, api_keys, webhooks,
  analytics, suppression, unsubscribes, contacts, audiences, campaigns,
  billing, team.
- `verify_webhook_signature` helper (HMAC-SHA256).
- `py.typed` marker — fully type-checkable with mypy / pyright.
- Built on `httpx` for HTTP/1.1 + HTTP/2 + connection pooling.
