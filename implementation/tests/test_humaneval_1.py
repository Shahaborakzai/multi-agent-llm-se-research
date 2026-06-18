
import sys
import os
sys.path.append(os.path.abspath("/workspace"))

from humaneval_1 import separate_paren_groups

def test_examples():
    assert separate_paren_groups("( ) (( )) (( )( ))") == ["()", "(())", "(()())"]
    assert separate_paren_groups("()()") == ["()", "()"]
    assert separate_paren_groups(" ( ( ) ) ") == ["(())"]
    assert separate_paren_groups("") == []
    assert separate_paren_groups("   ") == []
    assert separate_paren_groups("(()())(())") == ["(()())", "(())"]
    print("All tests passed.")

if __name__ == "__main__":
    test_examples()
