# SQL General

## Execution order (simplified)

* **FROM and JOINs** → Build the combined dataset (including time from the CROSS JOIN).
* **WHERE** → Apply filters.
* **GROUP BY / HAVING** → Aggregate if needed.
* **SELECT** → Project columns and compute expressions.
* **ORDER BY** → Sort the final result