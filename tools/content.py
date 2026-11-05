"""
Content of the HyperVelocity Engineering hands-on workshop exercise guide.

Edit this file, then rebuild the site:

    python tools/build_site.py

The pages are written to docs/ (GitHub Pages: Settings > Pages > Deploy from a branch > main > /docs).

Inline formatting in any text value:
    `code`              -> monospace
    **bold**            -> bold
    [link text](url)    -> link (external links open in a new tab)
    a line break "\n"   -> line break

Template cells:
    None                -> empty cell participants can type into
    ph("hint")          -> empty cell with a grey hint
    "text"              -> fixed text
"""

SITE = {
    "name": "HyperVelocity Engineering",
    "tagline": "Hands-on workshop · Exercise guide",
    "footer": "HyperVelocity Engineering · Hands-on workshop · Exercise guide",
    "footer_note": (
        "Links point to public documentation. HVE Core and HVE-Squad change quickly: "
        "use the versions installed for the workshop."
    ),
    "storage_note": (
        "Template cells are editable: type in them, then use **Copy as Markdown** to paste the result "
        "into your repository or wiki. What you type stays in this browser only; nothing is uploaded."
    ),
}

# ---------------------------------------------------------------------------
# Links used across the guide
# ---------------------------------------------------------------------------
U = {
    "hve_core": "https://microsoft.github.io/hve-core/",
    "first_workflow": "https://microsoft.github.io/hve-core/docs/getting-started/first-workflow/",
    "rpi": "https://microsoft.github.io/hve-core/docs/rpi/",
    "agents": "https://microsoft.github.io/hve-core/docs/agents/",
    "project_planning": "https://microsoft.github.io/hve-core/docs/agents/project-planning/",
    "backlog": "https://microsoft.github.io/hve-core/docs/agents/backlog/",
    "design_thinking": "https://microsoft.github.io/hve-core/docs/design-thinking/",
    "security": "https://microsoft.github.io/hve-core/docs/agents/security/",
    "customization": "https://microsoft.github.io/hve-core/docs/customization/",
    "team_adoption": "https://microsoft.github.io/hve-core/docs/customization/team-adoption/",
    "roles": "https://microsoft.github.io/hve-core/docs/hve-guide/roles/",
    "lifecycle": "https://microsoft.github.io/hve-core/docs/hve-guide/lifecycle/",
    "hve_builder": "https://microsoft.github.io/hve-core/docs/reference/skills/hve-core/hve-builder/",
    "squad": "https://peter-n91.github.io/hve-squad/",
    "squad_start": "https://peter-n91.github.io/hve-squad/getting-started.html",
    "squad_usage": "https://peter-n91.github.io/hve-squad/usage.html",
    "squad_demo": "https://peter-n91.github.io/hve-squad/demo.html",
    "squad_trouble": "https://peter-n91.github.io/hve-squad/troubleshooting.html",
    "squad_workshop": "https://peter-n91.github.io/hve-squad-hands-on-workshop/",
    "apm": "https://microsoft.github.io/apm/",
    "apm_gov": "https://github.com/microsoft/apm/blob/main/docs/src/content/docs/enterprise/governance-guide.md",
    "vs_overview": "https://code.visualstudio.com/docs/agent-customization/overview",
    "vs_skills": "https://code.visualstudio.com/docs/agent-customization/agent-skills",
    "vs_agents": "https://code.visualstudio.com/docs/agent-customization/custom-agents",
    "vs_mcp": "https://code.visualstudio.com/docs/agent-customization/mcp-servers",
    "vs_hooks": "https://code.visualstudio.com/docs/agent-customization/hooks",
    "gl_protected": "https://docs.gitlab.com/user/project/repository/branches/protected/",
    "gl_approvals": "https://docs.gitlab.com/user/project/merge_requests/approvals/rules/",
    "bb_checks": "https://confluence.atlassian.com/bitbucketserver/checks-for-merging-pull-requests-776640039.html",
    "gh_rulesets": (
        "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/"
        "managing-rulesets/about-rulesets"
    ),
    "gh_billing": (
        "https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing"
    ),
    "gh_metrics": (
        "https://docs.github.com/en/copilot/concepts/billing-and-usage/copilot-usage-metrics/copilot-metrics"
    ),
    "skills_spec": "https://agentskills.io/specification",
    "mcp_spec": "https://modelcontextprotocol.io/docs/getting-started/intro",
    "rai": "https://www.microsoft.com/en-us/ai/principles-and-approach",
    "skillup": "https://skillupwithlevelup.com/frontier",
    "sre": "https://learn.microsoft.com/en-us/azure/sre-agent/",
    "sre_overview": "https://learn.microsoft.com/en-us/azure/sre-agent/overview",
    "azmcp": "https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/",
    "azmcp_start": "https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started",
    "fabric_mcp": "https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/what-is-fabric-mcp-server",
    "workiq_mcp": "https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview",
    "deepwiki_docs": "https://docs.devin.ai/work-with-devin/deepwiki-mcp",
    "deepwiki": "https://mcp.deepwiki.com/",
    "context7": "https://github.com/upstash/context7",
    "gh_mcp": "https://github.com/mcp",
    "rovo_mcp": "https://developer.atlassian.com/cloud/rovo-mcp/",
    "mcp_atlassian": "https://github.com/sooperset/mcp-atlassian",
    "accelerators": "https://accelerators.ms/#section=accelerators",
}


# ---------------------------------------------------------------------------
# Small helpers to keep the page definitions readable
# ---------------------------------------------------------------------------
def ph(text):
    """An editable cell that shows a grey hint until someone types."""
    return {"ph": text}


def matrix(corner, cols, rows):
    """Row labels down the side, one empty cell per column."""
    return {
        "head": [corner] + list(cols),
        "rows": [[r] + [None] * len(cols) for r in rows],
        "row_header": True,
    }


def blank(cols, n=3, numbered=False, hints=None):
    """A header row plus n empty rows. hints: optional list of first-column hints, one per row."""
    rows = []
    for i in range(n):
        if numbered:
            row = [str(i + 1)] + [None] * (len(cols) - 1)
        else:
            row = [None] * len(cols)
        if hints and i < len(hints):
            row[1 if numbered else 0] = ph(hints[i])
        rows.append(row)
    return {"head": list(cols), "rows": rows, "row_header": numbered}


def form(fields, col="Our answer"):
    """A two-column form: field names on the left, an empty answer cell on the right."""
    rows = []
    for f in fields:
        if isinstance(f, tuple):
            rows.append([f[0], ph(f[1])])
        else:
            rows.append([f, None])
    return {"head": ["", col], "rows": rows, "row_header": True}


def brief(objective, input_, best_use, roles, roles_label="Roles (suggested)"):
    return {"type": "brief", "objective": objective, "input": input_, "best_use": best_use,
            "roles": roles, "roles_label": roles_label}


def work(steps, handin):
    return {"type": "work", "steps": steps, "handin": handin}


def section(id_, eyebrow, title, jump=None, lead=None):
    return {"type": "section", "id": id_, "eyebrow": eyebrow, "title": title, "jump": jump, "lead": lead}


def template(id_, label, spec, note=None):
    block = {"type": "template", "id": id_, "label": label, "note": note}
    block.update(spec)
    return block


def table(head, rows, row_header=False, caption=None, cls=None):
    return {"type": "table", "head": head, "rows": rows, "row_header": row_header,
            "caption": caption, "cls": cls}


def run_with(*items, label="Run it with"):
    """items: (label or None, text)."""
    return {"type": "runwith", "label": label, "items": list(items)}


def links(*items, label="Links"):
    """items: (link text, url)."""
    return {"type": "links", "label": label, "items": list(items)}


def done(text):
    return {"type": "done", "text": text}


def tips(*items, label="Tips"):
    return {"type": "tips", "label": label, "items": list(items)}


def callout(kind, title, text, actions=None):
    """kind: wait | info | next. actions: list of (label, href)."""
    return {"type": "callout", "kind": kind, "title": title, "text": text, "actions": actions or []}


def banner(text, kind="navy"):
    return {"type": "banner", "text": text, "kind": kind}


def code(text, caption=None, id_=None):
    return {"type": "code", "text": text, "caption": caption, "id": id_}


def para(text, cls=None):
    return {"type": "p", "text": text, "cls": cls}


def bullets(items, title=None, cls=None):
    return {"type": "list", "items": items, "title": title, "cls": cls}


def cols(*columns, cls=None):
    return {"type": "cols", "cols": [list(c) for c in columns], "cls": cls}


def numbered(items, cls=None):
    """Big numbered rows: items are (title, text) or plain text."""
    return {"type": "numbered", "items": items, "cls": cls}


def subhead(text, id_=None):
    return {"type": "h3", "text": text, "id": id_}


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------
HOME = {
    "kicker": "Advanced hands-on workshop",
    "title": "HyperVelocity Engineering",
    "title_line2": "Exercise guide",
    "lead": "Ten team exercises to apply HVE, HVE Core and HVE-Squad to real or anonymised scenarios",
    "goals_title": "What today is for",
    "goals": [
        "Experience a governed agentic lifecycle, end to end, on your own scenario",
        "Compare approaches: HVE Core, HVE-Squad or your own orchestrator",
        "Leave with a concrete view of where HVE fits into your existing engineering and AMS practices",
    ],
    "north_star": (
        "Each team finishes with evidence, decisions, a tested increment or a credible implementation plan, "
        "and one adoption commitment that continues after Microsoft leaves the room."
    ),
    "quote": "The question isn’t which tool wins. It’s where each approach adds the most value.",
    "how_to_use": [
        ("Follow along at your own pace",
         "Your facilitator presents and coordinates; this site has every brief, template and link, so your "
         "team can keep working without waiting for the screen."),
        ("Open labs, not time slots",
         "Exercises are numbered, not time-boxed. Teams work in four open labs and start the next exercise "
         "when they are ready."),
        ("Two parts per exercise",
         "A **brief** (objective, input, steps, what to hand in) and a **toolkit** (fill-in templates, how to "
         "run it with HVE Core or HVE-Squad, and links)."),
        ("Nobody waits for an agent",
         "Intermissions A–C fill waiting time while agents run. Exercise 9 is a backup for teams that "
         "finish early."),
    ],
}

# Groups shown in the sidebar and on the home page, in the order of the day.
GROUPS = [
    {"name": "Get started", "note": "Before the first lab"},
    {"name": "Open lab 1", "note": "Exercises 1–3"},
    {"name": "Open lab 2", "note": "Exercises 4–5 · Intermission A"},
    {"name": "Open lab 3", "note": "Exercises 6–7 · Intermissions B–C"},
    {"name": "Open lab 4", "note": "Exercises 8 and 10 · backup Exercise 9"},
    {"name": "Close", "note": "Playback and scorecard"},
    {"name": "Reference", "note": "All links and templates"},
]

# ---------------------------------------------------------------------------
# Pages, in step-by-step order
# kind: info | core | parallel | intermission | backup  (drives badges and colours)
# ---------------------------------------------------------------------------
PAGES = [
    # ------------------------------------------------------------- Get started
    {
        "slug": "agenda",
        "group": "Get started",
        "kind": "info",
        "nav": "Suggested agenda",
        "eyebrow": "The day at a glance · Suggested agenda",
        "title": "Ten exercises, three intermissions, four open labs",
        "summary": "A suggested one-day plan with four open labs, two breaks, lunch and a team playback.",
        "blocks": [
            callout(
                "info",
                "This agenda is a suggestion",
                "Your facilitator confirms the timings on the day. Exercises are numbered, not time-boxed: "
                "inside each open lab your team paces itself and picks up the next exercise when it is ready.",
            ),
            table(
                ["Time (suggested)", "Block", "Purpose"],
                [
                    ["09:00–09:30", "Arrival and technical recovery",
                     "Resolve final access issues; assign teams and roles"],
                    ["09:30–09:50", "[Kick-off and challenge framing](team-charter.html)",
                     "Confirm scenarios, success criteria and working agreements"],
                    ["09:50–11:15", "[Open lab 1](exercise-1.html) · Exercises 1–3",
                     "Predict the lifecycle, build an evidence map, define MVEs"],
                    {"cells": ["11:15–11:30", "Break", "Agents may continue running"], "cls": "pause"},
                    ["11:30–13:00", "[Open lab 2](exercise-4.html) · Exercises 4–5 · Intermission A",
                     "Intake to an approved backlog; design a reusable component"],
                    {"cells": ["13:00–14:00", "Lunch", "Short coach huddle and run health check"], "cls": "pause"},
                    ["14:00–15:30", "[Open lab 3](exercise-6.html) · Exercises 6–7 · Intermissions B–C",
                     "Bounded RPI build, gates and controls; AI versus script audit"],
                    {"cells": ["15:30–15:45", "Break", "Prepare evidence for cross-review"], "cls": "pause"},
                    ["15:45–17:10", "[Open lab 4](exercise-8.html) · Exercises 8 and 10",
                     "Red team and recovery; adoption path (Exercise 9 is backup)"],
                    ["17:10–17:30", "[Team playback and close](playback.html)",
                     "Show evidence, lessons, decisions, owners and next steps"],
                ],
                cls="agenda",
            ),
            section("labs", "How the labs run · Suggested split", "A core task and a parallel task in every lab",
                    jump="How the labs run"),
            table(
                ["Open lab", "Core task", "Parallel task, while agents run", "Hand in by the end of the lab"],
                [
                    ["**Open lab 1**",
                     "**[Ex 1 · Predict the lifecycle](exercise-1.html)**, then "
                     "**[Ex 2 · Evidence map](exercise-2.html)**\n"
                     "Whole team, then product owner, auditor, agent operator",
                     "**[Ex 3 · MVE bake-off](exercise-3.html)**\n"
                     "Architect, quality lead; agents run the experiments (may continue over the break)",
                     "Lifecycle map · evidence map · context manifest · questions · 2 MVE cards"],
                    ["**Open lab 2**",
                     "**[Ex 4 · Intake to approved backlog](exercise-4.html)**\n"
                     "Product owner, agent operator, quality lead",
                     "**[Ex 5 · Reusable component](exercise-5.html)**\n"
                     "Architect and one volunteer; [Intermission A](intermission-a.html) (PO canvas) "
                     "while Ex 4 agents run",
                     "Approved requirements · decision log · backlog · component spec · PO canvas"],
                    ["**Open lab 3**",
                     "**[Ex 6 · Bounded RPI work unit](exercise-6.html)**\n"
                     "Agent operator; product owner and architect approve the plan",
                     "**[Ex 7 · Gates and guardrails](exercise-7.html)**\n"
                     "Quality and governance lead, architect; [Intermissions B](intermission-b.html) and "
                     "[C](intermission-c.html) while Ex 6 runs",
                     "Research, plan, patch, review · gate map · control matrix · script-versus-AI audit"],
                    ["**Open lab 4**",
                     "**[Ex 8 · Red team and recovery](exercise-8.html)**, then "
                     "**[Ex 10 · Adoption path](exercise-10.html)**\n"
                     "Whole team; paired with another team for Ex 8",
                     "Backup · **[Ex 9 · Compare autonomy, cost and outcome](exercise-9.html)**\n"
                     "Auditor / observer, only if there is time; then playback preparation",
                     "Findings · recovery log · adoption canvas · pilot and owners"],
                ],
                row_header=True,
                cls="labs",
            ),
            banner("Teams pace themselves inside each lab. The auditor / observer keeps the log all day; "
                   "it feeds Exercise 8 and the playback.", kind="soft"),
            tips(
                "Exercise 7 is a core task but can start while Exercise 6 executes, because its input can be "
                "the Exercise 4 outputs.",
                "Exercise 9 is a backup: run it only if your team finishes early.",
                "Adapt the split to your team size and run speed.",
            ),
        ],
    },
    {
        "slug": "agreements-and-roles",
        "group": "Get started",
        "kind": "info",
        "nav": "Working agreements and roles",
        "eyebrow": "How we work today",
        "title": "Five working agreements",
        "summary": "How we work today, and the five roles every team fills.",
        "blocks": [
            numbered([
                ("Real, small, bounded",
                 "Use a real change where possible. If the source contains sensitive information, use an "
                 "anonymised or simplified version."),
                ("Nobody waits for an agent",
                 "Every waiting period has a parallel team activity with a concrete output."),
                ("Method first, tools second",
                 "HVE is the operating model, HVE Core a selectable toolkit, HVE-Squad an orchestration option. "
                 "Not a contest to crown one tool."),
                ("Enforce what is deterministic",
                 "Deterministic controls for deterministic checks; agents where judgement, synthesis or "
                 "exploration is needed."),
                ("Measure what matters",
                 "Accepted outcomes, human intervention, traceability and learning; not the volume of generated "
                 "code or tokens."),
            ]),
            banner("Strengthen what you already do · No magic multiplier · Your code stays on your own machines"),
            section("roles", "Team roles", "Five roles in every team", jump="Team roles"),
            {"type": "roles", "items": [
                ("Product owner / domain lead",
                 "Frames the outcome, answers questions and accepts or rejects requirements."),
                ("Architect", "Surfaces constraints, risks, dependencies and architecture decisions."),
                ("Agent operator", "Runs the chosen HVE Core or HVE-Squad flow and keeps the session moving."),
                ("Quality and governance lead",
                 "Defines acceptance criteria, controls, security and Responsible AI checks, and human gates."),
                ("Auditor / observer",
                 "Records assumptions, human interventions, timings, failures, cost signals and lessons."),
            ]},
            banner("~25 participants · 4–5 multidisciplinary teams · at least one experienced agent-mode user in "
                   "every team · in small teams, one person can hold two roles", kind="soft"),
            links(("HVE Core · Role guides", U["roles"]), label="Link"),
            tips(
                "Your code stays on your laptops: facilitators never need access to it.",
                "Keep the agreements visible on your table.",
                "The auditor’s log starts with Exercise 1; it feeds Exercises 8 and 9 and the final playback.",
            ),
        ],
    },
    {
        "slug": "team-charter",
        "group": "Get started",
        "kind": "info",
        "nav": "Kick-off: team charter",
        "eyebrow": "Kick-off",
        "title": "Write your team charter in 10 minutes",
        "summary": "Name your team, scenario, definition of done and what you want to learn.",
        "blocks": [
            para("The kick-off confirms scenarios, success criteria and working agreements.", cls="lead"),
            {"type": "timer", "value": "10", "unit": "minutes",
             "text": "Facilitators confirm every charter before Exercise 1 starts."},
            template("team-charter", "Team charter", form([
                "Team name and members (with roles)",
                "Scenario, in one line, and the owner who can answer questions",
                ("Type", "greenfield · brownfield · AMS change · modernisation"),
                "Definition of done, and at least one representative acceptance test",
                "What we want to learn today",
                "What a successful outcome looks like for us",
                ("How we will run it", "HVE Core · HVE-Squad · our own orchestrator"),
            ])),
            callout("next", "Not sure yet?",
                    "Pick a scenario and a runtime before you fill in the last rows.",
                    actions=[("Your scenario", "scenario.html"), ("How you run it", "how-you-run-it.html")]),
            tips("Be ready to read “What we want to learn today” aloud in 20 seconds: it tells the facilitators "
                 "how deep to go on mechanisms, limits and trade-offs."),
        ],
    },
    {
        "slug": "scenario",
        "group": "Get started",
        "kind": "info",
        "nav": "Your scenario",
        "eyebrow": "Your scenario",
        "title": "Bring a small, real change, or use a ready-made one",
        "summary": "What makes a good scenario, typical scenarios and ready-made fallbacks.",
        "blocks": [
            cols(
                [{"type": "checklist", "title": "A good scenario is…", "items": [
                    "Real, small and bounded: one change you can finish, or credibly plan, today",
                    "Anonymised or simplified if it contains sensitive information",
                    "Owned by someone in the team who can answer questions",
                    "Has a simple definition of done and at least one representative acceptance test",
                ]}],
                [{"type": "cardlist", "title": "Typical scenarios", "items": [
                    ("Change to an existing system",
                     "service request → application research → bounded change → regression review", None),
                    ("Dependency or security remediation",
                     "assess the package, interfaces, tests and rollback", None),
                    ("Modernisation slice",
                     "e.g. .NET Framework to current .NET or a Java upgrade, missing tests first", None),
                    ("Incident triage",
                     "rank hypotheses from logs and context, validate the fix, update the runbook", None),
                    ("A small greenfield feature", "", None),
                ]}],
                [{"type": "cardlist", "title": "Ready-made fallbacks", "items": [
                    ("Inventory-aware cart",
                     "“The catalogue shows 3 units in stock. The cart accepts 4.” Pre-run walkthrough and "
                     "recorded run from the facilitators.", None),
                    ("HVE-Squad self-led workshop",
                     "Northwind Traders: a product squad plus Azure, .NET and Power Platform tracks",
                     ("HVE-Squad hands-on workshop", U["squad_workshop"])),
                    ("HVE Core first full workflow",
                     "A short RPI warm-up on the hve-core repository itself",
                     ("HVE Core · Your first full workflow", U["first_workflow"])),
                ]}],
                cls="three",
            ),
            tips("The HVE-Squad self-led workshop has a Part 00 readiness check and takes about 3.5 hours for one "
                 "track, so use single parts, not the whole thing."),
        ],
    },
    {
        "slug": "how-you-run-it",
        "group": "Get started",
        "kind": "info",
        "nav": "How you run it",
        "eyebrow": "How you run it",
        "title": "Same deliverables, your choice of runtime",
        "summary": "HVE Core, HVE-Squad or your own orchestrator, plus a quick reference of entry points.",
        "blocks": [
            {"type": "runtimes", "items": [
                {"name": "HVE Core", "tag": None, "sub": "The toolkit you drive",
                 "points": [
                     "RPI Agent, or the four phase skills: research, plan, implement, review",
                     "Specialist agents for requirements, architecture decisions, security and Responsible AI "
                     "planning, a Design Thinking coach, and backlog managers for Jira, Azure DevOps and GitHub",
                     "You approve each phase",
                 ],
                 "best": "learning the method, one team, tight control"},
                {"name": "HVE-Squad", "tag": "Experimental", "sub": "Orchestration on the same spine",
                 "points": [
                     "One request: a coordinator routes it to a cast of HVE Core agents",
                     "Autonomy modes: interactive (default) · autonomous · autopilot",
                     "Cost ceiling, decisions log and consumption ledger",
                     "Always stops before anything irreversible: deploy, push, merge, schema change",
                 ],
                 "best": "multi-role work, an audit trail, cost visibility per run"},
                {"name": "Your own orchestrator", "tag": None, "sub": "Bring what you already use",
                 "points": [
                     "Welcome, if it shows the same evidence: research and plan before implementation, a review "
                     "record and a decision log",
                     "Scored on the same [common scorecard](scorecard.html)",
                 ],
                 "best": None},
            ]},
            banner("HVE is the operating model. The toolkit is optional; the evidence is not."),
            tips("HVE-Squad is a community project built on HVE Core, at design-partner stage."),
            section("quick-reference", "Quick reference", "Entry points, and where the evidence lives",
                    jump="Quick reference"),
            cols(
                [{"type": "refcard", "title": "HVE Core", "sub": "VS Code with GitHub Copilot Chat, or Copilot CLI",
                  "items": [
                      ("Agent picker →", "**RPI Agent**: describe the task; manual by default, full auto only "
                                         "on request"),
                      ("Phase skills →", "`/rpi-research` · `/rpi-plan` · `/rpi-implement` · `/rpi-review`"),
                      ("Before acting →", "`/rpi-challenger` (expose assumptions) · `/rpi-walkthrough` "
                                          "(explain code before changing it)"),
                      ("Specialist agents →", "BRD Builder · PRD Builder · ADR Creator · Security Planner · "
                                              "RAI Planner · DT Coach · Backlog Manager · Code Review"),
                      ("Backlog skills →", "`/backlog-plan` (read-only) · `/backlog-execute` (writes to the "
                                           "tracker)"),
                      ("Build your own →", "`/hve-builder`"),
                  ]}],
                [{"type": "refcard", "title": "HVE-Squad", "sub": None, "items": [
                    (None, "`/squad init` → review and confirm the proposed team (no autopilot on setup)"),
                    (None, "`/squad request=\"…\"` → interactive by default; add `mode=autonomous` or "
                           "`mode=autopilot`"),
                    (None, "add `cost-ceiling=<USD>` → spend forecast and a stop point"),
                    (None, "add `routing=off | ranked | economy | manual` → model choice per role"),
                    (None, "ask the coordinator to run `squad-doctor` before work starts"),
                    (None, "`/squad-governance-report` → governance dashboard"),
                    (None, "Copilot CLI or app: choose **Squad Coordinator** and send the same text without "
                           "`/squad`"),
                ]}],
                [{"type": "refcode", "title": "Where the evidence lives", "text": (
                    ".copilot-tracking/\n"
                    "├── research/   ← research notes\n"
                    "├── plans/      ← plan\n"
                    "│               (+ critique in reviews/plans/)\n"
                    "├── changes/    ← change log\n"
                    "├── reviews/    ← review records\n"
                    "└── squad/      ← HVE-Squad state\n"
                    "    ├── team.md · routing.md\n"
                    "    ├── decisions.md\n"
                    "    ├── history/\n"
                    "    ├── consumption.md\n"
                    "    └── state.json")}],
                cls="three ref",
            ),
            banner("Working memory is not the source of truth: **promote decisions to ADRs, requirements, docs and "
                   "the backlog**, and keep `.copilot-tracking/` out of main.", kind="warn"),
            links(("HVE Core · Agents", U["agents"]), ("HVE-Squad · Usage", U["squad_usage"])),
            tips(
                "HVE Core no longer ships prompt files: `/rpi` is retired, so use the RPI Agent and describe the "
                "task.",
                "The separate Azure DevOps, GitHub and Jira backlog agents are now one Backlog Manager.",
                "The Meeting Analyst agent is experimental and needs the Work IQ MCP server, which may not be "
                "available in your organisation; use the PRD Builder’s clarifying questions or `/rpi-research` on "
                "an anonymised transcript instead.",
                "For HVE-Squad, use a fixed, strong model for the coordinator, not Auto.",
            ),
            section("setup-pins", "Setup", "Pins for the day", jump="Setup pins"),
            bullets([
                "**HVE Core:** record the extension or plugin version installed for the workshop",
                "**HVE-Squad:** one pinned release tag for everyone (v0.18.1 at the time of writing; check "
                "Releases)",
                "**APM CLI:** exactly 0.29.0 (0.29.1 and 0.30.0 break the HVE-Squad install); the VS Code route "
                "for HVE-Squad needs it",
                "**PowerShell 7+** on every laptop",
                "**GitHub authenticated before installing** (`gh auth login` or `GITHUB_TOKEN`) to avoid rate "
                "limits",
                "**Do not install the official HVE Core plugin next to the HVE-Squad plugin pair:** every agent "
                "would exist twice",
                "**One fixed coordinator model** for all teams, not Auto",
            ], cls="pins"),
            callout("info", "Do not upgrade on the day",
                    "Use the versions installed during preparation. HVE Core and HVE-Squad change quickly."),
        ],
    },
    {
        "slug": "while-agents-run",
        "group": "Get started",
        "kind": "info",
        "nav": "While agents run",
        "eyebrow": "While agents run",
        "title": "Nobody watches a progress bar",
        "summary": "Seven useful things to do while an agent works, and where the intermissions fit.",
        "blocks": [
            numbered([
                "Predict the next artefact and write its acceptance criteria before it appears",
                "Prepare two alternative decisions and the evidence that would select between them",
                "Review partial evidence for missing, stale, sensitive or irrelevant context",
                "Design the next experiment, agentic workflow, CI/CD check or operational hand-off",
                "Inspect the audit trail and record every human intervention, override and correction",
                "Draft a skill, instruction or deterministic control from a problem observed in the run",
                "Prepare your two-minute playback: decision, evidence, result, failure and lesson",
            ], cls="compact"),
            {"type": "intermissions"},
            tips("Item 7 feeds the [team playback](playback.html) at the end of the day."),
        ],
    },
    # ------------------------------------------------------------- Open lab 1
    {
        "slug": "exercise-1",
        "group": "Open lab 1",
        "kind": "parallel",
        "num": "1",
        "nav": "Predict the lifecycle",
        "eyebrow": "Exercise 1 · Open lab 1 · Parallel or waiting-time task",
        "title": "Predict the lifecycle before the agents do",
        "summary": "Understand the lifecycle and expose hidden assumptions before automation starts.",
        "blocks": [
            brief("Understand the lifecycle and expose hidden assumptions before automation starts.",
                  "A ready-made end-to-end scenario or one of your own cases",
                  "Parallel or waiting-time task",
                  "Whole team; the auditor records the differences",
                  roles_label="Roles"),
            work(
                [
                    "Look only at the starting evidence and the desired outcome.",
                    "On paper, write the steps, roles, gates and artefacts you expect.",
                    "The facilitator reveals a pre-run walkthrough or logs, one stage at a time.",
                    "At each stage, compare your decision with the actual HVE or HVE-Squad path.",
                    "Label each difference: missing context · different judgement · unnecessary machinery.",
                ],
                [
                    "A hand-drawn lifecycle map",
                    "Three assumptions you would validate first",
                    "One change you would make to the automated flow",
                ],
            ),
            section("toolkit", "Exercise 1 · Hand-in and toolkit", "Map it first, then compare it",
                    jump="Hand-in and toolkit"),
            template("lifecycle-map", "Template 1 · Lifecycle map",
                     matrix("", ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"],
                            ["Steps", "Who decides", "Gate", "Artefact left behind"])),
            template("difference-log", "Template 2 · Difference log",
                     blank(["Stage", "What we predicted", "What actually happened", "Label"], n=3),
                     note="Label: missing context / different judgement / unnecessary machinery"),
            run_with((None, "The facilitators’ pre-run walkthrough or logs; for a team’s own case, the research, "
                            "plan and review files of a previous run, or the HVE-Squad decisions log")),
            links(("HVE Core · RPI workflow", U["rpi"]), ("HVE-Squad · Guided demos", U["squad_demo"])),
            done("Every difference carries a label, and the three assumptions are written down before the reveal "
                 "ends."),
            {"type": "reveal",
             "summary": "Reveal: the governed path",
             "warning": "Open this only after your team has drawn its own map. Your facilitator walks through it "
                        "one stage at a time.",
             "eyebrow": "Exercise 1 · Reveal",
             "title": "The governed path: people own the transitions",
             "phases": [
                 ("Discover", "conversation, ticket or incident → evidence map"),
                 ("Define", "requirements → architecture → backlog"),
                 ("Build", "Research → Plan → Implement → Review"),
                 ("Deliver and operate", "PR review, release and ITSM gates, feedback into the next loop"),
             ],
             "gates_title": "Five gates, one owner each",
             "gates": [
                 ("Evidence → BRD", "Product owner"),
                 ("BRD → PRD", "Product + engineering"),
                 ("PRD → Plan", "Architect"),
                 ("Plan → Implement", "Engineering lead"),
                 ("Review → Merge", "Release approver"),
             ],
             "run_title": "The recorded run (inventory-aware cart)",
             "run": [
                 "28-min transcript + 3 pages",
                 "7 unresolved questions",
                 "10 functional · 9 non-functional requirements · 15 acceptance criteria",
                 "19 answers from the owner",
                 "research",
                 "plan + critique: Pass",
                 "20 files · 56 tests",
                 "review",
                 "owner validation",
             ],
             "caveat": "One recorded demonstration on a sample app, not a benchmark or a productivity claim.",
             "links": [("HVE Core · AI-assisted project lifecycle", U["lifecycle"])],
             "banner": "Security and Responsible AI checks sit on these gates, not in a separate review.",
             "questions": [
                 "Who owns each of these gates in your projects today?",
                 "What was your most surprising difference, and which label did you give it?",
                 "The same lifecycle covers application management: the trigger is an incident or a service "
                 "request instead of a new product idea.",
             ]},
            tips(
                "If your own case has pre-run material (research, plan and review files of a previous run), use "
                "it; otherwise use the inventory-aware cart.",
                "The starting evidence is typically a stakeholder transcript and some context; nothing else until "
                "the reveal.",
                "Keep your map: it is reused in [Exercise 9](exercise-9.html) (backup) to compare predicted and "
                "actual human effort.",
            ),
        ],
    },
    {
        "slug": "exercise-2",
        "group": "Open lab 1",
        "kind": "core",
        "num": "2",
        "nav": "Evidence map",
        "eyebrow": "Exercise 2 · Open lab 1 · Core task",
        "title": "Build the evidence map and source-of-truth contract",
        "summary": "Turn fragmented project information into explicit, usable context.",
        "blocks": [
            brief("Turn fragmented project information into explicit, usable context.",
                  "Meeting notes, a ticket, a transcript, an architecture note and an existing backlog item",
                  "Core task",
                  "Product owner, auditor, agent operator"),
            work(
                [
                    "Sort the material into fact, decision, constraint, assumption and open question.",
                    "Choose the project’s source of truth and define what links back to it.",
                    "Write a short context manifest: sources, owners, freshness, sensitivity and allowed use.",
                    "Ask an agent to identify the gaps, then accept, reject or rewrite each gap as a team.",
                ],
                ["Evidence map", "Context manifest", "Prioritised clarification questions"],
            ),
            section("toolkit", "Exercise 2 · Hand-in and toolkit",
                    "Make context explicit, and decide what the agent may use", jump="Hand-in and toolkit"),
            template("evidence-map", "Evidence map", blank(["Item", "Type", "Source", "Owner"], n=4),
                     note="Type: fact · decision · constraint · assumption · open question"),
            template("context-manifest", "Context manifest",
                     blank(["Source", "Owner", "Freshness", "Sensitivity", "Allowed use"], n=3)),
            template("clarification-questions", "Clarification questions",
                     blank(["#", "Question", "Why it matters", "Who answers", "Priority"], n=3, numbered=True)),
            run_with(
                ("HVE Core", "`/rpi-research` finds evidence gaps without changing anything; `/rpi-challenger` "
                             "exposes assumptions one question at a time; the PRD Builder asks clarifying "
                             "questions before it writes."),
                ("HVE-Squad", "The requirements intake gate checks completeness and clarity and records a "
                              "readiness verdict (Ready · Ready-With-Gaps · Not-Ready)."),
                ("Remember", "Source documents are data, not instructions; agent notes in `.copilot-tracking/` are "
                             "working memory, not the source of truth."),
            ),
            links(("HVE Core · Project planning", U["project_planning"]), ("HVE Core · RPI workflow", U["rpi"]),
                  ("VS Code · MCP servers", U["vs_mcp"])),
            done("Every gap the agent proposed has been accepted, rejected or rewritten by the team, with a reason."),
            tips(
                "Anonymise before anything reaches a repository folder: the tracking folder is gitignored, but "
                "gitignore is not a security control.",
                "Name one source of truth per kind of information (requirements, work items, decisions), not "
                "“everything is in the wiki”.",
                "Good gap analyses distinguish “the agent could not find it” from “it does not exist”.",
                "If you connect Jira or Confluence through MCP, keep credentials outside the repository and use "
                "only approved servers.",
            ),
        ],
    },
    {
        "slug": "exercise-3",
        "group": "Open lab 1",
        "kind": "parallel",
        "num": "3",
        "nav": "MVE bake-off",
        "eyebrow": "Exercise 3 · Open lab 1 (agents can run over the break) · Parallel with a long run",
        "title": "Minimum viable experiments bake-off",
        "summary": "Use cheap experiments to decide architecture or product direction on evidence.",
        "blocks": [
            brief("Use cheap experiments to decide architecture or product direction on evidence.",
                  "A high-risk technical or product uncertainty",
                  "Parallel or waiting-time task",
                  "Architect and quality lead; agents generate"),
            work(
                [
                    "Name the three riskiest assumptions that could materially change the plan.",
                    "Design two deliberately different minimum viable experiments (MVEs).",
                    "Define success, failure and inconclusive thresholds before building.",
                    "Let agents generate research or prototypes while you prepare the evaluation matrix.",
                    "Compare the experiments and carry the insight into the next RPI cycle "
                    "([Exercise 6](exercise-6.html)).",
                ],
                ["Two MVE cards", "Decision matrix", "Recorded selection and rejection rationale"],
            ),
            section("toolkit", "Exercise 3 · Hand-in and toolkit",
                    "Set the thresholds first, then let the evidence decide", jump="Hand-in and toolkit"),
            template("mve-card", "MVE card",
                     matrix("", ["MVE A", "MVE B"],
                            ["Assumption tested", "Experiment: what we build or test", "Effort and time box",
                             "Success if…", "Failure if…", "Inconclusive if…", "Result", "Decision"])),
            template("decision-matrix", "Decision matrix",
                     {"head": ["Criterion", "MVE A", "MVE B"],
                      "rows": [[ph("e.g. strength of evidence"), None, None],
                               [ph("e.g. risk retired"), None, None],
                               [ph("e.g. effort, cost, fit"), None, None]],
                      "row_header": False},
                     note="Then record: Selected … because …  ·  Rejected … because …"),
            run_with(
                ("HVE Core", "DT Coach for solution-space concepts and low-fidelity prototypes; `/rpi-research` for "
                             "a read-only technical spike."),
                (None, "Run two agent sessions in parallel, one per MVE, on separate branches."),
                ("HVE-Squad", "the discovery gate offers a brainstorm when nothing is written down yet; a product "
                              "squad turns a business case into requirements, an experiment for the riskiest "
                              "assumption and a backlog."),
            ),
            {"type": "example", "title": "Example",
             "text": "Synthetic example (Northwind Traders, HVE-Squad workshop): a claim must reference order lines, "
                     "but the order system has no API and direct database access is forbidden. MVE: 30 cases, "
                     "3 staff, paper and local only. Proposed criteria: ≥ 90% under 2 minutes; licence and run cost "
                     "≤ EUR 900 a month. Honest limit: the experiment is a plan, not a result."},
            links(("HVE Core · Design Thinking", U["design_thinking"]), ("HVE-Squad · Usage", U["squad_usage"])),
            done("Thresholds were written before any agent output was seen, and the rejected option has a recorded "
                 "reason."),
            tips(
                "Agents make prototypes cheap enough to throw away: build two deliberately different bets, keep the "
                "insight, discard the concept.",
                "Write the thresholds before you see any agent output; otherwise you will rationalise whatever "
                "comes back.",
                "No product uncertainty? Use a technical one: a library choice, an integration path, a migration "
                "approach.",
                "Carry the winning insight into [Exercise 6](exercise-6.html) as an explicit input to the plan.",
            ),
        ],
    },
    # ------------------------------------------------------------- Open lab 2
    {
        "slug": "exercise-4",
        "group": "Open lab 2",
        "kind": "core",
        "num": "4",
        "nav": "Intake to approved backlog",
        "eyebrow": "Exercise 4 · Open lab 2 · Core task",
        "title": "From intake to an approved backlog",
        "summary": "Experience the human-owned transitions from evidence to build-ready work.",
        "blocks": [
            brief("Experience the human-owned transitions from evidence to build-ready work.",
                  "A small greenfield, brownfield or AMS change",
                  "Core task",
                  "Product owner decides; agent operator runs; quality lead writes acceptance criteria"),
            work(
                [
                    "Run intake and requirements clarification.",
                    "Generate or refine the business and product requirements (BRD / PRD), in your organisation’s "
                    "own terms and templates where possible.",
                    "Stop at unresolved questions: the product owner decides, defers or rejects.",
                    "Create a backlog with acceptance criteria and links to the source evidence.",
                    "Check whether the backlog preserves intent rather than merely decomposing text.",
                ],
                ["Approved requirements artefact", "Decision log", "Prioritised backlog with acceptance criteria"],
            ),
            callout("wait", "While your Exercise 4 agents run",
                    "The product owner and agent operator can pick up Intermission A: give the product owner a "
                    "canvas into the HVE loop.",
                    actions=[("Intermission A · PO canvas", "intermission-a.html"),
                             ("Exercise 5 · Reusable component", "exercise-5.html")]),
            section("toolkit", "Exercise 4 · Hand-in and toolkit",
                    "Every requirement traces back; open questions get an owner", jump="Hand-in and toolkit"),
            template("decision-log", "Decision log",
                     blank(["#", "Open question", "Decide · defer · reject", "Decided by", "Evidence link"], n=3,
                           numbered=True)),
            template("backlog-item", "Backlog item", form([
                "Title",
                "Priority",
                "User story",
                ("Acceptance criteria (testable)", "e.g. “Stock 3: quantity 3 passes, quantity 4 fails”"),
                "Source evidence link",
            ], col="Item")),
            template("approval-stamp", "Approval stamp on the requirements",
                     blank(["Version", "Approved by", "Date", "Open items"], n=1)),
            run_with(
                ("HVE Core", "BRD Builder, then PRD Builder (they ask the clarifying questions); Backlog Manager "
                             "(`/backlog-plan` to triage read-only, `/backlog-execute` to write to Jira, Azure "
                             "DevOps or GitHub); Functional Planner turns a PRD into a planned hierarchy."),
                ("HVE-Squad", "intake gate → requirements → experiment → backlog; the Tracker-Write Gate asks a "
                              "person before anything is written to the tracker."),
                ("Gates you exercise", "Evidence → BRD (product owner) · BRD → PRD (product + engineering)"),
            ),
            links(("HVE Core · Project planning", U["project_planning"]),
                  ("HVE Core · Backlog management", U["backlog"]), ("HVE-Squad · Usage", U["squad_usage"])),
            done("No open question was silently resolved by an agent, and every backlog item links to its evidence."),
            tips(
                "Use your organisation’s own document names (for example functional analysis or change-request "
                "templates) rather than forcing BRD/PRD vocabulary.",
                "The key moment is step 3: the agent must stop and ask, and the product owner answers in the files, "
                "not just in the chat.",
                "A business answer has to change the files (requirements, backlog, traceability), not just appear "
                "in chat.",
                "Pick one narrow, testable item from this backlog for [Exercise 6](exercise-6.html).",
            ),
        ],
    },
    {
        "slug": "exercise-5",
        "group": "Open lab 2",
        "kind": "parallel",
        "num": "5",
        "nav": "Reusable component",
        "eyebrow": "Exercise 5 · Open lab 2 · Parallel activity",
        "title": "Build one reusable skill, agent or connector",
        "summary": "Convert local know-how into a reusable component that can connect to the wider flow.",
        "blocks": [
            brief("Convert local know-how into a reusable component that can connect to the wider flow.",
                  "A repeated in-house method, internal agent, orchestrator or MCP pattern",
                  "Parallel or waiting-time task",
                  "Architect and one volunteer"),
            work(
                [
                    "Select one repeated task: discovery questions, Jira intake, architecture review, a code "
                    "standard, AMS triage…",
                    "Choose the smallest correct building block: instruction, prompt, skill, agent, hook or "
                    "control, or connector.",
                    "Define when it runs, its inputs, outputs, permissions and failure behaviour.",
                    "Prototype the component, or write its specification.",
                    "Explain where it plugs into HVE-Squad and where it should stay independent.",
                ],
                ["Component specification or working prototype", "Permission and failure model",
                 "Reuse and ownership plan"],
            ),
            section("toolkit", "Exercise 5 · Hand-in and toolkit", "Pick the smallest building block that works",
                    jump="Hand-in and toolkit"),
            table(
                ["If you need…", "→ Use…"],
                [
                    ["A rule that always applies to certain files",
                     "**Instruction** (narrow `applyTo` pattern; keep it short)"],
                    ["A workflow someone starts on demand",
                     "**Prompt file or skill entry point** (slash command)"],
                    ["Deep know-how, question banks, templates or scripts",
                     "**Skill** (short `SKILL.md`; detail in reference files)"],
                    ["A multi-step job with tools, phases or hand-offs",
                     "**Agent** (restrict its tools; hand off, don’t sprawl)"],
                    ["A rule that must hold whatever the model thinks",
                     "**Control**: hook, permission, schema or CI check"],
                    ["Governed access to Jira, Confluence, GitLab or another system",
                     "**Connector** (MCP server)"],
                ],
                cls="pick",
            ),
            template("component-spec", "Component spec", form([
                "Name",
                "Trigger: when it runs",
                "Inputs",
                "Outputs",
                "Permissions and tools",
                "On failure",
                "Owner and version",
                "Plugs into HVE-Squad as… / stays independent because…",
            ], col="Specification")),
            run_with((None, "HVE Core’s **hve-builder** skill (create, validate, review with a Pass / Revise / "
                            "Blocked verdict, correct). Package and pin it with **APM**: one manifest, a lockfile, "
                            "and an organisation policy for what may be installed.")),
            links(("HVE Core · hve-builder", U["hve_builder"]), ("VS Code · Customise agents", U["vs_overview"]),
                  ("Agent skills", U["vs_skills"]), ("Custom agents", U["vs_agents"]),
                  ("MCP servers", U["vs_mcp"]), ("Hooks", U["vs_hooks"]),
                  ("HVE Core · Customisation", U["customization"]), ("APM", U["apm"])),
            done("Someone outside the team could install and run it from the specification alone."),
            tips(
                "Many teams already have home-made orchestrations, agents and MCP servers; the goal is to turn one "
                "of them into something another team can safely reuse.",
                "Least machinery: one well-reviewed skill beats ten private orchestrations.",
                "Jira and Confluence on Data Center? Atlassian’s official remote MCP server "
                "([Rovo MCP](" + U["rovo_mcp"] + ")) is Cloud-only. The open-source "
                "[sooperset/mcp-atlassian](" + U["mcp_atlassian"] + ") server supports Server/Data Center but is "
                "not an Atlassian product: evaluate it under your security policy before use.",
                "APM lockfile governance is stable; its policy engine (`apm-policy.yml`) is an early preview, so "
                "pin the APM version.",
                "Further reading: [Agent Skills specification](" + U["skills_spec"] + ") and "
                "[Model Context Protocol](" + U["mcp_spec"] + ").",
            ),
        ],
    },
    {
        "slug": "intermission-a",
        "group": "Open lab 2",
        "kind": "intermission",
        "num": "A",
        "nav": "Intermission A · PO canvas",
        "eyebrow": "Intermission A · While Exercise 4 agents run · Open lab 2 · Parallel task",
        "title": "Give the product owner a canvas into the HVE loop",
        "summary": "Let a non-developer steer BRD, PRD and ADR generation without writing code.",
        "blocks": [
            brief("Let a non-developer steer BRD, PRD and ADR generation without writing code.",
                  "The team repo in the GitHub Copilot app, with the Atlassian and WorkIQ MCP servers connected",
                  "Waiting-time task during [Ex 4](exercise-4.html)",
                  "Product owner leads; agent operator pairs; auditor logs prompts and edits"),
            work(
                [
                    "Open the team repo in the GitHub Copilot app; connect the MCP servers.",
                    "Ask Copilot to generate a product-owner canvas: goals, users, scope, open questions, decisions.",
                    "Pull real context via MCP (Jira epic, Confluence, WorkIQ) and look up a matching accelerator at "
                    "[accelerators.ms](" + U["accelerators"] + ").",
                    "The PO approves the canvas; Copilot drafts BRD, PRD and ADR, citing sources. The ADR records: "
                    "adopt, adapt or build.",
                    "Tag each statement as sourced, assumed or PO-decided; log every PO correction.",
                ],
                ["PO canvas committed to the repo", "BRD, PRD and ADR drafts traced to sources",
                 "Log of PO edits, MCP sources and accelerator used"],
            ),
            {"type": "shared_ab", "fill": "Intermission A fills the **BRD**, **PRD** and **ADR** columns of "
                                          "Template 1."},
            links(("Microsoft AI Solution Accelerators", U["accelerators"]),
                  ("Work IQ MCP overview", U["workiq_mcp"]),
                  ("Accelerators: how they work", "resources.html#accelerators")),
            tips(
                "The canvas can be a simple Markdown file or page in the repo that the PO edits in plain language; "
                "Copilot regenerates the BRD, PRD and ADR from it.",
                "Use workshop data only and read-only MCP scopes.",
                "Compare the drafts with the [Exercise 4](exercise-4.html) outputs: what did the PO add that the "
                "agents missed?",
                "Accelerators are ready-made, maintained solution architectures with deployment guides and costing. "
                "Pick the closest match (for example Modernize your Code for a legacy codebase), cite it as the "
                "reference architecture in the ADR, and record whether you adopt, adapt or build.",
                "If an MCP server is unavailable, record it as missing context rather than pasting data by hand.",
                "The PO edit log is reused in [Exercise 9](exercise-9.html).",
            ),
        ],
    },
    # ------------------------------------------------------------- Open lab 3
    {
        "slug": "exercise-6",
        "group": "Open lab 3",
        "kind": "core",
        "num": "6",
        "nav": "Bounded RPI work unit",
        "eyebrow": "Exercise 6 · Open lab 3 · Core task",
        "title": "Execute a bounded RPI work unit",
        "summary": "Run Research → Plan → Implement → Review without losing traceability.",
        "blocks": [
            brief("Run Research → Plan → Implement → Review without losing traceability.",
                  "One narrow, testable backlog item (from [Exercise 4](exercise-4.html))",
                  "Core task",
                  "Agent operator runs; product owner and architect approve the plan; quality lead reviews"),
            work(
                [
                    "Agree the definition of done and the boundaries before execution.",
                    "Assign the run: HVE Core, HVE-Squad or your own orchestrator.",
                    "Require research and plan evidence before any implementation.",
                    "While it executes, the rest of the team works on [Exercise 7](exercise-7.html) and the "
                    "parallel activities.",
                    "Review the result against the requirement, the plan, the tests and the source evidence.",
                ],
                ["Research and plan artefacts", "Implementation or credible patch",
                 "Review evidence and unresolved risks"],
            ),
            callout("wait", "While Exercise 6 executes",
                    "The rest of the team starts Exercise 7 and the two intermissions for this lab.",
                    actions=[("Exercise 7 · Gates and guardrails", "exercise-7.html"),
                             ("Intermission B · Issue to patch", "intermission-b.html"),
                             ("Intermission C · AI versus script", "intermission-c.html")]),
            section("toolkit", "Exercise 6 · Hand-in and toolkit",
                    "One job, one artefact and one human decision per phase", jump="Hand-in and toolkit"),
            table(
                ["", "Research", "Plan", "Implement", "Review"],
                [
                    ["May", "read code, docs and sources; never writes code",
                     "files, tests, risks and rollback, then a critique (Pass · Revise · Blocked)",
                     "only the approved plan; tests after each change",
                     "check every acceptance criterion; never edits code"],
                    ["Leaves", "**research notes**", "**plan and critique**", "**change log and tests**",
                     "**review record**"],
                    ["You decide", "**“Is the evidence enough?”**", "**“Approve the plan”**",
                     "**“Do the checks pass?”**", "**“Accept, fix or follow up”**"],
                ],
                row_header=True,
                cls="phases-table",
            ),
            para("**Follow-up:** defects → implement · decision gaps → plan · missing evidence → research · "
                 "leftovers → a new backlog item", cls="followup"),
            run_with(
                ("HVE Core", "select the RPI Agent and describe the item (manual by default; full auto only on "
                             "request), or run `/rpi-research`, `/rpi-plan`, `/rpi-implement` and `/rpi-review` one "
                             "at a time"),
                ("HVE-Squad", "`/squad request=\"<backlog item>\" mode=autopilot cost-ceiling=<USD>` — the "
                              "Implementation Gate means work never begins cold; the Impactful-Action Gate stops "
                              "before deploy, push, merge or schema changes"),
                ("Your own orchestrator", "show the same four artefacts"),
                label="Start it",
            ),
            {"type": "note", "label": "Review language",
             "text": "execution status (Complete · Partial · Blocked) is recorded separately from the outcome "
                     "(Conformant · Conformant with justified divergence · Defects found · Residual work · Not "
                     "accepted), so “it ran” is never mistaken for “it is right”."},
            links(("HVE Core · RPI workflow", U["rpi"]), ("HVE-Squad · Getting started", U["squad_start"]),
                  ("HVE-Squad · Usage", U["squad_usage"]), ("HVE-Squad · Troubleshooting", U["squad_trouble"])),
            done("A named person has accepted, or sent back, the result on the basis of the review record."),
            tips(
                "Keep the item small enough for about an hour of implementation; if it cannot be sliced that small, "
                "it is an epic, not an exercise item.",
                "Carry the [Exercise 3](exercise-3.html) insight into the plan.",
                "The approval of the plan is a human decision: the product owner or architect signs it, not the "
                "agent.",
                "Plan IDs are stable (P01, P01-T01 …), so you can resume after clearing the chat without redoing "
                "the research.",
                "If a run drifts, route the problem to the earliest responsible phase instead of patching in place.",
                "For HVE-Squad, use the cost ceiling agreed for all teams and record any raise.",
                "If HVE-Squad misbehaves, ask the coordinator for `squad-doctor`, then check the troubleshooting "
                "page; if it is still blocked, run the item with HVE Core instead.",
            ),
        ],
    },
    {
        "slug": "exercise-7",
        "group": "Open lab 3",
        "kind": "core",
        "num": "7",
        "nav": "Gates and guardrails",
        "eyebrow": "Exercise 7 · Open lab 3 · Core task, starts while Exercise 6 runs",
        "title": "Human gates and deterministic guardrails",
        "summary": "Separate advice from enforcement and decide where people remain accountable.",
        "blocks": [
            brief("Separate advice from enforcement and decide where people remain accountable.",
                  "Outputs from [Exercise 4](exercise-4.html) or [6](exercise-6.html)",
                  "Core task",
                  "Quality and governance lead, architect"),
            work(
                [
                    "List every consequential transition: requirements approval, architecture choice, "
                    "implementation, merge, release.",
                    "Assign an owner and the evidence required for each gate.",
                    "Classify each rule: advisory, human gate or deterministic control.",
                    "Implement or describe one deterministic control: schema validation, CI check, permission "
                    "boundary or test.",
                    "Simulate a blocked gate and decide what evidence is needed to proceed.",
                ],
                ["Gate map", "Control matrix", "One tested blocked / override scenario"],
            ),
            section("toolkit", "Exercise 7 · Hand-in and toolkit", "Written rules advise. Controls enforce.",
                    jump="Hand-in and toolkit"),
            template("gate-map", "Gate map",
                     blank(["Transition", "Owner", "Evidence required", "Recorded where"], n=5,
                           hints=["requirements approval", "architecture choice", "implementation", "merge",
                                  "release"])),
            template("control-matrix", "Control matrix",
                     blank(["Rule", "Advisory · human gate · deterministic", "Enforced by", "Owner",
                            "On failure or override"], n=4)),
            code("# tracking-free merge: block agent working notes from main\n"
                 "if [ -n \"$(git ls-files .copilot-tracking)\" ]; then\n"
                 "  echo \"Remove .copilot-tracking/ and promote decisions before merge.\"\n"
                 "  exit 1\n"
                 "fi",
                 caption="Example: a required merge check — the same script runs in GitLab CI, Bitbucket "
                         "Pipelines, Azure Pipelines or GitHub Actions",
                 id_="merge-check"),
            {"type": "chips", "title": "Other deterministic options", "items": [
                "protected branches with required approvals",
                "required pipeline checks",
                "CODEOWNERS on docs and ADRs",
                "schema / front-matter lint for artefacts",
                "read-only tools for research and review",
                "agent hooks that block writes",
                "an APM policy for what agent packages may be installed",
            ]},
            links(("GitLab · Protected branches", U["gl_protected"]),
                  ("GitLab · Merge request approval rules", U["gl_approvals"]),
                  ("Bitbucket Data Center · Merge checks", U["bb_checks"]),
                  ("GitHub · Rulesets", U["gh_rulesets"]), ("VS Code · Agent hooks", U["vs_hooks"]),
                  ("APM · Governance", U["apm_gov"])),
            done("One control actually blocks something, and the override path names who may override and what "
                 "evidence they need."),
            tips(
                "Ask: “What happens today if someone skips this gate?” If the answer is “nothing”, the rule is "
                "advisory, whatever the process document says.",
                "Agents will sometimes skip a step; design for that.",
                "A gitignore entry is a convenience, not a control; the required check is the control. Mark the "
                "check as required in the merge-request settings.",
                "If your repositories are on GitLab or Bitbucket on-premises, prefer those examples. GitLab merge "
                "request approval rules need Premium or Ultimate; protected branches and “pipelines must succeed” "
                "work on all tiers.",
                "The APM policy engine is an early preview.",
                "Reuse the operations loop from [Intermission B](intermission-b.html) and the step verifier from "
                "[Intermission C](intermission-c.html) as inputs to your control matrix.",
            ),
        ],
    },
    {
        "slug": "intermission-b",
        "group": "Open lab 3",
        "kind": "intermission",
        "num": "B",
        "nav": "Intermission B · Issue to patch",
        "eyebrow": "Intermission B · While Exercise 6 executes · Open lab 3 · Parallel task",
        "title": "Close the loop: from Azure SRE Agent issue or ticket to patch",
        "summary": "Route auto-generated issues or customer tickets into an automated, knowledge-grounded patch flow.",
        "blocks": [
            brief("Route issues auto-generated by the Azure SRE Agent, or raised as customer tickets, into an "
                  "automated, knowledge-grounded patch flow.",
                  "Azure SRE Agent issues or customer tickets, Ex 6 review; instructions, skills, ADRs",
                  "Waiting-time task during [Ex 6](exercise-6.html)",
                  "Agent operator and architect; quality lead owns the human gate"),
            work(
                [
                    "Pick three issues: auto-raised by the Azure SRE Agent, or customer tickets.",
                    "Draft a label-triggered workflow: a GitHub agentic workflow, or Jenkins/Bamboo on Bitbucket "
                    "Data Center.",
                    "Ground each patch in knowledge: instructions, skills and ADRs, plus Jira and Confluence via "
                    "Atlassian MCP.",
                    "The agent opens a draft pull request with patch, tests and issue link; a human reviews, never "
                    "auto-merge.",
                    "Feed the outcome back: close, reopen, or turn the failure into a new instruction or skill.",
                ],
                ["Workflow or pipeline definition", "One draft patch PR traced to its issue",
                 "Loop diagram with the human gate marked"],
            ),
            {"type": "shared_ab", "fill": "Intermission B fills the **Issue** and **Patch** columns of Template 1, "
                                          "and Template 2 (operations loop)."},
            links(("Azure SRE Agent documentation", U["sre"]), ("Overview of Azure SRE Agent", U["sre_overview"])),
            tips(
                "Teams on GitHub use an agentic workflow or Actions to hand labelled issues to the Copilot coding "
                "agent.",
                "Teams on Bitbucket Data Center (on-prem) sketch the equivalent Jenkins or Bamboo job calling an "
                "agent CLI, and write the Jira update back through the Atlassian MCP server.",
                "Keep the loop bounded: draft PRs only, a retry limit, and a human merge.",
                "The trigger can be an issue generated automatically by the Azure SRE Agent from operational "
                "signals, or a ticket raised by a customer; the downstream flow is identical.",
                "The loop diagram feeds [Exercise 7](exercise-7.html) (gates and guardrails).",
            ),
        ],
    },
    {
        "slug": "intermission-c",
        "group": "Open lab 3",
        "kind": "intermission",
        "num": "C",
        "nav": "Intermission C · AI versus script",
        "eyebrow": "Intermission C · While Exercise 6 executes · Open lab 3 · Parallel task",
        "title": "What did we ask AI to do that a script could do?",
        "summary": "Find the steps that should be deterministic, and make every step the AI keeps verifiable.",
        "blocks": [
            brief("Find the steps that should be deterministic, and make every step the AI keeps verifiable.",
                  "The [Exercise 6](exercise-6.html) run: prompts, research, plan and change log, plus the "
                  "auditor’s log",
                  "Waiting-time task during [Ex 6](exercise-6.html)",
                  "Architect and quality lead; agent operator supplies the run files"),
            work(
                [
                    "List every task you asked the agent to do in the Ex 6 run.",
                    "Classify each: script alone · AI with a deterministic check · judgement.",
                    "For each script candidate, name the tool: lint, codemod, template, schema, CI check or git "
                    "hook.",
                    "For tasks where AI stays, add a fixed step list and a check that fails the run if a step is "
                    "skipped.",
                    "Run one script or check against the Ex 6 artefacts and record what it catches that the agent "
                    "missed.",
                ],
                ["Task list, classified by who should do it", "One script or check, run on Ex 6 output",
                 "Pass / fail check for each AI step"],
            ),
            section("toolkit", "Intermission C · Hand-in and toolkit",
                    "Script it, or make the AI prove every step", jump="Hand-in and toolkit"),
            template("run-audit", "Template 1 · Audit of the Ex 6 run",
                     matrix("", ["Research", "Plan", "Build", "Review", "Follow-up"],
                            ["Asked of the AI", "Script instead?", "Check per step",
                             "Decision: script, AI + check or AI"])),
            template("step-verifier", "Template 2 · Step verifier",
                     blank(["Step", "Required output", "Check (script)", "Fails if…"], n=3),
                     note="Example: every plan task ID (P01-T01…) appears in the change log and review record"),
            run_with((None, "The Ex 6 artefacts in `.copilot-tracking/` (research, plans, changes, reviews) · a shell "
                            "or Python script, schema validation or a CI check · the same check runs in GitLab CI, "
                            "Bitbucket Pipelines, Azure Pipelines or GitHub Actions")),
            {"type": "rules", "items": ["Scripts read the artefacts, never edit them",
                                        "A failed check blocks; it does not just warn"]},
            done("At least one task moved from AI to a script, or an AI step now has a check that fails when the "
                 "step is skipped."),
            tips(
                "Apply the working agreement “enforce what is deterministic” to your own run. Ask: “Which of these "
                "steps did we pay tokens for that a script would do the same way every time?”",
                "Typical candidates: renaming and moving files, formatting, counting, schema and front-matter "
                "checks, checking that every plan task ID (P01-T01 …) appears in the change log and the review "
                "record, and that every acceptance criterion has a test.",
                "Where AI stays (research, judgement, synthesis), make it more deterministic: a fixed step list, "
                "required output files, a schema for artefacts and a verifier that fails the run when a step is "
                "missing.",
                "Fill Template 1 across the five phases of the Exercise 6 run: for each, what did we ask the AI to "
                "do, could a script do it instead, and which check proves the step happened.",
                "Feed the best finding into [Exercise 7](exercise-7.html) (control matrix) and the adoption canvas "
                "in [Exercise 10](exercise-10.html).",
            ),
        ],
    },
    # ------------------------------------------------------------- Open lab 4
    {
        "slug": "exercise-8",
        "group": "Open lab 4",
        "kind": "core",
        "num": "8",
        "nav": "Red team and recovery",
        "eyebrow": "Exercise 8 · Open lab 4 · Core task",
        "title": "Cross-team red team and recovery drill",
        "summary": "Test whether the process is robust when challenged, interrupted or partially wrong.",
        "blocks": [
            brief("Test whether the process is robust when challenged, interrupted or partially wrong.",
                  "Another team’s outputs",
                  "Core task",
                  "Whole team, paired with another team",
                  roles_label="Roles"),
            work(
                [
                    "Exchange artefacts, not verbal explanations.",
                    "Challenge missing context, security, testability, operational readiness and traceability.",
                    "Inject one failure: missing project ID, tool error, incomplete experiment, stale context or "
                    "rejected assumption.",
                    "The original team recovers without silently discarding the evidence chain.",
                    "Record which faults were caught by controls, by agents or by people.",
                ],
                ["Red-team findings", "Recovery log", "Revised artefact or plan"],
            ),
            section("toolkit", "Exercise 8 · Hand-in and toolkit", "Challenge with artefacts, recover with evidence",
                    jump="Hand-in and toolkit"),
            {"type": "lenses", "title": "Five lenses", "items": [
                ("Context", "What is missing, stale or unsourced?"),
                ("Security", "Data, secrets, permissions, sensitive content?"),
                ("Testability", "Can every acceptance criterion be tested?"),
                ("Operational readiness", "Rollback, runbook, monitoring, hand-off?"),
                ("Traceability", "Evidence → decision → requirement → plan → result?"),
            ]},
            {"type": "chips", "title": "Fault cards (draw one)", "style": "faults", "items": [
                "Missing project ID", "Tool error", "Incomplete experiment", "Stale context", "Rejected assumption",
            ]},
            template("recovery-log", "Recovery log",
                     blank(["Fault", "Caught by (control · agent · person)", "Decision",
                            "Routed to (research · plan · implement · new item)", "Evidence kept"], n=3)),
            {"type": "note", "label": "Recovery rules",
             "text": "record the fault and the decision · route it to the earliest responsible phase · never delete "
                     "evidence to make the story look clean"},
            run_with(
                ("HVE Core", "the Code Review agent and `/rpi-review` compare the work with the requirements and "
                             "plan, read-only; `/rpi-challenger` tests the assumptions."),
                ("HVE-Squad", "team state and the append-only decisions log live in the repository, so a team can "
                              "resume after an interruption and show who decided what."),
            ),
            links(("HVE Core · RPI workflow", U["rpi"]), ("HVE Core · Security planning", U["security"])),
            done("Each team can show the fault, who or what caught it, and the evidence chain still intact after "
                 "recovery."),
            tips(
                "Pairing: A with B, C with D; with five teams, rotate (A reviews B, B reviews C … E reviews A).",
                "The facilitators hand out the five fault cards. The red team may not explain the fault; the "
                "original team must discover and handle it.",
                "Count the “caught by” tally at the end: it is a strong input for [Exercise 9](exercise-9.html) "
                "and for the adoption canvas (which controls are worth automating).",
            ),
        ],
    },
    {
        "slug": "exercise-10",
        "group": "Open lab 4",
        "kind": "core",
        "num": "10",
        "nav": "Adoption path",
        "eyebrow": "Exercise 10 · Open lab 4 · Core task",
        "title": "Design your adoption path",
        "summary": "Turn workshop learning into a repeatable internal practice and a real pilot.",
        "blocks": [
            brief("Turn workshop learning into a repeatable internal practice and a real pilot.",
                  "The day’s artefacts and lessons",
                  "Core task",
                  "Whole team; product owner and architect lead",
                  roles_label="Roles"),
            work(
                [
                    "Choose where HVE fits in your organisation’s current lifecycle, and where it does not.",
                    "Define the minimum shared practice: context, gates, evidence, reuse and metrics.",
                    "Select one Customer Zero or AMS / modernisation pilot.",
                    "Name a sponsor, practice owner, technical owner and first participating team.",
                    "Set 30-day success criteria and a review rhythm.",
                ],
                ["One-page adoption canvas", "Named pilot and owners",
                 "30-day experiment with measurable acceptance criteria"],
            ),
            section("toolkit", "Exercise 10 · Hand-in and toolkit", "One-page adoption canvas",
                    jump="Hand-in and toolkit"),
            {"type": "canvas", "id": "adoption-canvas", "label": "Adoption canvas", "items": [
                ("1", "Where HVE fits, and where it does not"),
                ("2", "Minimum shared practice: context · gates · evidence · reuse · metrics"),
                ("3", "Pilot: Customer Zero or AMS / modernisation"),
                ("4", "Owners: sponsor · practice owner · technical owner · first team"),
                ("5", "Baseline: what we measure today"),
                ("6", "30-day experiment: measurable acceptance criteria"),
                ("7", "Review rhythm: when, and with whom"),
                ("8", "Reusable assets from today: skills, controls, templates"),
                ("9", "Approvals and risks: security, legal, data"),
            ]},
            links(("HVE Core · Team adoption", U["team_adoption"]), ("APM · Governance", U["apm_gov"]),
                  ("Frontier Transformation Engineer (SkillUp)", U["skillup"])),
            done("The pilot has named owners, a start date and acceptance criteria someone could measure in 30 days."),
            tips(
                "Aim to industrialise the agentic development practice you already have, measure its impact and "
                "start with a controlled Customer Zero group.",
                "Use names, not roles, and measure a baseline before the pilot starts.",
                "Pick two metrics your organisation already reports rather than inventing new ones (for example "
                "lead time and rework from unclear requirements).",
                "Typical pilot scorecard: unplanned intervention rate, active human minutes per item, AI cost per "
                "accepted item, lead time and quality guardrails.",
            ),
        ],
    },
    {
        "slug": "exercise-9",
        "group": "Open lab 4",
        "kind": "backup",
        "num": "9",
        "nav": "Compare autonomy and cost (backup)",
        "eyebrow": "Backup · Exercise 9 · Parallel task · Run if there is time",
        "title": "Compare autonomy, cost and accepted outcome",
        "summary": "Evaluate usefulness rather than declaring a symbolic winner.",
        "blocks": [
            callout("info", "Backup exercise",
                    "Run it only if your team finishes early. It uses the [common scorecard](scorecard.html)."),
            brief("Evaluate usefulness rather than declaring a symbolic winner.",
                  "Two runs, teams or approaches",
                  "Parallel or waiting-time task",
                  "Auditor / observer with the agent operator"),
            work(
                [
                    "Normalise the scope and the definition of done.",
                    "Compare time to first useful output and time to accepted outcome.",
                    "Count human questions, corrections, approvals, retries and unplanned interventions.",
                    "Review AI consumption or available cost signals alongside quality and rework.",
                    "Identify one improvement that should become an instruction, skill, control or team practice.",
                ],
                ["Comparison scorecard", "One reusable improvement", "Recommendation by phase and context"],
            ),
            section("toolkit", "Backup · Exercise 9 · Hand-in and toolkit", "Count everything, then compare usefulness",
                    jump="Hand-in and toolkit"),
            {"type": "formula", "text": "Net improvement = time saved − (AI cost + extra review effort)",
             "sub": "Count failed and abandoned runs too."},
            template("comparison-sheet", "Comparison sheet",
                     matrix("Measure", ["Run A", "Run B"],
                            ["Same scope and definition of done?", "Time to first useful output",
                             "Time to accepted outcome", "Questions", "Corrections", "Approvals", "Retries",
                             "Unplanned interventions", "AI consumption / cost signal", "Quality and rework",
                             "Common scorecard total"])),
            run_with((None, "the auditor’s log · HVE-Squad `consumption.md` (model, tokens and estimated cost per "
                            "dispatch) and `decisions.md` · HVE Core research, plan, change and review files · "
                            "GitHub Copilot usage metrics and AI-credit consumption"),
                     label="Where the numbers come from"),
            template("recommendation", "Recommendation format",
                     {"head": ["Recommendation"], "rows": [[ph("In phase … and context …, use … because …")]],
                      "row_header": False}),
            links(("GitHub Copilot · Usage-based billing (AI credits)", U["gh_billing"]),
                  ("GitHub Copilot · Usage metrics", U["gh_metrics"]),
                  ("HVE-Squad · Usage › Cost admission control", U["squad_usage"])),
            done("The recommendation names a phase and a context, not a winner."),
            tips(
                "Typical pairs: HVE Core versus HVE-Squad on comparable items; interactive versus autopilot; or your "
                "run versus the team you red-teamed.",
                "Use logs and state files, not memory.",
                "Cheaper models can cost more if they need more cycles; strong models for research and planning, "
                "cheaper ones for implementation and checks is a common pattern.",
                "Measure cost per accepted outcome, not tokens per run.",
                "Reuse your [Exercise 1](exercise-1.html) lifecycle map to compare predicted and actual human "
                "effort, and the PO edit log from [Intermission A](intermission-a.html).",
            ),
        ],
    },
    # ------------------------------------------------------------- Close
    {
        "slug": "playback",
        "group": "Close",
        "kind": "info",
        "nav": "Playback and close",
        "eyebrow": "Playback and close",
        "title": "Two minutes per team, then commit",
        "summary": "Two minutes per team: decision, evidence, result, failure and lesson, then commitments.",
        "blocks": [
            template("playback", "Playback",
                     blank(["Decision", "Evidence", "Result", "Failure", "Lesson"], n=1)),
            template("commitments", "Commitments",
                     blank(["Named pilot", "Owner", "Measurement approach", "Reusable materials"], n=1)),
            banner("The workshop succeeds when your teams can continue independently."),
            tips(
                "Keep strictly to two minutes and bring one failure: the honest “not finished” beats a “done” that "
                "fails its tests.",
                "Prepare it while agents run: see [While agents run](while-agents-run.html), item 7.",
                "Score yourselves with the [common scorecard](scorecard.html), from logs and artefacts.",
            ),
        ],
    },
    {
        "slug": "scorecard",
        "group": "Close",
        "kind": "info",
        "nav": "Common scorecard",
        "eyebrow": "Common scorecard",
        "title": "One scorecard for every team and every approach",
        "summary": "Nine criteria rated 1–5, used in the playback and in the backup Exercise 9.",
        "blocks": [
            template("scorecard", "Common scorecard", {
                "head": ["Criterion", "What to observe", "Rating 1–5"],
                "rows": [
                    ["Accepted outcome", "Did the result satisfy the agreed scope and acceptance criteria?", None],
                    ["Lead time", "Time to first useful result and to accepted outcome", None],
                    ["Human effort", "Questions, corrections, approvals and unplanned interventions", None],
                    ["Quality", "Requirement coverage, technical coherence, tests and operational readiness", None],
                    ["Traceability", "Can the team connect evidence → decision → requirement → plan → result?",
                     None],
                    ["Control", "Could the team stop, redirect, recover and resume safely?", None],
                    ["Consumption", "AI and resource consumption relative to the value of the accepted result",
                     None],
                    ["Reuse", "What can now be reused as a skill, instruction, control, component or practice?",
                     None],
                    ["Learning", "What did the team understand that it did not understand before the run?", None],
                ],
                "row_header": True,
                "cls": "scorecard",
            }),
            tips("Used in the [playback](playback.html) and, if it is run, in [Exercise 9](exercise-9.html) "
                 "(backup). Score from logs and artefacts, not impressions."),
        ],
    },
    # ------------------------------------------------------------- Reference
    {
        "slug": "resources",
        "group": "Reference",
        "kind": "info",
        "nav": "Resources",
        "eyebrow": "Materials",
        "title": "Resources for the day",
        "summary": "Every link from the guide in one place, plus the hand-in templates.",
        "blocks": [{"type": "resources"}],
    },
]

# ---------------------------------------------------------------------------
# Resources page: one page, several sections
# items: (title, url, optional description)
# ---------------------------------------------------------------------------
RESOURCES = [
    {"id": "hve-core", "title": "HVE Core", "items": [
        ("Documentation", U["hve_core"], ""),
        ("Your first full workflow", U["first_workflow"], ""),
        ("RPI workflow", U["rpi"], "Research → Plan → Implement → Review"),
        ("Agents catalogue", U["agents"], ""),
        ("Project planning: BRD, PRD, ADR", U["project_planning"], ""),
        ("Backlog management", U["backlog"], ""),
        ("Design Thinking", U["design_thinking"], ""),
        ("Security planning", U["security"], ""),
        ("Customisation", U["customization"], ""),
        ("Team adoption", U["team_adoption"], ""),
        ("Role guides", U["roles"], ""),
        ("AI-assisted project lifecycle", U["lifecycle"], ""),
        ("hve-builder skill", U["hve_builder"], "Create, validate and review your own skills and agents"),
    ]},
    {"id": "hve-squad-apm", "title": "HVE-Squad and APM", "items": [
        ("HVE-Squad documentation", U["squad"], ""),
        ("Getting started", U["squad_start"], ""),
        ("Usage: autonomy, cost ceiling, routing", U["squad_usage"], "Includes cost admission control"),
        ("Guided demos", U["squad_demo"], ""),
        ("Troubleshooting", U["squad_trouble"], ""),
        ("Self-led hands-on workshop (Northwind Traders)", U["squad_workshop"], ""),
        ("APM · Agent Package Manager", U["apm"], ""),
        ("APM · Governance guide", U["apm_gov"], ""),
    ]},
    {"id": "platform", "title": "Platform documentation", "items": [
        ("VS Code · Customise agents", U["vs_overview"], ""),
        ("VS Code · Agent skills", U["vs_skills"], ""),
        ("VS Code · Custom agents", U["vs_agents"], ""),
        ("VS Code · MCP servers", U["vs_mcp"], ""),
        ("VS Code · Agent hooks (preview)", U["vs_hooks"], ""),
        ("GitLab · Protected branches", U["gl_protected"], ""),
        ("GitLab · Merge request approval rules", U["gl_approvals"], "Needs GitLab Premium or Ultimate"),
        ("Bitbucket Data Center · Merge checks", U["bb_checks"], ""),
        ("GitHub · Rulesets", U["gh_rulesets"], ""),
        ("GitHub Copilot · Usage-based billing (AI credits)", U["gh_billing"], ""),
        ("GitHub Copilot · Usage metrics", U["gh_metrics"], ""),
    ]},
    {"id": "standards", "title": "Standards and learning", "items": [
        ("Agent Skills specification", U["skills_spec"], ""),
        ("Model Context Protocol", U["mcp_spec"], ""),
        ("Microsoft Responsible AI principles", U["rai"], ""),
        ("Frontier Transformation Engineer, SkillUp", U["skillup"], ""),
    ]},
    {"id": "mcp", "title": "Agents and MCP servers", "groups": [
        {"title": "Azure SRE Agent and Microsoft MCP servers", "items": [
            ("Azure SRE Agent documentation", U["sre"], ""),
            ("Overview of Azure SRE Agent", U["sre_overview"], ""),
            ("Azure MCP Server documentation", U["azmcp"], ""),
            ("Azure MCP Server · Get started", U["azmcp_start"], ""),
            ("Fabric MCP Servers overview", U["fabric_mcp"], ""),
            ("Work IQ MCP overview", U["workiq_mcp"], ""),
        ]},
        {"title": "Recommended MCP servers", "items": [
            ("DeepWiki MCP · Documentation", U["deepwiki_docs"], ""),
            ("DeepWiki MCP · Server endpoint", U["deepwiki"], ""),
            ("Context7 MCP · Up-to-date library docs", U["context7"], ""),
            ("GitHub MCP Registry", U["gh_mcp"], ""),
        ]},
        {"title": "Jira and Confluence (Atlassian)", "items": [
            ("Atlassian Rovo MCP server", U["rovo_mcp"], "Official remote server; Atlassian Cloud only"),
            ("sooperset/mcp-atlassian", U["mcp_atlassian"],
             "Open source; supports Server/Data Center; not an Atlassian product, so evaluate it under your "
             "security policy first"),
        ]},
    ]},
]

ACCELERATORS = {
    "id": "accelerators",
    "title": "Accelerators: start from a proven architecture",
    "intro": (
        "Accelerators are ready-made, maintained solution architectures with deployment guides, costing and sample "
        "data. Use them as the reference architecture when you research and plan, instead of starting from a blank "
        "repo. The featured list is a selection relevant to this workshop; the full catalogue is on accelerators.ms."
    ),
    "how": [
        ("1 · Browse", "Discover ready-made solutions for your customer need"),
        ("2 · Select", "Pick the best fit and adapt it with built-in configuration"),
        ("3 · Review", "Check prerequisites and costing against your organisation"),
        ("4 · Deploy", "Follow the deployment guide to launch quickly and securely"),
        ("Included", "Proven architecture, documentation, costing, sample data"),
    ],
    "featured_link": ("Microsoft AI Solution Accelerators", U["accelerators"]),
    "featured": [
        ("Modernize your Code", "Migrate legacy code to modern languages with AI agents"),
        ("Container-Migration", "Automate container platform migration with AI"),
        ("Multi-Agent Custom Automation Engine", "Orchestrate a group of AI agents · Python, TypeScript, Bicep"),
        ("Deploy Your AI Application in Production", "Secure, extensible environment for AI Foundry workloads"),
    ],
    "in_workshop": (
        "**In the workshop · [Intermission A](intermission-a.html):** while Exercise 4 runs, the product owner "
        "looks for a matching accelerator, cites it as the reference architecture and records the ADR decision: "
        "adopt, adapt or build."
    ),
}

# Shared hand-in for Intermissions A and B (one template, filled across both intermissions)
SHARED_AB = {
    "eyebrow": "Intermissions A–B · Hand-in and toolkit",
    "title": "Connect real systems, keep the human gate",
    "trace": matrix("", ["BRD", "PRD", "ADR", "Issue", "Patch"],
                    ["Source (MCP)", "Who decides", "Gate", "Artefact left behind"]),
    "loop": blank(["Step", "Trigger", "Agent or system", "Human gate"], n=4, numbered=True),
    "loop_note": "Trigger: issue label · failed check · review comment · schedule",
    "run_with": (
        "GitHub Copilot app on the team repo · MCP: Atlassian (Jira, Confluence) and WorkIQ (mail, meetings, "
        "chats) · accelerators.ms (reference architecture) · Copilot coding agent · GitHub agentic workflow, or "
        "Jenkins/Bamboo on Bitbucket Data Center"
    ),
    "rules": ["Read-only MCP scopes; workshop data only", "Draft PRs only; a human merges"],
    "done": (
        "The PO approved the canvas, every BRD/PRD/ADR line has a source, and one issue reached a draft PR without "
        "manual coding."
    ),
    "shared_note": (
        "This hand-in is shared by Intermissions A and B: fill Template 1 across both. Reuse the operations loop in "
        "[Exercise 7](exercise-7.html)."
    ),
}
