# API Reference

The public API of the `virtual_lab` package consists of two exports.

---

## `Agent`

```python
from virtual_lab import Agent

agent = Agent(
    title="Immunologist",
    expertise="antibody engineering and immune response characterization",
    goal="guide the development of nanobodies",
    role="advise on immunogenicity and cross-reactivity",
    model="gpt-4o",
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | `str` | Display name of the agent (used in prompts and transcripts). |
| `expertise` | `str` | Domain the agent specialises in. |
| `goal` | `str` | High-level objective of the agent. |
| `role` | `str` | Specific responsibilities in the meeting. |
| `model` | `str` | OpenAI (or compatible) model to use. |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `prompt` | `str` | System prompt generated from the agent's attributes. |
| `message` | `dict` | OpenAI-format system message `{"role": "system", "content": ...}`. |

---

## `run_meeting`

```python
from virtual_lab import run_meeting

summary = run_meeting(
    meeting_type="team",          # "team" or "individual"
    agenda="...",                 # The scientific question or task
    save_dir=Path("discussions/test"),
    save_name="meeting_1",
    team_lead=principal_investigator,
    team_members=(immunologist, ml_specialist, computational_biologist),
    agenda_questions=("What nanobody scaffold should we use?",),
    agenda_rules=("Cite sources.", "Be concise."),
    num_rounds=2,
    pubmed_search=True,
    return_summary=True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `meeting_type` | `"team" \| "individual"` | required | Meeting format. |
| `agenda` | `str` | required | The scientific agenda / task description. |
| `save_dir` | `Path` | required | Directory where transcripts are saved. |
| `save_name` | `str` | `"discussion"` | Base filename for JSON and Markdown outputs. |
| `team_lead` | `Agent \| None` | `None` | Team lead for team meetings. |
| `team_members` | `tuple[Agent, ...] \| None` | `None` | Team members for team meetings. |
| `team_member` | `Agent \| None` | `None` | Specialist for individual meetings. |
| `agenda_questions` | `tuple[str, ...]` | `()` | Questions the final summary must answer. |
| `agenda_rules` | `tuple[str, ...]` | `()` | Rules the agents must follow. |
| `summaries` | `tuple[str, ...]` | `()` | Summaries of prior meetings to include as context. |
| `contexts` | `tuple[str, ...]` | `()` | Background context strings. |
| `num_rounds` | `int` | `0` | Number of discussion rounds before the final summary. |
| `temperature` | `float` | `0.2` | Sampling temperature for all agent calls. |
| `pubmed_search` | `bool` | `False` | Whether to equip agents with PubMed search. |
| `return_summary` | `bool` | `False` | If `True`, returns the final summary as a string. |

### Returns

`str | None` — The final meeting summary if `return_summary=True`, else `None`.

---

## Pre-built Agents (`virtual_lab.prompts`)

```python
from virtual_lab.prompts import PRINCIPAL_INVESTIGATOR, SCIENTIFIC_CRITIC
```

| Name | Role |
|------|------|
| `PRINCIPAL_INVESTIGATOR` | Team lead; synthesises and summarises. |
| `SCIENTIFIC_CRITIC` | Automatic critic in individual meetings. |
