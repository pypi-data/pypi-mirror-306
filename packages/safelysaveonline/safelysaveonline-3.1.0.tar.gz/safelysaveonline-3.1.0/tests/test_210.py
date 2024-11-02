# Simple test testing core functionality

import os
import shutil
from src import safelysave

if os.path.exists(safelysave.get_appdata_path()) == True:
    shutil.rmtree(safelysave.get_appdata_path())

repo = input('[Enter git repository] ')

profile = safelysave.create_profile(repo)

content = {
    "test": "check",
    "test2": "check2",
    "uuid": 'failed'
}
content2 = {
    "test3": "check3",
    "test4": "check4",
    "uuid": 'failed'
}

safelysave.add_dict(profile, content)
safelysave.add_dict(profile, content2)

data = safelysave.get_data(profile)

safelysave.remove_dict(profile, data[1]['uuid'])

safelysave.sync(profile)

safelysave.goto_profile_dir(profile)
os.remove('data')
os.remove('adds')
os.remove('removals')

safelysave.sync(profile)

data = safelysave.get_data(profile)
profiles = safelysave.get_profiles()

passed = 0
print("")

if len(data) == 1:
    print("Passed Test 1")
    passed += 1
else:
    print("Failed Test 1 (No or 2+ entries existing.")

if data[0]['test'] == 'check':
    print("Passed Test 2.1")
    passed += 1
else:
    print("Passed Test 2.1 (Entry is not valid.)")

if data[0]['test2'] == 'check2':
    print("Passed Test 2.2")
    passed += 1
else:
    print("Passed Test 2.2 (Entry is not valid.)")

if data[0]['uuid'] != 'failed':
    passed += 1
    print("Passed Test 2.3")
else:
    print("Passed Test 2.3 (Did not overwrite UUID.)")

if profiles[0] == profile:
    passed += 1
    print("Passed Test 3")
else:
    print("Failed Test 3 (Invalid or 2+ profiles existing.)")

print("")
print(f'[Result] Passed {passed}/5 tests.')
