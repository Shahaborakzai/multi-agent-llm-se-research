
import sys
import traceback
from humaneval_3 import below_zero

def run_tests():
    try:
        assert below_zero([1, 2, 3]) == False, "Test 1 failed"
        assert below_zero([1, 2, -4, 5]) == True, "Test 2 failed"
        assert below_zero([]) == False, "Test 3 failed (empty list should be False)"
        assert below_zero([-1]) == True, "Test 4 failed (single negative operation)"
        assert below_zero([5, -3, -2]) == False, "Test 5 failed (balance returns to zero but not below)"
        print("All tests passed.")
    except AssertionError as e:
        print(str(e))
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
