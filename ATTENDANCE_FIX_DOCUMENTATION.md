# Attendance Calculation Logic Fix

## Issue
The attendance calculation logic for the exemption threshold (65%) was incorrect in `index.py` at line 290.

## Bug Description
When calculating how many classes a student needs to attend to reach the 65% exemption threshold, the formula was using the wrong denominator:

**Incorrect Formula (Before):**
```python
attend = math.ceil(((exemption_threshold * total_hours) - present_hours) / exemption_threshold)
```

**Correct Formula (After):**
```python
attend = math.ceil(((exemption_threshold * total_hours) - present_hours) / (1 - exemption_threshold))
```

## Mathematical Explanation

When a student attends `x` more classes:
- New present hours: `present_hours + x`
- New total hours: `total_hours + x`
- Target: `(present_hours + x) / (total_hours + x) >= threshold`

Solving for x:
```
present_hours + x >= threshold * (total_hours + x)
present_hours + x >= threshold * total_hours + threshold * x
x - threshold * x >= threshold * total_hours - present_hours
x * (1 - threshold) >= threshold * total_hours - present_hours
x >= (threshold * total_hours - present_hours) / (1 - threshold)
```

Therefore, the denominator should be `(1 - threshold)`, NOT `threshold`.

## Impact Example

**Scenario:** Student has 50 present hours out of 100 total (50% attendance), needs to reach 65%

### With Old (Incorrect) Formula:
```
attend = (65 - 50) / 0.65 = 15 / 0.65 ≈ 23 classes
After attending: 73/123 = 59.35% ❌ (Still below 65%!)
```

### With Fixed (Correct) Formula:
```
attend = (65 - 50) / 0.35 = 15 / 0.35 ≈ 43 classes
After attending: 93/143 = 65.03% ✓ (Meets the threshold!)
```

## Other Formulas Verified

The following formulas in the codebase were verified to be **CORRECT**:

1. **Line 210** - Bunking calculation with 75% threshold:
   ```python
   bunk = math.floor((present_hours - (threshold * total_hours)) / threshold)
   ```
   ✓ This is correct because when bunking, present hours stay the same while total increases.

2. **Line 227** - Attend calculation with 75% threshold:
   ```python
   attend = math.ceil((threshold * total_hours - present_hours) / (1 - threshold))
   ```
   ✓ This is correct and uses the proper formula.

## Testing
Comprehensive test cases were created and validated the fix across multiple scenarios:
- Low attendance recovery (50% → 75%)
- Good attendance with bunking capacity
- Medical exemption scenarios (65% threshold)
- Edge cases (at threshold, above threshold)
- Critical low attendance cases

All tests passed successfully.

## Code Review & Security
- Code review: ✓ No issues found
- Security scan: ✓ No vulnerabilities detected

## Files Changed
- `index.py` - Line 290: Fixed the denominator in attendance calculation for exemption threshold
