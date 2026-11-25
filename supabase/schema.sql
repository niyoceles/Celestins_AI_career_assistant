-- Optional lead and unanswered-question storage for the career assistant.
-- Run this in the Supabase SQL Editor before configuring SUPABASE_URL and
-- SUPABASE_SECRET_KEY in the app's server environment.

create table if not exists public.career_leads (
    id uuid primary key default gen_random_uuid(),
    email text not null check (char_length(email) <= 254),
    name text not null default 'Name not provided',
    notes text not null default '',
    created_at timestamptz not null default now()
);

create table if not exists public.unknown_questions (
    id uuid primary key default gen_random_uuid(),
    question text not null check (char_length(question) <= 2000),
    created_at timestamptz not null default now()
);

alter table public.career_leads enable row level security;
alter table public.unknown_questions enable row level security;

revoke all on table public.career_leads from anon, authenticated;
revoke all on table public.unknown_questions from anon, authenticated;
grant all on table public.career_leads to service_role;
grant all on table public.unknown_questions to service_role;
