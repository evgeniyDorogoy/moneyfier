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

## Run in docker:
   1. Execute `mv .env.dev .env`;
   2. Edit environment variables in `.env`;
   3. Build `docker build --target dev -t moneyfier .` for DEV image or `docker build -t moneyfier .` for PROD one;
   4. Run `docker run --name moneyfier -d -p 8000:8000 --mount type=bind,source="$(pwd)",target=/usr/src/moneyfier 
   --env-file .env moneyfier` in case of running container in DEV mode, otherwise use `docker run --name moneyfier -d 
   -p 8000:8000 --env-file .env moneyfier` for the PROD one;