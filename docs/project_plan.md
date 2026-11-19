# Project plan outline

## Objective

Deliver a reproducible BI prototype that turns game-level basketball statistics into a team performance dashboard and evaluate it with predefined user tasks.

## Deliverables

1. Project charter, scope, stakeholders, and acceptance criteria.
2. Source and license record, data dictionary, and reproducible preparation script.
3. Clean team-game dataset generated locally from the source.
4. Power BI report and screenshots.
5. Test evidence, user evaluation summary, lessons learned, and final report.

## Acceptance criteria

- Script produces one row per team per source game for the selected scope.
- Sample output values reconcile with the source CSV and independent calculations.
- Dashboard filters by team/season as intended and shows the defined measures.
- Evaluation results report task correctness and completion time, with limitations stated.
- Repository README explains how to obtain data, prepare it, and open the report.

## Suggested work packages

| Work package | Main output |
|---|---|
| Initiation and scope | Charter, stakeholder list, scope statement |
| Data assessment | Source/license record, data profiling, data dictionary |
| Preparation | Normalized CSV and validation evidence |
| BI development | Dashboard and measure definitions |
| Verification | Test cases and defect log |
| Evaluation | Task results and user feedback |
| Closure | 10 knowledge-area review, lessons learned, final report |

## Risks to track

- Missing or inconsistent historical statistics.
- Dataset license or redistribution limits.
- Source schema differs from expected column names.
- Dashboard conclusions are overstated from a small sample.
- Project scope expands into player-level tracking without suitable source data.
