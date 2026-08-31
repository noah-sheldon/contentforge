# Database Design (Updated July 2026)

## V1: JSON State File (No Database)

```json
{
  "run_id": "run_20260725_120000",
  "run_type": "manual",
  "topic": "Building RAG at Scale",
  "status": "waiting_after_copywriter",
  "steps": {
    "copywriter": {
      "data": "I built a RAG pipeline. Here is what worked...",
      "completed_at": "2026-07-25T12:00:00"
    },
    "linkedin_approved": {
      "data": "Adapted LinkedIn post...",
      "completed_at": "2026-07-25T12:02:00"
    }
  },
  "output": {
    "linkedin": {
      "text": "I spent 6 months building RAG at Fitch...",
      "video_path": "output/week_30/linkedin.mp4"
    }
  },
  "created_at": "2026-07-25T12:00:00",
  "updated_at": "2026-07-25T12:05:00"
}
```

### Storage Map

```mermaid
erDiagram
    PIPELINE_STATE ||--o{ COPYWRITER_STEP : contains
    PIPELINE_STATE ||--o{ EXPERT_STEP : contains
    PIPELINE_STATE ||--o{ OUTPUT_FILE : produces

    PIPELINE_STATE {
        string run_id PK
        string run_type "manual|auto"
        string topic
        string status "started|waiting_after_*|completed"
        datetime created_at
        datetime updated_at
    }

    COPYWRITER_STEP {
        string data "master draft text"
        datetime completed_at
    }

    EXPERT_STEP {
        string platform "linkedin|x|threads"
        string status "pending|approved|rejected"
        string notes "review feedback"
        datetime completed_at
    }

    OUTPUT_FILE {
        string platform "linkedin|x|threads"
        string text "post copy"
        string video_path "output/week_N/platform.mp4"
    }
```

## V2: MongoDB (When Dashboard Is Built)

```mermaid
erDiagram
    weeks ||--o{ scripts : contains
    weeks ||--o{ renders : produces
    weeks ||--o{ content_calendar : schedules

    weeks {
        objectid id PK
        int week_number
        string topic_selected
        string status
        json research_data
        datetime created_at
    }

    scripts {
        objectid id PK
        objectid week_id FK
        string master_draft
        json platform_drafts "linkedin|x|threads"
        string status "draft|approved|rejected"
    }

    renders {
        objectid id PK
        objectid week_id FK
        string platform
        string text_path
        string video_path
        string status "pending|done|failed"
    }

    content_calendar {
        objectid id PK
        objectid week_id FK
        json entries "day, platform, caption, status"
    }
```
