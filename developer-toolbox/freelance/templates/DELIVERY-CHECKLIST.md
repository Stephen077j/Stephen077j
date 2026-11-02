# Software delivery checklist / Contrôle avant livraison

## Scope and acceptance
- [ ] Signed-off scope, expected behaviors and measurable acceptance criteria
- [ ] Client validated important UX and permission flows
- [ ] Accessibility and target-device checks performed

## Functional and technical
- [ ] Automated unit/integration/E2E tests passed
- [ ] Database migrations and backup restoration tested
- [ ] Error handling, validation, audit logs and role access reviewed
- [ ] Performance and concurrency tests appropriate for expected use
- [ ] Integration failures tested, including payments where applicable

## Security and legal
- [ ] No credentials in Git or frontend bundles
- [ ] Dependency and vulnerability review
- [ ] HTTPS, least privilege, secrets rotation, session lifecycle
- [ ] Privacy, licenses, data residency, retention and local laws reviewed
- [ ] Payment/SMS/email providers verified and approved by client

## Deployment
- [ ] Staging approval before production release
- [ ] Monitoring, alerting, backups and rollback procedure checked
- [ ] DNS, TLS, domain renewal and hosting ownership recorded
- [ ] Disaster recovery expectations documented

## Handover
- [ ] Administrator guide and user training
- [ ] Client access handed over through secure channel
- [ ] Contractual support period, SLA and escalation contacts
- [ ] Known limitations, warranties and maintenance plans documented

**Evidence:** Link to CI run, acceptance record, deployment checklist and signed client approval in the private client workspace.
