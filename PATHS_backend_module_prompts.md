# PATHS Backend Module Prompts (Anti-Gravity)

Use each prompt independently. Each one targets exactly one module and enforces Modular Monolith + Clean/Hexagonal Architecture.

## 1) AUTH Module Prompt
```text
Create the AUTH module for the Python FastAPI backend project PATHS (Personalized AI Talent Hiring System).

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/auth/
- Separate layers strictly into:
  - domain
  - application
  - infrastructure
  - presentation
- Assume shared/common utilities already exist for config, db sessions, auth helpers, logging, middleware, exceptions
- Do NOT regenerate the full project
- Production-style naming, team-friendly structure, extensible code

Module purpose:
Authentication and authorization.

Responsibilities:
- user login
- user registration
- refresh token flow
- password hashing
- JWT token creation/verification
- role-based access control (RBAC)
- permission checks
- logout / token invalidation strategy
- forgot/reset password placeholders
- email verification placeholders

Required files:
- domain/entities/auth_session.py
- domain/value_objects/token_payload.py
- application/use_cases/login.py
- application/use_cases/register.py
- application/use_cases/refresh_token.py
- application/services/auth_service.py
- infrastructure/security/jwt_service.py
- infrastructure/security/password_hasher.py
- infrastructure/repositories/token_repository.py
- presentation/routes/auth_routes.py
- presentation/dependencies/current_user.py
- presentation/schemas/auth_requests.py
- presentation/schemas/auth_responses.py
- tests for login/register/token validation

Also include:
- RBAC placeholder
- role examples: recruiter, admin, hiring_manager
- route examples: /auth/register, /auth/login, /auth/refresh, /auth/me

Output format:
1) Full folder tree
2) Purpose of each file
3) Starter code skeletons (interfaces, repositories, services, schemas, routes, DTOs, models, events where relevant)
4) Implementation notes
```

## 2) USERS Module Prompt
```text
Create the USERS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/users/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate the full project
- Use production-style naming and extensible patterns

Module purpose:
Manage platform users (recruiters, hiring managers, admins, interviewers, system operators).

Responsibilities:
- create/read/update/deactivate users
- profile management
- role assignment
- status management
- team membership links
- user preferences/settings placeholders

Required files:
- domain/entities/user.py
- domain/value_objects/email.py
- domain/enums/user_role.py
- domain/enums/user_status.py
- application/use_cases/create_user.py
- application/use_cases/update_user.py
- application/use_cases/get_user.py
- application/use_cases/deactivate_user.py
- application/services/user_service.py
- application/ports/user_repository.py
- infrastructure/persistence/models/user_model.py
- infrastructure/repositories/sql_user_repository.py
- presentation/routes/user_routes.py
- presentation/schemas/user_requests.py
- presentation/schemas/user_responses.py
- tests for CRUD and role assignment

Role support:
- recruiter
- hiring_manager
- admin
- interviewer

Output format:
1) Full folder tree
2) Short explanation of each file
3) Starter code skeletons
4) Notes on relations with auth and organizations modules
```

## 3) ORGANIZATIONS Module Prompt
```text
Create the ORGANIZATIONS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/organizations/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Manage organizations/companies, teams, departments, and hiring settings.

Responsibilities:
- create organizations
- manage organization profiles
- departments/business units
- recruiter team membership
- hiring preferences/settings
- organization-level permissions placeholders
- organization branding/settings placeholders

Required files:
- domain/entities/organization.py
- domain/entities/department.py
- domain/entities/team_membership.py
- application/use_cases/create_organization.py
- application/use_cases/update_organization.py
- application/use_cases/add_department.py
- application/use_cases/assign_user_to_organization.py
- application/services/organization_service.py
- application/ports/organization_repository.py
- infrastructure/persistence/models/organization_model.py
- infrastructure/persistence/models/department_model.py
- infrastructure/repositories/sql_organization_repository.py
- presentation/routes/organization_routes.py
- presentation/schemas/organization_requests.py
- presentation/schemas/organization_responses.py
- tests for org creation and membership assignment

Include organization fields:
- name
- industry
- size
- country
- hiring policy flags
- subscription/status placeholders

Output format:
1) Module folder tree
2) File purposes
3) Starter code skeletons
4) Notes on relation to users and jobs modules
```

## 4) JOBS Module Prompt
```text
Create the JOBS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/jobs/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Manage job openings, requirements, hiring stages, and lifecycle.

Responsibilities:
- create job postings
- edit job requirements
- define must-have and nice-to-have skills
- define experience/seniority
- set workflow stages
- open/close/archive jobs
- attach organization/department/owner
- scoring criteria placeholders

Required files:
- domain/entities/job.py
- domain/entities/job_requirement.py
- domain/entities/hiring_stage.py
- domain/enums/job_status.py
- application/use_cases/create_job.py
- application/use_cases/update_job.py
- application/use_cases/publish_job.py
- application/use_cases/archive_job.py
- application/services/job_service.py
- application/ports/job_repository.py
- infrastructure/persistence/models/job_model.py
- infrastructure/persistence/models/job_requirement_model.py
- infrastructure/repositories/sql_job_repository.py
- presentation/routes/job_routes.py
- presentation/schemas/job_requests.py
- presentation/schemas/job_responses.py
- tests for job lifecycle

Include fields:
- title
- description
- department
- location
- work_mode (remote/hybrid/on_site)
- required_skills
- preferred_skills
- years_of_experience
- education
- salary placeholder
- status

Output format:
1) Full tree
2) Short explanation
3) Starter code skeletons
4) Notes on how matching module consumes job data
```

## 5) CANDIDATES Module Prompt
```text
Create the CANDIDATES module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/candidates/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Manage candidate profiles, CV ingestion/parsing placeholders, enrichment, and lifecycle.

Responsibilities:
- create candidate records
- parse uploaded CV/resume placeholders
- normalize candidate data
- manage skills/education/experience
- candidate status tracking
- deduplication placeholder
- enrichment placeholders (LinkedIn/GitHub/external)

Required files:
- domain/entities/candidate.py
- domain/entities/resume.py
- domain/entities/experience.py
- domain/entities/education.py
- domain/entities/candidate_skill.py
- domain/enums/candidate_status.py
- application/use_cases/create_candidate.py
- application/use_cases/parse_resume.py
- application/use_cases/update_candidate.py
- application/use_cases/enrich_candidate.py
- application/services/candidate_service.py
- application/ports/candidate_repository.py
- application/ports/resume_parser_port.py
- infrastructure/persistence/models/candidate_model.py
- infrastructure/persistence/models/resume_model.py
- infrastructure/repositories/sql_candidate_repository.py
- infrastructure/adapters/resume_parser_adapter.py
- presentation/routes/candidate_routes.py
- presentation/schemas/candidate_requests.py
- presentation/schemas/candidate_responses.py
- workers/candidate_ingestion_worker.py
- tests for creation, parsing flow, enrichment placeholders

Include fields:
- full_name
- anonymized fields placeholder
- email/phone placeholders
- current_title
- years_of_experience
- skills
- education
- work_history
- source
- consent/privacy flags placeholder

Output format:
1) File tree
2) File purposes
3) Starter code skeletons
4) Notes on relation to matching, compliance, and audit
```

## 6) MATCHING Module Prompt
```text
Create the MATCHING module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/matching/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Score/rank candidates against jobs with explainability placeholders.

Responsibilities:
- compute candidate-job match scores
- rank candidates for a job
- combine rule-based + embedding-based scoring
- explain ranking factors
- support filters/thresholds
- produce recruiter-friendly summaries
- ranking history placeholders

Required files:
- domain/entities/match_score.py
- domain/entities/ranking_result.py
- domain/value_objects/score_breakdown.py
- application/use_cases/match_candidate_to_job.py
- application/use_cases/rank_candidates_for_job.py
- application/use_cases/explain_match.py
- application/services/matching_service.py
- application/ports/matching_repository.py
- application/ports/vector_similarity_port.py
- application/ports/graph_context_port.py
- infrastructure/repositories/sql_matching_repository.py
- infrastructure/adapters/qdrant_similarity_adapter.py
- infrastructure/adapters/neo4j_context_adapter.py
- presentation/routes/matching_routes.py
- presentation/schemas/matching_requests.py
- presentation/schemas/matching_responses.py
- workers/ranking_worker.py
- tests for scoring/ranking logic

Scoring dimensions placeholders:
- skill overlap
- semantic similarity
- experience fit
- education fit
- location/work-mode fit
- fairness/compliance adjustment hook
- explanation fields

Output format:
1) Folder tree
2) File explanations
3) Starter code skeletons
4) Notes on integration with jobs, candidates, rag, compliance
```

## 7) INTERVIEWS Module Prompt
```text
Create the INTERVIEWS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/interviews/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Interview scheduling, sessions, evaluations, and transcript placeholders.

Responsibilities:
- create interview sessions
- link candidate + job + interviewer
- schedule interview time
- define interview stages/types
- store evaluation results
- transcript placeholder
- feedback summary placeholder
- interviewer scorecards

Required files:
- domain/entities/interview_session.py
- domain/entities/interview_evaluation.py
- domain/entities/interview_question_set.py
- domain/enums/interview_status.py
- domain/enums/interview_type.py
- application/use_cases/schedule_interview.py
- application/use_cases/update_interview_status.py
- application/use_cases/submit_evaluation.py
- application/use_cases/get_interview_summary.py
- application/services/interview_service.py
- application/ports/interview_repository.py
- infrastructure/persistence/models/interview_session_model.py
- infrastructure/persistence/models/interview_evaluation_model.py
- infrastructure/repositories/sql_interview_repository.py
- infrastructure/adapters/calendar_adapter.py
- presentation/routes/interview_routes.py
- presentation/schemas/interview_requests.py
- presentation/schemas/interview_responses.py
- workers/interview_analysis_worker.py
- tests for scheduling and evaluation submission

Interview types:
- screening
- technical
- behavioral
- final

Output format:
1) Full module tree
2) Purposes
3) Starter code skeletons
4) Notes on relation to rag, agents, outreach, audit
```

## 8) RAG Module Prompt
```text
Create the RAG module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/rag/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Retrieval-augmented generation support for interview assistance, policy lookup, explainability.

Responsibilities:
- document ingestion placeholders
- chunking
- embedding generation placeholders
- vector search
- retrieval pipeline
- citation-ready context objects
- prompt context assembly
- recruiter Q&A and interview support

Required files:
- domain/entities/knowledge_document.py
- domain/entities/chunk.py
- domain/entities/retrieval_result.py
- application/use_cases/ingest_document.py
- application/use_cases/index_chunks.py
- application/use_cases/retrieve_context.py
- application/use_cases/build_prompt_context.py
- application/services/rag_service.py
- application/ports/vector_store_port.py
- application/ports/embedding_port.py
- application/ports/document_loader_port.py
- infrastructure/adapters/qdrant_vector_store.py
- infrastructure/adapters/embedding_adapter.py
- infrastructure/adapters/document_loader.py
- presentation/routes/rag_routes.py
- presentation/schemas/rag_requests.py
- presentation/schemas/rag_responses.py
- workers/document_indexing_worker.py
- tests for chunking/retrieval placeholders

Use cases:
- job-based interview question support
- compliance/policy retrieval
- candidate profile contextual assistance
- recruiter explainability assistant

Output format:
1) Tree
2) File purposes
3) Starter code skeletons
4) Notes on relation to interviews, matching, agents, compliance
```

## 9) AGENTS Module Prompt
```text
Create the AGENTS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/agents/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Orchestrate AI agents/workflows for sourcing, screening, ranking support, interview support, recruiter assistance, decision support.

Responsibilities:
- define agent roles
- orchestrate multi-step workflows
- manage agent state/context
- call tools/services from other modules
- human-in-the-loop checkpoints
- execution logs placeholders
- LangGraph/LangChain style orchestration

Required files:
- domain/entities/agent_task.py
- domain/entities/agent_workflow.py
- domain/entities/workflow_state.py
- domain/enums/agent_type.py
- application/use_cases/run_workflow.py
- application/use_cases/execute_agent_step.py
- application/use_cases/request_human_approval.py
- application/services/agent_orchestrator.py
- application/ports/llm_port.py
- application/ports/workflow_engine_port.py
- application/ports/tool_execution_port.py
- infrastructure/adapters/llm_adapter.py
- infrastructure/adapters/langgraph_workflow_adapter.py
- infrastructure/registry/tool_registry.py
- presentation/routes/agent_routes.py
- presentation/schemas/agent_requests.py
- presentation/schemas/agent_responses.py
- workers/agent_execution_worker.py
- tests for workflow orchestration placeholders

Agent examples:
- sourcing_agent
- ranking_assistant
- interview_copilot
- recruiter_assistant
- compliance_checker_hook
- development_plan_assistant

Output format:
1) Full tree
2) File explanations
3) Starter code skeletons
4) Notes on safe orchestration + HITL design
```

## 10) COMPLIANCE Module Prompt
```text
Create the COMPLIANCE module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/compliance/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Fairness, privacy, explainability, bias checks, policy validation hooks.

Responsibilities:
- fairness check hooks
- bias assessment placeholders
- privacy/consent checks
- sensitive attribute masking hooks
- explainability support
- compliance rule evaluation
- audit-ready results
- policy violation flags

Required files:
- domain/entities/compliance_rule.py
- domain/entities/compliance_result.py
- domain/entities/fairness_check.py
- domain/enums/compliance_status.py
- application/use_cases/run_candidate_compliance_check.py
- application/use_cases/run_ranking_compliance_check.py
- application/use_cases/generate_compliance_summary.py
- application/services/compliance_service.py
- application/ports/compliance_repository.py
- application/ports/policy_engine_port.py
- infrastructure/repositories/sql_compliance_repository.py
- infrastructure/adapters/policy_engine_adapter.py
- presentation/routes/compliance_routes.py
- presentation/schemas/compliance_requests.py
- presentation/schemas/compliance_responses.py
- workers/compliance_worker.py
- tests for rule evaluation placeholders

Placeholder checks:
- missing consent
- bias-sensitive field exposure
- explanation required
- ranking review required
- privacy risk flag

Output format:
1) File tree
2) File purposes
3) Starter code skeletons
4) Notes on relation to candidates, matching, interviews, audit
```

## 11) OUTREACH Module Prompt
```text
Create the OUTREACH module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/outreach/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Candidate communications: outreach, invitations, reminders, status updates.

Responsibilities:
- send interview invitations
- send outreach emails
- send status update notifications
- reminder scheduling placeholders
- communication templates
- delivery status tracking
- communication history placeholders

Required files:
- domain/entities/outreach_message.py
- domain/entities/notification_template.py
- domain/entities/delivery_status.py
- domain/enums/message_channel.py
- domain/enums/message_status.py
- application/use_cases/send_outreach_message.py
- application/use_cases/send_interview_invitation.py
- application/use_cases/send_reminder.py
- application/services/outreach_service.py
- application/ports/message_sender_port.py
- application/ports/template_renderer_port.py
- infrastructure/adapters/email_sender_adapter.py
- infrastructure/adapters/template_renderer.py
- infrastructure/repositories/outreach_repository.py
- presentation/routes/outreach_routes.py
- presentation/schemas/outreach_requests.py
- presentation/schemas/outreach_responses.py
- workers/outreach_worker.py
- tests for sending flow placeholders

Channels:
- email (active)
- SMS placeholder
- in-app notification placeholder

Output format:
1) Module tree
2) File purposes
3) Starter code skeletons
4) Notes on relation to interviews, candidates, audit
```

## 12) ANALYTICS Module Prompt
```text
Create the ANALYTICS module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/analytics/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Hiring analytics, pipeline metrics, ranking performance, recruiter insights, dashboards.

Responsibilities:
- hiring funnel metrics
- time-to-fill placeholders
- candidate pipeline analytics
- ranking performance summaries
- interview stage metrics
- recruiter activity metrics
- organization/job level analytics
- export/report placeholders

Required files:
- domain/entities/metric_snapshot.py
- domain/entities/funnel_metric.py
- domain/value_objects/analytics_query.py
- application/use_cases/get_dashboard_metrics.py
- application/use_cases/get_job_analytics.py
- application/use_cases/get_recruiter_analytics.py
- application/use_cases/get_pipeline_metrics.py
- application/services/analytics_service.py
- application/ports/analytics_repository.py
- infrastructure/repositories/sql_analytics_repository.py
- presentation/routes/analytics_routes.py
- presentation/schemas/analytics_requests.py
- presentation/schemas/analytics_responses.py
- tests for analytics aggregation placeholders

Metrics examples:
- candidates per stage
- shortlisted vs rejected
- average ranking score
- interview conversion
- recruiter workload
- compliance flags count
- outreach response rate placeholder

Output format:
1) Full tree
2) Short explanation
3) Starter code skeletons
4) Notes on relation to audit and decision support
```

## 13) AUDIT Module Prompt
```text
Create the AUDIT module for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith
- Clean / Hexagonal Architecture
- Scope only this module under: app/modules/audit/
- Layers: domain, application, infrastructure, presentation
- Assume shared/common utilities already exist
- Do NOT regenerate full project

Purpose:
Immutable-style audit logs for actions, AI decisions, access events, compliance traceability.

Responsibilities:
- log key actions
- track actor/action/target/timestamp
- record system + AI-generated events
- support traceability for compliance/debugging
- query audit history
- entity-level audit trail
- security event placeholders

Required files:
- domain/entities/audit_log.py
- domain/entities/audit_event.py
- domain/value_objects/actor_context.py
- application/use_cases/log_action.py
- application/use_cases/get_entity_audit_history.py
- application/use_cases/search_audit_logs.py
- application/services/audit_service.py
- application/ports/audit_repository.py
- infrastructure/persistence/models/audit_log_model.py
- infrastructure/repositories/sql_audit_repository.py
- presentation/routes/audit_routes.py
- presentation/schemas/audit_requests.py
- presentation/schemas/audit_responses.py
- tests for logging and querying

Audit examples:
- user login
- candidate created
- resume parsed
- ranking generated
- interview evaluation submitted
- outreach sent
- compliance check executed
- admin permission changed

Output format:
1) File tree
2) Purpose of each part
3) Starter code skeletons
4) Notes on cross-module integration hooks
```

## 14) SHARED/COMMON Module Prompt
```text
Create the SHARED/COMMON backend foundation for the Python FastAPI backend project PATHS.

Constraints:
- Modular Monolith support layer
- Scope only shared foundation under: app/shared/
- Do NOT regenerate full project
- Production-ready naming, reusable contracts, easy extension

Purpose:
Cross-cutting components used by all modules.

Responsibilities:
- app config/settings
- environment handling
- logging
- custom exceptions
- middleware
- db session management
- base ORM models
- security helpers
- response/pagination utilities
- event bus / task queue abstraction
- common enums / base classes

Expected structure:
- app/shared/config/
- app/shared/logging/
- app/shared/security/
- app/shared/exceptions/
- app/shared/middleware/
- app/shared/database/
- app/shared/events/
- app/shared/utils/
- app/shared/contracts/

Required files:
- config/settings.py
- config/environment.py
- logging/logger.py
- exceptions/base.py
- exceptions/http_exceptions.py
- middleware/request_context.py
- middleware/error_handler.py
- database/base.py
- database/session.py
- database/unit_of_work.py (placeholder)
- security/passwords.py
- security/jwt_utils.py
- events/event_bus.py
- events/task_dispatcher.py
- utils/pagination.py
- utils/datetime_utils.py
- utils/id_generator.py
- contracts/base_repository.py
- contracts/base_service.py

Output format:
1) Folder tree
2) File purposes
3) Starter code skeletons
4) Notes on how feature modules should depend on shared code safely
```
