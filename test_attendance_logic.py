"""
Test cases to verify attendance calculation logic
"""
import math

def test_attend_calculation_correct():
    """Test the correct formula for calculating classes to attend"""
    # Scenario: Need to reach 75% from 50%
    threshold = 0.75
    total_hours = 100
    present_hours = 50
    
    # Using correct formula from line 227
    attend = math.ceil((threshold * total_hours - present_hours) / (1 - threshold))
    
    # Verify: after attending these classes, we should be at or above threshold
    new_present = present_hours + attend
    new_total = total_hours + attend
    new_percentage = new_present / new_total
    
    print(f"Test 1 - Correct attend formula (75% threshold):")
    print(f"  Current: {present_hours}/{total_hours} = {present_hours/total_hours*100:.2f}%")
    print(f"  Must attend: {attend} classes")
    print(f"  After: {new_present}/{new_total} = {new_percentage*100:.2f}%")
    assert new_percentage >= threshold, f"Failed: {new_percentage*100:.2f}% < {threshold*100}%"
    print("  ✓ PASSED\n")

def test_attend_calculation_incorrect():
    """Test the INCORRECT formula currently on line 290"""
    # Scenario: Need to reach 65% from 50%
    exemption_threshold = 0.65
    total_hours = 100
    present_hours = 50
    
    # Using INCORRECT formula from line 290
    attend_incorrect = math.ceil((exemption_threshold * total_hours - present_hours) / exemption_threshold)
    
    # Verify: this will NOT reach the threshold
    new_present = present_hours + attend_incorrect
    new_total = total_hours + attend_incorrect
    new_percentage = new_present / new_total
    
    print(f"Test 2 - INCORRECT attend formula (65% threshold) - LINE 290 BUG:")
    print(f"  Current: {present_hours}/{total_hours} = {present_hours/total_hours*100:.2f}%")
    print(f"  Incorrect calculation says attend: {attend_incorrect} classes")
    print(f"  After: {new_present}/{new_total} = {new_percentage*100:.2f}%")
    print(f"  ✗ FAILS: {new_percentage*100:.2f}% < {exemption_threshold*100}% (does not meet threshold!)\n")

def test_attend_calculation_correct_exemption():
    """Test the CORRECT formula for 65% threshold"""
    # Scenario: Need to reach 65% from 50%
    exemption_threshold = 0.65
    total_hours = 100
    present_hours = 50
    
    # Using CORRECT formula
    attend_correct = math.ceil((exemption_threshold * total_hours - present_hours) / (1 - exemption_threshold))
    
    # Verify: this WILL reach the threshold
    new_present = present_hours + attend_correct
    new_total = total_hours + attend_correct
    new_percentage = new_present / new_total
    
    print(f"Test 3 - CORRECT attend formula (65% threshold) - PROPOSED FIX:")
    print(f"  Current: {present_hours}/{total_hours} = {present_hours/total_hours*100:.2f}%")
    print(f"  Correct calculation says attend: {attend_correct} classes")
    print(f"  After: {new_present}/{new_total} = {new_percentage*100:.2f}%")
    assert new_percentage >= exemption_threshold, f"Failed: {new_percentage*100:.2f}% < {exemption_threshold*100}%"
    print(f"  ✓ PASSED\n")

def test_bunk_calculation():
    """Test the bunk calculation formula (line 210)"""
    # Scenario: Currently at 85%, can bunk some classes while staying above 75%
    threshold = 0.75
    total_hours = 100
    present_hours = 85
    
    # Using formula from line 210 (which is correct)
    bunk = math.floor((present_hours - (threshold * total_hours)) / threshold)
    if bunk < 0:
        bunk = 0
    
    # Verify: after bunking these classes, we should still be at or above threshold
    new_present = present_hours
    new_total = total_hours + bunk
    new_percentage = new_present / new_total
    
    print(f"Test 4 - Bunk calculation (line 210 - correct):")
    print(f"  Current: {present_hours}/{total_hours} = {present_hours/total_hours*100:.2f}%")
    print(f"  Can bunk: {bunk} classes")
    print(f"  After: {new_present}/{new_total} = {new_percentage*100:.2f}%")
    assert new_percentage >= threshold, f"Failed: {new_percentage*100:.2f}% < {threshold*100}%"
    print("  ✓ PASSED\n")

def test_edge_case_exact_threshold():
    """Test when exactly at threshold"""
    exemption_threshold = 0.65
    total_hours = 100
    present_hours = 65  # Exactly at threshold
    
    # Using correct formula
    attend = math.ceil((exemption_threshold * total_hours - present_hours) / (1 - exemption_threshold))
    
    print(f"Test 5 - Edge case: exactly at threshold:")
    print(f"  Current: {present_hours}/{total_hours} = {present_hours/total_hours*100:.2f}%")
    print(f"  Must attend: {attend} classes")
    assert attend == 0, f"Should be 0 when already at threshold, got {attend}"
    print("  ✓ PASSED (should be 0)\n")

if __name__ == "__main__":
    print("=" * 60)
    print("ATTENDANCE CALCULATION LOGIC TESTS")
    print("=" * 60)
    print()
    
    test_attend_calculation_correct()
    test_attend_calculation_incorrect()
    test_attend_calculation_correct_exemption()
    test_bunk_calculation()
    test_edge_case_exact_threshold()
    
    print("=" * 60)
    print("SUMMARY:")
    print("  - Line 227 (attend with 75% threshold): ✓ CORRECT")
    print("  - Line 210 (bunk calculation): ✓ CORRECT")
    print("  - Line 290 (attend with 65% threshold): ✗ INCORRECT")
    print()
    print("FIX REQUIRED:")
    print("  Line 290 should use (1 - exemption_threshold) as denominator")
    print("  Instead of: / exemption_threshold")
    print("  Should be:  / (1 - exemption_threshold)")
    print("=" * 60)
