## Install dependencies:
   1. [**direnv**](https://direnv.net/) - `sudo apt-get install direnv`
   2. [**pipenv**](https://pipenv.readthedocs.io) `pip install --user pipenv`
   
## Set-up project:
   1. Allow **direnv** to set/unset environment variables while enter/exit to/from project folder. For perform this action
   execute `direnv allow` inside project folder;
   2. Make **.envrc** file (config file for [**direnv**]) and populete it with environment variables which you vant to set;
   3. Install **pipenv** for managing dependencies in an easy way. After **pipenv** will be installed, you have to create
   **virtual environment** by execute `pipenv --python <version>`. After **virtual environment** directory will be 
   successfully created inside project dir, install dependencies by running `pipenv install --skip-lock` which lead to 
   installing dependencies from **Pipfile**;
