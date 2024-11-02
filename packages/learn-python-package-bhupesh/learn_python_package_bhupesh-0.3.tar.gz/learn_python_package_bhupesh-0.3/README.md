# My Package

This is a simple Python package that provides 3 defs.
Ihave created on 30-10-24 for learning purposes .

## Installation

You can install this package using pip:
=================================================================================

Example to use the Package:

import package_a

```bash
package_a.greet('Nikhil')
package_a.age_calculator(222)
package_a.tax_calculator(233)
   ```

output: 
```bash
Hello, Nikhil !
your age is : 22 decades and 2 years
tax calculator is here : 
your total amount including tax is : 256.3
```

=============================================================================================

To publish your Python package to PyPI (Python Package Index) so that it can be installed via `pip`, you’ll need to follow these steps. Since your package is already on GitHub, I assume you have a `setup.py` file configured. Here’s a concise guide to help you publish your package:

### Step 1: Prepare Your Package
Make sure your package has the necessary files:
- **setup.py**: Contains metadata about your package.
- **README.md**: Provides a description of your package.
- **LICENSE**: (optional but recommended) Specifies the license for your package.
- Any other necessary files.

### Step 2: Install Required Tools
You'll need `twine` to upload your package to PyPI and `setuptools` to build it. If you haven't installed them, run:

```bash
pip install setuptools wheel twine
```

### Step 3: Build Your Package
1. **Navigate to your package directory** where the `setup.py` file is located:
   ```bash
   cd path/to/your/package
   ```

2. **Build the package** by running the following command:
   ```bash
   python setup.py sdist bdist_wheel
   ```
   - This will create a `dist/` directory containing your package files.

### Step 4: Create a PyPI Account
If you don’t have an account, create one on [PyPI](https://pypi.org/account/register/).

### Step 5: Generate an API Token
1. After creating your account, go to your [PyPI account settings](https://pypi.org/manage/account/#api-tokens).
2. Create an API token for uploading your package.

### Step 6: Store Your Token in GitHub Secrets (Optional)
If you want to automate the publishing process using GitHub Actions, store your token in your GitHub repository secrets as explained in the previous responses.

### Step 7: Upload Your Package to PyPI
1. **Upload using twine**:
   - Run the following command to upload your package:
   ```bash
   twine upload dist/*
   ```
   - When prompted, enter your PyPI username and the API token you created.

### Step 8: Verify Your Package
After uploading, you can verify that your package is available on PyPI by visiting:
```
https://pypi.org/project/your-package-name/
```

### Step 9: Install Your Package
Now, you can install your package using pip:
```bash
pip install your-package-name
```

### Summary
1. Ensure your package is ready (with `setup.py`, README, etc.).
2. Install `setuptools`, `wheel`, and `twine`.
3. Build your package.
4. Create a PyPI account and an API token.
5. Upload your package using `twine`.


================================================================
To update your Python package with new changes, follow these steps:

### 1. Make Your Changes Locally
### 2. Rebuild the Package
Ensure your working directory is set to your package's root directory:
```bash
cd path/to/your/package
```
Then, create the updated package distributions:
```bash
python setup.py sdist bdist_wheel
```
Or, if using `pyproject.toml` (with `build`):
```bash
pip install build
python -m build
```

### 3. Publish the Updated Package to PyPI
1. Install `twine` if it’s not already installed:
   ```bash
   pip install twine
   ```

2. Upload the updated package to PyPI:
   ```bash
   twine upload dist/*
   ```
   You will be prompted to enter your PyPI username and password.

### 4. Verify the Update on PyPI
- Visit [PyPI](https://pypi.org/) and search for your package to ensure the updated version is published.
- Check that the version number and any new features or changes are reflected.

### 5. Update Your Local Installation (Optional)
If you want to test your newly published version:
```bash
pip install your-package-name --upgrade
```
