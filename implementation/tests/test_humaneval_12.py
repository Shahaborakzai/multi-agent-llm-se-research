
from humaneval_12 import longest

def test_longest():
    assert longest([]) is None
    assert longest(['a', 'b', 'c']) == 'a'
    assert longest(['a', 'bb', 'ccc']) == 'ccc'
    # multiple same length, return first
    assert longest(['ab', 'cd', 'efg', 'hij']) == 'efg'
    # single element
    assert longest(['single']) == 'single'

if __name__ == "__main__":
    test_longest()
    print("All tests passed.")
