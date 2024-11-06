.PHONY : help bump-major bump-minor bump-patch clean upload-package upload-test-package 

help : 
	@echo "lilytk - makefile help"
	@echo "----------------------"
	@echo "bump-major          - bump major version"
	@echo "bump-minor          - bump minor version"
	@echo "bump-patch          - bump patch version"
	@echo "clean               - cleans up the build artifacts"
	@echo "install             - install package from source"
	@echo "test                - runs unit tests"
	@echo "upload-package      - builds and uploads the package to PyPi"
	@echo "upload-test-package - builds and uploads the package to Test PyPi"

bump-major : 
	@echo "Bumping major version..."
	@bumpver update -n --verbose --major
	@echo "Done :O"

bump-minor : 
	@echo "Bumping minor version..."
	@bumpver update -n --verbose --minor
	@echo "Done :O"

bump-patch : 
	@echo "Bumping patch version..."
	@bumpver update -n --verbose --patch
	@echo "Done :O"

clean :
	@echo "Cleaning..."
	@rm -rf dist
	@find . -path '**/__pycache__' -exec rm -rf {} \;
	@echo "Done!!"

dist/* :
	@echo "Building package..."
	@python3 -m build
	@echo "Done uwu"

install : dist/*
	@pip install --force-reinstall dist/lilytk-*.whl

upload-package : clean dist/*
	@twine upload --repository pypi dist/*

upload-test-package : clean dist/*
	@twine upload --repository testpypi dist/*
