enva
echo "=== install build ==="
python3 -m pip install --upgrade build
echo "=== build ==="
python3 -m build
echo "=== install twine ==="
python3 -m pip install --upgrade twine
echo "=== upload ==="
python3 -m twine upload --verbose --repository testpypi dist/*
echo "=== removing ==="
rip dist
