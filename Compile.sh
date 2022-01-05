# Clear the list dist to avoid duplications
rm -Rf dist
rm -f shrink.spec

pyinstaller -c -F -i ./src/icon.ico ./src/shrink.py

# Clear the build-directories
rm -Rf ./src/__pycache__
rm -Rf ./build

cp ./src/icon.ico ./dist/