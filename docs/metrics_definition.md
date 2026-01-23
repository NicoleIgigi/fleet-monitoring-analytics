# Metrics Definitions & Assumptions

This document defines the key metrics used in the **Fleet System Health Dashboard** and explains how to interpret them.  
**Note:** All data in this project is **simulated** for portfolio purposes.

---

## Data scope

The dashboard monitors fleet performance using weekly aggregated metrics. Filters (Region, Model, Week) apply to all visuals and change the metric values accordingly.

**Dimensions**
- **week**: weekly time bucket used for trending
- **region**: simulated operating region (e.g., West, East, Kigali)
- **model**: simulated platform variant (A/B/C)

---

## Vehicle model definitions (A, B, C)

The `model` field represents **simulated platform variants**:
- **Model A**: baseline platform configuration (simulated)
- **Model B**: alternative configuration with different operating characteristics (simulated)
- **Model C**: less common / specialized configuration (simulated)

These are placeholders to demonstrate segmentation by platform type without using proprietary identifiers.

---

## Core metrics

### 1) Total Flights
**Meaning:** The total number of flights observed in the selected filters.

**Formula**
- `Total Flights = SUM(flights_total)`

**How to use it**
- Provides context for volume (higher volume makes trends more meaningful)
- Useful for interpreting whether changes are due to performance or simply fewer/more flights

---

### 2) Total Successful Flights
**Meaning:** The total number of successful flights in the selected filters.

**Formula**
- `Total Successful Flights = SUM(flights_success)`

---

### 3) Reliability (Weighted)
**Meaning:** Overall fleet reliability (success rate) across the selected filters.

**Formula**
- `Reliability (Weighted) = Total Successful Flights ÷ Total Flights`

**Why “weighted” matters**
This approach computes reliability using totals (not simple averaging across groups), so it remains accurate when slicing by region/model/week.

**Interpretation**
- Higher is better
- Use the weekly trend chart to identify dips and recoveries

---

### 4) Critical Events per 100 Flights (Weighted)
**Meaning:** A safety/system-health signal showing how many high/critical events occur per 100 flights.

**Formula**
- `Critical Events per 100 Flights = (Total Critical Events ÷ Total Flights) × 100`

**Interpretation**
- Lower is better
- Spikes may indicate operational, hardware, or software issues even if reliability remains stable

---

## Status logic

### Reliability Status
A simplified label to support fast monitoring decisions.

**Thresholds**
- ✅ **Good**: Reliability ≥ 95%
- ⚠️ **Watch**: 93% ≤ Reliability < 95%
- ❌ **Risk**: Reliability < 93%

**Why this is useful**
- Helps highlight when performance is below target and may require investigation
- Encourages consistent interpretation across technical and non-technical stakeholders

---

## Target line

### Reliability Target (95%)
A reference line on the reliability trend chart used as a performance benchmark.

**Meaning**
- Weeks below the target are candidates for investigation
- Compare reliability dips against safety event spikes and segment by region/model

---

## Assumptions (for this simulated dataset)

- “Successful flight” is defined by the simulated data generation logic (portfolio-only).
- “Critical events” represent high-severity safety/health signals (e.g., GPS glitches, battery drops).
- Regions and models are simulated categories to demonstrate fleet segmentation.

---

## Suggested analysis workflow (how a systems team would use this)
1. Identify weeks where reliability dips below target.
2. Check whether critical events increased in the same period.
3. Use Region + Model filters to localize the issue.
4. On the **Critical Event Drivers** page, identify which event types contribute most to safety risk.
5. Prioritize investigation on the top 1–2 drivers and the most impacted region/model segments.
