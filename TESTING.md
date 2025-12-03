# Testing Guide

This project uses **pytest** for comprehensive unit testing.

## Quick Start

```bash
# Install dependencies (including pytest)
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v
```

## Test Structure

```
tests/
├── __init__.py          # Makes tests a package
├── conftest.py          # Shared fixtures
└── test_new_agent.py   # Unit tests for new_agent.py
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output (shows each test)
pytest -v

# Run specific test file
pytest tests/test_new_agent.py

# Run specific test class
pytest tests/test_new_agent.py::TestExtractScore

# Run specific test
pytest tests/test_new_agent.py::TestExtractScore::test_extract_percentage_score

# Run and show print statements
pytest -s

# Run with detailed failure info
pytest -vv
```

### Coverage (Optional)

If you want to see code coverage:

```bash
# Install coverage plugin
pip install pytest-cov

# Run with coverage
pytest --cov=new_agent --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Categories

### Unit Tests

All tests in `test_new_agent.py` are unit tests that:
- Mock external API calls
- Test individual functions in isolation
- Don't require real API keys
- Run quickly

### Test Classes

1. **TestExtractScore** - Tests score extraction logic
   - Handles `percentage_score` field
   - Handles `score` field
   - Handles missing scores
   - Handles None values

2. **TestFilterPassed** - Tests candidate filtering
   - Filters by threshold
   - Handles edge cases (all pass, none pass)
   - Handles exact threshold matches
   - Handles empty lists

3. **TestGetCandidatesPage** - Tests API pagination
   - Successful API calls
   - Error handling
   - Offset parameter

4. **TestGetAllCandidates** - Tests multi-page fetching
   - Single page results
   - Multiple page results
   - Empty results

5. **TestInviteToTest** - Tests candidate invitation
   - Successful invitations
   - Error handling
   - Missing email handling
   - Name fallback logic

6. **TestSendRecruiterInvite** - Tests recruiter invite logging
   - Normal cases
   - Missing name handling

7. **TestMakeSession** - Tests session creation
   - Header configuration
   - Token inclusion

## Fixtures

Shared test fixtures are defined in `conftest.py`:

- `mock_candidate` - Standard candidate with all fields
- `mock_candidate_no_email` - Candidate without email
- `mock_candidate_no_score` - Candidate without score
- `mock_candidates_list` - List of test candidates
- `mock_session` - Mock requests session
- `mock_api_response_success` - Successful API response
- `mock_api_response_error` - Error API response
- `mock_api_response_paginated` - Paginated API responses

## Writing New Tests

### Example Test

```python
def test_my_function(mock_candidate):
    """Test description"""
    result = my_function(mock_candidate)
    assert result == expected_value
```

### Using Fixtures

```python
def test_with_fixture(mock_candidates_list):
    result = filter_passed(mock_candidates_list, 70)
    assert len(result) == 3
```

### Mocking API Calls

```python
@patch('new_agent.requests.Session')
def test_api_call(mock_session_class):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    
    mock_session = Mock()
    mock_session.get.return_value = mock_response
    mock_session_class.return_value = mock_session
    
    # Your test code here
```

## Test Configuration

Configuration is in `pytest.ini`:
- Test discovery patterns
- Output formatting
- Markers for test categorization

## Continuous Integration

You can run tests in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: pytest tests/ -v
```

## Best Practices

1. **Test isolation** - Each test should be independent
2. **Mock external calls** - Don't make real API calls in unit tests
3. **Clear test names** - Test names should describe what they test
4. **Use fixtures** - Reuse common test data via fixtures
5. **Test edge cases** - Test empty lists, None values, etc.

## Troubleshooting

### Tests fail with import errors
- Make sure you're in the project root directory
- Check that `new_agent.py` is in the same directory

### Mock not working
- Make sure you're patching the right module path
- Use `@patch('new_agent.function_name')` not `@patch('function_name')`

### Environment variables in tests
- Tests use mocked values, not real `.env` file
- Use `@patch` decorators to override module-level variables

