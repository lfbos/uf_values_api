# UF Values API

## Install

* Clone the project

    `git clone https://github.com/lfbos/uf_values_api.git`

* Access to the project

    `cd uf_values_api`

* Create python environment

    * Virtualenvwrapper: using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/):

        ```
        mkvirtualenv env_name --python=python3 # if you have by default python2 
        pip install -r requirements.txt
        ```

    * Virtualenv: using [virtualenv](https://virtualenv.pypa.io/en/stable/):

        ```
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
        ```

* Migrate database `python manage.py migrate`

* Load initial data (could take a while) `python manage.py load_all_uf_values`

* Once the previous script is finished, you can check the api [http://localhost:8000/uf/list/](http://localhost:8000/uf/list/)

## Install and run celery

The application has a task that runs every day at the end of the date (23:00 hrs), to update the uf values for the current year,
to run the task celery must be installed and running.

* Install broker (RabbitMQ):
  - Ubuntu: 
    `sudo apt-get install rabbitmq-server` to check if rabbit is running successfully after being installed, you can check with the command `sudo service rabbitmq-server status`
  
  - Mac OS:
    With homebrew `brew install rabbitmq` to check if rabbit is running successfully after being installed, you can check with the command `brew services list`
   
   For more information [RabbitMQ](http://www.rabbitmq.com/download.html)
* Run celery:
  In a separated console run the following command `celery worker -A uf_values_api --loglevel=info`, and that's it!
  
## API doc (endpoints)
* /uf/list/:

    - Methods: GET
    - Response: list of uf values, items fields value (UF value in Chilean pesos), date (date of UF value)
    - Filter options:
      - year (e.g.: ?year=2017): filter uf values by year
      - value (e.g.: ?value=26396.79): filter by uf value
      - date (e.g.: ?date=2017-01-01): filter by date

* /uf/price/:
    - Methods: GET
    - Response: gets the corresponding uf price calculated when a value (chilean pesos) and a date are passed.
    - Filter required:
      - value: chilean value to transform
      - date: date to get the corresponding uf value (format yyyymmdd)
      e.g.: ?value=26396.79&date=20170101
    - Response: value and date input, price (uf value calculated).
