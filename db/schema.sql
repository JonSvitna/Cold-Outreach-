create extension if not exists vector;
create extension if not exists pgcrypto;

create table if not exists campaigns (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    status text not null default 'draft',
    objective text,
    channel text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists leads (
    id uuid primary key default gen_random_uuid(),
    campaign_id uuid references campaigns(id) on delete set null,
    company_name text not null,
    company_domain text,
    contact_name text,
    contact_role text,
    linkedin_url text,
    source text,
    state text not null default 'NEEDS_MORE_RESEARCH',
    confidence_score numeric(4, 3),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists lead_profiles (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid not null references leads(id) on delete cascade,
    industry text,
    employee_size text,
    tech_stack jsonb not null default '[]'::jsonb,
    compliance_signals jsonb not null default '[]'::jsonb,
    hiring_activity jsonb not null default '[]'::jsonb,
    likely_contacts jsonb not null default '[]'::jsonb,
    pain_signals jsonb not null default '[]'::jsonb,
    enrichment_sources jsonb not null default '{}'::jsonb,
    profile_embedding vector(1536),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists outreach_sequences (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid not null references leads(id) on delete cascade,
    status text not null default 'draft',
    current_step integer not null default 0,
    next_send_at timestamptz,
    cadence jsonb not null default '[]'::jsonb,
    suppression_reason text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists outreach_messages (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid not null references leads(id) on delete cascade,
    sequence_id uuid references outreach_sequences(id) on delete set null,
    channel text not null,
    sequence_position text,
    subject text,
    body text not null,
    status text not null default 'draft',
    guardrail_status text,
    approved_by text,
    approved_at timestamptz,
    sent_at timestamptz,
    provider_message_id text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists message_versions (
    id uuid primary key default gen_random_uuid(),
    message_id uuid not null references outreach_messages(id) on delete cascade,
    version_number integer not null,
    subject text,
    body text not null,
    change_reason text,
    created_by_agent text,
    created_at timestamptz not null default now(),
    unique (message_id, version_number)
);

create table if not exists responses (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid not null references leads(id) on delete cascade,
    message_id uuid references outreach_messages(id) on delete set null,
    raw_body text not null,
    classification text not null,
    next_action text,
    escalation_required boolean not null default false,
    received_at timestamptz not null default now(),
    created_at timestamptz not null default now()
);

create table if not exists notifications (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid references leads(id) on delete set null,
    channel text not null,
    priority text not null default 'normal',
    event_type text not null,
    payload jsonb not null default '{}'::jsonb,
    status text not null default 'pending',
    sent_at timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists escalation_events (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid references leads(id) on delete set null,
    response_id uuid references responses(id) on delete set null,
    event_type text not null,
    severity text not null,
    summary text not null,
    assigned_to text not null default 'Sean',
    resolved_at timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists suppression_list (
    id uuid primary key default gen_random_uuid(),
    email text,
    domain text,
    lead_id uuid references leads(id) on delete set null,
    reason text not null,
    source text not null,
    created_at timestamptz not null default now(),
    unique nulls not distinct (email, domain)
);

create table if not exists activity_logs (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid references leads(id) on delete set null,
    campaign_id uuid references campaigns(id) on delete set null,
    actor text not null,
    action text not null,
    state_before text,
    state_after text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists prompt_memory (
    id uuid primary key default gen_random_uuid(),
    lead_id uuid references leads(id) on delete cascade,
    memory_type text not null,
    content text not null,
    embedding vector(1536),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_leads_campaign_id on leads(campaign_id);
create index if not exists idx_leads_state on leads(state);
create index if not exists idx_outreach_sequences_lead_id on outreach_sequences(lead_id);
create index if not exists idx_outreach_messages_lead_id on outreach_messages(lead_id);
create index if not exists idx_responses_lead_id on responses(lead_id);
create index if not exists idx_notifications_status on notifications(status);
create index if not exists idx_escalation_events_lead_id on escalation_events(lead_id);
create index if not exists idx_activity_logs_lead_id on activity_logs(lead_id);
