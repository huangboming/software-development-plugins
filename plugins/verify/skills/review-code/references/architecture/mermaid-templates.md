# Mermaid Diagram Templates (C4-Style)

Adapt these templates to the repo’s actual services and data flows.

## System Context (C4-Style)

```mermaid
flowchart LR
  U["User / Client"] -->|"Uses"| API["Backend API"]
  API -->|"Reads/Writes"| DB[("Primary Database")]
  API -->|"Publishes/Consumes"| Q[["Queue / Stream"]]
  API -->|"Calls"| EXT["External Service"]
```

## Container / Service Topology

```mermaid
flowchart LR
  subgraph Platform
    API["api-service"]
    WORK["worker-service"]
    CRON["cron / scheduler"]
  end

  API --> DB[("Postgres")]
  API --> CACHE[("Redis")]
  WORK --> DB
  API --> Q[["Kafka"]]
  WORK --> Q
```

## Sequence Diagram (Critical Flow)

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant A as API
  participant D as Database
  participant E as External Service

  C->>A: Request
  A->>D: Query / Transaction
  D-->>A: Result
  A->>E: External call (with timeout/retry)
  E-->>A: Response
  A-->>C: Response
```
