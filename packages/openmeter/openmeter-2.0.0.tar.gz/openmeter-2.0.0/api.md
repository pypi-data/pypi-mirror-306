# Events

Types:

```python
from openmeter.types import IngestedEvent, EventListResponse, EventIngestResponse
```

Methods:

- <code title="get /api/v1/events">client.events.<a href="./src/openmeter/resources/events.py">list</a>(\*\*<a href="src/openmeter/types/event_list_params.py">params</a>) -> <a href="./src/openmeter/types/event_list_response.py">EventListResponse</a></code>
- <code title="post /api/v1/events">client.events.<a href="./src/openmeter/resources/events.py">ingest</a>(\*\*<a href="src/openmeter/types/event_ingest_params.py">params</a>) -> <a href="./src/openmeter/types/event_ingest_response.py">EventIngestResponse</a></code>

# Meters

Types:

```python
from openmeter.types import Meter, MeterQueryResult, MeterListResponse
```

Methods:

- <code title="post /api/v1/meters">client.meters.<a href="./src/openmeter/resources/meters/meters.py">create</a>(\*\*<a href="src/openmeter/types/meter_create_params.py">params</a>) -> <a href="./src/openmeter/types/meter.py">Meter</a></code>
- <code title="get /api/v1/meters/{meterIdOrSlug}">client.meters.<a href="./src/openmeter/resources/meters/meters.py">retrieve</a>(meter_id_or_slug) -> <a href="./src/openmeter/types/meter.py">Meter</a></code>
- <code title="get /api/v1/meters">client.meters.<a href="./src/openmeter/resources/meters/meters.py">list</a>() -> <a href="./src/openmeter/types/meter_list_response.py">MeterListResponse</a></code>
- <code title="delete /api/v1/meters/{meterIdOrSlug}">client.meters.<a href="./src/openmeter/resources/meters/meters.py">delete</a>(meter_id_or_slug) -> None</code>
- <code title="get /api/v1/meters/{meterIdOrSlug}/query">client.meters.<a href="./src/openmeter/resources/meters/meters.py">query</a>(meter_id_or_slug, \*\*<a href="src/openmeter/types/meter_query_params.py">params</a>) -> <a href="./src/openmeter/types/meter_query_result.py">MeterQueryResult</a></code>

## Subjects

Types:

```python
from openmeter.types.meters import SubjectListResponse
```

Methods:

- <code title="get /api/v1/meters/{meterIdOrSlug}/subjects">client.meters.subjects.<a href="./src/openmeter/resources/meters/subjects.py">list</a>(meter_id_or_slug) -> <a href="./src/openmeter/types/meters/subject_list_response.py">SubjectListResponse</a></code>

# Subjects

Types:

```python
from openmeter.types import Subject, SubjectListResponse, SubjectUpsertResponse
```

Methods:

- <code title="get /api/v1/subjects/{subjectIdOrKey}">client.subjects.<a href="./src/openmeter/resources/subjects/subjects.py">retrieve</a>(subject_id_or_key) -> <a href="./src/openmeter/types/subject.py">Subject</a></code>
- <code title="get /api/v1/subjects">client.subjects.<a href="./src/openmeter/resources/subjects/subjects.py">list</a>() -> <a href="./src/openmeter/types/subject_list_response.py">SubjectListResponse</a></code>
- <code title="delete /api/v1/subjects/{subjectIdOrKey}">client.subjects.<a href="./src/openmeter/resources/subjects/subjects.py">delete</a>(subject_id_or_key) -> None</code>
- <code title="post /api/v1/subjects">client.subjects.<a href="./src/openmeter/resources/subjects/subjects.py">upsert</a>(\*\*<a href="src/openmeter/types/subject_upsert_params.py">params</a>) -> <a href="./src/openmeter/types/subject_upsert_response.py">SubjectUpsertResponse</a></code>

## Entitlements

Types:

```python
from openmeter.types.subjects import (
    EntitlementValue,
    EntitlementListResponse,
    EntitlementHistoryResponse,
)
```

Methods:

- <code title="post /api/v1/subjects/{subjectIdOrKey}/entitlements">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">create</a>(subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_create_params.py">params</a>) -> <a href="./src/openmeter/types/entitlement.py">Entitlement</a></code>
- <code title="get /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementId}">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">retrieve</a>(entitlement_id, \*, subject_id_or_key) -> <a href="./src/openmeter/types/entitlement.py">Entitlement</a></code>
- <code title="get /api/v1/subjects/{subjectIdOrKey}/entitlements">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">list</a>(subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_list_params.py">params</a>) -> <a href="./src/openmeter/types/subjects/entitlement_list_response.py">EntitlementListResponse</a></code>
- <code title="delete /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementId}">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">delete</a>(entitlement_id, \*, subject_id_or_key) -> None</code>
- <code title="get /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementId}/history">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">history</a>(entitlement_id, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_history_params.py">params</a>) -> <a href="./src/openmeter/types/subjects/entitlement_history_response.py">EntitlementHistoryResponse</a></code>
- <code title="put /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementIdOrFeatureKey}/override">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">override</a>(entitlement_id_or_feature_key, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_override_params.py">params</a>) -> <a href="./src/openmeter/types/entitlement.py">Entitlement</a></code>
- <code title="post /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementId}/reset">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">reset</a>(entitlement_id, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_reset_params.py">params</a>) -> None</code>
- <code title="get /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementIdOrFeatureKey}/value">client.subjects.entitlements.<a href="./src/openmeter/resources/subjects/entitlements/entitlements.py">value</a>(entitlement_id_or_feature_key, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlement_value_params.py">params</a>) -> <a href="./src/openmeter/types/subjects/entitlement_value.py">EntitlementValue</a></code>

### Grants

Types:

```python
from openmeter.types.subjects.entitlements import EntitlementGrant, GrantListResponse
```

Methods:

- <code title="post /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementIdOrFeatureKey}/grants">client.subjects.entitlements.grants.<a href="./src/openmeter/resources/subjects/entitlements/grants.py">create</a>(entitlement_id_or_feature_key, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlements/grant_create_params.py">params</a>) -> <a href="./src/openmeter/types/subjects/entitlements/entitlement_grant.py">EntitlementGrant</a></code>
- <code title="get /api/v1/subjects/{subjectIdOrKey}/entitlements/{entitlementIdOrFeatureKey}/grants">client.subjects.entitlements.grants.<a href="./src/openmeter/resources/subjects/entitlements/grants.py">list</a>(entitlement_id_or_feature_key, \*, subject_id_or_key, \*\*<a href="src/openmeter/types/subjects/entitlements/grant_list_params.py">params</a>) -> <a href="./src/openmeter/types/subjects/entitlements/grant_list_response.py">GrantListResponse</a></code>

# Entitlements

Types:

```python
from openmeter.types import Entitlement, ListEntitlementsResult
```

Methods:

- <code title="get /api/v1/entitlements/{entitlementId}">client.entitlements.<a href="./src/openmeter/resources/entitlements/entitlements.py">retrieve</a>(entitlement_id) -> <a href="./src/openmeter/types/entitlement.py">Entitlement</a></code>
- <code title="get /api/v1/entitlements">client.entitlements.<a href="./src/openmeter/resources/entitlements/entitlements.py">list</a>(\*\*<a href="src/openmeter/types/entitlement_list_params.py">params</a>) -> <a href="./src/openmeter/types/list_entitlements_result.py">ListEntitlementsResult</a></code>

## Features

Types:

```python
from openmeter.types.entitlements import Feature, ListFeaturesResult
```

Methods:

- <code title="post /api/v1/features">client.entitlements.features.<a href="./src/openmeter/resources/entitlements/features.py">create</a>(\*\*<a href="src/openmeter/types/entitlements/feature_create_params.py">params</a>) -> <a href="./src/openmeter/types/entitlements/feature.py">Feature</a></code>
- <code title="get /api/v1/features/{featureId}">client.entitlements.features.<a href="./src/openmeter/resources/entitlements/features.py">retrieve</a>(feature_id) -> <a href="./src/openmeter/types/entitlements/feature.py">Feature</a></code>
- <code title="get /api/v1/features">client.entitlements.features.<a href="./src/openmeter/resources/entitlements/features.py">list</a>(\*\*<a href="src/openmeter/types/entitlements/feature_list_params.py">params</a>) -> <a href="./src/openmeter/types/entitlements/list_features_result.py">ListFeaturesResult</a></code>
- <code title="delete /api/v1/features/{featureId}">client.entitlements.features.<a href="./src/openmeter/resources/entitlements/features.py">archive</a>(feature_id) -> None</code>

## Grants

Types:

```python
from openmeter.types.entitlements import GrantPaginatedResponse, GrantListResponse
```

Methods:

- <code title="get /api/v1/grants">client.entitlements.grants.<a href="./src/openmeter/resources/entitlements/grants.py">list</a>(\*\*<a href="src/openmeter/types/entitlements/grant_list_params.py">params</a>) -> <a href="./src/openmeter/types/entitlements/grant_list_response.py">GrantListResponse</a></code>
- <code title="delete /api/v1/grants/{grantId}">client.entitlements.grants.<a href="./src/openmeter/resources/entitlements/grants.py">void</a>(grant_id) -> None</code>

# Notifications

## Channels

Types:

```python
from openmeter.types.notifications import NotificationChannel, ChannelListResponse
```

Methods:

- <code title="post /api/v1/notification/channels">client.notifications.channels.<a href="./src/openmeter/resources/notifications/channels.py">create</a>(\*\*<a href="src/openmeter/types/notifications/channel_create_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/notification_channel.py">NotificationChannel</a></code>
- <code title="get /api/v1/notification/channels/{channelId}">client.notifications.channels.<a href="./src/openmeter/resources/notifications/channels.py">retrieve</a>(channel_id) -> <a href="./src/openmeter/types/notifications/notification_channel.py">NotificationChannel</a></code>
- <code title="put /api/v1/notification/channels/{channelId}">client.notifications.channels.<a href="./src/openmeter/resources/notifications/channels.py">update</a>(channel_id, \*\*<a href="src/openmeter/types/notifications/channel_update_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/notification_channel.py">NotificationChannel</a></code>
- <code title="get /api/v1/notification/channels">client.notifications.channels.<a href="./src/openmeter/resources/notifications/channels.py">list</a>(\*\*<a href="src/openmeter/types/notifications/channel_list_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/channel_list_response.py">ChannelListResponse</a></code>
- <code title="delete /api/v1/notification/channels/{channelId}">client.notifications.channels.<a href="./src/openmeter/resources/notifications/channels.py">delete</a>(channel_id) -> None</code>

## Events

Types:

```python
from openmeter.types.notifications import NotificationEvent, EventListResponse
```

Methods:

- <code title="get /api/v1/notification/events/{eventId}">client.notifications.events.<a href="./src/openmeter/resources/notifications/events.py">retrieve</a>(event_id) -> <a href="./src/openmeter/types/notifications/notification_event.py">NotificationEvent</a></code>
- <code title="get /api/v1/notification/events">client.notifications.events.<a href="./src/openmeter/resources/notifications/events.py">list</a>(\*\*<a href="src/openmeter/types/notifications/event_list_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/event_list_response.py">EventListResponse</a></code>

## Rules

Types:

```python
from openmeter.types.notifications import NotificationRule, RuleListResponse
```

Methods:

- <code title="post /api/v1/notification/rules">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">create</a>(\*\*<a href="src/openmeter/types/notifications/rule_create_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/notification_rule.py">NotificationRule</a></code>
- <code title="get /api/v1/notification/rules/{ruleId}">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">retrieve</a>(rule_id) -> <a href="./src/openmeter/types/notifications/notification_rule.py">NotificationRule</a></code>
- <code title="put /api/v1/notification/rules/{ruleId}">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">update</a>(rule_id, \*\*<a href="src/openmeter/types/notifications/rule_update_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/notification_rule.py">NotificationRule</a></code>
- <code title="get /api/v1/notification/rules">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">list</a>(\*\*<a href="src/openmeter/types/notifications/rule_list_params.py">params</a>) -> <a href="./src/openmeter/types/notifications/rule_list_response.py">RuleListResponse</a></code>
- <code title="delete /api/v1/notification/rules/{ruleId}">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">delete</a>(rule_id) -> None</code>
- <code title="post /api/v1/notification/rules/{ruleId}/test">client.notifications.rules.<a href="./src/openmeter/resources/notifications/rules.py">test</a>(rule_id) -> <a href="./src/openmeter/types/notifications/notification_event.py">NotificationEvent</a></code>

## Webhook

Methods:

- <code title="post /api/v1/notification/webhook/svix">client.notifications.webhook.<a href="./src/openmeter/resources/notifications/webhook.py">svix</a>(\*\*<a href="src/openmeter/types/notifications/webhook_svix_params.py">params</a>) -> None</code>

# Portal

## Meters

Methods:

- <code title="get /api/v1/portal/meters/{meterSlug}/query">client.portal.meters.<a href="./src/openmeter/resources/portal/meters.py">query</a>(meter_slug, \*\*<a href="src/openmeter/types/portal/meter_query_params.py">params</a>) -> <a href="./src/openmeter/types/meter_query_result.py">MeterQueryResult</a></code>

## Tokens

Types:

```python
from openmeter.types.portal import PortalToken, TokenListResponse
```

Methods:

- <code title="post /api/v1/portal/tokens">client.portal.tokens.<a href="./src/openmeter/resources/portal/tokens.py">create</a>(\*\*<a href="src/openmeter/types/portal/token_create_params.py">params</a>) -> <a href="./src/openmeter/types/portal/portal_token.py">PortalToken</a></code>
- <code title="get /api/v1/portal/tokens">client.portal.tokens.<a href="./src/openmeter/resources/portal/tokens.py">list</a>(\*\*<a href="src/openmeter/types/portal/token_list_params.py">params</a>) -> <a href="./src/openmeter/types/portal/token_list_response.py">TokenListResponse</a></code>
- <code title="post /api/v1/portal/tokens/invalidate">client.portal.tokens.<a href="./src/openmeter/resources/portal/tokens.py">invalidate</a>(\*\*<a href="src/openmeter/types/portal/token_invalidate_params.py">params</a>) -> None</code>

# Debug

## Metrics

Types:

```python
from openmeter.types.debug import MetricListResponse
```

Methods:

- <code title="get /api/v1/debug/metrics">client.debug.metrics.<a href="./src/openmeter/resources/debug/metrics.py">list</a>() -> str</code>
