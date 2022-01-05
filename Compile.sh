# Clear the last dist to avoid duplications
rm -Rf dist
rm -f shrink.spec

echo Build the new exec-file out of the original script
pyinstaller -i src/icon.png src/shrink.py

# Clear the build-directories
rm -Rf src/__pycache__
rm -Rf build

# Copy the Icon into the final directory
cp src/icon.png dist/shrink/

echo your executable can be found at /dist/shrink/shrink
# Sorry for all the files :)