# Unittests - Parameterized tests

<pre>@parameterized.expand([...]):</pre> This decorator is the core of parameterized testing.

It takes a list of tuples (or lists). Each inner tuple represents a single test case.

The elements within each inner tuple correspond to the arguments of your test method (test_access_nested_map).

In our case, for each test run, parameterized will unpack (nested_map, path, expected_result) into the arguments of test_access_nested_map.

Example: For the first test run, nested_map will be {"a": 1}, path will be ("a",), and expected_result will be 1.

def test_access_nested_map(self, nested_map, path, expected_result):: The test method signature now includes the parameters defined in parameterized.expand.

result = access_nested_map(nested_map, path): This is the first line of your test body. It calls the function under test with the dynamic inputs.

self.assertEqual(result, expected_result): This is the second line. It asserts that the actual result matches the expected_result provided by parameterized.