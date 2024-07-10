def pytest_sessionstart(session):
    print("sessionstart")
    print(session)
    print(dir(session))

def pytest_sessionfinish(session, exitstatus):
    print("sessionfinish")
    print(session, exitstatus)