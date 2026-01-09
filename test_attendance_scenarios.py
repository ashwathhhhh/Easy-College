"""
Comprehensive test scenarios for attendance calculation logic
Simulating real-world scenarios
"""
import math

def calculate_attend_classes(present_hours, total_hours, threshold):
    """Calculate how many classes to attend to reach threshold"""
    attend = math.ceil((threshold * total_hours - present_hours) / (1 - threshold))
    return max(0, attend)

def calculate_bunk_classes(present_hours, total_hours, threshold):
    """Calculate how many classes can be bunked while maintaining threshold"""
    bunk = math.floor((present_hours - (threshold * total_hours)) / threshold)
    return max(0, bunk)

def test_scenario_1():
    """Student with low attendance (50%) needs to reach 75%"""
    print("Scenario 1: Low attendance recovery")
    print("-" * 50)
    present = 50
    total = 100
    threshold = 0.75
    
    attend = calculate_attend_classes(present, total, threshold)
    new_present = present + attend
    new_total = total + attend
    final_percentage = (new_present / new_total) * 100
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Must attend: {attend} classes")
    print(f"Final: {new_present}/{new_total} = {final_percentage:.2f}%")
    assert final_percentage >= threshold * 100, f"Failed to reach {threshold*100}%"
    print("✓ PASSED\n")

def test_scenario_2():
    """Student with good attendance (85%) wants to know how many to bunk"""
    print("Scenario 2: Good attendance - bunking capacity")
    print("-" * 50)
    present = 85
    total = 100
    threshold = 0.75
    
    bunk = calculate_bunk_classes(present, total, threshold)
    new_present = present
    new_total = total + bunk
    final_percentage = (new_present / new_total) * 100
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Can bunk: {bunk} classes")
    print(f"Final: {new_present}/{new_total} = {final_percentage:.2f}%")
    assert final_percentage >= threshold * 100, f"Failed to maintain {threshold*100}%"
    print("✓ PASSED\n")

def test_scenario_3():
    """Student with medical exemption needs to reach 65% (not 75%)"""
    print("Scenario 3: Medical exemption - 65% threshold")
    print("-" * 50)
    present = 40
    total = 100
    exemption_threshold = 0.65
    
    attend = calculate_attend_classes(present, total, exemption_threshold)
    new_present = present + attend
    new_total = total + attend
    final_percentage = (new_present / new_total) * 100
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Must attend: {attend} classes")
    print(f"Final: {new_present}/{new_total} = {final_percentage:.2f}%")
    assert final_percentage >= exemption_threshold * 100, f"Failed to reach {exemption_threshold*100}%"
    print("✓ PASSED\n")

def test_scenario_4():
    """Edge case: Already at exact threshold"""
    print("Scenario 4: Already at threshold")
    print("-" * 50)
    present = 75
    total = 100
    threshold = 0.75
    
    attend = calculate_attend_classes(present, total, threshold)
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Must attend: {attend} classes")
    assert attend == 0, "Should be 0 when already at threshold"
    print("✓ PASSED (correctly shows 0)\n")

def test_scenario_5():
    """Edge case: Above threshold, can still bunk"""
    print("Scenario 5: Above threshold with bunking room")
    print("-" * 50)
    present = 90
    total = 100
    threshold = 0.75
    
    bunk = calculate_bunk_classes(present, total, threshold)
    new_present = present
    new_total = total + bunk
    final_percentage = (new_present / new_total) * 100
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Can bunk: {bunk} classes")
    print(f"Final: {new_present}/{new_total} = {final_percentage:.2f}%")
    assert final_percentage >= threshold * 100, f"Failed to maintain {threshold*100}%"
    print("✓ PASSED\n")

def test_scenario_6():
    """Critical case: Very low attendance with exemption"""
    print("Scenario 6: Critical low attendance (30%) with 65% target")
    print("-" * 50)
    present = 30
    total = 100
    exemption_threshold = 0.65
    
    attend = calculate_attend_classes(present, total, exemption_threshold)
    new_present = present + attend
    new_total = total + attend
    final_percentage = (new_present / new_total) * 100
    
    print(f"Current: {present}/{total} = {(present/total)*100:.2f}%")
    print(f"Must attend: {attend} classes")
    print(f"Final: {new_present}/{new_total} = {final_percentage:.2f}%")
    assert final_percentage >= exemption_threshold * 100, f"Failed to reach {exemption_threshold*100}%"
    print("✓ PASSED\n")

if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE ATTENDANCE CALCULATION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_scenario_1()
        test_scenario_2()
        test_scenario_3()
        test_scenario_4()
        test_scenario_5()
        test_scenario_6()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("The attendance calculation logic is working correctly!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
