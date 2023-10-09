# Template for ECS639U Group Coursework

This template should be used as the starting point for your group coursework in the module ECS639U Web Programming (at Queen Mary University of London). Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Fork this repo and clone your fork:

    ```console
    $ git clone https://github.qmul.ac.uk/eew252/cwgroup
    ```

3. Install dependencies:

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. If everything is alright, you should be able to start the Django development server:

    ```console
    $ python manage.py runserver
    ```

6. Open your browser and go to http://127.0.0.1:8000, you will be greeted with a welcome page.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
